# Deployment Guide

## Step 1. Download Files
To start, clone or download this repository and navigate to the project's root directory.

## Step 2. Setup Resources

## ARM template deployment

# Using the deploy button
Whenever the .bicep files are modified, the main.json file needs to be updated by running:
`az bicep build --file main.bicep --outdir .`

This is because the Deploy to Azure button does not yet support .bicep files.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fnsmaassel%2FOverdose-Prevention-Solution-Accelerator%2Fmain%2Fmain.json)

# Building the ARM template
Create resource group
az group create --name "OOA-rg" --location "westus"

Create deployment group and deploy via ARM template
<!-- Resource Group deploy -->
`az deployment group create --name "NickOOADeployment" --resource-group "Nick-OOA-rg" --template-file "./main.bicep"`
az deployment sub create --name "OOADeployment" --template-file "./main.bicep" --parameters resourceGroupLocation="westus"

<!-- Subscription deploy -->
<!--    Deploy everything at once -->
az deployment sub create --name "OOADeployment" --location "westus" --template-file "./main.bicep"
<!--    Deploy just the frontend -->
az deployment group create --name "OOAFrontendDeployment" --resource-group OOA-rg --template-file "./dotnetApp.bicep"
<!--    Deploy just the backend/function app -->
az deployment group create --name "OOAFunctionAppDeployment" --resource-group OOA-rg --template-file "./functionApp.bicep"
<!-- How to pass parameters to a bicep file: -->
  <!-- --parameters storageAccountType=Standard_GRS -->

## Teardown
<!-- Delete everything -->
az group delete --name "OOA-rg"

## Step 3. Upload Sample Dataset

## Step 4. Security Access

## Step 5. text here

## Step 6. text here

# Congratulations
You have completed this solution accelerator and should now have a report to explore the personalized recommendations:

