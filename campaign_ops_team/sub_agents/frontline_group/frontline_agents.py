from google.adk.agents import LlmAgent
from campaign_ops_team.tools.tools import internal_data_agent_tool
from campaign_ops_team.config import retry_config, MODEL
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