@description('Deploy a Key Vault with optional access to principal ids')
param namePrefix string
param location string = resourceGroup().location
param keyVaultName string = ''
param principalIds array = []
param enableSoftDelete bool = true
param enablePurgeProtection bool = false
param tags object = {}
param enabled bool = true

var kvName = empty(keyVaultName) ? '${namePrefix}-kv' : keyVaultName

resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' = if (enabled) {
  name: kvName
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    accessPolicies: [for id in principalIds: {
      tenantId: subscription().tenantId
      objectId: id
      permissions: {
        secrets: [ 'get' ]
      }
    }]
    enableSoftDelete: enableSoftDelete
    enablePurgeProtection: enablePurgeProtection
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
  }
}

output keyVaultResourceId string = keyVault.id
output keyVaultName string = keyVault.name
