resource "google_pubsub_topic" "pubsub" {
  for_each = local.terraform_queues
  name = each.value.name
  message_retention_duration = each.value.message_retention
  project = local.gcp_project
}
