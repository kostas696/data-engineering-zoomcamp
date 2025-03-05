import os
import requests
import pandas as pd
from google.cloud import storage

# Base URL for downloading datasets
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/"

# Google Cloud Storage Bucket
BUCKET = os.environ.get("GCP_GCS_BUCKET", "+")

def upload_to_gcs(bucket, object_name, local_file):
    """Uploads a file to Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)

    # Reduce chunk size to 5MB (default is 256MB)
    blob.chunk_size = 5 * 1024 * 1024  # 5MB

    # Upload file
    blob.upload_from_filename(local_file)
    print(f"Uploaded {local_file} to gs://{bucket.name}/{object_name}")


def download_and_upload(year, service):
    """Downloads taxi data, converts it to Parquet, and uploads it to GCS."""
    for month in range(1, 13):
        month_str = f"{month:02d}"  # Format month as two digits (01, 02, ..., 12)
        file_name = f"{service}_tripdata_{year}-{month_str}.csv.gz"
        request_url = f"{BASE_URL}{service}/{file_name}"

        print(f"Downloading: {request_url}")
        response = requests.get(request_url)
        if response.status_code == 200:
            with open(file_name, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")

            # Define column types and datetime columns for each service
            dtype_mapping = {}
            datetime_columns = []

            if service == "green":
                dtype_mapping = {
                    "VendorID": "Int64",
                    "RatecodeID": "Int64",
                    "PULocationID": "Int64",
                    "DOLocationID": "Int64",
                    "passenger_count": "Int64",
                    "trip_distance": "float64",
                    "fare_amount": "float64",
                    "extra": "float64",
                    "mta_tax": "float64",
                    "tip_amount": "float64",
                    "tolls_amount": "float64",
                    "ehail_fee": "float64",
                    "improvement_surcharge": "float64",
                    "total_amount": "float64",
                    "payment_type": "Int64",
                    "trip_type": "Int64",
                    "congestion_surcharge": "float64",
                }
                datetime_columns = ["lpep_pickup_datetime", "lpep_dropoff_datetime"]

            elif service == "yellow":
                dtype_mapping = {
                    "VendorID": "Int64",
                    "RatecodeID": "Int64",
                    "passenger_count": "Int64",
                    "trip_distance": "float64",
                    "PULocationID": "Int64",
                    "DOLocationID": "Int64",
                    "payment_type": "Int64",
                    "fare_amount": "float64",
                    "extra": "float64",
                    "mta_tax": "float64",
                    "tip_amount": "float64",
                    "tolls_amount": "float64",
                    "improvement_surcharge": "float64",
                    "total_amount": "float64",
                    "congestion_surcharge": "float64",
                }
                datetime_columns = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]

            elif service == "fhv":
                dtype_mapping = {
                    "PUlocationID": "Int64",
                    "DOlocationID": "Int64",
                    "SR_Flag": "float64",
                }
                datetime_columns = ["pickup_datetime", "dropOff_datetime"]

            # Load CSV with parse_dates for datetime columns
            df = pd.read_csv(
                file_name, compression="gzip", low_memory=False, parse_dates=datetime_columns
            )

            # Convert columns to specified types
            for col, dtype in dtype_mapping.items():
                if col in df.columns:
                    df[col] = df[col].astype(dtype)

            # Save as Parquet
            parquet_file = file_name.replace(".csv.gz", ".parquet")
            df.to_parquet(parquet_file, engine="pyarrow")
            print(f"Converted to Parquet: {parquet_file}")

            # Upload to GCS
            upload_to_gcs(BUCKET, f"{service}/{parquet_file}", parquet_file)

            # Remove local files to save space
            os.remove(file_name)
            os.remove(parquet_file)
        else:
            print(f"Failed to download: {request_url}")


# Run the script for all required datasets
services = ["green", "yellow", "fhv"]
years = ["2019", "2020"]

for service in services:
    for year in years:
        if service == "fhv" and year == "2020":
            continue  # Skip FHV 2020 since it's not required
        download_and_upload(year, service)