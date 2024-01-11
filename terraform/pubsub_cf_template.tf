resource "google_cloudfunctions2_function" "http_cf_template" {
  for_each = local.http_functions
  name = each.key
  project = local.gcp_project

  build_config {
    runtime = "python312"
    entry_point = each.value.handler
    environment_variables = {
      GOOGLE_FUNCTION_SOURCE = each.value.source
    }

    source {
      storage_source {
        bucket = google_storage_bucket.wewu_less.name
        object = google_storage_bucket_object.wewu_less_sources.name
      }
    }

  }

  service_config {
    environment_variables = merge(
      each.value.environment,
      {
        LAMBDA_IDENTIFIER = each.key
      },
      local.common_environment
    )

    ingress_settings = "ALLOW_INTERNAL_ONLY"
    all_traffic_on_latest_revision = true
    available_memory = each.value.memory
    timeout_seconds = each.value.timeout_seconds
  }

  event_trigger {
    trigger_region = local.region
    event_type = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic = each.trigger_topic
    retry_policy = each.auto_retry ? "RETRY_POLICY_RETRY" : "RETRY_POLICY_DO_NOT_RETRY"
  }

  location = local.region
}
