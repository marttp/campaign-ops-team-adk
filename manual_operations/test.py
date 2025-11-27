import asyncio
import os
import vertexai
from vertexai import agent_engines

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)

# Get the most recently deployed agent
agents_list = list(agent_engines.list())
if agents_list:
    remote_agent = agents_list[0]  # Get the first (most recent) agent
    print(f"✅ Connected to deployed agent: {remote_agent.resource_name}")
else:
    print("❌ No agents found. Please deploy first.")


client = vertexai.Client(
    project=GOOGLE_CLOUD_PROJECT,
    location=GOOGLE_CLOUD_LOCATION,
)

adk_app = client.agent_engines.get(name=remote_agent.resource_name)


async def main():
    user_id = "user_123123123"
    session = await adk_app.async_create_session(user_id=user_id)
    print(session)
    async for event in adk_app.async_stream_query(
        user_id=user_id,
        session_id=session["id"],
        message="Hello",
    ):
        print(event)


asyncio.run(main())
