param prefix string
param location string

resource ai 'Microsoft.Insights/components@2020-02-02' = {
  name: '${prefix}-ai'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

output instrumentationKey string = ai.properties.InstrumentationKey
output appInsightsId string = ai.id
