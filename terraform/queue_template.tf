resource "google_pubsub_topic" "pubsub" {
  for_each = local.queues
  name = each.topic
  message_retention_duration = each.message_retention_duration
}
