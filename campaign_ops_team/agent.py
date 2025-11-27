import logging
import vertexai
from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from .config import MODEL, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, retry_config

# from campaign_ops_team.sub_agents.frontline_group.frontline_agents import intake_agent, frontline_critic_agent
# from campaign_ops_team.sub_agents.planner_group.planner_agents import (
#     goal_planning_agent, segmentation_discovery_agent, planner_critic_agent, reporter_agent, google_search_agent
# )
# from campaign_ops_team.sub_agents.delivery_group.delivery_agent import delivery_agent

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

vertexai.init(
    project=GOOGLE_CLOUD_PROJECT,
    location=GOOGLE_CLOUD_LOCATION,
)

root_agent = Agent(
    model=Gemini(model=MODEL, retry_options=retry_config),
    name="root_agent",
    description="Campaign Ops Orchestrator",
    instruction="""
    You are the Campaign Ops Orchestrator.
    Your goal is to manage the end-to-end campaign creation process.
    
    The process flow must be followed:
    1. Frontline Group
    2. Planner Group
    3. Delivery Group

    Start by asking about the goals and objectives that company want to achieve.
    Then transfer to the Frontline Group.
    """,
    tools=[],
)
