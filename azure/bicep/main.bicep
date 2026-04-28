@description('Prefix for resource names')
param prefix string = 'voice'
@description('Location for all resources')
param location string = resourceGroup().location

@description('Container image to deploy for backend (acr loginServer/image:tag)')
param backendContainerImage string = ''

@description('PostgreSQL admin username')
param postgresAdmin string = 'pgadmin'
@description('PostgreSQL admin password (secure)')
@secure()
param postgresPassword string

@description('SKU for PostgreSQL flexible server')
param postgresSkuName string = 'Standard_D2s_v3'

// ACR
module acr 'modules/acr.bicep' = {
  name: '${prefix}-acr'
  params: {
    prefix: prefix
    location: location
    sku: 'Basic'
  }
}

// Log Analytics workspace
module logAnalytics 'modules/loganalytics.bicep' = {
  name: '${prefix}-loganalytics'
  params: {
    prefix: prefix
    location: location
  }
}

// Container Apps managed environment
module appsEnv 'modules/containerAppsEnv.bicep' = {
  name: '${prefix}-appsenv'
  params: {
    prefix: prefix
    location: location
    logAnalyticsWorkspaceId: logAnalytics.outputs.workspaceResourceId
  }
}

// App Insights
module appInsights 'modules/appinsights.bicep' = {
  name: '${prefix}-appi'
  params: {
    prefix: prefix
    location: location
  }
}

// Key Vault
module kv 'modules/keyvault.bicep' = {
  name: '${prefix}-kv'
  params: {
    prefix: prefix
    location: location
  }
}

// PostgreSQL Flexible Server
module pg 'modules/postgres.bicep' = {
  name: '${prefix}-pg'
  params: {
    prefix: prefix
    location: location
    administratorLogin: postgresAdmin
    administratorPassword: postgresPassword
    skuName: postgresSkuName
  }
}

// Container App for backend
module backendApp 'modules/containerApp.bicep' = {
  name: '${prefix}-backend'
  params: {
    prefix: prefix
    location: location
    environmentId: appsEnv.outputs.environmentId
    containerImage: empty(backendContainerImage) ? acr.outputs.loginServer : backendContainerImage
    registryLoginServer: acr.outputs.loginServer
    registryUsername: acr.outputs.username
    registryPassword: acr.outputs.password
    appInsightsInstrumentationKey: appInsights.outputs.instrumentationKey
    postgresHost: pg.outputs.fqdn
    postgresUsername: '${postgresAdmin}@${pg.name}'
    postgresPassword: postgresPassword
    keyVaultId: kv.outputs.vaultId
  }
}

output acrLoginServer string = acr.outputs.loginServer
output containerAppName string = backendApp.outputs.containerAppName
output postgresFqdn string = pg.outputs.fqdn
output keyVaultId string = kv.outputs.vaultId
output appInsightsKey string = appInsights.outputs.instrumentationKey
