project_id        = "platinum-lead-450019-j6"
region            = "europe-west3"
gcs_bucket_name   = "souf-de-zoomcamp-project"
composer_env_name = "crypto-composer"
dataproc_cluster  = "crypto-dataproc"
airflow_service_account = "composer-env-sa@platinum-lead-450019-j6.iam.gserviceaccount.com"
airflow_env_variables = {
  GOOGLE_BUCKET_NAME = "souf-de-zoomcamp-project"
}
