Azure IaC for voice-bot

This folder contains Bicep modules and a top-level `main.bicep` to deploy the minimal infrastructure required to run the backend service in Azure.

Included modules:
- Log Analytics workspace
- Azure Container Registry
- App Service Plan
- Web App (Linux single-container)
- Key Vault
- Storage Account
- Cognitive Services (placeholder for Azure OpenAI / Cognitive account)

Usage (az cli):

```bash
az deployment group create --resource-group <rg> --template-file azure/iac/main.bicep --parameters containerImage=<acrLoginServer>/myimage:tag
```

Notes:
- This is a starting scaffold modeled after your golden-standard repos. Validate the Azure OpenAI/Cognitive resource requirements for your region and subscription before deploying.
- Consider adding Role Assignments, KeyVault access policies and any Managed Identity wiring required by your runtime.
