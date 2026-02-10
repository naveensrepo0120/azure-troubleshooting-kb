variable "project_name" {
  description = "Short project name"
  type        = string
}

variable "app_service_sku" {
  description = "App Service Plan SKU"
  type        = string
  default     = "D1"
}
