from datetime import datetime, timedelta
from airflow import models
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator

# Replace with your actual bucket and script
PROJECT_ID = "platinum-lead-450019"
REGION = "europe-west3"
CLUSTER_NAME = "crypto-dataproc-cluster"
GCS_PYSPARK_URI = "gs://souf-de-zoomcamp-project/spark_jobs/transform_crypto_data.py"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

PYSPARK_JOB = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {"main_python_file_uri": GCS_PYSPARK_URI},
}

with models.DAG(
    "dataproc_crypto_transform",
    default_args=default_args,
    schedule_interval="@hourly",  # adjust as needed
    start_date=datetime(2024, 3, 27),
    catchup=False,
    tags=["crypto", "dataproc", "transform"],
) as dag:

    submit_pyspark_job = DataprocSubmitJobOperator(
        task_id="submit_pyspark_transform",
        job=PYSPARK_JOB,
        region=REGION,
        project_id=PROJECT_ID,
    )

    submit_pyspark_job
