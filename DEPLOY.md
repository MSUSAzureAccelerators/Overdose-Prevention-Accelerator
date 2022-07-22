# Deployment Guide

## Step 1. Download Files
To start, clone or download this repository and navigate to the project's root directory.

## Step 2. Setup Resources

# Using the deploy button
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fnsmaassel%2FOverdose-Prevention-Solution-Accelerator%2Fmain%2Fmain.json)

Note - Whenever the .bicep files are modified, the main.json file needs to be updated by running: 
`az bicep build --file main.bicep --outdir .`

*(The Deploy to Azure button does not yet support .bicep files)*

# Deploying the app from the command line
### Create resource group
`az group create --name "OOA-rg" --location "westus"`

### Create deployment group and deploy via ARM template
<!-- Resource Group deploy -->
`az deployment sub create --name "OOADeployment" --template-file "./main.bicep" --parameters resourceGroupLocation="westus"`

## Alternative deployment methods
<!-- Subscription deploy -->
### Deploy everything at once ###
`az deployment sub create --name "OOADeployment" --location "westus" --template-file "./main.bicep"`

### Deploy just the frontend ###
`az deployment group create --name "OOAFrontendDeployment" --resource-group OOA-rg --template-file "./dotnetApp.bicep"`

### Deploy just the backend/function app ###
`az deployment group create --name "OOAFunctionAppDeployment" --resource-group OOA-rg --template-file "./functionApp.bicep"`

## Teardown
If you want to delete everything created, just delete the resource group as follows:
<!-- Delete everything -->
`az group delete --name "OOA-rg"`

## Step 3. Upload Data
To upload the data used for the solution, follow these steps:

1. Open the Data Lake (called `oaadatastore` in this deployment package)
1. Click the tab on the left column menu called Storage browser
1. Click on the Blob containers square
1. Click Add container, type in a name, and click Create
1. Click Upload and upload these files:
  - Individual-Risk-Profile/models/calibXGB.model
  - Individual-Risk-Profile/models/colNamesList.zip
  - Individual-Risk-Profile/models/modelXGBCal.explainer
  - Individual-Risk-Profile/models/modelXGBCalPredProbs.npy

## Step 4. Function App Configuration

To ensure the Web App can connect to the Function App in this solution, follow these steps:

1. Open the Function App (called `oaamodelling` in this deployment package)
1. Click the tab on the left column menu called App Keys
1. Click the eye icon next to the `default` key to display the value; copy that value
1. Add that token, and URL to the appsettings.json file under the "WebServiceUrl" section. Include the URL: `\<Function App Name\>.azurewebsites.net/api/\<Function Name\>?code=` and the token in each property, for use in the Web App

## Step 5. Individual Score Web App Configuration

## Step 6. Community Level Web App Configuration

# Congratulations
You have completed this solution accelerator and should now have a report to explore the personalized recommendations:

