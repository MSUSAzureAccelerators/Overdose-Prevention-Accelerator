#%%
# Load packages
import numpy as np
import pandas as pd
import csv
import scipy
import pickle
from CUSP_functions import generate_featureset
from CUSP_functions import evaluator

# for random forest
from sklearn.ensemble import RandomForestRegressor
# make_score is for incorportating the lc20 as gridsearch eval metric
from sklearn.metrics import r2_score,  make_scorer
# kfold is for feature selection; predefined split is for gridsearch (cuz it's faster)
from sklearn.model_selection import GridSearchCV, KFold, PredefinedSplit, cross_val_score
# pipeline is for building pipeline to feed into gridsearch
from sklearn.pipeline import Pipeline

# set display max so that you can see as many rows/cols
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

#%%
all_periods = [20162, 20171, 20172, 20181, 20182, 20191, 20192, 20201]

# because we will do t-1 and t-2 features to predict t overdose rank, so we start with 20171 ~ 20161 & 20162 features
first_round_train_val_periods = [20171, 20172, 20181, 20182, 20191, 20192]
first_round_test_period = [20201]

second_round_train_val_periods = [20171, 20172, 20181, 20182, 20191]
second_round_test_period = [20192]

t_minus2 = all_periods[0:-1]
t_minus1 = all_periods[1:]
t_transform = dict(zip(t_minus2, t_minus1))

#%%
# read in the dataset
# full = pd.read_csv("data/dataset_v4_0715_084729_A_rank____shift_min.csv")
full = generate_featureset('A', 'rank', 'csv', scale = None, roll_avg = None, pca = None, shift = True, train_periods = all_periods, test_periods = [], ties = 'min', geo = False, spatial = False)

#%%
# prep the rf main df
full_rf = full.copy()

# read the same df for prep t-2 features
# in that case y of 20171 ~ x of 20162 and 20161
# so our periods for modeling would be 20171 - 20201
# in the prepared dataset, if one record is 20171, bc it's shifted, the features are already 20162's
# therefore, we need to pull 20161 features from record marked as 20162
full_2 = full.copy()
# the features pulled through this process are actually 20162 - 20191
full_t_previous = full_2[full_2.full_period.isin(t_minus2)]
# add suffix for those features to distinguish them
full_t_previous = full_t_previous.add_suffix('_t-2')
# only keep from geoid_t-1 to overdose_rank_t-1 - actually this drops the year_t-1 and period_t-1 columns
full_t_previous = full_t_previous.loc[:, 'geoid_t-2':'overdose_rank_t-2']
# rename the geoid and full_period column, and we will join the t-1 df to main df using those two columns as keys
full_t_previous = full_t_previous.rename(columns = {'geoid_t-2': 'geoid', 'full_period_t-2': 'full_period'})
# manually shift period by + 1 aka. the original record marked as 20162, which means x is from 20161, will be shifted as 20171
# in that way, the record marked as 20171 will have the features from 20161 (this is the t-2)
full_t_previous['full_period'].replace(t_transform, inplace = True)

# join to the main df
full_rf = full_rf.merge(full_t_previous, on = ['geoid', 'full_period'], how = 'left')
full_rf = full_rf[full.full_period.isin(t_minus1)]

#%%
# set y variable as the normalized rank
full_rf['y'] = full_rf['overdose_rank']
# create index based on period and geoid
full_rf['period_geoid'] = full_rf['full_period'].astype(str) + '_' +  full_rf['geoid'].astype(str)
# this is going to be passed into the custom scorer as the "signal" - period and geoid
full_rf.set_index('period_geoid', inplace = True)
# to make sure each period's record stay together for the kfold
full_rf.sort_index(ascending = True, inplace = True)

#%%
pipeline = Pipeline([('RandomForest', RandomForestRegressor(random_state = 1234))])
# put all the parameters that you would like to go through in gridsearch 
parameters = {'RandomForest__max_features': ['auto', 10, 11],
              'RandomForest__max_depth': range(3, 8),
              'RandomForest__min_samples_leaf': [20, 50, 100],
              'RandomForest__n_estimators': [30, 40, 50]}


# here it's the custimzed scorer - we need to wrap it up for feeding into gridsearch
def lc20_scorer(y_true, y_pred): 
    # y, y_pred
    # pull the period from the validation set
    period = int(list(y_true.index)[0][0:5])
    # pull geoids from the validation set
    geoid = [int(idx[6:]) for idx in list(y_true.index)]
     # call the eval function here to get the LC 20% capture
    result, rest = evaluator(np.array(y_pred), np.array(geoid), period, target_var = 'rank', ties = 'min', simple = True)
    return result.loc['20%', 'LC']

lc20 = make_scorer(lc20_scorer, greater_is_better = True)

#%%
include = ['PDMP_total_persons_receiving_buprenorphine_at_least_7_days',
'ACS_units_occupied_renter_pct_t-2',
'EMS_total_count_t-2',
'ACS_pop_hisp_pct',
'PDMP_total_days_supply_buprenorphine_t-2',
'PDMP_total_persons_receiving_buprenorphine_at_least_180_days',
'EMS_total_count',
'ACS_pop_hisp_white_alone_pct',
'PDMP_total_mme_dispensed',
'ACS_hh_med_income_t-2',
'ACS_pop_hisp_pct_t-2',
'PDMP_total_persons_initiating_buprenorphine_t-2',
'ACS_pop_hisp_other_alone_pct_t-2',
'segregation_classification_Predominantly Non-White_t-2',
'ACS_pop_hisp_other_alone_pct',
'PDMP_total_patients',
'PDMP_total_persons_with_multiple_prescribers_or_dispensers_t-2',
'ACS_pop_density_t-2',
'PDMP_total_persons_initiating_buprenorphine',
'ACS_pop_never_married_pct',
'ACS_pop_inc_poverty_line_ratio_0_2',
'ACS_hh_med_income',
'EMS_age_35_44_t-2',
'ACS_pop_hisp_white_alone_pct_t-2',
'ACS_pop_inc_poverty_line_ratio_2_over_t-2']

#%%
# here it's looking through the top k features, and for each feature set, we do gridsearch twice to test on 20201 and 20192
# we will use the feature set that has the best performances on average, and parameters accordingly

# get the list of top k featues 
#include = include
# first round of test: test 20201, train on 20162-20191 & val on 20192
# preparing the train and val data frame for gridsearch
X_train_val = full_rf[full_rf.full_period.isin(first_round_train_val_periods)].loc[:, full_rf.columns.isin(include)]
y_train_val = full_rf[full_rf.full_period.isin(first_round_train_val_periods)].loc[:, 'y']

# preparing the test data frame
X_test = full_rf[full_rf.full_period.isin(first_round_test_period)].loc[:,  full_rf.columns.isin(include)]
y_test_geoid = full_rf[full_rf.full_period.isin(first_round_test_period)].loc[:, 'geoid']
y_test = full_rf[full_rf.full_period.isin(first_round_test_period)].loc[:, 'y']

# use the predefined split to set 20171 - 20191 as training set (-1) and 20192 as validation set (1)
split_index = [-1 if int(x[0:5]) < first_round_train_val_periods[-1] else 1 for x in X_train_val.index]
cv_pd = PredefinedSplit(split_index)
# gridsearch with lc20 as the scorer
grid_search = GridSearchCV(pipeline, parameters, verbose = 2,  cv = cv_pd, n_jobs = 8, scoring = lc20)
# get the best model using training with 20171 - 20191 and validating on 20192
grid_search.fit(X_train_val, y_train_val)
# predict on 20201
y_pred = grid_search.predict(X_test)
# get the lc20 eval on 20201
test_result_df, other = evaluator(np.array(y_pred), np.array(y_test_geoid), first_round_test_period[0], target_var = 'rank', ties = 'min', simple = True)
test_result = test_result_df.loc['20%', 'LC']
# print the result
print("first test: " +  str(grid_search.best_score_) + ", " + str(test_result) +  ", params:" + str(grid_search.best_params_))

#second round of test: test 20192, train on 20162-20182 & val on 20191
# preparing the train and val data frame for gridsearch
X_train_val = full_rf[full_rf.full_period.isin(second_round_train_val_periods)].loc[:, full_rf.columns.isin(include)]
y_train_val = full_rf[full_rf.full_period.isin(second_round_train_val_periods)].loc[:, 'y']
# preparing the test data frame for gridsearch
X_test = full_rf[full_rf.full_period.isin(second_round_test_period)].loc[:,  full_rf.columns.isin(include)]
y_test_geoid = full_rf[full_rf.full_period.isin(second_round_test_period)].loc[:, 'geoid']
y_test = full_rf[full_rf.full_period.isin(second_round_test_period)].loc[:, 'y']

# use the predefined split to set 20171 - 20182 as training set (-1) and 20191 as validation set (1)
split_index = [-1 if int(x[0:5]) < second_round_train_val_periods[-1] else 1 for x in X_train_val.index]
cv_pd = PredefinedSplit(split_index)

# gridsearch with lc20 as the scorer
grid_search = GridSearchCV(pipeline, parameters, verbose = 2,  cv = cv_pd, n_jobs = 8, scoring = lc20)

# get the best model using training with 20171 - 20182 and validating on 20191
grid_search.fit(X_train_val, y_train_val)
# predict on 20192
y_pred = grid_search.predict(X_test)
# get the lc20 eval on 20192
test_result_2_df, other = evaluator(np.array(y_pred), np.array(y_test_geoid), second_round_test_period[0], target_var = 'rank', ties = 'min', simple = True)
test_result_2 = test_result_2_df.loc['20%', 'LC']
# print the result
print("second test: " +   str(grid_search.best_score_) + ", " + str(test_result_2) +  ", params:" + str(grid_search.best_params_))
print("avg test = " + str((test_result + test_result_2)/2))

#%%
# this is the first round of test - best model

X_train_val = full_rf[full_rf.full_period.isin(first_round_train_val_periods)].loc[:, full_rf.columns.isin(include)]
y_train_val = full_rf[full_rf.full_period.isin(first_round_train_val_periods)].loc[:, 'y']

# preparing the test data frame
X_test = full_rf[full_rf.full_period.isin(first_round_test_period)].loc[:,  full_rf.columns.isin(include)]
y_test_geoid = full_rf[full_rf.full_period.isin(first_round_test_period)].loc[:, 'geoid']
y_test = full_rf[full_rf.full_period.isin(first_round_test_period)].loc[:, 'y']

reg = RandomForestRegressor(max_depth=3, max_features=10,
                     min_samples_leaf=20, n_estimators=30,
                     random_state=1234)
reg.fit(X_train_val, y_train_val)

y_pred = reg.predict(X_test)

test_result_df, other = evaluator(np.array(y_pred), np.array(y_test_geoid), first_round_test_period[0], target_var = 'rank', ties = 'min', simple = True)
test_result = test_result_df.loc['20%', 'LC']

#%%
# this is the second round of test - best model

X_train_val = full_rf[full_rf.full_period.isin(second_round_train_val_periods)].loc[:, full_rf.columns.isin(include)]
y_train_val = full_rf[full_rf.full_period.isin(second_round_train_val_periods)].loc[:, 'y']

# preparing the test data frame
X_test = full_rf[full_rf.full_period.isin(second_round_test_period)].loc[:,  full_rf.columns.isin(include)]
y_test_geoid = full_rf[full_rf.full_period.isin(second_round_test_period)].loc[:, 'geoid']
y_test = full_rf[full_rf.full_period.isin(second_round_test_period)].loc[:, 'y']

reg = RandomForestRegressor(max_depth=3, max_features=11,
                     min_samples_leaf=20, n_estimators=30,
                     random_state=1234)
reg.fit(X_train_val, y_train_val)

y_pred = reg.predict(X_test)

test_result_df, other = evaluator(np.array(y_pred), np.array(y_test_geoid), second_round_test_period[0], target_var = 'rank', ties = 'min', simple = True)
test_result = test_result_df.loc['20%', 'LC']
