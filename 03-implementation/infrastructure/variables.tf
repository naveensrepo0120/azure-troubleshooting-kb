variable "location" {
  description = "Azure region"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "project_name" {
  description = "Short project name"
  type        = string
}

variable "app_service_sku" {
  description = "App Service Plan SKU"
  type        = string
  default     = "B1"
}

variable "cosmos_account_name" {
  description = "Cosmos DB account name"
  type        = string
}

variable "search_service_name" {
  description = "Azure Cognitive Search service name"
  type        = string
}

