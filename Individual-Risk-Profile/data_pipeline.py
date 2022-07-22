#%%
#Import Required Libraries
from collections import defaultdict
import operator


import pandas as pd
import numpy as np
import joblib  #Used to save/load (pickle) models
from scipy import stats
import shap

#Custom data prep function used in both training and prediction 
import OpioidDataPrep as odp
import OpioidExecution as oe

#%%
#Set initial parameter(s)
pd.set_option('display.max_rows', 200)
pd.options.display.max_columns = 150
modelDir = 'models/'

print('Pandas Version', pd.__version__)

# import sklearn
# print('SciKit Learn Version', sklearn.__version__)

#%%
#Simulate User Input

inputDict = dict()

'''
[{'NAME': 'sharad', 'AGE2': 27, 'IRSEX': 1, 'IREDUHIGHST2': 11}, {'IRALCAGE': 13, 'IRALCRC': 1, 'IRALCFY': 300, 
'BNGDRKMON': 1, 'HVYDRKMON': 1}, {'TXYRRECVD2': 1, 'TXEVRRCVD2': 1}, {'IRCIGRC': 1, 'CIGDLYMO': 1, 'CIGAGE': 13, 
'PIPEVER': 1, 'IRCGRRC': 1, 'IRSMKLSSREC': 1}, {'IRMJRC': 1, 'MJYRTOT': 300, 'FUMJ18': 1, 'FUMJ21': 1}, 
{'ADDPREV': 1, 'ADDSCEV': 1}, {'BOOKED': 1}]
'''

#DEMOGRAPHICS
inputDict['NAME'] = 'Joe Capstone' #We will delete this column
inputDict['IRSEX'] = 1 #Gender: 'Male' or 'Female'
inputDict['EDUHIGHCAT'] = 1 #Education:
inputDict['AGE2'] = 10 #Age: Remember, don't enter an age, but an age code from the codebook
    
#ALCOHOL
inputDict['IRALCRC'] = 9 #(Alcohol Recency)
inputDict['IRALCFY'] = 12 #(Alcohol Frequency Past Year)
inputDict['CABINGEVR'] = 2 #(Ever binge drank)
inputDict['IRALCAGE'] = 21 #(First time used alcohol)

#DRUGS + ALCOHOL
inputDict['TXYRRECVD2'] = 0 #(Ever alcohol/drug treatment, past yr)
inputDict['TXEVRRCVD2'] = 1 #(Ever alcohol/drug treatment, lifetime)

#TOBACCO
inputDict['IRCIGRC'] = 1 #(Tobacco Recency, incl. Never)
#inputDict['CIGDLYMO'] = 1 #(Tobacco 30+ consecutive days)
inputDict['CIGAGE'] = 13 #(Tobacco Use Daily)
inputDict['TOBYR'] = 1 #(Used any tobacco product in past year, cigar, cigarette, etc.)
inputDict['FUCIG18'] = 1 #(Used cigarettes before 18)
    
#WEED
inputDict['IRMJRC'] = 1 #(Weed recency)
inputDict['IRMJFY'] = 2 #(Weed days in past year)
inputDict['FUMJ18'] = 1 #(First used weed prior to age 18)

#HARD DRUGS
inputDict['IRCOCRC'] = 9 #(Cocaine Recency)
inputDict['IRCRKRC'] = 9 #(Crack Recency)
inputDict['IRHERRC'] = 1 #(Heronie Recency)
inputDict['IRHALLUCREC'] = 9 #(Hallucinogen Recency)
inputDict['IRLSDRC'] = 9 #(LSD Recency)
inputDict['IRECSTMOREC'] = 9 #(Ecstacy Recency)
inputDict['IRINHALREC'] = 9 #(Inhalant Recency)
inputDict['IRMETHAMREC'] = 9 #(Meth Recency)

#DEPRESSION
inputDict['ADDPREV'] = 1 #(Several days of depression)
inputDict['ADDSCEV'] = 1 #(Several days of discouraged about life)
    
##OTHER
inputDict['BOOKED'] = 1 #(Ever arrested & booked)

print(inputDict)

#%%
#Convert to dataframe

#Web App Test
runWebAppTest = True
predFI = None
if runWebAppTest:
    predProb, predPercentile, predFI = oe.generateReport(inputDict)  #This one line "does all the work"
    print('Predicted Probability: {:.3%}'.format(predProb))
    print('Percentile of Predicted Probability: {:.3%}'.format(predPercentile))
    print('Feature Importance (sorted low to high):')
predFI

#%%
#Convert inputs to list (pandas conversion to dataframe requires dict values to be lists)
if not runWebAppTest: 
    '''If we run our web app test, these next two lines already run in that and thus
    can't be run here (they'll double-list the dictionary)
    '''
    for k in inputDict:
        inputDict[k] = [inputDict[k]]
print(inputDict)

#Convert dict to dataframe
df = pd.DataFrame.from_dict(inputDict)

#Run preprocessing on dataframe
df = odp.preprocess(df)

#Resort by column name (necessary to feed the model)
df = odp.sortDFbyColName(df)

#Convert to numpy
inputArr = df.values

#%%
#Load Models
#
model = joblib.load(modelDir+'calibLR.model')
explainer = joblib.load(modelDir+'modelLRCal.explainer')
probs = np.load(modelDir+'modelLRCalPredProbs.npy')

#XGB
# model = joblib.load(modelDir+'modelXGB.model')
# explainer = joblib.load(modelDir+'modelXGB.explainer')
# probs = np.load(modelDir+'modelXGBPredProbs.npy')

#Load feature names (column names)
colNamesList = joblib.load(modelDir+'colNamesList.zip')
colNamesList

#Calculate Prediciton
predM = model.predict_proba(inputArr)[0][1]
print('Predicted Probability: {:.3%}'.format(predM))

#Calculate Percentile
pct = stats.percentileofscore(probs, predM)/100
print('Percentile of Predicted Probability: {:.3%}'.format(pct))
print(inputArr)
#Generate shapley values from this row
shapVal = explainer.shap_values(inputArr)

#Aggregate shapley values for one-hot vectors
shapDict = defaultdict(list) #Handy: creates blank list if key doesn't exist, or appends to it if it does.

#Get everything before the '_' character of each column name
#Then create the column index numbers for those keys 
#These numbers correspond to the locations in the shapley output array
for i, colName in enumerate(colNamesList):
    shapDict[colName.split('_')[0]].append(i)
    
#Make a list of aggregated values shapley
for k in shapDict: #Loop through every key in the dict
    shapSum = 0.0 #Reset to 0
    for index in shapDict[k]: #Loop through every item in the key's value (a list of column indexes)
        shapSum += shapVal[1][0][index] #Add the value for each item
        #print('index',index,' | k', k, ' | shapVal[1][0][index]', shapVal[1][0][index])
    shapDict[k] = shapSum #Replace the list with the aggregated shapley value (the sum of each individual value)
    #print('NEXT k')

sortedShapDict = dict(sorted(shapDict.items(), key=operator.itemgetter(1)))
print('Feature Importance (sorted low to high):')
print(sortedShapDict)  
# %%
