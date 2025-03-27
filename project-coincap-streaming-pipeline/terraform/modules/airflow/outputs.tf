output "composer_airflow_uri" {
  value       = google_composer_environment.airflow_env.config[0].airflow_uri
  description = "The web interface URL for Airflow"
}
