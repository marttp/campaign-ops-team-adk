import google.genai.types as types
from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.tools import AgentTool
from ..tools import segment_group_preparing_tool
from google.adk.models import Gemini
from .google_search_agent import search_agent

MODEL = "gemini-2.5-flash-lite"

retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Goal Planning Agent
goal_planning_agent = LlmAgent(
    name="goal_planning_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Converts the frontline package into actionable goals, KPIs, and sequencing.",
    instruction="""
    You are the Goal Planning Agent. Take the `frontline_result` JSON, restate the campaign_type and
    objectives, then produce a structured planning brief that shows how the campaign will move from
    concept to activation. Think deliberately about four pillars: Action (what gets built or launched),
    How (channels, tooling, sequencing), Adapt (contingencies, personalization, experimentation), and
    Integration & Collaboration (partners, dependent orgs, required approvals).

    Respond using JSON with the following keys:
    - campaign_type
    - primary_goal
    - secondary_goal (null if none)
    - action_framework: list of objects each containing {action, how, adapt_plan, integration_points, collaboration_owner}
    - measurement_plan: {primary_kpis: [], secondary_kpis: [], checkpoints: []}
    - schedule_intent: {launch_window, cadences, prerequisites}
    - dependencies_and_notes: include frontline insights, blockers, or data requests
    """,
    tools=[AgentTool(agent=search_agent)],
    output_key="goal_plan",
)

# Segmentation Discovery Agent
segmentation_discovery_agent = LlmAgent(
    name="segmentation_discovery_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Turns the goal plan into concrete segments, rules, and integration hooks.",
    instruction="""
    You are the Segmentation Discovery Agent. Using the latest `goal_plan`, explore behavioral,
    demographic, and lifecycle signals to create executable segments. For each segment, clarify how
    it supports the action plan, which tools or data integrations it needs, and collaboration touchpoints
    (growth ops, data science, CRM engineering, etc.).

    Provide JSON with:
    - segment_overview: bullet summary tying segments to actions/how/adapt/integration themes
    - segments: list where each item includes {name, definition, estimated_size, activation_channel,
      tooling_or_integrations, collaboration_required, risks, next_best_action}
    - tool_calls: capture any invocations or outputs from `segment_group_preparing_tool`
    """,
    tools=[segment_group_preparing_tool, AgentTool(agent=search_agent)],
    output_key="segments_plan",
)

# Planner Critic Agent
planner_critic_agent = LlmAgent(
    name="planner_critic_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Validates feasibility, conflicts, and downstream readiness for Planner outputs.",
    instruction="""
    You are the Planner Critic Agent. Evaluate the combined `goal_plan` and `segments_plan` for:
    - alignment with frontline intent and campaign objectives
    - completeness across action/how/adapt/integration/collaboration dimensions
    - feasibility of timelines, KPIs, and tool dependencies
    - clarity of hand-off requirements for the Reporter/Delivery groups

    If the plans meet the bar, respond exactly with "APPROVED". If not, provide concise, prioritized
    feedback including what needs to change and where (goal plan vs. segments).
    """,
    output_key="planner_critic_feedback",
)

# Reporter Agent
reporter_agent = LlmAgent(
    name="reporter_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Produces a clean, validated, normalized JSON for delivery.",
    instruction="""
    You are the Reporter Agent, the final step of the Planner group. Synthesize the approved
    `goal_plan` + `segments_plan` into the orchestrator-ready JSON contract:
    {
      "campaign_type": str,
      "primary_goal": str,
      "secondary_goal": str | null,
      "segments": [...],
      "audience_size": estimates per key segment and total,
      "constraints": [risks, compliance, dependencies],
      "schedule_plan": {launch_window, cadences, blockers},
      "delivery_plan": {channel_handoffs, creative_needs, tooling_integration},
      "risks": [{risk, mitigation, owner}],
      "confidence": 0-1 float,
      "references": {audience_tools_used, frontline_links}
    }

    Ensure the JSON is valid, compact, and explicitly mentions collaboration/integration notes needed
    by the Delivery group.
    """,
)

# Planner Loop + Manager Agent
planner_strategy_loop = LoopAgent(
    name="planner_strategy_loop",
    sub_agents=[goal_planning_agent, segmentation_discovery_agent, planner_critic_agent],
    max_iterations=3,
)

planner_manager_agent = SequentialAgent(
    name="planner_manager_agent",
    sub_agents=[planner_strategy_loop, reporter_agent],
)
