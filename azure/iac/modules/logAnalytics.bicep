param name string
param location string = resourceGroup().location

@description('Creates a Log Analytics Workspace')
resource la 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: name
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
  }
}

output logAnalyticsResourceId string = la.id
