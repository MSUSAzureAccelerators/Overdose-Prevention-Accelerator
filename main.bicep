// Learn about bicep modules: https://docs.microsoft.com/en-us/azure/azure-resource-manager/bicep/modules

targetScope = 'subscription'

@description('Name for the resource group.')
param resourceGroupName string = 'OOA-rg'

@description('Location for all resources.')
param resourceGroupLocation string = 'westus'

resource ooaRG 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: resourceGroupLocation
}

@description('The name of your Web Site.')
var siteName = 'ooa-${uniqueString(ooaRG.id)}'

module frontendApp 'dotnetApp.bicep' = {
  name: '${siteName}-frontend'
  scope: ooaRG
  // params: {
  //     location: ooaRG.location
  // }
}

module functionApp 'functionApp.bicep' = {
  name: '${siteName}-functionApp'
  scope: ooaRG
  // params: {
    // location: ooaRG.location
    // appInsightsLocation: ooaRG.location
  // }
}
