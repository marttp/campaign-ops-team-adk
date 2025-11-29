from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.google_search_tool import google_search

from campaign_ops_team.config import retry_config, MODEL

# Google Search Agent
google_search_agent = LlmAgent(
    name="google_search_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Supports competitive research, seasonal patterns, industry insights.",
    instruction="""
    You are the Google Search Agent. Your goal is to provide competitive research, seasonal patterns, and industry insights.
    Use the google_search tool to find information.
    """,
    tools=[google_search],
)
