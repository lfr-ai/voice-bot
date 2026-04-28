param prefix string
param location string

resource kv 'Microsoft.KeyVault/vaults@2022-07-01' = {
  name: '${prefix}-kv'
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    accessPolicies: []
    enabledForDeployment: true
    enableSoftDelete: true
  }
}

output vaultId string = kv.id
output vaultName string = kv.name
