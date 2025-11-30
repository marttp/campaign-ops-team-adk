from google.adk.agents import LlmAgent
import google.genai.types as types

from ..tools import (
    eligibility_tool,
    email_tool,
    push_notification_tool,
    find_audience_tool,
    create_audience_tool,
    campaign_creation_tool,
)
from google.adk.models import Gemini

MODEL = "gemini-2.5-flash-lite"

retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Delivery Agent
delivery_agent = LlmAgent(
    name="delivery_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Coordinates tools to prepare user attributes, email/push payloads, and final campaign components.",
    instruction="""
    You are the Delivery Agent. Your goal is to execute the campaign plan.
    Use the available tools to:
    1. Set eligibility rules.
    2. Find and create the audience.
    3. Prepare email and push payloads.
    4. Create the final campaign.
    Output the final campaign creation result.
    """,
    tools=[
        eligibility_tool,
        email_tool,
        push_notification_tool,
        find_audience_tool,
        create_audience_tool,
        campaign_creation_tool,
    ],
)
