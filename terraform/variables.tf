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

variable "vm_name" {
  default = "flask-vm"
}

variable "admin_username" {
  default = "azureuser"
}

variable "vm_size" {
  default = "Standard_B2as_v2"
}

variable "azure_storage_account" {
  type = string
}

variable "azure_storage_key" {
  type      = string
  sensitive = true
}

variable "azure_container_name" {
  type    = string
  default = "files"
}