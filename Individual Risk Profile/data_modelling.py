#%%
#Import Required Libraries
import itertools

#General libraries
import numpy as np
import pandas as pd
import joblib  #Used to save (pickle) models

#Model Preprocessing
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE #conda install -c conda-forge imbalanced-learn

#Modeling
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
import xgboost #Tricky installation, see instructions (search for XGBoost)

#Model evaluation
from sklearn.metrics import (accuracy_score, roc_curve, roc_auc_score, auc, confusion_matrix, 
                             classification_report, brier_score_loss, precision_score, 
                             recall_score, f1_score, log_loss, make_scorer)
from sklearn.model_selection import (learning_curve, validation_curve)
import shap

#Calibration
from sklearn.calibration import calibration_curve
from sklearn.calibration import CalibratedClassifierCV

#Visualization
import matplotlib.pyplot as plt
import seaborn as sns

import OpioidDataPrep as odp  #Custom functions for this project

#%%
#Define Directories
dataDir = 'data/processed/'
modelDir = 'models/'

#Notebook Custom Parameters
useSMOTE = True
# %%
df = pd.read_csv(dataDir+'processed.csv')
df = odp.sortDFbyColName(df)

# %%
xCols = df.columns.difference(['MISUSE'])
dfX = df[xCols]
dfY = df.drop(xCols, axis=1)

#%%
#Train, Val, Test splits
trainPct = 0.6
valPct = 0.25
testPct = 0.15

#Splitsville!
trainX, valtestX, trainY, valtestY = train_test_split(
    dfX, dfY, train_size=(trainPct), shuffle=True)
valX, testX, valY, testY = train_test_split(
     valtestX, valtestY, train_size=(valPct/(valPct+testPct)), shuffle=True)

#%%
#SMOTE Oversampling
if useSMOTE:
    #From https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8
    os = SMOTE(random_state=0)
    columns = trainX.columns
    osX, osY = os.fit_resample(trainX, trainY)
    osX = pd.DataFrame(data=osX,columns=columns)
    osY = pd.DataFrame(data=osY,columns=['MISUSE'])

    #Finally, set trainX and trainY to be osX and osY 
    #(allows the model to use trainX and trainY regardless of whether oversampling is selected)
    trainX, trainY = osX, osY

#%%
#Save column names to a pickle file
colNamesList = list(trainX.columns)

joblib.dump(colNamesList, modelDir+'colNamesList.zip')
    
'''To open in other files:
colNamesList = joblib.load(modelDir+'colNamesList.zip')
'''

#Convert dataframes to numpy arrays (do this AFTER saving column names)
trainX = trainX.values
trainY = trainY.values
valX = valX.values
valY = valY.values
testX = testX.values
testY = testY.values

#Save input data as numpy objects (for use in calculating feature importance, i.e., Shapley values)
np.save(arr=valX, file=modelDir+'valX.npy', allow_pickle=True)
np.save(arr=testX, file=modelDir+'testX.npy', allow_pickle=True)

#%%
#Set and train a logistic regression model
modelLR = LogisticRegression()
modelLR.fit(trainX, trainY)

#%%
custScoreBrier = make_scorer(brier_score_loss, greater_is_better=True, needs_proba=True)

train_sizes, train_scores, test_scores = learning_curve(modelLR, trainX, trainY, n_jobs=-1, 
                                                        shuffle=True, verbose=2, cv=5, scoring=custScoreBrier)

#brier_score_loss
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

plt.figure()
plt.title("Learning Curve, LRClassifier")
plt.legend(loc="best")
plt.xlabel("Training examples")
plt.ylabel("Brier Loss Score (lower is better)")
#plt.gca().invert_yaxis()

# box-like grid
plt.grid()

# plot the std deviation as a transparent range at each training set size
plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1, color="r")
plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.1, color="g")

# plot the average training and test score lines at each training set size
plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training score")
plt.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation score")

# sizes the window for readability and displays the plot
# shows error from 0 to 1.1
#plt.ylim(-.1,1.1)
print('RED = Training Data')
print('GREEN = Cross Validation Data')
plt.show()

#%%
param_range=[5,10,15,20,25]

train_scores, test_scores = validation_curve(modelLR, trainX, trainY, cv=5, n_jobs=-1, verbose=2,
                                              param_name="C", param_range=param_range, scoring=custScoreBrier)

#%%
#Custom Brier Scoring
def xg_Brier(y: np.ndarray, t: xgboost.DMatrix):
    t = t.get_label()
    return "Brier", float(brier_score_loss(t, y))

#%%
#Set and train the XGB model
modelXGB = xgboost.XGBClassifier(learning_rate=0.1, max_depth=3, n_estimators=630, n_jobs=-1,
                                booster='gbtree'
                                )

# MD=5 NE=300:  .11___
# MD=3 NE=630:  .1117

#LONG TIME STABLE MODEL
# modelXGB = xgboost.XGBClassifier(learning_rate=0.1, max_depth=10, n_estimators=90, n_jobs=-1,
#                                 booster='gbtree'
#                                 )
'''Notes:
    1. n_jobs=-1 maximizes CPU utilization
    2. Beware running high max_depth and n_estimators; the shapley estimator in notebook 5
    crashes with high values ("The kernel appears to have died" with no error messages).'''
eval_set = [(trainX, trainY), (testX, testY)]
modelXGB.fit(trainX, trainY, verbose=True, eval_set=eval_set) # eval_metric=['logloss'],

#%%
#Now we'll calibrate the model
runCalibration = True

#%%
if runCalibration:
    calibratorLR = CalibratedClassifierCV(modelLR, cv='prefit', method='isotonic')
    calibratorLR.fit(valX, valY)

#%%
#Now recalculate predictions and print results
if runCalibration:
    predsLRCal = calibratorLR.predict(testX)
    predProbsLRCal = calibratorLR.predict_proba(testX)[:,1]
    #resultsSummary(predsLRCal, predProbsLRCal, testY)
    
    np.save(file=modelDir+'modelLRCalPredProbs.npy', arr=predProbsLRCal)

#%%
if runCalibration:
    calibratorXGB = CalibratedClassifierCV(modelXGB, method='sigmoid', cv='prefit')
    #cv='prefit' fails. Resorting the data didn't work.
    #Also, INCREASING TO cv=10 (FROM 3) GAVE A HUGE IMPROVEMENT.
    
    calibratorXGB.fit(valX, valY)

#%%
#Now recalculate predictions and print results
if runCalibration:
    predsXGBCal = calibratorXGB.predict(testX)
    predProbsXGBCal = calibratorXGB.predict_proba(testX)[:,1]
    #resultsSummary(predsXGBCal, predProbsXGBCal, testY)
    
    np.save(file=modelDir+'modelXGBCalPredProbs.npy', arr=predProbsXGBCal)

#%%
#Save model and any other necessary files
joblib.dump(modelLR, modelDir+'modelLR.model')
joblib.dump(modelXGB, modelDir+'modelXGB.model')

if runCalibration:
    joblib.dump(calibratorLR, modelDir+'calibLR.model')
    joblib.dump(calibratorXGB, modelDir+'calibXGB.model')

# %%
kSize = 100
valX_Kmeans = shap.kmeans(valX, kSize)
explainerLRCal = shap.KernelExplainer(calibratorLR.predict_proba, valX_Kmeans)
explainerXGBCal = shap.KernelExplainer(calibratorXGB.predict_proba, valX_Kmeans)

# %%
joblib.dump(explainerLRCal, modelDir+'modelLRCal.explainer')
joblib.dump(explainerXGBCal, modelDir+'modelXGBCal.explainer')

# %%
