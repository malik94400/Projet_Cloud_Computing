variable "location" {
  default = "francecentral"
}

variable "resource_group_name" {
  default = "terraform-flask-rg"
}

variable "storage_account_name" {
  type = string
}

variable "container_name" {
  default = "files"
}
