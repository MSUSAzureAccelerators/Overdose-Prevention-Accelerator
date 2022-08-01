# Deployment Guide

## Step 1. Download Files
To start, clone or download this repository and navigate to the project's root directory.

## Step 2. Setup Resources
1. Deploy the resource group: 

      Run using Azure CLI 
        
        `az group create --name "OOA-rg" --location "westus"`

      Use this resource group for all subsequent resources.

1. Deploy the function app to the resource group:
    - The function app is contained in this folder "OOA Function App"
    - You can follow the instructions here for deploying a function app to Azure from VS Code: https://docs.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=python#quick-function-app-create
        
1. Upload data to the function app:
  To upload the data used for the solution, follow these steps:

    1. Open the Data Lake (called `ooadatastore` in this deployment package)
    1. Click the tab on the left column menu called Storage browser
    1. Click on the Blob containers square
    1. Click Add container, type in a name, and click Create
    1. Click Upload and upload these files:
        - Individual-Risk-Profile/models/calibXGB.model
        - Individual-Risk-Profile/models/colNamesList.zip
        - Individual-Risk-Profile/models/modelXGBCal.explainer
        - Individual-Risk-Profile/models/modelXGBCalPredProbs.npy

1. Configure Key Vault
  To configure the Key Vault, follow these steps:

    1. In the Data Lake (called `ooadatastore` in this deployment package), click the tab on the left column menu called Access keys
    1. Click the Show button next to the Key value for key1, and copy that value
    1. Open the Key Vault (called `ooavault` in this deployment package)
    1. Click the tab on the let column menu called Secrets
    1. Click Generate/Import Secret
    1. Enter a Name for the secret (called `ooadatastoresecret` in this deployment package) and enter the copied key in the Value field, then click Create


1. Function App Configuration

    To ensure the Web App can connect to the Function App in this solution, follow these steps:

      1. Open the Function App (called `ooamodelling` in this deployment package)
      1. Click the tab on the left column menu called App Keys
      1. Click the eye icon next to the `default` key to display the value; copy that value

1. Deploy the frontend app:

      [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fnsmaassel%2FOverdose-Prevention-Solution-Accelerator%2Fmain%2Fmain.json)

    Note - Whenever the .bicep files are modified, the main.json file needs to be updated by running: 
    
    `az bicep build --file main.bicep --outdir .`

    *(The Deploy to Azure button does not yet support .bicep files)*

    After the frontend app is deplouyed
     1. Add the token, and URL to the appsettings.json file, in the Overdose-Accelerator-Web project, under the "WebServiceUrl" section. Include the URL: `\<Function App Name\>.azurewebsites.net/api/\<Function Name\>?code=` and the token in each property, for use in the Web App.
     1. You can then
        a. Publish the app with the new appsettings.json file from VS Code
        b. Or go to the Azure Portal find the web app inside your resource group and open it to view it's overview. 
            i. Scroll dow on the left hand menue to the Development Tools section and select App Service Editor and directly edit the appsettings.json file. 
            i. After editing and saveing the file you will need to return to the over view page at the top and restart the front end app.  

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
