resource "google_cloudfunctions2_function" "cf_template" {
  for_each = local.functions
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
        SOURCES_MD5 = google_storage_bucket_object.wewu_less_sources.md5hash
      },
      local.common_environment
    )

    available_memory = each.value.memory
    timeout_seconds = 60
  }

  location = local.region
}
