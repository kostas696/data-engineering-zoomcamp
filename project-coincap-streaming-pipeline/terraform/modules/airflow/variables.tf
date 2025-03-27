variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  description = "GCP region"
}

variable "airflow_env_name" {
  type        = string
  default     = "coincap-airflow"
}

variable "machine_type" {
  type        = string
  default     = "n1-standard-2"
}

variable "image_version" {
  type        = string
  default     = "composer-2.5.0-airflow-2.6.3"
}

variable "python_version" {
  type        = string
  default     = "3"
}

variable "service_account_email" {
  type        = string
  description = "Service account for Composer to run Airflow"
}

variable "env_variables" {
  type        = map(string)
  default     = {}
  description = "Optional environment variables for Airflow"
}
