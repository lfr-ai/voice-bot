param name string
param location string = resourceGroup().location
param image string
param acrLoginServer string
param planId string

resource site 'Microsoft.Web/sites@2022-03-01' = {
  name: name
  location: location
  kind: 'linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: planId
    siteConfig: {
      linuxFxVersion: 'DOCKER|${image}'
      appSettings: [
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_URL'
          value: 'https://${acrLoginServer}'
        }
      ]
    }
  }
}

output defaultHostName string = site.properties.defaultHostName
output siteId string = site.id
output principalId string = site.identity.principalId
output tenantId string = site.identity.tenantId
