import requests
import pandas as pd
from google.cloud import bigquery

# --- 1. Configuration ---
# Replace with your project, dataset, and table details
project_id = "qwiklabs-gcp-04-91797af16116"
dataset_id = "chronic_disease_indicators"
table_id = "chronic_disease_indicators_table"

# URL of the raw CSV data
csv_url = "/Users/Samarth.Maganahalli/Downloads/U.S._Chronic_Disease_Indicators.csv"

# Construct the full BigQuery table reference
table_ref = f"{project_id}.{dataset_id}.{table_id}"


# --- 2. Fetch CSV Data into Pandas ---
print(f"Fetching data from {csv_url}...")
try:
    # Use pandas to read the CSV data directly from the URL
    df = pd.read_csv(csv_url)
    print(f"Successfully fetched and parsed {len(df)} rows.")

    # --- 3. Load DataFrame into BigQuery ---
    # Initialize the BigQuery client
    client = bigquery.Client(project=project_id)

    # Configure the load job
    job_config = bigquery.LoadJobConfig(
        # Overwrite the table if it already exists
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        # Let BigQuery infer the schema from the DataFrame
        autodetect=True,
    )

    # Start the load job from the DataFrame
    print(f"Loading data into BigQuery table: {table_ref}...")
    load_job = client.load_table_from_dataframe(
        dataframe=df,
        destination=table_ref,
        job_config=job_config
    )

    # Wait for the job to complete
    load_job.result()

    # Check the result
    destination_table = client.get_table(table_ref)
    print(f"✅ Load job finished. Loaded {destination_table.num_rows} rows into {table_ref}.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from URL: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
