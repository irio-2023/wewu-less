locals {
  common_environment = {
    MONGODB_URL = "mongodb+srv://wewu-less:Wx8YdE6NvB7NIRvU@wewu-cluster.1cimcqs.mongodb.net/?retryWrites=true&w=majority"
    GOOGLE_CLOUD_PROJECT = local.gcp_project
  }

  gcp_project = "wewu-410223"
}
