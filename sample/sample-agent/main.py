import logging

import dotenv
from google.adk.agents import Agent

dotenv.load_dotenv()

logger = logging.getLogger(__name__)


root_agent = Agent(
    name="sample_adk_agent",
    model="gemini-2.5-pro",
    description=(
        "Agent to answer questions about the time and weather in a city and query google docs."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
        " and query google docs."
    ),
)
