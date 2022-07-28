// References:
// https://github.com/Azure/azure-quickstart-templates/blob/master/quickstarts/microsoft.web/web-app-loganalytics/main.bicep

// Kudu: https://docs.microsoft.com/en-us/azure/app-service/resources-kudu

@description('Name that will be used to build associated artifacts')
param appName string = 'OOA-${uniqueString(resourceGroup().id)}'

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Which Pricing tier our App Service Plan to')
param skuName string = 'S1'

@description('How many instances of our app service will be scaled out to')
param skuCapacity int = 1

@description('The URL for the GitHub repository that contains the project to deploy.')
param repoURL string = 'https://github.com/MSUSSolutionAccelerators/Overdose-Prevention-Solution-Accelerator.git'

@description('The branch of the GitHub repository to use.')
param branch string = 'main'

var appServicePlanName = 'asp-${appName}'
var webSiteName = toLower('wapp-${appName}')
// var appInsightName = toLower('appi-${appName}')
// var logAnalyticsName = toLower('la-${appName}')

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
  // dependsOn: [
  //   logAnalyticsWorkspace
  // ]
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
    appServiceLogging
  ]
}

resource appServiceLogging 'Microsoft.Web/sites/config@2021-03-01' = {
  parent: appService
  name: 'appsettings'
  properties: {
    // APPINSIGHTS_INSTRUMENTATIONKEY: appInsights.properties.InstrumentationKey
    PROJECT: 'Overdose-Accelerator-Web\\OverdoseAcceleratorWeb.csproj'
    clientUrl: 'http://${appName}.azurewebsites.net'
    netFrameworkVersion: 'v6.0'
  }
  // dependsOn: [
  //   appServiceSiteExtension
  //   appSource
  // ]
}

// resource appServiceSiteExtension 'Microsoft.Web/sites/siteextensions@2020-06-01' = {
//   parent: appService
//   name: 'Microsoft.ApplicationInsights.AzureWebSites'
//   dependsOn: [
//     appInsights
//   ]
// }

// resource appServiceAppSettings 'Microsoft.Web/sites/config@2020-06-01' = {
//   parent: appService
//   name: 'logs'
//   properties: {
//     applicationLogs: {
//       fileSystem: {
//         level: 'Warning'
//       }
//     }
//     httpLogs: {
//       fileSystem: {
//         retentionInMb: 40
//         enabled: true
//       }
//     }
//     failedRequestsTracing: {
//       enabled: true
//     }
//     detailedErrorMessages: {
//       enabled: true
//     }
//   }
// }

// resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
//   name: appInsightName
//   location: location
//   kind: 'string'
//   tags: {
//     displayName: 'AppInsight'
//     ProjectName: appName
//   }
//   properties: {
//     Application_Type: 'web'
//     WorkspaceResourceId: logAnalyticsWorkspace.id
//   }
// }

// resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2020-08-01' = {
//   name: logAnalyticsName
//   location: location
//   tags: {
//     displayName: 'Log Analytics'
//     ProjectName: appName
//   }
//   properties: {
//     sku: {
//       name: 'PerGB2018'
//     }
//     retentionInDays: 120
//     features: {
//       searchVersion: 1
//       legacy: 0
//       enableLogAccessUsingOnlyResourcePermissions: true
//     }
//   }
// }
