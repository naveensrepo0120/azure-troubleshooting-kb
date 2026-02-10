output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "backend_api_url" {
  value = azurerm_app_service.api.default_site_hostname
}

output "frontend_web_url" {
  value = azurerm_app_service.web.default_site_hostname
}

output "backend_managed_identity_principal_id" {
  value = azurerm_app_service.api.identity[0].principal_id
}
