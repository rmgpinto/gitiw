module "redis" {
  source         = "../modules/memorystore"
  name           = "${var.project_name}-${var.environment}"
  region         = var.google_region
  redis_version  = var.redis.version
  memory_size_gb = var.redis.memory_size_gb
}

module "cluster" {
  source         = "../modules/cluster"
  name           = "${var.project_name}-${var.environment}"
  region         = var.google_region
  min_node_count = var.kubernetes_cluster.min_node_count
  max_node_count = var.kubernetes_cluster.max_node_count
  node_type      = var.kubernetes_cluster.node_type
}
