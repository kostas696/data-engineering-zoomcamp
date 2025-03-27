variable "project_id" {
  description = "The ID of your GCP project"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "europe-west1"
}

variable "gcs_bucket_name" {
  description = "The name of the bucket used for raw crypto data"
  type        = string
}

variable "airflow_env_name" {
  type    = string
  default = "coincap-airflow"
}

variable "airflow_machine_type" {
  type    = string
  default = "n1-standard-2"
}

variable "airflow_image_version" {
  type    = string
  default = "composer-2.5.0-airflow-2.6.3"
}

variable "airflow_python_version" {
  type    = string
  default = "3"
}

variable "airflow_service_account" {
  type        = string
  description = "Service account email for Composer to use"
}

variable "airflow_env_variables" {
  type        = map(string)
  default     = {}
  description = "Airflow environment variables"
}
