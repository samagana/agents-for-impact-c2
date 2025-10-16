import json
import requests
import io
from google.cloud import bigquery

# --- 1. Configuration ---
# Replace with your project, dataset, and table details
project_id = "qwiklabs-gcp-04-91797af16116"
dataset_id = "cancer"
table_id = "chronic_disease_indicators"

# URL of the raw JSON data from data.gov
json_url = "https://data.cdc.gov/api/views/hksd-2xuw/rows.json?accessType=DOWNLOAD"

# Construct the full BigQuery table reference
table_ref = f"{project_id}.{dataset_id}.{table_id}"


print(f"Fetching data from {json_url}...")
try:
    response = requests.get(json_url, timeout=60)
    response.raise_for_status()  # Raise an error for bad responses

    # Load the JSON data
    data = response.json()
    
    # Extract the list of records
    records = data.get('fuel_stations', [])
    
    if not records:
        print("No records found in the 'fuel_stations' key. Exiting.")
    else:
        # Convert list of dictionaries to a newline-delimited JSON (NDJSON) string
        ndjson_data = "\n".join([json.dumps(record) for record in records])
        print(f"Successfully fetched and prepared {len(records)} records.")

        # --- 3. Load Data into BigQuery ---
        # Initialize the BigQuery client
        client = bigquery.Client(project=project_id)

        # Configure the load job
        job_config = bigquery.LoadJobConfig(
            autodetect=True,  # Infer schema automatically
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE, # Overwrite table
        )

        # Convert the NDJSON string to bytes
        data_as_bytes = ndjson_data.encode("utf-8")

        # Start the load job from memory
        print(f"Loading data into table: {table_ref}")
        load_job = client.load_table_from_file(
            file_obj=io.BytesIO(data_as_bytes),
            destination=table_ref,
            job_config=job_config,
        )

        # Wait for the job to complete
        load_job.result()

        print(f"✅ Load job finished. Loaded {load_job.output_rows} rows into {table_ref}.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
