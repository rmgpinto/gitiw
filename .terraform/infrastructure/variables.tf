variable "project_id" {
  description = "Project id"
}

variable "project_name" {
  description = "Project name"
}

variable "environment" {
  description = "Environment"
}

variable "google_region" {
  description = "Google region"
}

variable "redis" {
  description = "Redis variables"
  type = object({
    version        = string
    memory_size_gb = number
  })
}
