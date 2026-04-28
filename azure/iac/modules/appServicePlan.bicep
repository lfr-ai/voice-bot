param name string
param location string = resourceGroup().location
param skuName string = 'P1v2'
param skuTier string = 'PremiumV2'

resource plan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: name
  location: location
  sku: {
    name: skuName
    tier: skuTier
    capacity: 1
  }
  properties: {
    reserved: true
  }
}

output planId string = plan.id
