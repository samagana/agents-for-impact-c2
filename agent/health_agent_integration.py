"""
Integration module for connecting Streamlit UI with ADK Health Agents
"""
import os
import json
import requests
from typing import Dict, List, Any
import logging
from health_agent.main import root_agent as health_agent
from data_agent.main import root_agent as data_agent
from insights_agent.main import root_agent as insights_agent

logger = logging.getLogger(__name__)

class HealthAgentIntegration:
    """Integration class for ADK Health Agents with Streamlit UI"""
    
    def __init__(self):
        self.health_agent = health_agent
        self.data_agent = data_agent
        self.insights_agent = insights_agent
        self.api_base_url = os.getenv("ADK_API_URL", "http://localhost:8080")
    
    async def chat_with_health_agent(self, user_input: str, user_role: str, location: str) -> str:
        """
        Chat with the health agent and get contextualized response

        Args:
            user_input: User's question or input
            user_role: Role of the user (Public Health Staff, Community Organizations, Residents)
            location: Geographic location context

        Returns:
            Agent response as string
        """
        try:
            # Enhance the prompt with context
            contextualized_prompt = f"""User Role: {user_role}
Location: {location}

{user_input}

Please provide a helpful, specific response tailored to this user's role and location. Include actionable insights and recommendations."""

            # Use synchronous run method which is simpler
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.health_agent.run, contextualized_prompt)

            # Extract content from response
            if hasattr(response, 'content'):
                return str(response.content)
            elif hasattr(response, 'text'):
                return str(response.text)
            else:
                return str(response)

        except Exception as e:
            logger.error(f"Error in health agent chat: {e}", exc_info=True)
            # Return a more informative fallback
            return f"I'm experiencing connectivity issues with the health intelligence system. However, I can tell you that for {user_role} in {location}, I can help answer questions about health data and provide recommendations. Please try asking your question in a different way or check back later."
    
    async def get_health_insights(self, location: str, user_role: str) -> List[str]:
        """
        Get health insights for a specific location and user role

        Args:
            location: Geographic location
            user_role: User role for contextualized insights

        Returns:
            List of insight strings
        """
        try:
            prompt = f"""Generate 4 specific, actionable health insights for {location} tailored for {user_role}.

Focus on:
1. Key health indicators and current trends
2. Resource gaps and opportunities
3. Actionable recommendations
4. Risk factors and mitigation strategies

Format each insight as a brief, clear statement starting with an action word or key finding. Each insight should be on a new line."""

            # Use synchronous run method
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.insights_agent.run, prompt)

            # Extract content
            if hasattr(response, 'content'):
                insights_text = str(response.content)
            elif hasattr(response, 'text'):
                insights_text = str(response.text)
            else:
                insights_text = str(response)

            # Parse insights into list - look for numbered items or bullet points
            insights = []
            for line in insights_text.split('\n'):
                line = line.strip()
                # Remove bullet points, numbers, and common prefixes
                line = line.lstrip('•-*').strip()
                line = ''.join(line.split('.', 1)[1:]).strip() if line and line[0].isdigit() else line

                if line and len(line) > 20:  # Only keep substantial insights
                    insights.append(line)

            return insights[:4] if insights else self._get_fallback_insights(user_role)

        except Exception as e:
            logger.error(f"Error getting health insights: {e}", exc_info=True)
            return self._get_fallback_insights(user_role)
    
    async def get_data_analysis(self, query: str, location: str) -> Dict[str, Any]:
        """
        Get data analysis from the data agent
        
        Args:
            query: Data analysis query
            location: Location context
            
        Returns:
            Dictionary with analysis results
        """
        try:
            prompt = f"""
            Analyze health data for {location} based on this query: {query}
            
            Provide:
            1. Key findings
            2. Data trends
            3. Statistical insights
            4. Recommendations
            """
            
            # Get response from data agent
            analysis_text = ""
            async for chunk in self.data_agent.run_async(prompt):
                if hasattr(chunk, 'content'):
                    analysis_text += chunk.content
                elif hasattr(chunk, 'text'):
                    analysis_text += chunk.text
                elif isinstance(chunk, str):
                    analysis_text += chunk
                else:
                    analysis_text += str(chunk)
            
            return {
                "analysis": analysis_text,
                "location": location,
                "query": query,
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"Error in data analysis: {e}")
            return {
                "analysis": "Unable to retrieve data analysis at this time.",
                "location": location,
                "query": query,
                "error": str(e)
            }
    
    async def get_resource_recommendations(self, location: str, user_role: str) -> Dict[str, Any]:
        """
        Get resource allocation recommendations
        
        Args:
            location: Geographic location
            user_role: User role for contextualized recommendations
            
        Returns:
            Dictionary with resource recommendations
        """
        try:
            prompt = f"""
            Provide resource allocation recommendations for {location} for {user_role}.
            
            Include:
            1. Priority resource needs
            2. Capacity gaps
            3. Budget recommendations
            4. Implementation timeline
            5. Expected outcomes
            """
            
            # Get response from insights agent
            recommendations_text = ""
            async for chunk in self.insights_agent.run_async(prompt):
                if hasattr(chunk, 'content'):
                    recommendations_text += chunk.content
                elif hasattr(chunk, 'text'):
                    recommendations_text += chunk.text
                elif isinstance(chunk, str):
                    recommendations_text += chunk
                else:
                    recommendations_text += str(chunk)
            
            return {
                "recommendations": recommendations_text,
                "location": location,
                "user_role": user_role,
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"Error getting resource recommendations: {e}")
            return {
                "recommendations": "Unable to generate recommendations at this time.",
                "location": location,
                "user_role": user_role,
                "error": str(e)
            }
    
    def _get_fallback_response(self, user_input: str, user_role: str) -> str:
        """Fallback response when agent is unavailable"""
        fallback_responses = {
            'Public Health Staff': [
                "I can help you analyze health data and identify intervention opportunities in your area.",
                "Based on current health indicators, I recommend focusing on preventive care programs.",
                "Consider implementing community health worker programs to improve outreach."
            ],
            'Community Organizations': [
                "I can help you identify community health needs and available resources.",
                "Consider partnering with local health departments for screening programs.",
                "Community engagement programs can help address social determinants of health."
            ],
            'Residents': [
                "I can help you find local health resources and preventive care options.",
                "Regular health screenings are important for early detection of health issues.",
                "Community health programs can help you manage chronic conditions."
            ]
        }
        
        import random
        return random.choice(fallback_responses.get(user_role, fallback_responses['Public Health Staff']))
    
    def _get_fallback_insights(self, user_role: str) -> List[str]:
        """Fallback insights when agent is unavailable"""
        fallback_insights = {
            'Public Health Staff': [
                "Monitor chronic disease prevalence trends in your jurisdiction",
                "Assess resource capacity gaps in mental health services",
                "Evaluate community health worker program effectiveness",
                "Review preventive care program coverage and outcomes"
            ],
            'Community Organizations': [
                "Identify underserved populations in your service area",
                "Assess transportation barriers to healthcare access",
                "Evaluate food security and nutrition program needs",
                "Review social isolation and community engagement opportunities"
            ],
            'Residents': [
                "Schedule regular health screenings and checkups",
                "Access community health programs for chronic disease management",
                "Utilize preventive care services available in your area",
                "Connect with local health resources and support groups"
            ]
        }
        
        return fallback_insights.get(user_role, fallback_insights['Public Health Staff'])
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

# Global instance for use in Streamlit app
health_integration = HealthAgentIntegration()
