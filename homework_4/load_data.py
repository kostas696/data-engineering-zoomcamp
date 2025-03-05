import os
import requests
import pandas as pd
from google.cloud import storage
import multiprocessing
from tqdm import tqdm

services = ['fhv', 'green', 'yellow']
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
BUCKET = os.environ.get("GCP_GCS_BUCKET", "nyc-taxi_dbt")

def upload_to_gcs(bucket, object_name, local_file):
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

def process_file(file_info):
    year, service, month = file_info
    file_name = f"{service}_tripdata_{year}-{month}.csv.gz"
    request_url = f"{init_url}{service}/{file_name}"

    try:
        r = requests.get(request_url)
        r.raise_for_status()
        with open(file_name, 'wb') as f:
            f.write(r.content)

        df = pd.read_csv(file_name, compression='gzip', low_memory=False)

        if service == 'green' or service == 'yellow':
            df['passenger_count'] = pd.to_numeric(df['passenger_count'], errors='coerce').fillna(0).astype('int64')
            df['trip_distance'] = pd.to_numeric(df['trip_distance'], errors='coerce')
            df['RatecodeID'] = pd.to_numeric(df['RatecodeID'], errors='coerce').fillna(0).astype('int64')
            df['PULocationID'] = pd.to_numeric(df['PULocationID'], errors='coerce').fillna(0).astype('int64')
            df['DOLocationID'] = pd.to_numeric(df['DOLocationID'], errors='coerce').fillna(0).astype('int64')
            df['payment_type'] = pd.to_numeric(df['payment_type'], errors='coerce').fillna(0).astype('int64')
            df['store_and_fwd_flag'] = df['store_and_fwd_flag'].fillna('Unknown').astype(str)

            # Timestamp parsing
            if service == 'green':
                df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'], errors='coerce')
                df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'], errors='coerce')
            elif service == 'yellow':
                df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], errors='coerce')
                df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'], errors='coerce')

        elif service == 'fhv':
            df['PUlocationID'] = pd.to_numeric(df['PUlocationID'], errors='coerce').fillna(0).astype('int64')
            df['DOlocationID'] = pd.to_numeric(df['DOlocationID'], errors='coerce').fillna(0).astype('int64')
            df['SR_Flag'] = pd.to_numeric(df['SR_Flag'], errors='coerce') 
            df['Affiliated_base_number'] = df['Affiliated_base_number'].fillna('Unknown').astype(str)
            df['dispatching_base_num'] = df['dispatching_base_num'].fillna('Unknown').astype(str)

            # Convert integer timestamps to datetime objects
            df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], unit='s', errors='coerce')
            df['dropOff_datetime'] = pd.to_datetime(df['dropOff_datetime'], unit='s', errors='coerce')

        parquet_file_name = file_name.replace('.csv.gz', '.parquet')
        df.to_parquet(parquet_file_name, engine='pyarrow')

        upload_to_gcs(BUCKET, f"{service}/{parquet_file_name}", parquet_file_name)

        os.remove(file_name)
        os.remove(parquet_file_name)

        return f"Processed: {service}/{parquet_file_name}"

    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Connection Error: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"General Error: {err}"
    except FileNotFoundError:
        return f"File not found on the remote server: {request_url}"

if __name__ == "__main__":
    file_infos = []
    for service in services:
        if service == 'fhv':
            year_list = ['2019']
        else:
            year_list = ['2019', '2020']
        for year in year_list:
            for i in range(12):
                month = '0' + str(i + 1)
                month = month[-2:]
                file_infos.append((year, service, month))

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = list(tqdm(pool.imap(process_file, file_infos), total=len(file_infos)))

    for result in results:
        print(result)