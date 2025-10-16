import logging
import os

import dotenv
from google.adk.agents import Agent
from google.adk.auth.auth_credential import AuthCredentialTypes
from google.adk.tools.bigquery import BigQueryCredentialsConfig
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
from google.adk.tools.bigquery import BigQueryToolset
import google.auth

dotenv.load_dotenv()

logger = logging.getLogger(__name__)


root_agent = Agent(
    name="insights_agent",
    model="gemini-2.5-pro",
    description=(
        "Generates summaries or comparisons."
    ),
    instruction=("You are responsible for generating the summary to the user."),
)
