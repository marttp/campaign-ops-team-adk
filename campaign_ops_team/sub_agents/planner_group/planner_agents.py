from google.adk.agents import LlmAgent

from campaign_ops_team.tools.tools import google_search, segment_group_preparing_tool
from campaign_ops_team.config import retry_config, MODEL
from google.adk.models import Gemini

# Goal Planning Agent
goal_planning_agent = LlmAgent(
    name="goal_planning_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Converts frontline output into structured goals, KPIs, and scheduling intent.",
    instruction="""
    You are the Goal Planning Agent. Your goal is to convert the frontline intake into structured goals, KPIs, and scheduling intent.
    Output a structured plan.
    """
)

# Segmentation Discovery Agent
segmentation_discovery_agent = LlmAgent(
    name="segmentation_discovery_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Generates segments, rules, estimate sizes, explores customer behavior.",
    instruction="""
    You are the Segmentation Discovery Agent. Your goal is to generate actionable segments, eligibility rules, and size estimates.
    Use the segment_group_preparing_tool if needed.
    """,
    tools=[segment_group_preparing_tool]
)

# Planner Critic Agent
planner_critic_agent = LlmAgent(
    name="planner_critic_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Validates strategy feasibility, conflicts, and quality.",
    instruction="""
    You are the Planner Critic Agent. Evaluate the Goal and Segmentation outputs.
    Check for feasibility, conflicts, and quality.
    If good, output "APPROVED".
    If not, provide feedback.
    """
)

# Google Search Agent
google_search_agent = LlmAgent(
    name="google_search_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Supports competitive research, seasonal patterns, industry insights.",
    instruction="""
    You are the Google Search Agent. Your goal is to provide competitive research, seasonal patterns, and industry insights.
    Use the google_search tool to find information.
    """,
    tools=[google_search]
)

# Reporter Agent
reporter_agent = LlmAgent(
    name="reporter_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Produces a clean, validated, normalized JSON for delivery.",
    instruction="""
    You are the Reporter Agent. You are the final step of the Planner group.
    Produce a clean JSON object including:
    - campaign_type
    - goals
    - segments
    - schedule
    - constraints
    - delivery_plan
    Ensure no missing fields.
    """
)
