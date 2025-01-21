terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.16.0"
    }
  }
}

provider "google" {
  project     = "nodal-empire-447803-h7"
  region      = "us-central1"
  credentials = "./keys/terra_keys.json"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "bucket-nodal-empire-447803-h7"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "Delete"
    }
  }
}