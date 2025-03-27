module "gcs" {
  source      = "./modules/gcs"
  project_id  = var.project_id
  location    = var.region
  bucket_name = var.gcs_bucket_name
}

module "dataproc" {
  source     = "./modules/dataproc"
  project_id = var.project_id
  region     = var.region
}

module "airflow" {
  source                = "./modules/airflow"
  project_id            = var.project_id
  region                = var.region
  airflow_env_name      = var.airflow_env_name
  machine_type          = var.airflow_machine_type
  image_version         = var.airflow_image_version
  python_version        = var.airflow_python_version
  service_account_email = var.airflow_service_account
  env_variables         = var.airflow_env_variables
}
