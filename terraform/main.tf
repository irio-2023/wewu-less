terraform {
  required_providers {
    google = {
      source  = "hashicorp/google",
      version = "5.1.0"
    }
  }

  backend "gcs" {
    bucket = "wewu-less-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = "wewu_less"
  region = local.region
}

resource "random_id" "wewu_less_bucket_id" {
  byte_length = 16
}

resource "google_storage_bucket" "wewu_less" {
  project = local.gcp_project
  name = "${random_id.wewu_less_bucket_id.hex}-gcf-source"
  location = "US"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "wewu_less_sources" {
  source = local.source_code_path
  name = "$wewu_less_sources-${local.source_code_hash}.zip"
  bucket = google_storage_bucket.wewu_less.name
}

output "bucket" {
  value = google_storage_bucket.wewu_less
}
