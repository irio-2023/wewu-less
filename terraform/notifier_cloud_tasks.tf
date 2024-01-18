resource "random_string" "random" {
  length           = 16
  special          = false
}

resource "google_cloud_tasks_queue" "notifier_cloud_tasks_queue" {
  name = random_string.random.result
  location = local.region
  project = local.gcp_project

  retry_config {
    max_attempts = 5
    max_retry_duration = "4s"
    max_backoff = "3s"
    min_backoff = "2s"
    max_doublings = 1
  }
}
