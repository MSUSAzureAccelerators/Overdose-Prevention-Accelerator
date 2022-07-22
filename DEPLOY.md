# Deployment Guide

## Step 1. Download Files
To start, clone or download this repository and navigate to the project's root directory.

## Step 2. Setup Resources
1. Deploy the resource group: 

      Run using Azure CLI 
        
        `az group create --name "OOA-rg" --location "westus"`

      Use this resource group for all subsequent resources.

2. Deploy the function app to the resource group:
    - The function app is contained in this folder "OOA Function App"
    - You can follow the instructions here for deploying a function app to Azure from VS Code: https://docs.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=python#quick-function-app-create

3. Upload data to the function app:
  To upload the data used for the solution, follow these steps:

    1. Open the Data Lake (called `ooadatastore` in this deployment package)
    2. Click the tab on the left column menu called Storage browser
    3. Click on the Blob containers square
    4. Click Add container, type in a name, and click Create
    5. Click Upload and upload these files:
        - Individual-Risk-Profile/models/calibXGB.model
        - Individual-Risk-Profile/models/colNamesList.zip
        - Individual-Risk-Profile/models/modelXGBCal.explainer
        - Individual-Risk-Profile/models/modelXGBCalPredProbs.npy

4. Function App Configuration

    To ensure the Web App can connect to the Function App in this solution, follow these steps:

      1. Open the Function App (called `ooamodelling` in this deployment package)
      1. Click the tab on the left column menu called App Keys
      1. Click the eye icon next to the `default` key to display the value; copy that value
      1. Add that token, and URL to the appsettings.json file under the "WebServiceUrl" section. Include the URL: `\<Function App Name\>.azurewebsites.net/api/\<Function Name\>?code=` and the token in each property, for use in the Web App.

5. Deploy the frontend app:

      [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fnsmaassel%2FOverdose-Prevention-Solution-Accelerator%2Fmain%2FdotnetApp.json)

    Note - Whenever the .bicep files are modified, the main.json file needs to be updated by running: 
    
    `az bicep build --file main.bicep --outdir .`

    *(The Deploy to Azure button does not yet support .bicep files)*

# Congratulations
You have completed this solution accelerator and should now have a report to explore the personalized recommendations:

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
