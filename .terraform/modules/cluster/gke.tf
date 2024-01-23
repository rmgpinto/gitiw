resource "google_container_cluster" "cluster" {
  name                     = var.name
  location                 = var.region
  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_service_account" "default" {
  account_id   = "gke-sa"
  display_name = "Service Account"
}

resource "google_container_node_pool" "preemptible_nodes" {
  name     = "${var.name}-node-pool"
  cluster  = google_container_cluster.cluster.name
  location = var.region
  node_config {
    machine_type = var.node_type
    spot         = true
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = google_service_account.default.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
  autoscaling {
    min_node_count = var.min_node_count
    max_node_count = var.max_node_count
  }
}
