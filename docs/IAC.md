# Infrastructure as Code (Azure Bicep)

This repository avoids using Azure Key Vault for secrets. Provide secrets via
environment variables or via the platform secret configuration at deploy time.

Current IaC coverage (under `azure/iac`):

- ACR (container registry)
- Container App / Web App deployment
- Log Analytics
- Storage
- Cognitive Services (Azure OpenAI / Speech)

Key changes made

- Removed Key Vault module and references. Secrets are injected via environment
  variables or platform-managed secret stores.
- Kept `cognitiveServices.bicep` for Azure OpenAI / Speech resource provisioning.
