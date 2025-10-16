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
    
    # Refresh credentials if expired
    if hasattr(application_default_credentials, 'expired') and application_default_credentials.expired:
        import google.auth.transport.requests
        request = google.auth.transport.requests.Request()
        application_default_credentials.refresh(request)
    
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

        You MUST use the query_bigquery tool to execute SQL queries.

        Available Datasets:
        
        🏥 HEALTHCARE FACILITIES (PROJECT DATASETS - USE THESE FIRST!):
        - qwiklabs-gcp-04-91797af16116.dental.dental_data
          * Dental clinics with addresses, phone, services
          * Filters: accepts_uninsured, free_services, sliding_scale
          * Has lat/long for proximity calculations
          * Includes uninsured_rate and population by county
        
        - qwiklabs-gcp-04-91797af16116.cal_hosp_ratings.cal-hosp-ratings-2011-2018_copy
          * California hospital ratings and performance
          * Has Hospital, County, Performance_Rating, Latitude, Longitude
          * Use for finding healthcare facilities
        
        📊 HEALTH DATA (PROJECT DATASETS):
        - qwiklabs-gcp-04-91797af16116.chronic_disease_indicators.chronic_disease_indicators_table
          * Disease prevalence by location (state/county)
          * Topics: diabetes, cardiovascular, asthma, etc.
          * Use for health outcome analysis
        
        - qwiklabs-gcp-04-91797af16116.global_aq.global_aq_data
          * Real-time air quality with lat/long
          * Pollutants by city/location with timestamps
        
        💰 DEMOGRAPHICS & SOCIOECONOMIC (PUBLIC):
        - bigquery-public-data.census_bureau_acs.zip_codes_2018_5yr (income, poverty, employment)
        - bigquery-public-data.census_bureau_acs.county_2018_5yr (county demographics)
        - bigquery-public-data.broadstreet_adi.area_deprivation_index_by_zipcode (disadvantage index)
        - bigquery-public-data.census_bureau_usa.population_by_zip_2010
        
        🌫️ ENVIRONMENTAL (PUBLIC):
        - bigquery-public-data.epa_historical_air_quality.air_quality_annual_summary
        - bigquery-public-data.epa_historical_air_quality.pm25_frm_daily_summary
        - bigquery-public-data.epa_historical_air_quality.o3_daily_summary
        
        📈 HEALTH OUTCOMES (PUBLIC):
        - bigquery-public-data.america_health_rankings.ahr (state health rankings)
        - bigquery-public-data.covid19_open_data.covid19_open_data

        ALWAYS call query_bigquery() with your SQL. Do NOT just return SQL text.
    """,
    tools=[bigquery_toolset],
)
