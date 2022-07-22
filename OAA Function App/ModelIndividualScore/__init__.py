from collections import defaultdict
from io import BytesIO
import json
import logging
import operator
import os

import azure.functions as func
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import joblib
import numpy as np
import pandas as pd
from scipy import stats

from . import OpioidDataPrep as odp

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Parameters/Configurations
    abs_acct_name='ooadatastore'
    abs_acct_url=f'https://{abs_acct_name}.blob.core.windows.net/'
    abs_container_name='individual'

    try:
        key_vault_name = 'ooavault'
        key_vault_Uri = f"https://{key_vault_name}.vault.azure.net"
        blob_secret_name = 'ooadatastoresecret'

        # Authenticate and securely retrieve Key Vault secret for access key value.
        az_credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=key_vault_Uri, credential= az_credential)
        access_key_secret = secret_client.get_secret(blob_secret_name)

        # Initialize Azure Service SDK Clients
        abs_service_client = BlobServiceClient(
            account_url = abs_acct_url,
            credential = az_credential
        )

        abs_container_client = abs_service_client.get_container_client(container=abs_container_name)

    except Exception as e:
        logging.info(e)
        return func.HttpResponse(
                f"!! This HTTP triggered function executed unsuccessfully. \n\t {e} ",
                status_code=200
            )

    req = req.get_json()
    df = pd.DataFrame([req])
    df = df.rename(columns={'Education': 'EDUHIGHCAT', 'Age': 'AGE2', 'Gender': 'IRSEX', 'AgeFirstAlcohol': 'IRALCAGE', 'RecentAlcohol': 'IRALCRC',
    'DaysAlcoholUseYear': 'IRALCFY', 'MoreDrinks': 'CABINGEVR', 'HadTreatmentPastYear': 'TXYRRECVD2', 'HadTreatment': 'TXEVRRCVD2', 'RecentCigarettes': 'IRCIGRC', 'AgeFirstDailySmoke': 'CIGAGE',
    'TobaccoPastYear': 'TOBYR', 'RecentCannabis': 'IRMJRC', 'DaysCannabisPastYear': 'IRMJFY', 'FirstCannabisUse': 'FUMJ18', 'RecentCocaine': 'IRCOCRC', 'RecentCrack': 'IRCRKRC', 'RecentHeroin': 'IRHERRC', 'RecentHallucinogens': 'IRHALLUCREC',
    'RecentLSD': 'IRLSDRC', 'RecentEctasy': 'IRECSTMOREC', 'RecentInhalents': 'IRINHALREC', 'RecentMeth': 'IRMETHAMREC', 'Depressed': 'ADDPREV', 'Discouraged': 'ADDSCEV', 'Arrested': 'BOOKED'})
   
    # Converting Boolean Values
    df['CABINGEVR'] = np.where(df['CABINGEVR']==0, 2, 1)
    df['FUMJ18'] = np.where(df['FUMJ18']==0, 2, 1)
    df['ADDPREV'] = np.where(df['ADDPREV']==0, 2, 1)
    df['ADDSCEV'] = np.where(df['ADDSCEV']==0, 2, 1)
    df['BOOKED'] = np.where(df['BOOKED']==0, 2, 1)
    df['TXYRRECVD2'] = np.where(df['TXYRRECVD2']==0, 0, 1)
    df['TXEVRRCVD2'] = np.where(df['TXEVRRCVD2']==0, 0, 1)
    
    # Modifying Alcohol Questions
    df['IRALCAGE'] = np.where(df['EverAlcohol']==0, 991, df['IRALCAGE'])
    df['IRALCRC'] = np.where(df['EverAlcohol']==0, 9, df['IRALCRC'])
    df['IRALCFY'] = np.where(df['EverAlcohol']==0, 991, df['IRALCFY'])
    df['IRALCAGE'] = np.where(df['EverAlcohol']==0, 91, df['IRALCAGE'])
    df['IRALCFY'] = np.where(df['IRALCRC']==3, 992, df['IRALCFY'])

    # Modifying Tobacco Questions
    df['IRCIGRC'] = np.where(df['EverSmoked']==0, 9, df['IRCIGRC'])
    df['CIGAGE'] = np.where(df['EverSmoked']==0, 9, df['CIGAGE'])
    df['TOBYR'] = np.where(df['EverSmoked']==0, 9, df['TOBYR'])
    
    # Modifying Cannabis Questions
    df['IRMJRC'] = np.where(df['EverCannabis']==0, 9, df['IRMJRC'])
    df['IRMJFY'] = np.where(df['EverCannabis']==0, 991, df['IRMJRC'])
    df['IRMJFY'] = np.where(df['IRMJRC']==3, 993, df['IRMJRC'])
    
    # Modifying Other Drug Questions
    drug_features = ['IRCOCRC', 'IRCRKRC', 'IRHERRC', 'IRHALLUCREC', 'IRLSDRC', 'IRECSTMOREC', 'IRINHALREC', 'IRMETHAMREC']
    for drug in drug_features:
        df[drug] = np.where(df['EverOther']==0, 9, df[drug])
        df[drug] = np.where(df[drug]==0, 9, df[drug])
    
    # Converting Smoking Age Questions to Binary
    df['FUCIG18'] = np.where(df['AgeFirstSmoke']<18, 2, 1)
    df['FUMJ18'] = np.where(df['FUMJ18']<18, 2, 1)
    
    # Converting Sex Variable to Binary
    df['IRSEX'] = np.where(df['IRSEX']=='Male', 1, 2)
    
    df = df.drop(columns=['EverAlcohol', 'EverSmoked', 'AgeFirstSmoke', 'EverCannabis', 'EverOther'])

    df = odp.preprocess(df)
    df = odp.sortDFbyColName(df)
    inputArr = df.values

    model = abs_container_client.download_blob('calibXGB.model').content_as_bytes()
    model = BytesIO(model)
    model = joblib.load(model)

    explainer = abs_container_client.download_blob('modelXGBCal.explainer').content_as_bytes()
    explainer = BytesIO(explainer)
    explainer = joblib.load(explainer)

    probs = abs_container_client.download_blob('modelXGBCalPredProbs.npy').content_as_bytes()
    #probs = BytesIO(probs)
    probs = np.frombuffer(probs)

    colNamesList = abs_container_client.download_blob('colNamesList.zip').content_as_bytes()
    colNamesList = BytesIO(colNamesList)
    colNamesList = joblib.load(colNamesList)

    #Calculate Prediciton
    predM = model.predict_proba(inputArr)[0][1]
    print('Predicted Probability: {:.3%}'.format(predM))
    
    #Calculate Percentile
    pct = stats.percentileofscore(probs, predM)/100
    print('Percentile of Predicted Probability: {:.3%}'.format(pct))
    print(inputArr)

    explain = {'IRSEX': 'Sex', 'EDUHIGHCAT': 'Educational Attainment', 'AGE2': 'Age',
                'IRALCRC': 'Recent Alcohol Use', 'IRALCFY': 'Frequency of Alcohol Use', 'CABINGEVR': 'Binge Drinking', 'IRALCAGE': 'Age at First Use of Alcohol',
                'TXYRRECVD2': 'Substance Use Treatment in Past Year', 'TXEVRRCVD2': 'Any Substance Use Treatment',
                'IRCIGRC': 'Recent Use of Tobacco', 'CIGAGE': 'Age at First Daily Use of Tobacco', 'TOBYR': 'Use of Tobacco in the Past Year', 'FUCIG18': 'First Use of Tobacco Prior to Age 18',
                'IRMJRC': 'Recent Use of Cannabis', 'IRMJFY': 'Frequency of Cannabis Use', 'FUMJ18': 'First Use of Cannabis Prior to Age 18',
                'IRCOCRC': 'Recent Use of Cocaine', 'IRCRKRC': 'Recent Use of Crack Cocaine', 'IRHERRC': 'Recent Use of Heroin','IRHALLUCREC': 'Recent Use of Hallucinogens',
                'IRLSDRC': 'Recent Use of LSD', 'IRECSTMOREC': 'Recent Use of Ecstacy', 'IRINHALREC': 'Recent Use of Inhalants', 'IRMETHAMREC': 'Recent Use of Methamphetamines',
                'ADDPREV': 'Several Days of Depression', 'ADDSCEV': 'Several Days of Feeling Discouraged', 'BOOKED': 'Arrested and Booked in the Criminal Justice System'}

    #Generate shapley values from this row
    shapVal = explainer.shap_values(inputArr)

    #Aggregate shapley values for one-hot vectors
    shapDict = defaultdict(list) #Handy: creates blank list if key doesn't exist, or appends to it if it does.

    #Get everything before the '_' character of each column name
    #Then create the column index numbers for those keys 
    #These numbers correspond to the locations in the shapley output array
    for i, colName in enumerate(colNamesList):
        shapDict[colName.split('_')[0]].append(i)
    
    for k in shapDict: #Loop through every key in the dict
        shapSum = 0.0 #Reset to 0
        for index in shapDict[k]: #Loop through every item in the key's value (a list of column indexes)
            shapSum += shapVal[1][0][index] #Add the value for each item
            #print('index',index,' | k', k, ' | shapVal[1][0][index]', shapVal[1][0][index])
        shapDict[k] = shapSum

    shapDict = sorted(shapDict.items(), key=operator.itemgetter(1), reverse=True)
    
    features = {}
    for i in range(len(shapDict)):
        features[explain[shapDict[i][0]]] = round(100*shapDict[i][1], 2)
    
    scores = {'score': round(100*predM, 2), 'percentile': round(100*pct, 2), 'features': features}

    return func.HttpResponse(json.dumps(scores))
    
