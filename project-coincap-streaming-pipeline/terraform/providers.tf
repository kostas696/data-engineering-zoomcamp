terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.27"
    }
  }

  required_version = ">= 1.4.0"
}
