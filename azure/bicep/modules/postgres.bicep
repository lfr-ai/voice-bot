param prefix string
param location string
param administratorLogin string
@secure()
param administratorPassword string
param skuName string = 'Standard_D2s_v3'

resource pg 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: '${prefix}-pg'
  location: location
  sku: {
    name: 'Standard_D2s_v3'
    tier: 'GeneralPurpose'
  }
  properties: {
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorPassword
    version: '14'
    storage: {
      storageSizeGB: 32
    }
    network: {
      delegatedSubnetResourceId: ''
      publicNetworkAccess: 'Enabled'
    }
  }
}

output fqdn string = pg.properties.fullyQualifiedDomainName
output name string = pg.name
