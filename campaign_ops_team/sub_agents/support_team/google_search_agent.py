from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.google_search_tool import google_search

from campaign_ops_team.config import retry_config, MODEL

# Google Search agent
google_search_agent = LlmAgent(
    name="google_search_agent",
    model=Gemini(model=MODEL, retry_options=retry_config),
    description="Searches for information using Google search",
    instruction="""Use the google_search tool to find information on the given topic. Return the raw search results.
    If the user asks for a list of papers, then give them the list of research papers you found and not the summary.""",
    tools=[google_search]
)
