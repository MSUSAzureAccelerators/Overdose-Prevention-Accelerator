// Learn about bicep modules: https://docs.microsoft.com/en-us/azure/azure-resource-manager/bicep/modules

targetScope = 'subscription'

var resourceGroupName = 'OOA-rg'

resource ooaRG 'Microsoft.Resources/resourceGroups@2021-04-01' existing = {
  name: resourceGroupName
}

@description('The name of your Web Site.')
var siteName = 'ooa-${uniqueString(ooaRG.id)}'

module frontendApp 'dotnetApp.bicep' = {
  name: '${siteName}-frontend'
  scope: ooaRG
  params: {
      location: ooaRG.location
  }
}

module functionApp 'functionApp.bicep' = {
  name: '${siteName}-functionApp'
  scope: ooaRG
  params: {
    location: ooaRG.location
    // appInsightsLocation: ooaRG.location
  }
}
