import logging
import os
import json
from typing import Dict, Any, List

import dotenv
from google.adk.agents import Agent
from google.adk.tools.function_tool import FunctionTool
import urllib.request
import urllib.parse

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

def search_nearby_places(location: str, place_type: str = "hospital", radius: int = 5000) -> str:
    """
    Search for nearby places using Google Places API.
    
    Args:
        location: Location to search near (e.g., "90210" or "Los Angeles, CA")
        place_type: Type of place to search for (e.g., "hospital", "pharmacy", "doctor")
        radius: Search radius in meters (default 5000m = ~3 miles)
    
    Returns:
        JSON string with nearby places including name, address, phone, rating
    """
    try:
        # First geocode the location
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(location)}&key={MAPS_API_KEY}"
        with urllib.request.urlopen(geocode_url, timeout=10) as response:
            geocode_data = json.loads(response.read().decode())
        
        if geocode_data.get("status") != "OK":
            return json.dumps({"error": f"Could not find location: {location}"})
        
        lat = geocode_data["results"][0]["geometry"]["location"]["lat"]
        lng = geocode_data["results"][0]["geometry"]["location"]["lng"]
        
        # Now search for places
        places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={place_type}&key={MAPS_API_KEY}"
        with urllib.request.urlopen(places_url, timeout=10) as response:
            places_data = json.loads(response.read().decode())
        
        if places_data.get("status") not in ["OK", "ZERO_RESULTS"]:
            return json.dumps({"error": f"Search failed: {places_data.get('status')}"})
        
        # Format results
        results = []
        for place in places_data.get("results", [])[:5]:  # Limit to top 5
            results.append({
                "name": place.get("name"),
                "address": place.get("vicinity"),
                "rating": place.get("rating", "N/A"),
                "open_now": place.get("opening_hours", {}).get("open_now", "Unknown")
            })
        
        return json.dumps({
            "location_searched": location,
            "coordinates": {"lat": lat, "lng": lng},
            "type": place_type,
            "results": results
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_directions(origin: str, destination: str, mode: str = "driving") -> str:
    """
    Get directions between two locations.
    
    Args:
        origin: Starting location (address, zip code, or place name)
        destination: Ending location (address, zip code, or place name)
        mode: Travel mode - "driving", "walking", "transit", or "bicycling"
    
    Returns:
        JSON string with route information including distance, duration, and steps
    """
    try:
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={urllib.parse.quote(origin)}&destination={urllib.parse.quote(destination)}&mode={mode}&key={MAPS_API_KEY}"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        if data.get("status") != "OK":
            return json.dumps({"error": f"Could not get directions: {data.get('status')}"})
        
        route = data["routes"][0]
        leg = route["legs"][0]
        
        # Extract key steps
        steps = []
        for step in leg["steps"][:8]:  # First 8 steps
            steps.append({
                "instruction": step["html_instructions"].replace("<b>", "").replace("</b>", "").replace("<div", " ").replace("</div>", ""),
                "distance": step["distance"]["text"],
                "duration": step["duration"]["text"]
            })
        
        return json.dumps({
            "origin": leg["start_address"],
            "destination": leg["end_address"],
            "distance": leg["distance"]["text"],
            "duration": leg["duration"]["text"],
            "mode": mode,
            "steps": steps
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})

def calculate_distance(origin: str, destination: str) -> str:
    """
    Calculate distance and travel time between two locations.
    
    Args:
        origin: Starting location
        destination: Ending location
    
    Returns:
        JSON string with distance and duration for driving, walking, and transit
    """
    try:
        results = {}
        for mode in ["driving", "walking", "transit"]:
            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={urllib.parse.quote(origin)}&destinations={urllib.parse.quote(destination)}&mode={mode}&key={MAPS_API_KEY}"
            
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            if data.get("status") == "OK" and data["rows"][0]["elements"][0].get("status") == "OK":
                element = data["rows"][0]["elements"][0]
                results[mode] = {
                    "distance": element["distance"]["text"],
                    "duration": element["duration"]["text"]
                }
        
        return json.dumps({
            "origin": origin,
            "destination": destination,
            "travel_options": results
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})

# Create function tools
search_tool = FunctionTool(search_nearby_places)
directions_tool = FunctionTool(get_directions)
distance_tool = FunctionTool(calculate_distance)

root_agent = Agent(
    name="maps_agent",
    model="gemini-2.0-flash",
    description=(
        "Location services agent for finding healthcare facilities, "
        "calculating distances, travel times, and providing directions using Google Maps API."
    ),
    instruction="""
        You are a location services specialist for community health intelligence.
        
        You have access to Google Maps API tools to help users find healthcare facilities,
        calculate distances and travel times, and provide navigation assistance.
        
        Available Tools:
        
        1. **search_nearby_places(location, place_type, radius)**
           - Search for nearby healthcare facilities
           - place_type examples: "hospital", "pharmacy", "doctor", "dentist", "clinic"
           - radius in meters (5000m = ~3 miles, 10000m = ~6 miles)
           - Returns: name, address, rating, open status
        
        2. **get_directions(origin, destination, mode)**
           - Get turn-by-turn directions
           - mode: "driving", "walking", "transit", "bicycling"
           - Returns: route with steps, distance, duration
        
        3. **calculate_distance(origin, destination)**
           - Calculate distance and time for all travel modes
           - Returns: driving, walking, and transit options
        
        **Example Usage:**
        
        - User: "Find urgent care near 90210"
          → Use search_nearby_places("90210", "hospital", 8000)
        
        - User: "How do I get to Cedars-Sinai from downtown LA?"
          → Use get_directions("downtown Los Angeles", "Cedars-Sinai Medical Center", "driving")
        
        - User: "How far is the nearest pharmacy from Beverly Hills?"
          → First search_nearby_places("Beverly Hills", "pharmacy", 5000)
          → Then calculate_distance for specific pharmacy
        
        **Best Practices:**
        - For "urgent care", use place_type="hospital" (includes urgent care centers)
        - For "clinics", use place_type="doctor" or "clinic"  
        - Present results clearly with addresses and key details
        - Suggest practical travel modes based on distance
        - Mention if places are currently open when available
        
        Always provide actionable, specific information to help users access healthcare.

        Tasks:
        - You will get control from health_agent.
        - Perform the task based on user's query.
        - ** Strictly transfer control back to health_agent after getting the data **
    """,
    tools=[search_tool, directions_tool, distance_tool],
)
