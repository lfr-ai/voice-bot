param namePrefix string
param location string
param workspaceResourceId string
param kind string = 'web'
param applicationType string = 'web'
param retentionInDays int = 90
param tags object
param enabled bool = true

var appInsightsName = '${namePrefix}-ai'

resource appInsights 'Microsoft.Insights/components@2020-02-02' = if (enabled) {
  name: appInsightsName
  location: location
  tags: tags
  kind: kind
  properties: {
    Application_Type: applicationType
    WorkspaceResourceId: workspaceResourceId
  }
}

output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
