param prefix string
param location string
param sku string = 'Basic'

resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01' = {
  name: '${prefix}acr'
  location: location
  sku: {
    name: sku
  }
  properties: {
    adminUserEnabled: true
  }
}

// Create admin credentials (listCredentials)
output loginServer string = acr.properties.loginServer
output registryName string = acr.name

// For runtime usage we also call listCredentials in deployment outputs via CLI or deployment script
