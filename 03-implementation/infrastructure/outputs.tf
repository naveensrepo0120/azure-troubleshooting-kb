output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "backend_api_url" {
  value = azurerm_linux_web_app.api.default_hostname
}

output "frontend_web_url" {
  value = azurerm_linux_web_app.web.default_hostname
}

output "backend_managed_identity_principal_id" {
  value = azurerm_linux_web_app.api.identity[0].principal_id
}

output "cosmos_endpoint" {
  value = azurerm_cosmosdb_account.cosmos.endpoint
}

output "search_service_name" {
  value = azurerm_search_service.search.name
}

output "search_endpoint" {
  value = "https://${azurerm_search_service.search.name}.search.windows.net"
}
