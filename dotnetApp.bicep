@description('The name of you Web Site.')
param siteName string = 'OOA-${uniqueString(resourceGroup().id)}'

@description('Location for all resources.')
param location string = resourceGroup().location

@description('The pricing tier for the hosting plan.')
param sku string = 'F1'

@description('The instance size of the hosting plan (small, medium, or large).')
param workerSize string = '0'

@description('The URL for the GitHub repository that contains the project to deploy.')
param repoURL string = 'https://github.com/nsmaassel/Overdose-Prevention-Solution-Accelerator.git'

@description('The branch of the GitHub repository to use.')
param branch string = 'main'

var hostingPlanName_var = 'hpn-${resourceGroup().name}'

resource hostingPlanName 'Microsoft.Web/serverfarms@2020-12-01' = {
  name: hostingPlanName_var
  location: location
  sku: {
    name: sku
    capacity: workerSize
  }
  properties: {
    name: hostingPlanName_var
  }
}

resource siteName_resource 'Microsoft.Web/sites@2020-12-01' = {
  name: siteName
  location: location
  properties: {
    serverFarmId: hostingPlanName.id
  }
}

resource siteName_web 'Microsoft.Web/sites/sourcecontrols@2020-12-01' = {
  parent: siteName_resource
  name: 'web'
  location: location
  properties: {
    repoUrl: repoURL
    branch: branch
    isManualIntegration: true
  }
}

resource siteName_config 'Microsoft.Web/sites/config@2021-03-01' = {
  parent: siteName_resource
  name: 'appsettings'
  properties: {
    PROJECT: 'OverdoseAcceleratorWeb\\OverdoseAcceleratorWeb.csproj'
    clientUrl: 'http://${siteName}.azurewebsites.net'
    netFrameworkVersion: 'v6.0'
  }
  dependsOn: [
    siteName_web
  ]
}
