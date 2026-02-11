# =========================
# Resource Group
# =========================
resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
}

# =========================
# App Service Plan (LOW COST – D1)
# =========================
resource "azurerm_service_plan" "plan" {
  name                = "asp-${var.project_name}-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = var.app_service_sku
}

# =========================
# Backend API App (Linux)
# =========================
resource "azurerm_linux_web_app" "api" {
  name                = "app-${var.project_name}-api-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.plan.id

  identity {
    type = "SystemAssigned"
  }

  site_config {}

  app_settings = {
    WEBSITE_RUN_FROM_PACKAGE = "1"
    ENVIRONMENT              = var.environment
  }
}

# =========================
# Frontend Web App (Linux)
# =========================
resource "azurerm_linux_web_app" "web" {
  name                = "app-${var.project_name}-web-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.plan.id

  site_config {}

  app_settings = {
    WEBSITE_RUN_FROM_PACKAGE = "1"
    ENVIRONMENT              = var.environment
    API_BASE_URL             = azurerm_linux_web_app.api.default_hostname
  }
}

# =========================
# Cosmos DB Account (SQL API – SERVERLESS)
# =========================
resource "azurerm_cosmosdb_account" "cosmos" {
  name                = var.cosmos_account_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  offer_type = "Standard"
  kind       = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }

  capabilities {
    name = "EnableServerless"
  }
}

# =========================
# Cosmos DB SQL Database
# =========================
resource "azurerm_cosmosdb_sql_database" "db" {
  name                = "troubleshootingdb"
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.cosmos.name
}

# =========================
# Cosmos DB SQL Container
# =========================
resource "azurerm_cosmosdb_sql_container" "container" {
  name                = "troubleshooting"
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.cosmos.name
  database_name       = azurerm_cosmosdb_sql_database.db.name

  partition_key_path = "/id"
}

# =========================
# Cosmos DB SQL RBAC (Managed Identity – DATA PLANE)
# =========================
resource "azurerm_cosmosdb_sql_role_assignment" "cosmos_data_access" {
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.cosmos.name

  role_definition_id  = "${azurerm_cosmosdb_account.cosmos.id}/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002"

  principal_id        = azurerm_linux_web_app.api.identity[0].principal_id
  scope               = azurerm_cosmosdb_account.cosmos.id
}

# Azure Cognitive Search
resource "azurerm_search_service" "search" {
  name                = var.search_service_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku = "basic"

  replica_count = 1
  partition_count = 1
}

resource "azurerm_role_assignment" "search_access" {
  scope                = azurerm_search_service.search.id
  role_definition_name = "Search Service Contributor"
  principal_id         = azurerm_linux_web_app.api.identity[0].principal_id
}


