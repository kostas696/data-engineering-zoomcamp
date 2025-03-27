from airflow import models
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.utils.dates import days_ago

PROJECT_ID = "platinum-lead-450019"
REGION = "europe-west3"
CLUSTER_NAME = "crypto-dataproc"
GCS_PY_FILE = "gs://souf-de-zoomcamp-project/spark_jobs/transform_crypto_data.py"

PYSPARK_JOB = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {"main_python_file_uri": GCS_PY_FILE}
}

with models.DAG(
    dag_id="dataproc_transform_dag",
    schedule_interval=None,  # or "0 * * * *" for hourly
    start_date=days_ago(1),
    catchup=False,
    tags=["crypto", "spark", "gcs"],
) as dag:

    submit_pyspark_job = DataprocSubmitJobOperator(
        task_id="run_crypto_transformation",
        job=PYSPARK_JOB,
        region=REGION,
        project_id=PROJECT_ID,
    )
