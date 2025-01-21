variable "project"{
    description = "project"
    default = "nodal-empire-447803-h7"
}

variable "credentials" {
  description = "my credential"
  default = "./keys/terra_keys.json"
}
variable "region" {
  description = "region"
  default = "us-central1"
}

variable "location"{
    description = "project location"
    default = "US"
}
variable "bq_dataset_name"{
    description = "big query dataset name "
    default = "demo_dataset"
}

variable "gcs_bucket_name"{
    description = "gcs bucket name "
    default = "bucket-nodal-empire-447803-h7"
}


variable "gcs_storage_class" {
  description = "bckt storage class"
  default = "STANDARD"
}