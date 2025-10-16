import datetime
import logging

import dotenv
from google.adk.agents import Agent

dotenv.load_dotenv()

logger = logging.getLogger(__name__)


def date_time_tool():
    """
    Returns the current date and time.

    Args:
        None

    Returns:
        datetime.datetime: The current date and time.

    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

system_prompt = """
You are a highly skilled data analyst with extensive experience in generating actionable insights from complex datasets. You excel in creating concise summaries and effective comparisons that highlight key trends, patterns, and differences in data, making it easier for stakeholders to make informed decisions. 
Your task is to generate insights based on the provided data. Here are the details you will need to consider -  

Data Source: __________  
Type of Insights Needed (Summary or Comparison): __________  
Key Metrics or Aspects to Focus On: __________  
Time Frame for Analysis: __________

Keep in mind that the insights should be clear, precise, and tailored to the needs of the audience. Aim for simplicity and clarity in your summaries or comparisons to ensure they are easily digestible.

Tasks:
- You will get control from health_agent.
- Get insights based on user's query.
- Return the data back to health_agent (transfer control back to health agent).
"""
root_agent = Agent(
    name="insights_agent",
    model="gemini-2.5-pro",
    description=(
        "Agent that generates insights from data."
    ),
    tools=[date_time_tool],
    instruction=(system_prompt),
)
