import logging
import os
import vertexai
import google.genai.types as types
from google.adk.agents.llm_agent import Agent
from google.adk.tools import AgentTool
from google.adk.models.google_llm import Gemini
from vertexai import agent_engines
from .prompt import CAMPAIGN_ORCHESTRATOR_PROMPT

# Import Manager Agents
from .sub_agents.frontline_agents import frontline_manager_agent
from .sub_agents.planner_agents import planner_manager_agent
from .sub_agents.delivery_agent import delivery_agent

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

# Initialize Vertex AI
vertexai.init(
    project=GOOGLE_CLOUD_PROJECT,
    location=GOOGLE_CLOUD_LOCATION,
)

MODEL = "gemini-2.5-flash-lite"

retry_config = types.HttpRetryOptions(
    attempts=2,
    exp_base=3,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

root_agent = Agent(
    model=Gemini(model=MODEL, retry_options=retry_config),
    name="root_agent",
    description="Campaign Ops Orchestrator",
    instruction=CAMPAIGN_ORCHESTRATOR_PROMPT,
    tools=[
        AgentTool(agent=frontline_manager_agent),
        AgentTool(agent=planner_manager_agent),
        AgentTool(agent=delivery_agent),
    ],
)

# Wrap the agent in an AdkApp object
app = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)
