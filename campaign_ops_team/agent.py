import logging
import vertexai
from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
import google.genai.types as types
import os

MODEL = "gemini-2.5-flash-lite"

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

# safety_settings = [
#     types.SafetySetting(
#         category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
#         threshold=types.HarmBlockThreshold.OFF,
#     ),
# ]

generate_content_config = types.GenerateContentConfig(
    #    safety_settings=safety_settings,
    temperature=0.28,
    max_output_tokens=1000,
    top_p=0.95,
)


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
