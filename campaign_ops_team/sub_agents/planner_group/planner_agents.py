from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from ...tools import segment_group_preparing_tool
from ...config import MODEL, retry_config
from google.adk.models import Gemini
from ..support_team.google_search_agent import google_search_agent

# Goal Planning Agent
goal_planning_agent = LlmAgent(
    name="goal_planning_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Converts frontline output into structured goals, KPIs, and scheduling intent.",
    instruction="""
    You are the Goal Planning Agent. Your goal is to convert the frontline intake into structured goals, KPIs, and scheduling intent.
    Output a structured plan.
    """,
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
    tools=[segment_group_preparing_tool],
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
    """,
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
    """,
)

# Planner Manager Agent
planner_manager_agent = LlmAgent(
    name="planner_manager_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Orchestrates the Planner Group to produce a detailed campaign plan.",
    instruction="""
    You are the Planner Manager. Your goal is to produce a detailed campaign plan JSON.

    Follow this process:
    1. Call `goal_planning_agent` with the input.
    2. Call `segmentation_discovery_agent` with the goal plan.
    3. Call `planner_critic_agent` to evaluate the Goal and Segmentation.
    4. If the critic output contains "APPROVED", proceed to step 6.
    5. If the critic provides feedback, call `goal_planning_agent` (and `segmentation_discovery_agent` if needed) to refine the plan. Repeat steps 3-5 (max 3 times).
    6. Call `reporter_agent` with the final plan components to generate the final JSON.

    You may use `google_search_agent` at any time for research if requested or needed.
    """,
    tools=[
        AgentTool(agent=goal_planning_agent),
        AgentTool(agent=segmentation_discovery_agent),
        AgentTool(agent=planner_critic_agent),
        AgentTool(agent=reporter_agent),
        AgentTool(agent=google_search_agent),
    ],
)
