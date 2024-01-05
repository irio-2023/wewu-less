terraform {
  required_providers {
    google = {
      source  = "hashicorp/google",
      version = "5.1.0"
    }
  }
}

provider "google" {
  project = "wewu_less"
  region = local.region
  credentials = file("/Users/pfuchs/.config/gcloud/application_default_credentials.json")
}

resource "random_id" "wewu_less_bucket_id" {
  byte_length = 16
}

resource "google_storage_bucket" "wewu_less" {
  project = "wewu-410223"
  name = "${random_id.wewu_less_bucket_id.hex}-gcf-source"
  location = "US"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "wewu_less_sources" {
  source = "${path.module}/cloud_platform/wewu_less.zip"
  name = "wewu_less_sources.zip"
  bucket = google_storage_bucket.wewu_less.name
}

output "bucket" {
  value = google_storage_bucket.wewu_less
}