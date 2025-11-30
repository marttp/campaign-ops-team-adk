from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from ...tools import internal_data_agent_tool
from ...config import MODEL, retry_config
from google.adk.models import Gemini
from pydantic import BaseModel, Field
from typing import List


class CampaignScenarioEstimate(BaseModel):
    goal: str = Field(
        description="The primary objective of this campaign (e.g., increase DAU, drive GMV).",
    )
    possible_features: List[str] = Field(
        description="List of product features that could be involved in this campaign.",
    )
    best_case: str = Field(
        description="Optimistic outcome scenario if the campaign performs exceptionally well.",
    )
    worst_case: str = Field(
        description="Negative outcome scenario if the campaign fails or underperforms.",
    )
    average_case: str = Field(
        description="Expected or most likely outcome scenario under typical conditions.",
    )


# Intake Agent
intake_agent = LlmAgent(
    name="intake_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Discover possible features that fit the goal of the user request by taking a look in internal metrics and product features.",
    instruction="""
    You are the Intake Agent. Your goal is to discover possible features that fit the goal of the user request.
    User will provide a short metric goal or complex goal. Your work will be to find the best possible features that fit the goal.
    Use the internal_data_agent_tool to get context about product features and company metrics.
    Output a structured summary of the intake.
    """,
    tools=[internal_data_agent_tool],
    output_schema=CampaignScenarioEstimate,
    output_key="intake_result",
)

# Frontline Critic Agent
frontline_critic_agent = LlmAgent(
    name="frontline_critic_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Evaluates the Intake Agent's output.",
    instruction="""
    You are the Frontline Critic Agent. Your goal is to evaluate the Intake Agent's output for realism, missing elements, and conflicts.
    If the intake is good, output "APPROVED".
    If there are issues, explain them clearly so the Intake Agent can fix them.
    """,
)

# Frontline Manager Agent
frontline_manager_agent = LlmAgent(
    name="frontline_manager_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Orchestrates the Frontline Group to produce a validated intake summary.",
    instruction="""
    You are the Frontline Manager. Your goal is to produce a validated campaign intake summary.

    Follow this process:
    1. Call the `intake_agent` with the user's request.
    2. Call the `frontline_critic_agent` to evaluate the intake output.
    3. If the critic output contains "APPROVED", you are done. Return the intake output.
    4. If the critic provides feedback, call the `intake_agent` again with the feedback to refine the intake.
    5. Repeat steps 2-4 until approved or for a maximum of 3 iterations.

    Return the final approved intake summary.
    """,
    tools=[AgentTool(agent=intake_agent), AgentTool(agent=frontline_critic_agent)],
    output_schema=CampaignScenarioEstimate,
    output_key="frontline_result",
)
