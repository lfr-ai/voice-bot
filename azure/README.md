Azure infrastructure for the voice-bot project

This folder contains Bicep modules and deployment scripts to provision the minimal
and recommended Azure resources for running the voice-bot application in a cloud
environment. It is modeled after the patterns used in the organization's
golden-standard IaC (see claim_handler_v3/azure/iac) and follows best practices:

- Separate modules (KeyVault, Log Analytics, App Insights, ACR, Container App)
- Parameters per environment (dev/test/prod)
- Deploy scripts for PowerShell and bash

Resources provisioned (configurable):
- Key Vault (secrets like OPENAI_KEY)
- Azure Container Registry (for building and storing images)
- Log Analytics workspace
- Application Insights
- Azure Container Apps environment + container app running the FastAPI

Usage

1. Edit `parameters/{env}.json` with appropriate names and values.
2. Deploy with:

```bash
az deployment group create \
  --resource-group my-rg \
  --template-file azure/iac/main.bicep \
  --parameters @azure/iac/parameters/dev.parameters.json
```

Or run the included `deploy.sh` / `deploy.ps1` scripts.
