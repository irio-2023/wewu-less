locals {
  common_environment = {
    MONGODB_URL = "mongodb+srv://wewu-less:Wx8YdE6NvB7NIRvU@wewu-cluster.1cimcqs.mongodb.net/?retryWrites=true&w=majority"
    GOOGLE_CLOUD_PROJECT = local.gcp_project
  }

  gcp_project = "wewu-410223"
  source_code_path = "${path.module}/cloud_platform/wewu_less.zip"
  source_code_hash = filebase64sha256(local.source_code_path)
}
