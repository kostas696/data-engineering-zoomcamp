output "bucket_name" {
  value = google_storage_bucket.crypto_data_bucket.name
}

output "bucket_url" {
  value = google_storage_bucket.crypto_data_bucket.url
}