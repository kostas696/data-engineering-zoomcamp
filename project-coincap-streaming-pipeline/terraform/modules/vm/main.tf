resource "google_compute_instance" "airflow_vm" {
  name         = var.vm_name
  machine_type = "e2-medium"
  zone         = var.zone

  tags = ["airflow"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network    = var.network_self_link
    subnetwork = var.subnet_self_link
    access_config {}
  }

  metadata_startup_script = file("${path.module}/startup.sh")

  service_account {
    email  = var.service_account_email
    scopes = ["cloud-platform"]
  }
}

resource "google_compute_firewall" "airflow_firewall" {
  name    = "allow-airflow-ssh"
  network = var.network_self_link

  allow {
    protocol = "tcp"
    ports    = ["22", "8080"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["airflow"]
}
