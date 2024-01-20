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

    available_memory = each.value.memory
    timeout_seconds = each.value.timeout_seconds
  }

  location = local.region
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}
