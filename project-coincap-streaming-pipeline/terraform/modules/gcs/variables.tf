variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
}

variable "location" {
  description = "The location for the GCS bucket"
  type        = string
  default     = "EU"
}

variable "bucket_name" {
  description = "The name of the GCS bucket"
  type        = string
}