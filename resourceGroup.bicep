targetScope = 'subscription'

@description('Name for the resource group.')
param resourceGroupName string = 'OOA-rg'

@description('Location for all resources.')
param resourceGroupLocation string = 'westus'

resource ooaRG 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: resourceGroupLocation
}
