locals {
  public_cloud_functions = {
    for k, v in local.http_functions : k => v
    if try(v.is_public, false)
  }
}

resource "google_cloud_run_service_iam_member" "public_cf_member" {
  for_each = local.public_cloud_functions
  location = google_cloudfunctions2_function.http_cf_template[each.key].location
  member   = "allUsers"
  role     = "roles/run.invoker"
  service  = google_cloudfunctions2_function.http_cf_template[each.key].name
}
