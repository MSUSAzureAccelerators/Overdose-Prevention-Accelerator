@description('The name of the function app that you wish to create.')
param appName string = 'OOA-API-${uniqueString(resourceGroup().id)}'

@description('Storage Account type')
param storageAccountType string = 'Standard_LRS'

@description('Location for all resources.')
param location string = resourceGroup().location

// @description('Location for Application Insights')
// param appInsightsLocation string

@description('Which Pricing tier our App Service Plan to')
param skuName string = 'S1'

@description('How many instances of our app service will be scaled out to')
param skuCapacity int = 1

@description('The language worker runtime to load in the function app.')
param runtime string = 'python'

// *** Source control deployment is not currently working for the function app, so this has been disabled. ***
@description('The URL for the GitHub repository that contains the project to deploy.')
param repoURL string = 'https://github.com/MSUSSolutionAccelerators/Overdose-Prevention-Solution-Accelerator.git'

@description('The branch of the GitHub repository to use.')
param branch string = 'main'

var functionAppName = appName
var appServicePlanName = appName
// var applicationInsightsName = appName
var storageAccountName = 'ooads${uniqueString(resourceGroup().id)}'
var functionWorkerRuntime = runtime

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-08-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: storageAccountType
  }
  kind: 'Storage'
}

resource appServicePlan 'Microsoft.Web/serverfarms@2021-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: skuName
    capacity: skuCapacity
  }
  kind: 'functionapp,linux'
  properties: {
    perSiteScaling: false
    elasticScaleEnabled: false
    maximumElasticWorkerCount: 1
    isSpot: false
    reserved: true
    isXenon: false
    hyperV: false
    targetWorkerCount: 0
    targetWorkerSizeId: 0
    zoneRedundant: false
  }
}

resource functionApp 'Microsoft.Web/sites@2021-03-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp,linux'
  identity: {
    type: 'SystemAssigned'
  }
  dependsOn: [
#disable-next-line no-unnecessary-dependson
    storageAccount
#disable-next-line no-unnecessary-dependson
    appServicePlan
  ]
  tags: {
    displayName: 'Function App'
    ProjectName: appName
  }
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      numberOfWorkers: 1
      linuxFxVersion: 'Python|3.9'
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccountName};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccountName};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: toLower(functionAppName)
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'WEBSITE_NODE_DEFAULT_VERSION'
          value: '~10'
        }
        // {
        //   name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
        //   value: applicationInsights.properties.InstrumentationKey
        // }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: functionWorkerRuntime
        }
      ]
      ftpsState: 'FtpsOnly'
      minTlsVersion: '1.2'
    }
    httpsOnly: true
  }
}
