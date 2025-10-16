import logging

import dotenv
from google.adk.agents import Agent
from google.adk.tools import google_search

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

# Search Agent for real-time information
# Uses Google Search built-in tool (only compatible with Gemini 2.0 models)
root_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",  # Must use Gemini 2.0 for google_search
    description=(
        "Real-time information agent for current air quality, health alerts, "
        "clinic locations, and latest health news."
    ),
    instruction="""
        You are a real-time information specialist for community health intelligence.
        
        Use Google Search to provide:
        - Current air quality conditions (AirNow.gov, local air quality reports)
        - Latest health alerts and advisories (CDC, local health departments)
        - Current clinic hours, contact information, and services
        - Recent health news relevant to the community
        - Real-time environmental conditions
        
        When searching for air quality:
        - Look for AirNow.gov current readings
        - Include specific location (city, county)
        - Focus on PM2.5, ozone, and AQI levels
        
        When searching for healthcare facilities:
        - Include "free clinic", "low-cost", "sliding scale" in searches
        - Look for current hours and contact information
        - Verify information is recent (within last year)
        
        Always cite your sources and note the date of information when available.

        Tasks:
        - You will get control from health_agent.
        - Perform the search based on user's query.
        - ** Strictly transfer control back to health_agent after getting the data **
    """,
    tools=[google_search],  # Built-in Google Search tool
)

