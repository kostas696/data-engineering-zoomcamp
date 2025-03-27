output "gcs_bucket_name" {
  description = "Name of the raw data GCS bucket"
  value       = module.gcs.bucket_name
}

output "gcs_bucket_url" {
  description = "URL of the raw data GCS bucket"
  value       = module.gcs.bucket_url
}

output "airflow_uri" {
  value       = module.airflow.composer_airflow_uri
  description = "The Airflow Web UI URI"
}
