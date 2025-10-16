import logging
import os

import dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from agent.insights_agent import root_agent as insights_root_agent

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
    tools=[AgentTool(insights_root_agent)],
)
