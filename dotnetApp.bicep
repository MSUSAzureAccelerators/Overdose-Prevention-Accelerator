@description('Name that will be used to build associated artifacts')
param appName string = 'OOA-${uniqueString(resourceGroup().id)}'

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Which Pricing tier our App Service Plan to')
param skuName string = 'S1'

@description('How many instances of our app service will be scaled out to')
param skuCapacity int = 1

@description('The URL for the GitHub repository that contains the project to deploy.')
// param repoURL string = 'https://github.com/MSUSSolutionAccelerators/Overdose-Prevention-Solution-Accelerator.git'
// Sample deployment from a forked repo
param repoURL string = 'https://github.com/nsmaassel/Overdose-Prevention-Solution-Accelerator.git'

@description('The branch of the GitHub repository to use.')
// param branch string = 'main'
// Sample deployment from a branch named 'deploy'
param branch string = 'deploy'

var appServicePlanName = 'asp-${appName}'
var webSiteName = toLower('wapp-${appName}')

resource appServicePlan 'Microsoft.Web/serverfarms@2020-12-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: skuName
    capacity: skuCapacity
  }
  tags: {
    displayName: 'HostingPlan'
    ProjectName: appName
  }
}

resource appService 'Microsoft.Web/sites@2020-12-01' = {
  name: webSiteName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  tags: {
    displayName: 'Website'
    ProjectName: appName
  }
  properties: {
    serverFarmId: appServicePlan.id
  }
}

resource appSource 'Microsoft.Web/sites/sourcecontrols@2020-12-01' = {
  parent: appService
  name: 'web'
  location: location
  properties: {
    repoUrl: repoURL
    branch: branch
    isManualIntegration: true
  }
  dependsOn: [
    appServiceConfig
  ]
}

resource appServiceConfig 'Microsoft.Web/sites/config@2021-03-01' = {
  parent: appService
  name: 'appsettings'
  properties: {
    PROJECT: 'Overdose-Accelerator-Web\\OverdoseAcceleratorWeb.csproj'
    clientUrl: 'http://${appName}.azurewebsites.net'
    netFrameworkVersion: 'v6.0'
  }
}
