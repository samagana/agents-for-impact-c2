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

# Define an appropriate credential type
CREDENTIALS_TYPE = AuthCredentialTypes.API_KEY

# Write modes define BigQuery access control of agent:
# ALLOWED: Tools will have full write capabilites.
# BLOCKED: Default mode. Effectively makes the tool read-only.
# PROTECTED: Only allows writes on temporary data for a given BigQuery session.


tool_config = BigQueryToolConfig(write_mode=WriteMode.ALLOWED)

if CREDENTIALS_TYPE == AuthCredentialTypes.OAUTH2:
    # Initiaze the tools to do interactive OAuth
    credentials_config = BigQueryCredentialsConfig(
        client_id=os.getenv("OAUTH_CLIENT_ID"),
        client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
    )
elif CREDENTIALS_TYPE == AuthCredentialTypes.SERVICE_ACCOUNT:
    # Initialize the tools to use the credentials in the service account key.
    creds, _ = google.auth.load_credentials_from_file("service_account_key.json")
    credentials_config = BigQueryCredentialsConfig(credentials=creds)
else:
    # Initialize the tools to use the application default credentials.
    application_default_credentials, _ = google.auth.default()
    credentials_config = BigQueryCredentialsConfig(
        credentials=application_default_credentials
    )

bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config,
    tool_filter=[
        "list_dataset_ids",
        "get_dataset_info",
        "list_table_ids",
        "get_table_info",
        "execute_sql",
    ],
)

system_prompt = """
You are a highly skilled data agent with extensive experience in querying various datasets to extract relevant information for projects. Your expertise lies in identifying the most suitable data sources, understanding project requirements, and ensuring accurate and efficient data retrieval.

Your task is to generate a system prompt that will facilitate querying the right data for a specific project. Here is some information of type of data you have and the dataset available.

Project ID: qwiklabs-gcp-04-91797af16116
Available Datasets: {
global_aq : Global air quality data
dental_data : Information about dental clinics
cal_hosp_ratings : hospital ratings in California
}
"""
root_agent = Agent(
    name="data_agent",
    model="gemini-2.5-pro",
    description=(
        "Queries BigQuery datasets such as air quality, clinics or vaccination stats."
    ),
    instruction="""
        You are a helpful agent who can work with BigQuery datasets.

        Always run the bigquery tools in project-id: qwiklabs-gcp-04-91797af16116 unless
        explicitly told otherwise.
    """,
    tools=[bigquery_toolset],
)
