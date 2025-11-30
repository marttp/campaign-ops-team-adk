import google.genai.types as types
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.models import Gemini
from google.adk.tools.function_tool import FunctionTool

MODEL = "gemini-2.5-flash-lite"

retry_config = types.HttpRetryOptions(
    attempts=2,
    exp_base=3,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


# ---------------------------------------------------------------------------
# Local tool definitions (mock implementations for Delivery group)
# ---------------------------------------------------------------------------


def eligibility_tool(rules: str) -> str:
    return f"Eligibility Rules Set: {rules}"


def find_audience_tool(criteria: str) -> str:
    return f"Audience Found: [Mock] criteria={criteria}, matched_users=42,000"


def create_audience_tool(audience_name: str, criteria: str) -> str:
    return f"Audience Created: {audience_name} using {criteria}"


def email_tool(template_id: str, content: str) -> str:
    return f"Email Payload: template={template_id}, content={content[:60]}..."


def push_notification_tool(title: str, body: str) -> str:
    return f"Push Payload: title={title}, body={body[:80]}..."


def campaign_creation_tool(campaign_name: str, details: str) -> str:
    return f"Campaign Created: {campaign_name} | details={details[:80]}..."


# Eligibility Specialist Agent
eligibility_specialist_agent = LlmAgent(
    name="eligibility_specialist_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Prepares eligibility attributes and audience objects from planner instructions.",
    instruction="""
    You are the Eligibility Specialist in the Delivery group. Consume `planner_result` and translate the
    delivery_plan.eligible guidance plus relevant segments into a concrete audience definition.

    Required steps:
    1. List the exact eligibility attributes/rules (e.g., ">=20 wallet transactions in 30 days", "spend >=10,000 THB").
    2. Call `eligibility_tool` with a concise rule string to document the configuration.
    3. Call `find_audience_tool` to simulate user counts and capture the result.
    4. Call `create_audience_tool` to register the audience name that will be referenced downstream.
    5. Call `campaign_creation_tool` to log the eligibility configuration as a campaign artifact (same
       interface the other specialists use).

    If the planner output is missing any value, infer it from segments + KPI targets before proceeding. Provide
    JSON like {
      "audience_name": str,
      "eligibility_rules": [str],
      "tool_outputs": {
          "eligibility": str,
          "find_audience": str,
          "create_audience": str,
          "campaign_creation": str
      },
      "notes": str
    }
    """,
    tools=[
        FunctionTool(eligibility_tool),
        FunctionTool(find_audience_tool),
        FunctionTool(create_audience_tool),
        FunctionTool(campaign_creation_tool),
    ],
    output_key="eligibility_output",
)

# Email Specialist Agent
email_specialist_agent = LlmAgent(
    name="email_specialist_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Creates the email payload with full subject/body/CTA per planner delivery plan.",
    instruction="""
    You are the Email Campaign Specialist. Use `planner_result.delivery_plan.email`, campaign_theme, hero_promise,
    and segments to craft consumer-facing creative that sounds like "Free Point Dash" or "Spend 10K THB in June,
    get 5% cashback on 10 trips in July". If any creative element is missing, derive it from the planner
    action_plan + KPI targets so downstream systems have concrete copy.

    Required output JSON:
    {
      "subject": str,
      "body": str,
      "cta": str,
      "personalization": [str],
      "kpi_threshold": str,
      "tool_output": str,
      "creation_result": str,
      "notes": str
    }

    Always call `email_tool` with the template/content you construct and capture the response in `tool_output`.
    After the payload is ready, call `campaign_creation_tool` with the email campaign name + summary and store
    the response in `creation_result`.
    """,
    tools=[FunctionTool(email_tool), FunctionTool(campaign_creation_tool)],
    output_key="email_output",
)

# Push Specialist Agent
push_specialist_agent = LlmAgent(
    name="push_specialist_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Creates push notification payload from planner delivery plan.",
    instruction="""
    You are the Push Notification Specialist. Study `planner_result.delivery_plan.push`, campaign_theme, hero_promise,
    schedule, and KPIs to produce a ready-to-send push payload. If planner content is incomplete, infer the
    title/body/CTA and describe personalization logic derived from segments so that the push reads like a real
    consumer hook (e.g., "Unlock 5% Cashback on Your Next 10 Rides").

    Output JSON:
    {
      "title": str,
      "body": str,
      "cta": str,
      "personalization": [str],
      "kpi_threshold": str,
      "tool_output": str,
      "creation_result": str,
      "notes": str
    }

    Always call `push_notification_tool` with the payload you craft and record the response in `tool_output`.
    After the payload is ready, call `campaign_creation_tool` with the push campaign name + summary and store
    the response in `creation_result`.
    """,
    tools=[FunctionTool(push_notification_tool), FunctionTool(campaign_creation_tool)],
    output_key="push_output",
)

# Run channel specialists in parallel
delivery_parallel_agent = ParallelAgent(
    name="delivery_parallel_agent",
    sub_agents=[
        eligibility_specialist_agent,
        email_specialist_agent,
        push_specialist_agent,
    ],
)

# Aggregator Agent
delivery_aggregator_agent = LlmAgent(
    name="delivery_aggregator_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Synthesizes channel outputs and finalizes campaign creation.",
    instruction="""
    You are the Delivery Aggregator Agent. Combine `planner_result`, `eligibility_output`, `email_output`, and
    `push_output` to finalize the execution packet. If any specialist left placeholders or if planner data was
    incomplete, you must outline the missing content structure (objective, KPI thresholds, creative brief). Do not
    call any additional tools; rely on the specialist `creation_result` fields as the canonical create-campaign
    outputs.

    Produce JSON with:
    {
      "campaign_name": str,
      "campaign_type": str,
      "campaign_theme": str,
      "hero_promise": str,
      "campaign_messaging": planner_result.campaign_messaging,
      "audience_reference": str,
      "eligible": eligibility_output,
      "email": email_output,
      "push": push_output,
      "kpi_targets": planner_result.kpi_targets,
      "launch_plan": planner_result.schedule_plan,
      "summary": str,
      "creation_events": {
          "eligible": eligibility_output.tool_outputs.campaign_creation,
          "email": email_output.creation_result,
          "push": push_output.creation_result
      }
    }
    Always describe any inferred content or KPIs you authored so downstream reviewers know what was assumed.
    """,
    output_key="delivery_result",
)

# Delivery Agent Pipeline
delivery_agent = SequentialAgent(
    name="delivery_agent",
    sub_agents=[delivery_parallel_agent, delivery_aggregator_agent],
)
