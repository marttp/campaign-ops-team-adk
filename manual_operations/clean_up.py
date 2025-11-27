import os
import vertexai
from vertexai import agent_engines

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)

agents_list = list(agent_engines.list())
if agents_list:
    remote_agent = agents_list[0]
else:
    print("❌ No agents found. Please deploy first.")

agent_engines.delete(resource_name=remote_agent.resource_name, force=True)

print("✅ Agent successfully deleted")
