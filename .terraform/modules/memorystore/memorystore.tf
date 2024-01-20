resource "google_redis_instance" "redis_instance" {
  name           = var.name
  location_id    = "${var.region}-a"
  tier           = "BASIC"
  memory_size_gb = var.memory_size_gb
  redis_version  = var.redis_version
}
