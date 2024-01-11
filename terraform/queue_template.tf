resource "google_pubsub_topic" "pubsub" {
  for_each = local.queues
  name = each.value.topic
  message_retention_duration = each.value.message_retention
}
