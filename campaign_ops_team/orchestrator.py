import logging
import uuid
from typing import Optional

from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool

# Sub-agents
from campaign_ops_team.sub_agents.frontline_group.frontline_agents import (
    intake_agent,
    frontline_critic_agent,
)
from campaign_ops_team.sub_agents.planner_group.planner_agents import (
    goal_planning_agent,
    segmentation_discovery_agent,
    planner_critic_agent,
    reporter_agent,
    # google_search_agent # If needed
)
from campaign_ops_team.sub_agents.delivery_group.delivery_agent import delivery_agent

logger = logging.getLogger(__name__)

async def _get_response_text(runner: InMemoryRunner, message: str, session_id: str) -> str:
    full_text = ""
    # Attempt to use string message. If it fails, we might need types.Content
    try:
        async for event in runner.run_async(user_id="orchestrator", session_id=session_id, new_message=message):
            # Inspect event for text content
            if hasattr(event, "content") and event.content:
                parts = getattr(event.content, "parts", [])
                if parts:
                    for part in parts:
                        text = getattr(part, "text", "")
                        if text:
                            full_text += text
    except Exception as e:
        logger.error(f"Error during agent run: {e}")
        raise e

    return full_text

async def run_frontline_group(request: str) -> str:
    """Executes the Frontline Group agents to process a campaign request. Returns the intake summary."""
    logger.info("Starting Frontline Group execution.")

    # Initialize runners
    intake_runner = InMemoryRunner(agent=intake_agent)
    critic_runner = InMemoryRunner(agent=frontline_critic_agent)

    intake_session = str(uuid.uuid4())
    critic_session = str(uuid.uuid4())

    # 1. Initial Intake
    current_request = f"Analyze this campaign request: {request}"
    intake_output = await _get_response_text(intake_runner, current_request, intake_session)
    logger.debug(f"Intake output: {intake_output}")

    # Loop max 3 times
    for i in range(3):
        # 2. Critic
        critic_input = f"Evaluate this intake summary:\n{intake_output}"
        critique = await _get_response_text(critic_runner, critic_input, critic_session)
        logger.debug(f"Critic output (iteration {i}): {critique}")

        if "APPROVED" in critique:
            logger.info("Frontline Group Approved.")
            return intake_output

        # 3. Refine
        refine_input = f"The critic provided this feedback:\n{critique}\nPlease refine the intake summary."
        intake_output = await _get_response_text(intake_runner, refine_input, intake_session)
        logger.debug(f"Refined Intake: {intake_output}")

    logger.warning("Frontline Group max iterations reached. Returning last intake.")
    return intake_output

async def run_planner_group(frontline_output: str) -> str:
    """Executes the Planner Group agents (Goal, Segmentation, Critic, Reporter) to create a detailed campaign plan. Takes Frontline output as input."""
    logger.info("Starting Planner Group execution.")

    goal_runner = InMemoryRunner(agent=goal_planning_agent)
    seg_runner = InMemoryRunner(agent=segmentation_discovery_agent)
    critic_runner = InMemoryRunner(agent=planner_critic_agent)
    reporter_runner = InMemoryRunner(agent=reporter_agent)

    goal_session = str(uuid.uuid4())
    seg_session = str(uuid.uuid4())
    critic_session = str(uuid.uuid4())
    reporter_session = str(uuid.uuid4())

    # Initial Goal Planning
    current_input = frontline_output

    goal_output = await _get_response_text(goal_runner, f"Create a goal plan based on this intake:\n{current_input}", goal_session)

    # Loop max 3 times
    for i in range(3):
        # Segmentation
        seg_output = await _get_response_text(seg_runner, f"Based on this goal plan, generate segments:\n{goal_output}", seg_session)

        # Critic
        critic_input = f"Evaluate the following strategy.\nGOAL PLAN:\n{goal_output}\n\nSEGMENTATION:\n{seg_output}"
        critique = await _get_response_text(critic_runner, critic_input, critic_session)

        if "APPROVED" in critique:
            logger.info("Planner Group Approved.")
            # Reporter
            reporter_input = f"Finalize this plan for delivery.\nGOAL PLAN:\n{goal_output}\n\nSEGMENTATION:\n{seg_output}"
            final_report = await _get_response_text(reporter_runner, reporter_input, reporter_session)
            return final_report

        # Refine Goal Planning
        goal_output = await _get_response_text(goal_runner, f"Critic feedback:\n{critique}\nPlease update the goal plan.", goal_session)

    # Fallback to reporter
    logger.warning("Planner Group max iterations reached. Proceeding to Reporter.")
    reporter_input = f"Finalize this plan (iterations exceeded).\nGOAL PLAN:\n{goal_output}\n\nSEGMENTATION:\n{seg_output}"

    final_report = await _get_response_text(reporter_runner, reporter_input, reporter_session)
    return final_report

async def run_delivery_group(planner_output: str) -> str:
    """Executes the Delivery Group agent to finalize and schedule the campaign. Takes Planner output as input."""
    logger.info("Starting Delivery Group execution.")

    delivery_runner = InMemoryRunner(agent=delivery_agent)
    session_id = str(uuid.uuid4())

    delivery_input = f"Execute the following campaign plan:\n{planner_output}"
    result = await _get_response_text(delivery_runner, delivery_input, session_id)

    return result

# Define Tools
run_frontline_group_tool = FunctionTool(func=run_frontline_group)
run_planner_group_tool = FunctionTool(func=run_planner_group)
run_delivery_group_tool = FunctionTool(func=run_delivery_group)
