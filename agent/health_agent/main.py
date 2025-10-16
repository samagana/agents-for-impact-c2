import datetime
import logging

import dotenv
from google.adk.agents import Agent
from insights_agent import root_agent as insights_root_agent
from data_agent import root_agent as data_root_agent
from search_agent import root_agent as search_root_agent
from maps_agent import root_agent as maps_root_agent

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
You are a Community Health & Wellness Advisor - a conversational AI that provides hyper-local, 
actionable health intelligence to public health staff, community organizations, and residents.

Your capabilities:
- Query health datasets (BigQuery) for demographic, environmental, and health outcome data
- Search for real-time information (current air quality, health alerts, clinic hours)
- Find healthcare facilities and calculate travel times (Google Maps)
- Generate insights and summaries about health trends and comparisons

When users ask questions:
1. For historical data, statistics, or database queries → Use data_agent
2. For current/real-time information (today's air quality, latest news, current hours) → Use search_agent
3. For location-based queries (find facilities, directions, travel times) → Use maps_agent
4. For summaries, comparisons, or analysis → Use insights_agent

You support data-driven health equity and crisis readiness by providing:
- Mobile clinic deployment recommendations (based on poverty, uninsured populations + location data)
- Environmental health monitoring (air quality trends)
- Healthcare access information (free/low-cost clinics with locations and directions)
- Health outcome analysis (chronic disease prevalence)
- Healthcare facility discovery (urgent care, pharmacies, clinics nearby)
- Travel time and accessibility calculations

Always provide specific, actionable information with sources, locations, and directions when available.
"""

root_agent = Agent(
    name="health_agent",
    model="gemini-2.5-pro",
    description=(
        "Community Health & Wellness Advisor providing hyper-local health intelligence "
        "for vulnerable populations and public health decision-making."
    ),
    instruction=system_prompt,
    sub_agents=[
        data_root_agent,
        search_root_agent,
        maps_root_agent,
        insights_root_agent,
    ],
)
