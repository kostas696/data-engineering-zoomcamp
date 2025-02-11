import dlt
import os
import urllib.request
from google.cloud import storage, bigquery
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up GCS details
BUCKET_NAME = "data-engineering-kostas696"
PROJECT_ID = "platinum-lead-450019-j6"
DATASET_NAME = "nyc_taxi_data"
TABLE_NAME = "yellow_taxi_trips"
REGION = "europe-west3"  # Desired region for GCS and BigQuery

# Base URL for NYC Taxi data
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-"
MONTHS = [f"{i:02d}" for i in range(1, 7)]
DOWNLOAD_DIR = "data"

# Create local directory if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Initialize Google Cloud Storage client
client = storage.Client(PROJECT_ID)
bucket = client.bucket(BUCKET_NAME)

# Initialize BigQuery client and create dataset if it doesn't exist
def create_bigquery_dataset():
    bigquery_client = bigquery.Client(project=PROJECT_ID)
    dataset_id = f"{PROJECT_ID}.{DATASET_NAME}"
    
    try:
        # Check if the dataset already exists
        bigquery_client.get_dataset(dataset_id)
        print(f"Dataset {DATASET_NAME} already exists.")
    except Exception:
        # Create the dataset if it doesn't exist
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = REGION  # Set the region
        dataset = bigquery_client.create_dataset(dataset, timeout=30)
        print(f"Created dataset {DATASET_NAME} in region {REGION}.")

# Function to download files
def download_file(month):
    url = f"{BASE_URL}{month}.parquet"
    file_path = os.path.join(DOWNLOAD_DIR, f"yellow_tripdata_2024-{month}.parquet")
    
    try:
        print(f"Downloading: {url}")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

# Function to upload files to GCS
def upload_to_gcs(file_path):
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)

    # Set the location of the blob to match the bucket's region
    blob.location = REGION  # Explicitly set the region

    # Reduce chunk size to avoid timeout issues
    blob.chunk_size = 10 * 1024 * 1024  # 10MB chunks

    try:
        print(f"Uploading {file_path} to GCS...")
        blob.upload_from_filename(file_path, timeout=600)  # 10-minute timeout
        print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")
        return f"gs://{BUCKET_NAME}/{blob_name}"
    except Exception as e:
        print(f"Failed to upload {file_path}: {e}")
        return None

# Function to load data into BigQuery using DLT
def load_data_to_bigquery():
    pipeline = dlt.pipeline(
        pipeline_name="nyc_taxi_pipeline",
        destination="bigquery",
        dataset_name=DATASET_NAME
    )

    # Load data from GCS
    gcs_files = [f"gs://{BUCKET_NAME}/yellow_tripdata_2024-{month}.parquet" for month in MONTHS]

    print("Loading data into BigQuery...")
    pipeline.run(
        gcs_files, 
        table_name=TABLE_NAME, 
        write_disposition="append"
    )
    print("Data successfully loaded into BigQuery!")

if __name__ == "__main__":
    print("Starting the DLT-based ingestion process...")

    # Step 1: Create BigQuery dataset if it doesn't exist
    create_bigquery_dataset()

    # Step 2: Download Parquet files in parallel
    with ThreadPoolExecutor() as executor:
        download_futures = {executor.submit(download_file, month): month for month in MONTHS}
        file_paths = [future.result() for future in as_completed(download_futures) if future.result()]

    # Step 3: Upload to GCS in parallel
    with ThreadPoolExecutor() as executor:
        upload_futures = {executor.submit(upload_to_gcs, fp): fp for fp in file_paths}
        gcs_paths = [future.result() for future in as_completed(upload_futures) if future.result()]

    # Step 4: Load into BigQuery
    if gcs_paths:
        load_data_to_bigquery()

    print("DLT Pipeline Completed Successfully!")
