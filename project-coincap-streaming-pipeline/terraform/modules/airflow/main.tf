resource "google_composer_environment" "airflow_env" {
  name   = var.airflow_env_name
  region = var.region
  project = var.project_id

  config {
    node_config {
      location         = var.region
      machine_type     = var.machine_type
      service_account  = var.service_account_email
    }

    software_config {
      image_version = var.image_version
      python_version = var.python_version
      env_variables = var.env_variables
    }

    workloads_config {
      scheduler {
        cpu        = 1
        memory_gb  = 2
        storage_gb = 1
      }
      web_server {
        cpu        = 1
        memory_gb  = 2
        storage_gb = 1
      }
      worker {
        cpu        = 1
        memory_gb  = 2
        storage_gb = 1
      }
    }
  }
}
