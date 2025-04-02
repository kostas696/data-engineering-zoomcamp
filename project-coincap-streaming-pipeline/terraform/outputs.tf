output "vm_ip_address" {
  value = module.vm.external_ip
}

output "bucket_name" {
  value = module.gcs.bucket_name
}
