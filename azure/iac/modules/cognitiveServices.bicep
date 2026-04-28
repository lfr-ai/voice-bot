param name string
param location string = resourceGroup().location
param kind string = 'CognitiveServices'
param skuName string = 'S0'

resource cognitive 'Microsoft.CognitiveServices/accounts@2022-12-01' = {
  name: name
  location: location
  sku: {
    name: skuName
  }
  kind: kind
  properties: {
    // regional properties may be required for some account kinds; keep minimal here
  }
}

output resourceId string = cognitive.id
