param prefix string
param location string
param logAnalyticsWorkspaceId string

resource env 'Microsoft.App/managedEnvironments@2023-10-01' = {
  name: '${prefix}-env'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: reference(logAnalyticsWorkspaceId).customerId
        sharedKey: listKeys(logAnalyticsWorkspaceId, '2020-08-01').primarySharedKey
      }
    }
  }
}

output environmentId string = env.id
output environmentName string = env.name
