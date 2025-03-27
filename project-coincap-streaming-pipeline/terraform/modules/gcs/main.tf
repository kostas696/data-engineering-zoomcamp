resource "google_storage_bucket" "raw_data" {
  name          = var.raw_bucket_name
  location      = var.location
  force_destroy = true
}

resource "google_storage_bucket" "processed_data" {
  name          = var.processed_bucket_name
  location      = var.location
  force_destroy = true
}
