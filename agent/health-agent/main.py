import logging
import os

import dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StdioServerParameters

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

TARGET_FOLDER_PATH = "/tmp"


tools = [
    McpToolset(
        connection_params=StdioConnectionParams(
            server_params = StdioServerParameters(
                command='npx',
                args=[
                    "-y",  # Argument for npx to auto-confirm install
                    "@modelcontextprotocol/server-filesystem",
                    # IMPORTANT: This MUST be an ABSOLUTE path to a folder the
                    # npx process can access.
                    # Replace with a valid absolute path on your system.
                    # For example: "/Users/youruser/accessible_mcp_files"
                    # or use a dynamically constructed absolute path:
                    os.path.abspath(TARGET_FOLDER_PATH),
                ],
            ),
        ),
        # Optional: Filter which tools from the MCP server are exposed
        # tool_filter=['list_directory', 'read_file']
    )
]


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
