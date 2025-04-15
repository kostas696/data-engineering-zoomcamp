provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

module "network" {
  source          = "./modules/network"
  network_name    = var.network_name
  subnet_name     = var.subnet_name
  subnet_ip_range = var.subnet_ip_range
  region          = var.region
}

module "gcs" {
  source      = "./modules/gcs"
  bucket_name = var.bucket_name
  location    = var.location
  project_id  = var.project_id
}

module "vm" {
  source                = "./modules/vm"
  vm_name               = var.vm_name
  zone                  = var.zone
  network_self_link     = module.network.network_self_link
  subnet_self_link      = module.network.subnet_self_link
  service_account_email = var.service_account_email
}