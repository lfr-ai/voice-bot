Azure Bicep templates for the voice-bot project

This folder contains modular Bicep files to provision the common infrastructure
used by the service. It follows the golden-standard template layout and is
intended for development and staging environments. Review and harden for
production workloads.

Resources provisioned (by default):
- Azure Container Registry (ACR)
- Log Analytics workspace
- Container Apps managed Environment
- Container App for backend
- PostgreSQL Flexible Server
- Key Vault
- Application Insights

Prereqs
- Azure CLI (az)
- You must have the following resource providers registered:
  - Microsoft.ContainerRegistry
  - Microsoft.OperationalInsights
  - Microsoft.App
  - Microsoft.DBforPostgreSQL
  - Microsoft.KeyVault
  - Microsoft.Insights

Register providers (if needed):

```bash
az provider register --namespace Microsoft.ContainerRegistry
az provider register --namespace Microsoft.OperationalInsights
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.DBforPostgreSQL
az provider register --namespace Microsoft.KeyVault
az provider register --namespace Microsoft.Insights
```

Deploy (resource group scoped):

```bash
az deployment group create \
  --resource-group my-rg \
  --template-file ./azure/bicep/main.bicep \
  --parameters @./azure/bicep/parameters.json
```

Notes & next steps
- ACR admin credentials are enabled temporarily to simplify bootstrap; in
  production prefer Service Principal / managed identity with ACR role assignment.
- The PostgreSQL server defaults to public network access for developer
  convenience. Consider using VNet integration or private endpoints for production.
- The Container App image can be provided as `backendContainerImage` (e.g.
  "myacr.azurecr.io/voice:latest") or left empty to use the newly created ACR.
- Consider adding network, monitoring, backup, and security hardening modules.
