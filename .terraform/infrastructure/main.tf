module "redis" {
  source         = "../modules/memorystore"
  name           = "${var.project_name}-${var.environment}"
  region         = var.google_region
  version        = var.redis.version
  memory_size_gb = var.redis.memory_size_gb
}
