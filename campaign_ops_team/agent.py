from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from config import retry_config, MODEL

root_agent = Agent(
    model=Gemini(model=MODEL, retry_options=retry_config),
    name='root_agent',
    description='????',
    instruction='???',
)
