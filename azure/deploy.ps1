param(
  [Parameter(Mandatory=$true)][string]$resourceGroup,
  [string]$env = 'dev'
)

$paramFile = "azure/iac/parameters/$env.parameters.json"

if (-not (Test-Path $paramFile)) {
  Write-Error "Parameters file not found: $paramFile"
  exit 2
}

az deployment group create --resource-group $resourceGroup --template-file azure/iac/main.bicep --parameters "@$paramFile"

Write-Host "Deployment complete."
