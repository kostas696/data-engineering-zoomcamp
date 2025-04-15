resource "google_project_service" "compute" {
  service = "compute.googleapis.com"
  project = var.project_id
}

resource "google_project_service" "storage" {
  service = "storage.googleapis.com"
  project = var.project_id
}
