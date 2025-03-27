terraform {
  required_version = ">= 1.3.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.80.0"
    }
  }

  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file("${path.module}/../gcloud/kafka-consumer-key.json")
}
