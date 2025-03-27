resource "google_dataproc_cluster" "dataproc_cluster" {
  name    = "crypto-dataproc-cluster"
  region  = var.region
  project = var.project_id

  cluster_config {
    master_config {
      num_instances = 1
      machine_type  = "n1-standard-2"
    }

    worker_config {
      num_instances = 2
      machine_type  = "n1-standard-2"
    }

    software_config {
      image_version       = "2.1-debian11" # or latest stable
      optional_components = ["JUPYTER", "ANACONDA"]
    }

    gce_cluster_config {
      metadata = {
        enable-oslogin = "TRUE"
      }
    }
  }
}
