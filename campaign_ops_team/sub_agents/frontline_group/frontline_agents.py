from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from campaign_ops_team.tools.tools import internal_data_agent_tool
from campaign_ops_team.config import MODEL, retry_config
from google.adk.models import Gemini

# Intake Agent
intake_agent = LlmAgent(
    name="intake_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Extracts campaign type, objectives, rough segmentation hypotheses, and constraints.",
    instruction="""
    You are the Intake Agent. Your goal is to extract campaign type, objectives, rough segmentation hypotheses, and constraints from the user request.
    Use the internal_data_agent_tool to get context about product features and company metrics.
    Output a structured summary of the intake.
    """,
    tools=[internal_data_agent_tool]
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
    """
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
    tools=[
        AgentTool(agent=intake_agent),
        AgentTool(agent=frontline_critic_agent)
    ]
)
