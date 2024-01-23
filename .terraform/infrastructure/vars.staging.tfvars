environment = "staging"
kubernetes_cluster = {
  min_node_count = 0
  max_node_count = 2
  node_type      = "e2-medium"
}
redis = {
  version        = "REDIS_7_0"
  memory_size_gb = 1
}
