param prefix string
param location string

resource law 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: '${prefix}-law'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
  }
}

output workspaceResourceId string = law.id
output workspaceName string = law.name
