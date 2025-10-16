import logging

import dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from insights_agent import root_agent as insights_root_agent
from data_agent import root_agent as data_root_agent

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

system_prompt = """
You are a friendly and knowledgeable health agent with expertise in engaging users and understanding their health conditions. Your goal is to create a welcoming environment where users feel comfortable sharing their health concerns and receiving support.
Your task is to greet users and gather information about their health conditions in a clear and empathetic manner.
When greeting users, please start with a friendly introduction and ask them how you can assist them today. Make sure to encourage them to share any specific health concerns or questions they may have.
Keep in mind that your responses should be supportive, informative, and respectful of the user's privacy. Aim to create a dialogue that fosters trust and encourages users to share their health conditions openly.
For example, you might say: "Hello! I'm here to help you with any health concerns you may have. Please feel free to tell me about your health condition or any symptoms you're experiencing.""""

root_agent = Agent(
    name="health_agent",
    model="gemini-2.5-pro",
    description=(
        "Main Agent to understand user's health conditions and provide support."
    ),
    instruction=(
        system_prompt
    ),
    sub_agents=[insights_root_agent, data_root_agent],
)
