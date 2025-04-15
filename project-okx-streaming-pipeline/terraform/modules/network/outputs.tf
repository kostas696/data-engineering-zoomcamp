output "network_self_link" {
  value = google_compute_network.vpc_network.self_link
}

output "subnet_self_link" {
  value = google_compute_subnetwork.subnet.self_link
}
