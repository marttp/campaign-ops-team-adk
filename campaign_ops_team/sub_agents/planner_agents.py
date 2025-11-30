import google.genai.types as types
from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.tools import AgentTool
from google.adk.tools.function_tool import FunctionTool
from google.adk.models import Gemini
from .google_search_agent import search_agent
from .frontline_agents import internal_data_agent_tool

MODEL = "gemini-2.5-flash-lite"

retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


def segment_group_preparing_tool(segment_criteria: str) -> str:
    return f"Segment Prepared: {segment_criteria}"


# Goal Planning Agent
goal_planning_agent = LlmAgent(
    name="goal_planning_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Converts the frontline package into actionable campaign definition, actions, and KPIs.",
    instruction="""
    You are the Goal Planning Agent. Take the `frontline_result` JSON, confirm the campaign_type, and
    craft the official campaign definition that the Planner group will own. You must translate the intake
    hypotheses into SPECIFIC action items, campaign narratives, and collaboration asks that Delivery can
    later execute. If baseline information is unclear, call `internal_data_agent_tool` to pull the
    `mock_current_kpis` for the 1,000-user scale reference. When metrics or KPI thresholds are missing,
    recommend concrete values yourself (grounded in baselines) without asking the user; note any assumptions
    so they can be confirmed at the end of the pipeline.

    Think through:
    - Action: what must be built/launched (journeys, promos, messaging themes)
    - How: channels, tooling, sequencing, and resource owners
    - Adapt: contingency tests, personalization logic, experimentation plans
    - Integration & Collaboration: teams, approvals, data dependencies for eligibility/email/push

    Respond using JSON with:
    {
      "campaign_type": str,
      "campaign_name": str,
      "campaign_theme": str (consumer-facing theme, e.g., "Free Points Blitz"),
      "hero_promise": str (short slogan level promise),
      "primary_goal": str,
      "secondary_goals": [str],
      "action_plan": [
         {"action": str, "channel_focus": list of strings chosen from ["eligible", "email", "push", "omni"], "how": str,
          "quant_target": {"metric": str, "target_value": str, "timeframe": str},
          "reward_logic": str,
          "consumer_message": str (e.g., "Spend 10K THB now, unlock 5% cashback next month"),
          "adapt_plan": str,
          "collaboration_owner": str,
          "success_metric": str}
      ],
      "measurement_plan": {
          "primary_kpis": [],
          "secondary_kpis": [],
          "checkpoints": [],
          "kpi_targets": [
              {"metric": str, "baseline": str, "target": str, "unit": str, "timeframe": str}
          ]
      },
      "schedule_intent": {"launch_window": str, "cadences": [], "prerequisites": []},
      "collaboration_matrix": [{"team": str, "need": str, "status": str}],
      "open_questions": [str]
    }
    Every KPI target must be numeric (e.g., ">=20 QR transactions per user in 30 days" or "Pay >=10,000 THB
    this month to unlock a 200 THB reward next month").
    """,
    tools=[AgentTool(agent=search_agent), FunctionTool(func=internal_data_agent_tool)],
    output_key="goal_plan",
)

# Segmentation Discovery Agent
segmentation_discovery_agent = LlmAgent(
    name="segmentation_discovery_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Turns the goal plan into explicit segments/audience instructions.",
    instruction="""
    You are the Segmentation Discovery Agent. Pair the `goal_plan` with the frontline evidence to produce
    highly specific audience definitions. Each segment must describe who they are, why they matter to the
    action plan, how large they are, and what eligibility attributes or personalization hooks Delivery must
    configure. Pull baselines from `internal_data_agent_tool` when you need concrete numbers. When a numeric
    detail (frequency, spend, reward) is missing, recommend it directly based on mock KPIs instead of escalating
    back to the user.

    Provide JSON with:
    {
      "segment_overview": ["summary bullets tying segments back to campaign actions"],
      "segments": [
        {
          "name": str,
          "campaign_alignment": str,
          "definition": str,
          "estimated_size": str,
          "eligibility_attributes": [str],
          "activation_channel": str from {"eligible", "email", "push", "omni"},
          "tooling_or_integrations": [str],
          "collaboration_required": [str],
          "frequency_goal": str (e.g., ">=20 wallet transactions/user/month"),
          "spend_goal": str (e.g., ">=10,000 THB per user in 30 days"),
          "reward_mechanics": str,
          "offer_copy": str (specific benefit line such as "Spend 10K THB, earn 5% cashback"),
          "cta_hint": str (imperative CTA like "Activate Cashback Run"),
          "risks": [str],
          "next_best_action": str
        }
      ],
      "tool_calls": record outputs from `segment_group_preparing_tool` whenever you need to materialize
        a segment definition or pass it to Delivery tooling.
    }

    Call `segment_group_preparing_tool` to draft any complex criteria objects and cite its outputs in
    "tool_calls". Use the Google Search agent if market/seasonal insight is necessary.
    """,
    tools=[
        FunctionTool(func=segment_group_preparing_tool),
        AgentTool(agent=search_agent),
        FunctionTool(func=internal_data_agent_tool),
    ],
    output_key="segments_plan",
)

# Planner Critic Agent
planner_critic_agent = LlmAgent(
    name="planner_critic_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Validates feasibility, conflicts, and downstream readiness for Planner outputs.",
    instruction="""
    You are the Planner Critic Agent. Pressure-test both `goal_plan` and `segments_plan`:
    - Do the proposed campaign actions ladder up to the frontline objective and have clear owners?
    - Are the eligibility/email/push plans specific enough for Delivery to create content + audiences?
    - Are timelines, KPIs, and dependencies realistic and de-conflicted?
    - Do segments have concrete attributes, tooling notes, and coverage of total audience size?

    If the plans meet the bar, respond exactly with "APPROVED". Otherwise provide concise, prioritized
    feedback referencing which part (goal plan vs. segments) must change.
    """,
    output_key="planner_critic_feedback",
)

# Reporter Agent
reporter_agent = LlmAgent(
    name="reporter_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Produces a clean, validated, normalized JSON for delivery.",
    instruction="""
    You are the Reporter Agent, the final step of the Planner group. Merge the approved `goal_plan`
    and `segments_plan` into the orchestrator contract. Output JSON that Delivery can consume without
    guessing. Required shape:
    {
      "campaign_type": str,
      "campaign_name": str,
      "campaign_theme": str,
      "hero_promise": str,
      "primary_goal": str,
      "secondary_goals": [str],
      "campaign_messaging": [
          {"audience": str, "message": str, "timeframe": str}
      ],
      "segments": list of segment objects copied from `segments_plan`,
      "kpi_targets": [
          {"metric": str, "baseline": str, "target": str, "unit": str, "timeframe": str}
      ],
      "audience_size": {"total_estimate": str, "per_segment": [{"name": str, "estimate": str}]},
      "constraints": [str],
      "schedule_plan": {"launch_window": str, "cadences": [], "blockers": []},
      "delivery_plan": {
          "eligible": {"objective": str, "attributes": [str], "notes": str,
                        "kpi_threshold": str},
          "email": {"objective": str, "content_brief": {"subject": str, "body": str, "cta": str},
                     "personalization": [str],
                     "kpi_threshold": str},
          "push": {"objective": str, "content_brief": {"title": str, "body": str, "cta": str},
                    "personalization": [str],
                    "kpi_threshold": str}
      },
      "risks": [{"risk": str, "severity": str, "mitigation": str, "owner": str}],
      "confidence": float between 0 and 1,
      "references": {"audience_tools_used": [str], "frontline_links": [str], "notes": str}
    }

    Ensure all narrative text is concise and grounded in the upstream evidence so Delivery can set
    eligibility, draft content (email + push), and finalize the campaign payloads immediately. Every
    KPI/threshold must state a numeric requirement such as ">=20 wallet transactions per user in 30 days"
    or "Pay 10,000 THB this month to receive 200 THB next month". The campaign name, theme, hero promise, and
    campaign_messaging entries must read like persuasive, consumer-facing copy (e.g., "Free Point Dash"
    or "Spend 10K THB in June, unlock 5% cashback on 10 July rides"). Proactively recommend any missing
    metrics or creative details rather than pausing for user clarification; only surface clarifying questions
    alongside the final output if absolutely necessary.
    """,
    output_key="planner_result",
)

# Planner Loop + Manager Agent
planner_strategy_loop = LoopAgent(
    name="planner_strategy_loop",
    sub_agents=[
        goal_planning_agent,
        segmentation_discovery_agent,
        planner_critic_agent,
    ],
    max_iterations=3,
)

planner_manager_agent = SequentialAgent(
    name="planner_manager_agent",
    sub_agents=[planner_strategy_loop, reporter_agent],
)
