targetScope = 'subscription'

@description('Nome del Resource Group')
param resourceGroupName string

@description('Location')
param location string = 'westeurope'

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
}

output resourceGroupId string = rg.id
