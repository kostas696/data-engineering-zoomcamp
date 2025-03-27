output "bucket_name" {
  description = "The name of the created GCS bucket"
  value       = google_storage_bucket.crypto_data_bucket.name
}

output "bucket_url" {
  description = "The URL of the created GCS bucket"
  value       = google_storage_bucket.crypto_data_bucket.url
}