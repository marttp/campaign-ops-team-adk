import logging
import vertexai
from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from vertexai import agent_engines

from .config import MODEL, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, retry_config
from .prompt import CAMPAIGN_ORCHESTRATOR_PROMPT
from .orchestrator import run_frontline_group_tool, run_planner_group_tool, run_delivery_group_tool

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# Initialize Vertex AI
# Note: In some environments this might need specific credentials or project ID handling.
# If GOOGLE_CLOUD_PROJECT is set, it uses it.
vertexai.init(
    project=GOOGLE_CLOUD_PROJECT,
    location=GOOGLE_CLOUD_LOCATION,
)

root_agent = Agent(
    model=Gemini(model=MODEL, retry_options=retry_config),
    name="root_agent",
    description="Campaign Ops Orchestrator",
    instruction=CAMPAIGN_ORCHESTRATOR_PROMPT,
    tools=[
        run_frontline_group_tool,
        run_planner_group_tool,
        run_delivery_group_tool
    ],
)

# Wrap the agent in an AdkApp object
app = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)
