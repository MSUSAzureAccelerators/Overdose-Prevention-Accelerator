# ## USER INPUTS

# are you generating the standard featureset (A) or a custom featureset (B)? 
# feature_set = A or B
# 
# do you want your target variable to be overdose_count, perc_totaloverdoses, normalized_rank?
# target_variable = count, perc, or rank
# 
# do you want to include a rolling average of overdose deaths for each CBG?
# roll_avg = True
# 
# do you want PCA?
# pca = True
# 
# how do you want to deal with rank ties?
# 'min' - what we've been using so far
# 'average' - what Daniel thinks is best
# note this MUST match how you've created your dataset
# 
# Do you want to scale the data (using sklearn StandardScaler)?
# scale = True
# 
# do you want to shift the target variable back one period?
# shift = true
# 
# do you want csv or pkl?
# form = csv or pkl
# 
# desired time periods by default
# time_periods = [20161, 20162, 20171, 20172, 20181, 20182]
# 
# do you want to aggregate spatial neighbors? 
# If so, indicate which features to aggregate
# 'all' - all features
# 'no_ACS' - all features excluding ACS
# 'target' - just the target variable

# ## Pre-loaded Featuresets

# There are some preloaded datasets:
#     
#     A: all ~120 features - do not modify
#     B: custom featureset ! this is the one you modify if you want to test including/excluding features
#     C: 75 RFE features chosen by sklearn on overdose COUNTS - probably best used when predicting counts
#     D: 75 RFE features chosen by sklearn on overdose RANKs - probably best used predicting ranks

# In[4]:


def generate_featureset(feature_set, target_variable, form, 
                        train_periods = [20162, 20171, 20172, 20181, 20182, 20191, 20192], test_periods = [20201], scale = False, 
                        roll_avg = True, pca = False, shift = True, kernel = 'poly', ties = 'min', geo = False,  
                        spatial = False):
    # Load packages
    import pandas as pd
    import time
    from datetime import datetime
    import numpy as np
    
    all_time_periods = [20161, 20162, 20171, 20172, 20181, 20182, 20191, 20192, 20201]
    #all_time_periods.reverse()
    time_periods = train_periods + test_periods
    
    #indicate which col to use in indicator_xwalk
    include_flag = feature_set + '_include_flag'
    
    #generate datetime_string
    now = datetime.now()
    datetime_str = str(now.month).zfill(2) + str(now.day).zfill(2) + "_" + str(now.hour + 2).zfill(2) + str(now.minute).zfill(2) + str(now.second).zfill(2)

    #create tags for output dataset
    avg_tag = ''
    scale_tag = ''
    pca_tag = ''
    shift_tag = ''
    
    if roll_avg:
        avg_tag = 'roll'
        
    if scale == 'standardize':
        scale_tag = 'stand'
    if scale == 'normalize':
        scale_tag = 'norm'
    
    if pca == 'pca':
        pca_tag = 'pca'
        #create an error in the event user has not chosen standardize
        class PCA_std_error(Exception):
            '''raised when user has asked for PCA but has not specified standardization'''
            pass
        try:
            if scale != 'standardize':
                raise PCA_std_error()
        except PCA_std_error:
            print("PCA requires standardization, which user has not selected.")
            raise PCA_std_error()
            
    if pca == 'kpca':
        pca_tag = 'kpca'
        #create an error in the event user has not chosen standardize
        class PCA_std_error(Exception):
            '''raised when user has asked for PCA but has not specified standardization'''
            pass
        try:
            if scale != 'standardize':
                raise PCA_std_error()
        except PCA_std_error:
            print("PCA requires standardization, which user has not selected.")
            raise PCA_std_error()
                
    
    if shift:
        shift_tag = 'shift'
        
    if target_variable == 'count':
        target = 'overdose_count'
    if target_variable == 'perc':
        target = 'overdose_perc'
    if target_variable == 'rank':
        target = 'overdose_rank'
    
    #create file suffix
    suffix = datetime_str + '_' + feature_set + '_' + target_variable + '_' + scale_tag + '_' + pca_tag + '_' + avg_tag + '_' + shift_tag + '_' + ties
    
    # Read in indicator xwalk - go to the csv file to edit the include flag - there's full indicator meaning in the csv
    # SUDORS, PDMP, EMS, ACS and LANDUSE indicators can be filtered using "startswith" - added prefix and cleaned up names already
    # year, peroid, geoid are the ones without prefix
    indicator_xwalk = pd.read_csv("E:\\PROVIDENT_shared\\NYU_SHARE\Data\\CUSP_Full_Data\\indicator_xwalk_0702.csv",
                                 usecols = ['original_name', 'clean_name', include_flag])

    indicator_xwalk = indicator_xwalk[indicator_xwalk[include_flag] == True]

    indicator_rename_dict = dict(zip(indicator_xwalk.original_name, indicator_xwalk.clean_name))
    
    # Read in the full MASTER data frame
    # note: 2020 ACS data is all 0 right now
    master = pd.read_csv("E:\\PROVIDENT_shared\\master_datasets\\PROVIDENT_Master_V.4_prepared_by_CEP_2021.07.02.csv",
                        usecols = list(indicator_xwalk.original_name))
    master.rename(columns = indicator_rename_dict, inplace = True)
    
    #drop unincorporated CBGs
    unwanted_cbgs = [440099901000, 440099902000, 440059900000, 440050401031]
    master = master.loc[ ~master['geoid'].isin(unwanted_cbgs), :]
    

    # merge the master file with additinal ACS indicators
    additional = pd.read_csv("E:\\PROVIDENT_shared\\NYU_SHARE\Data\\CUSP_Full_Data\\additional.csv")
    additional = additional[['geoid', 'year', 'ACS_pop_no_health_insurance_pct', 'ACS_hh_public_assistance_pct']]
    # no ACS 2020 data to join on, leaving them as 0
    full = master.merge(additional, on = ['geoid', 'year'], how = 'left').fillna(0)
    
    #merge with urban/non-urban and equity classifications
    classifications = pd.read_csv("E:\\PROVIDENT_shared\\NYU_SHARE\Data\\CUSP_Full_Data\\equity_classification_06.13.2021.csv", usecols =['GEOID', 'urban_classification', 'poverty_classification', 'segregation_classification'])
    classifications = classifications.rename(columns = {'GEOID':'geoid'})
    
    seg = pd.get_dummies(classifications[['segregation_classification']])
    cols = list(seg.columns)
    cols.remove('segregation_classification_Unclassified')
    classifications[cols] = seg[cols]
    classifications = classifications.drop(columns = ['segregation_classification'])

    urban = pd.get_dummies(classifications[['urban_classification']])
    cols = list(urban.columns)
    cols.remove('urban_classification_Unclassified')
    classifications[cols] = urban[cols]
    classifications = classifications.drop(columns = ['urban_classification'])

    poverty = pd.get_dummies(classifications[['poverty_classification']])
    cols = list(poverty.columns)
    cols.remove('poverty_classification_Unclassified')
    classifications[cols] = poverty[cols]
    classifications = classifications.drop(columns = ['poverty_classification'])
    
    full = full.merge(classifications, on = ['geoid'], how='left')

    #create a combined col for time period
    full['full_period'] = full.year * 10 + full.period
    full = full.drop(columns = ['period', 'year'])
    full = full.loc[ full['full_period'].isin(all_time_periods), :]
    
    #some columns have all zeros for the entire time period, just remove them
    full = full.loc[:, full.sum(axis=0) != 0.]
    
     ## change target to percent of total
    if target_variable == 'rank':
        full['overdose_rank'] = full.groupby('full_period')['overdose_count'].rank(pct = True, method = ties)
        
    if target_variable == 'perc':
        #calculate percentile for each period
        annual_totals = full.groupby('full_period')['overdose_count'].sum()
        full['overdose_perc'] = ''

        for index, row in full.iterrows():
            try:
                full.loc[index, 'overdose_perc'] = np.round(row['overdose_count'] / float(annual_totals[row['full_period']]),6)
            except:
                full.loc[index , 'overdose_perc'] = 0.
        full['overdose_perc'] = full['overdose_perc'].astype(float)
    
    #add coordinates
    if geo:
        # import coordinates
        coords = pd.read_csv('E:/PROVIDENT_shared/NYU_SHARE/Data/CUSP_Full_Data/coords_RI_cbg.csv')
        coords = coords.loc[ ~coords['geoid'].isin(unwanted_cbgs), :]
        full = full.merge(coords, on = 'geoid', how = 'left')
    

    ## shift ######################################
    if shift:
        full[target + '_t-1'] = full[target]
        iteration = 0
        for period in all_time_periods[:-1]: #loop over all of the time periods and assign the next period's target to the current, ignore final time period
            full.loc[ full['full_period'] == period, target] = full.loc[ full['full_period'] == all_time_periods[iteration+1], target].values
            iteration += 1
            
    ## add in a rolling average mean overdose deaths for each CBG 
    if roll_avg:
        full_lite = full[['full_period', 'geoid', 'overdose_count']].pivot(index = 'geoid', columns = 'full_period', values = 'overdose_count')
        full_lite.reset_index(inplace = True)
        full_lite['ma_20161'] = 0
        full_lite['ma_20162'] = full_lite[20161] #will match 20161
        full_lite['ma_20171'] = (full_lite[20161]+full_lite[20162])/2
        full_lite['ma_20172'] = (full_lite[20162]+full_lite[20171])/2
        full_lite['ma_20181'] = (full_lite[20171]+full_lite[20172])/2
        full_lite['ma_20182'] = (full_lite[20172]+full_lite[20181])/2
        full_lite['ma_20191'] = (full_lite[20181]+full_lite[20182])/2
        full_lite['ma_20192'] = (full_lite[20182]+full_lite[20191])/2
        full_lite['ma_20201'] = (full_lite[20191]+full_lite[20192])/2

        full_lite = full_lite[['geoid', 'ma_20161', 'ma_20162', 'ma_20171', 'ma_20172', 'ma_20181', 'ma_20182', 'ma_20191', 'ma_20192', 'ma_20201']].melt(id_vars = 'geoid')
        full_lite.full_period = full_lite.full_period.str.replace('ma_', '').astype(int)
        full_lite.rename(columns = {'value': 'moving_average_count'}, inplace = True)

        #merge with entire dataset
        full = full.merge(full_lite, how = 'left', on = ['geoid', 'full_period'])
        
    ## spatial aggregation######
    if spatial:
        full_cols = list(full.columns)

        #columns we definitely do not want to aggregate
        non_feature_cols = ['full_period', 'geoid', target, 'x', 'y'] 
        #we ignore the target, so there are no issues with feeding it future data
        
        

        #indicate which features you want in neighborhood
        if spatial == 'all':
            feature_cols = [x for x in full_cols if x not in non_feature_cols]
        elif spatial == 'no_ACS':
            feature_cols = [x for x in full_cols if x[:3] is not 'ACS']
            feature_cols = [x for x in feature_cols if x not in non_feature_cols]
        elif (spatial == 'target') & (shift == True):
            feature_cols = [target + '_t-1']
        elif spatial == 'target':
            feature_cols = [target]

        #create new columns with prefix
        prefix = 'neighbor_'
        neigh_cols = [prefix + x for x in feature_cols]

        #add new neighbor columns to dataframe
        full[neigh_cols] = pd.DataFrame([[0.] * len(neigh_cols)], index = full.index)

        geoids = full['geoid'].unique() #get unique geoids
        
        #import distance matrix
        dist = pd.read_pickle('E:/PROVIDENT_shared/NYU_SHARE/Data/CUSP_Full_Data/dist_matrix_norm_inverse.pkl')
        
        #loop through geoids
        for geoid in geoids:
            #create weight dictionary based on current geoids
            weights = dist[geoid].to_dict()
            full['weights'] = full['geoid'].map(weights) #map to column of full, this gets rewritte with each iteration
            neigh_data = full[feature_cols].multiply(full['weights'], axis = 'index') #multiply data by weights, geoid self weight is 0, so geoid's own data is ignored
            neigh_data['full_period'] = full['full_period'] #copy over full period col
            neigh_avg = neigh_data.groupby(by = 'full_period').sum() #groupby full period and sum to give weighted average
            geoid_df = full.loc[ (full['geoid'] == geoid) & (full['full_period'].isin(neigh_avg.index)), neigh_cols]
            neigh_avg = neigh_avg.set_index(geoid_df.index)
            geoid_df[neigh_cols] = neigh_avg[feature_cols]
            full.loc[full['geoid'] == geoid, neigh_cols] = geoid_df[neigh_cols].astype(float)
            full[neigh_cols] = full[neigh_cols].astype(float)

        full = full.drop(columns = ['weights'])
    
    #rename full_period to correct name if shifted
    if shift:
        rename_dict = {20161: 20162, 20162: 20171, 20171: 20172, 20172: 20181, 20181:20182, 20182: 20191, 20191:20192, 20192:20201, 20201:20202}
        full['full_period'].replace(rename_dict, inplace=True)
    else:
        ACS_feature_cols = [x for x in list(full.columns) if 'ACS' in x]
        for period in [20201]: # this is only for temp use beacuse the 20201 data does not have new ACS data, so we just copy 20192 ACS. This doesn't really matter because we never train on 20201 features
            full.loc[ full['full_period'] == period, ACS_feature_cols] = full.loc[ full['full_period'] == 20192, ACS_feature_cols].values
        
        
    # remove undesired time periods
    full = full[ full['full_period'].isin(time_periods)]
    
    
        
    ## standardize/normalize

    if scale == 'standardize':
        from sklearn.preprocessing import StandardScaler
        from pickle import dump
        
        scaler = StandardScaler()
        if target_variable == 'rank' or target_variable == 'perc':
            unwanted_cols = ['geoid', 'full_period', target, 'overdose_count']
        else:
            unwanted_cols = ['geoid', 'full_period', target]
        #data = full.loc[ :, ~full.columns.isin(unwanted_cols)] # we don't want to scale geoid
        #data_cols = list(data.columns)
        #separated_cols = full[unwanted_cols]
        #separated_cols.reset_index(inplace = True)
        
        #fit transform training data without unwanted columns and replace existing training
        full.loc[ full['full_period'].isin(train_periods), ~full.columns.isin(unwanted_cols)] = scaler.fit_transform(
            full.loc[ full['full_period'].isin(train_periods), ~full.columns.isin(unwanted_cols)])
        
        #transform test data
        full.loc[ full['full_period'].isin(test_periods), ~full.columns.isin(unwanted_cols)] = scaler.transform(
            full.loc[ full['full_period'].isin(test_periods), ~full.columns.isin(unwanted_cols)])
        
        #data_scaled = pd.DataFrame(data_scaled, columns = data_cols)
        #full = pd.concat((separated_cols, data_scaled), axis=1)
        #full = full.drop(columns = 'index')
        scaler_name = 'scaler_' + datetime_str + '.pkl'
        dump(scaler, open('data/' + scaler_name, 'wb')) #save the scaler so you can unscale down the line
        
    if scale == 'normalize':
        from sklearn.preprocessing import MinMaxScaler
        from pickle import dump
        
        scaler = MinMaxScaler()
        unwanted_cols = ['geoid', 'full_period', 'year', target]
        #data = full.loc[ :, ~full.columns.isin(unwanted_cols)] # we don't want to scale geoid
        #data_cols = list(data.columns)
        #separated_cols = full[unwanted_cols]
        #separated_cols.reset_index(inplace = True)
        
        #fit transform training data without unwanted columns and replace existing training
        full.loc[ full['full_period'].isin(train_periods), ~full.columns.isin(unwanted_cols)] = scaler.fit_transform(
            full.loc[ full['full_period'].isin(train_periods), ~full.columns.isin(unwanted_cols)])
        
        #transform test data
        full.loc[ full['full_period'].isin(test_periods), ~full.columns.isin(unwanted_cols)] = scaler.transform(
            full.loc[ full['full_period'].isin(test_periods), ~full.columns.isin(unwanted_cols)])
        
        #data_scaled = pd.DataFrame(data_scaled, columns = data_cols)
        #full = pd.concat((separated_cols, data_scaled), axis=1)
        #full = full.drop(columns = 'index')
        scaler_name = 'scaler_' + datetime_str + '.pkl'
        dump(scaler, open('data/' + scaler_name, 'wb')) #save the scaler so you can unscale down the line
        
    ## PCA
    if pca == 'pca':
        from sklearn.decomposition import PCA
        import matplotlib.pyplot as plt
        
        #data = full.loc[ :, ~full.columns.isin(unwanted_cols)] # we don't want to scale geoid
        #separated_cols = full[unwanted_cols]
        #separated_cols.reset_index(inplace = True)
        
        PCA = PCA()
        #fit transform training data without unwanted columns and replace existing training
        full.loc[ full['full_period'].isin(train_periods), ~full.columns.isin(unwanted_cols)] = PCA.fit_transform(
            full.loc[ full['full_period'].isin(train_periods), ~full.columns.isin(unwanted_cols)])
        
        #transform test data
        full.loc[ full['full_period'].isin(test_periods), ~full.columns.isin(unwanted_cols)] = PCA.transform(
            full.loc[ full['full_period'].isin(test_periods), ~full.columns.isin(unwanted_cols)])
        
        #rename columns
        cols = list(full.columns)
        remaining_cols = [col for col in cols if col not in unwanted_cols]
        new_cols = unwanted_cols + remaining_cols
        full = full[new_cols] #reorder so that our identifying and target columns are first
        PC_cols = [ 'pc'+ str(n) for n in range(1, len(remaining_cols)+1)]
        full.columns = unwanted_cols + PC_cols
        
        eigenvalues = PCA.explained_variance_ratio_
        n=50
        import matplotlib.pyplot as plt
        plt.bar(np.arange(n), eigenvalues[:n].cumsum())
        plt.ylabel('explained variance')
        plt.xlabel('# pcs')
        plt.show()
        
    ##KPCA
    if pca == 'kpca':
        print
        from sklearn.decomposition import KernelPCA
        import matplotlib.pyplot as plt
        
        #data = full.loc[ :, ~full.columns.isin(unwanted_cols)] # we don't want to scale geoid or label or 
        #separated_cols = full[unwanted_cols]
        #separated_cols.reset_index(inplace = True)
        total_dimensions = len(full.columns) - len(unwanted_cols)
        PCA = KernelPCA(n_components = total_dimensions, kernel = kernel, degree = 8) #lets only retain as many components as there are dimensions
        
        #fit transform training data without unwanted columns and replace existing training
        full.loc[ full['full_period'].isin(train_periods), ~full.columns.isin(unwanted_cols)] = PCA.fit_transform(
            full.loc[ full['full_period'].isin(train_periods), ~full.columns.isin(unwanted_cols)])

        #transform test data

        full.loc[ full['full_period'].isin(test_periods), ~full.columns.isin(unwanted_cols)] = PCA.transform(
            full.loc[ full['full_period'].isin(test_periods), ~full.columns.isin(unwanted_cols)])

        #rename columns
        cols = list(full.columns)
        remaining_cols = [col for col in cols if col not in unwanted_cols]
        new_cols = unwanted_cols + remaining_cols
        full = full[new_cols] #reorder so that our identifying and target columns are first
        PC_cols = [ 'pc'+ str(n) for n in range(1, len(remaining_cols)+1)]
        full.columns = unwanted_cols + PC_cols

        
        explained_variance = np.var(full.loc[ full['full_period'].isin(train_periods), ~full.columns.isin(unwanted_cols)], axis = 0)
        explained_var_ratio = explained_variance / np.sum(explained_variance)
        cum_explained_var = np.cumsum(explained_var_ratio)
        n=50
        import matplotlib.pyplot as plt
        plt.bar(np.arange(n), cum_explained_var[:n])
        plt.ylabel('explained variance')
        plt.xlabel('# pcs')
        plt.show()
    
    ## output

    file_name = 'dataset_v4_' + suffix
    
    if target_variable == 'rank' or target_variable == 'perc':
        try:
            full = full.drop(columns = ['overdose_count'])
        except:
            pass
    
    #create train test label
    full['label'] = ''
    full.loc[ full['full_period'].isin(train_periods), 'label'] = 'train'
    full.loc[ full['full_period'].isin(test_periods), 'label'] = 'test'
    cols = list(full.columns)
    new_cols = [cols[-1]] + cols[:-1]
    full = full[new_cols]
    

    if form == 'csv':
        full.to_csv('data/' + file_name + '.csv',index=False )
        print(file_name + '.csv')
    else:
        import pickle
        full.to_pickle('data/' + file_name + '.pkl')
        print(file_name + '.pkl')
    
    num_features = len(full.columns) - 4 #there are 3 columns that are not features, including the target column
    print('total_features:', num_features)
        
    return full


def evaluator(pred_array, geoid_array, eval_period, target_var = 'rank', ties = 'min', num_periods_predicted = 1, eval_index = 1, simple = False):
    import pandas as pd
    import numpy as np
    import pickle
    from sklearn.metrics import r2_score
    town_dict = pickle.load(open('E:\\PROVIDENT_shared\\NYU_SHARE\\Data\\CUSP_Full_Data\\geo_town_dict.pkl', 'rb')) # geoid and town dict
                              
    #vars
    total_preds = num_periods_predicted * 811
    indexer1 = (eval_index - 1) * 811
    indexer2 = eval_index * 811
    period_to_take = eval_period
    
    df = pd.DataFrame()
    df['prediction'] = pred_array[indexer1 : indexer2]
    df['geoid'] = geoid_array[indexer1 : indexer2]


    ##bring in actual od counts
    # read in the master df to pull the geoid x overdose count
    master = pd.read_csv("E:\\PROVIDENT_shared\\master_datasets\\PROVIDENT_Master_V.4_prepared_by_CEP_2021.07.02.csv",
                        usecols = ['geoid', 'year', 'period', 'all_drug_overdose_count'])
    
    #drop unincorporated CBGs
    unwanted_cbgs = [440099901000, 440099902000, 440059900000, 440050401031]
    master = master.loc[ ~master['geoid'].isin(unwanted_cbgs), :]

    # filter specific years
    master['full_period'] = master.year * 10 + master.period
    master = master[master.full_period == period_to_take]
    # ground truth as a dictionary
    actual_result = dict(zip(master.geoid, master.all_drug_overdose_count))
    df['actual'] = df['geoid'].map(actual_result) #map onto geoids
    
    
    #this is not necessary 
    if target_var == 'rank':
        df['actual_od_rank'] = df['actual'].rank(method = ties, pct = True)
    if target_var == 'perc':
        #calculate percentile for each period
        annual_total = df['actual'].sum()
        df['actual_od_perc'] = df['actual'] / annual_total
    if target_var == 'count':
        #calculate percentile for each period
        df['actual_od_count'] = df['actual']



    #map towns onto geoids
    df['town'] = df['geoid'].map(town_dict)
                              
    #this notebook takes the prediction and ground thruths as arrays. The tensors from pytorch need to be transposed from long to wide
    #transpose shape and rank by predicted ods
    df['pred_global_rank'] = df['prediction'].rank(method = ties, ascending=False) #taking the first prediction. I.e. 2018

    #actual_df = pd.DataFrame(np.transpose(actual.numpy()))
    df['actual_global_rank'] = df['actual'].rank(method = ties, ascending=False)

    #reorder columns so its nice
    cols = list(df.columns)
    new_cols = [cols[1], cols[3], cols[2], cols[0], cols[5], cols[4]]
    df = df[new_cols]

    df = df.sort_values(by='prediction', ascending=True) #sort by highest rank (rank of 1 = highest OD count)

    #rank within towns
    df['pred_town_rank'] = df.groupby('town')['prediction'].rank(ties, ascending=False) #rank within towns

    #output R2 in case user wants to check R2 against what their model produced
    r2 = r2_score(df['actual_od_' + target_var], df['prediction']) #calculate R2
    print(r2)
                 
    def run_scenarios(df):
        thresholds = [0.05, 0.1, 0.15, 0.2] #set our % CBGs desired
        constraints = [0, 1] #set top x CBGs in each town desired (for lightly constrained = 1.)
        evaluation = pd.DataFrame(columns=constraints, index=thresholds) #instantiate df to store evaluation

    
        def capture_func(threshold, constraint):
            # first lets grab the top x CBGs"
            # do this by looping through each town, sorting by town rank and returning the first x entries
            targeted_CBGs = list()
            
            for town in df['town'].unique():
                town_CBGs = df.loc[ df['town'] == town, :].sort_values(by = 'pred_town_rank')['geoid'][:constraint]
                for targeted_CBG in town_CBGs:
                    targeted_CBGs.append(targeted_CBG)
                    
            #targeted_CBGs = list(df.loc[ df['pred_town_rank'] == constraint, 'geoid'].values) #for lightly constrained this 

            #next remove these geoids from the set and take the top x% of CBGs remaining where x = threshold - constraint/811
            remaining_CBGs = df[ ~df['geoid'].isin(targeted_CBGs)].sort_values(by=['pred_global_rank']) #get the remaining unselected CBgs

            num_selected = len(targeted_CBGs) #find how many CBGs we have already targeted with the constraint above


            num_to_select = np.floor((threshold * 815 - num_selected)) #find how many more we need to hit the threshold and round down

            #select additional CBGs based on num_to_select and add to target list
            if num_to_select < 1:
                targeted_CBGs = targeted_CBGs
            else:
                targeted_CBGs += list(remaining_CBGs.iloc[ 0:int(num_to_select), 0]) #the 0 col indexing here is key, since this col must hold the geoids

            
            captured_ods = df.loc[ df['geoid'].isin(targeted_CBGs), 'actual'].sum() #sum the ods captured under targeted CBGs
            performance = captured_ods / df['actual'].sum() #divide by total od count
            return performance, targeted_CBGs
                              
        for constraint in constraints:
            for threshold in thresholds:
                #create column in df for targeted or not
                threshold_col_name = str(threshold * 100)
                if constraint == 1 :
                    constraint_col_name = 'LC'
                else: 
                    constraint_col_name = 'UC'
                col_name = str(constraint_col_name + threshold_col_name)
                df[col_name] = 0
                
                #run eval
                scenario_eval, targeted_CBGs = capture_func(threshold, constraint)
                #add scenario eval to evaluation df
                evaluation.loc[threshold, constraint] = np.round(scenario_eval,3)*100
                #mark columns as targeted or not
                df.loc[ df['geoid'].isin(targeted_CBGs), col_name] = 1

        evaluation = evaluation.rename(columns = {0:'UC', 1:'LC'})
        evaluation['% targeted'] = ['5%', '10%', '15%', '20%']
        evaluation = evaluation.set_index('% targeted')

        return evaluation, df # if you want to output a specific scenario, return results.loc['20%', 'LC'] for example
    if simple == True:
        acc_df, results_df = run_scenarios(df)
        results_df = results_df[['geoid', 'prediction', 'LC20.0']]
        results_df.columns = ['geoid', 'risk', 'LC20']
        return acc_df, results_df
    else:	
        return run_scenarios(df)
		
def lc20_scorer(y_true, y_pred): 
    # y, y_pred
    # pull the period from the validation set
    period = int(list(y_true.index)[0][0:5])
    # pull geoids from the validation set
    geoid = [int(idx[6:]) for idx in list(y_true.index)]
     # call the eval function here to get the LC 20% capture
    result1 = evaluator_scorer(np.array(y_pred), np.array(geoid), val_periods[0], num_periods_predicted = 2, eval_index = 1,target_var = 'rank', ties = 'min')
    result2 = evaluator_scorer(np.array(y_pred), np.array(geoid), val_periods[1], num_periods_predicted = 2, eval_index = 2,target_var = 'rank', ties = 'min')
    return (result1 + result2) / 2
