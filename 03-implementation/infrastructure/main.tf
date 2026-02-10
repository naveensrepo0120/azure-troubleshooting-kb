resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
}

resource "azurerm_app_service_plan" "plan" {
  name                = "asp-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku {
    tier = "Shared"
    size = var.app_service_sku
  }
}

# Backend API App Service
resource "azurerm_app_service" "api" {
  name                = "app-${var.project_name}-api-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.plan.id

  identity {
    type = "SystemAssigned"
  }

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE" = "1"
    "ENVIRONMENT"              = var.environment
  }
}

# Frontend Web App Service
resource "azurerm_app_service" "web" {
  name                = "app-${var.project_name}-web-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.plan.id

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE" = "1"
    "ENVIRONMENT"              = var.environment
    "API_BASE_URL"             = azurerm_app_service.api.default_site_hostname
  }
}
