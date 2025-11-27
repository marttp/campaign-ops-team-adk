from google.adk.agents import LlmAgent

from campaign_ops_team.tools.tools import (
    eligibility_tool, email_tool, push_notification_tool,
    find_audience_tool, create_audience_tool, campaign_creation_tool
)
from campaign_ops_team.config import retry_config, MODEL
from google.adk.models import Gemini
from campaign_ops_team.config import MODEL, retry_config

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
        eligibility_tool, email_tool, push_notification_tool,
        find_audience_tool, create_audience_tool, campaign_creation_tool
    ]
)
