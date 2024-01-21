locals {
  public_cloud_functions = {
    for k, v in local.http_functions : k => v
    if try(v.is_public, false)
  }
}

resource "google_cloudfunctions2_function_iam_member" "public_cf_member" {
  for_each = local.public_cloud_functions
  project = local.gcp_project
  region = local.region
  cloud_function = google_cloudfunctions2_function.http_cf_template[each.key].name
  role = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
