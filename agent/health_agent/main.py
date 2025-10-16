import logging

import dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from insights_agent import root_agent as insights_root_agent
from data_agent import root_agent as data_root_agent

dotenv.load_dotenv()

logger = logging.getLogger(__name__)


root_agent = Agent(
    name="health_agent",
    model="gemini-2.5-pro",
    description=(
        "Agent to answer questions about the time and weather in a city and query google docs."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
        " and query google docs."
    ),
    sub_agents=[insights_root_agent, data_root_agent],
)
