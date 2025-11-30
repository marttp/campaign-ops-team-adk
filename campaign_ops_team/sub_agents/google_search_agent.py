from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.google_search_tool import google_search
import google.genai.types as types

MODEL = "gemini-2.5-flash-lite"

retry_config = types.HttpRetryOptions(
    attempts=2,
    exp_base=3,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Google Search Agent
search_agent = LlmAgent(
    name="google_search_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Supports competitive research, seasonal patterns, industry insights.",
    instruction="""
    You are the Google Search Agent. Your goal is to provide competitive research, seasonal patterns, and industry insights.
    Use the google_search tool to find information.
    """,
    tools=[google_search],
)
