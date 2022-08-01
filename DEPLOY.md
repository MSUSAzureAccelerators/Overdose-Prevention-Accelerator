# Deployment Guide

Deployment steps can be found in the README.md file.

Below are some additional commands you can use to deploy your project.

# Other resources

## Alternative deployment via command line
### Create resource group
`az group create --name "OOA-rg" --location "westus"`

### Create deployment group and deploy via ARM template
<!-- Resource Group deploy -->
`az deployment sub create --name "OOADeployment" --template-file "./main.bicep" --parameters resourceGroupLocation="westus"`

## Alternative deployment methods
<!-- Subscription deploy -->
### Deploy everything at once
`az deployment sub create --name "OOADeployment" --location "westus" --template-file "./main.bicep"`

### Deploy just the frontend
`az deployment group create --name "OOAFrontendDeployment" --resource-group OOA-rg --template-file "./dotnetApp.bicep"`

### Deploy just the backend/function app
`az deployment group create --name "OOAFunctionAppDeployment" --resource-group OOA-rg --template-file "./functionApp.bicep"`

## Teardown
If you want to delete everything created, just delete the resource group as follows:
<!-- Delete everything -->
`az group delete --name "OOA-rg"`
