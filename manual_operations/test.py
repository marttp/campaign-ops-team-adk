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
    # print(session)
    # {'appName': '8208879046184927232', 'userId': 'user_123123123', 'state': {}, 'events': [], 'id': '8586600048110862336', 'lastUpdateTime': 1764279302.661221}
    async for event in adk_app.async_stream_query(
        user_id=user_id,
        session_id=session["id"],
        message="Hello",
    ):
        try:
            print(event["content"]["parts"][0]["text"])
        except (KeyError, IndexError, TypeError):
            print(event)


asyncio.run(main())
