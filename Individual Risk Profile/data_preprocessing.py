#%%
import os
import zipfile

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import OpioidDataPrep as odp

#%%
features = [#DEMOGRAPHICS
              'IRSEX', #(Gender):  Subtract 1 from this field to make it 0=Male, 1=Female
              'EDUHIGHCAT', #(Highest Education)
              'AGE2', #(Age): Scale and center
    
              #ALCOHOL
              'IRALCRC', #(Alcohol Recency): Straight One Hot
              'IRALCFY', #(Alcohol Frequency Past Year):  Bin
              'CABINGEVR', #(Ever binge drank):  Recode then bin
              'IRALCAGE', #(First time used alcohol): Bin

              #DRUGS + ALCOHOL
              'TXYRRECVD2', #(Ever alcohol/drug treatment, past yr): No action required (already binary, 0 and 1)
              'TXEVRRCVD2', #(Ever alcohol/drug treatment, lifetime): No action required (already binary, 0 and 1)

              'IRCIGRC', #(Tobacco Recency, incl. Never):  Straight One Hot
              'CIGAGE', #(Tobacco Use Daily):  Bin
              'TOBYR', #(Used any tobacco product in past year (cigar, cigarette, etc.))
              'FUCIG18', #(Used cigarettes before 18): Subtract 1
              
              #WEED
              'IRMJRC', #(Weed recency): Straight One Hot
              'IRMJFY', #(Weed days in past year):  Bin
              'FUMJ18', #(First used weed prior to age 18): Subtract 1
    
              #Hard Drugs
              'IRCOCRC', #(Cocaine recency):  Straight One Hot
              'IRCRKRC', #(Crack recency):  Straight One Hot
              'IRHERRC', #(Heroine recency):  Straight One Hot
              'IRHALLUCREC', #(Hallucinogen recency):  Straight One Hot    
              'IRLSDRC', #(LSD recency):  Straight One Hot
              'IRECSTMOREC', #(Ecstacy recency):  Straight One Hot
              'IRINHALREC', #(Inhalant recency):  Straight One Hot
              'IRMETHAMREC', #(Meth recency):  Straight One Hot

              #DEPRESSION
              'ADDPREV', #(Several days of depression): One Hot
              'ADDSCEV', #(Several days of discouraged about life): One Hot
    
              ##OTHER
              'BOOKED', #(Ever arrested & booked): Recode + One Hot
                      
              #OUTCOME VARIABLE    
              'MISUSE',
             ]

#%%
#Read in all survey data from 2015-2020
data_2015 = pd.read_csv('data/raw/NSDUH-2015-DS0001-bndl-data-tsv.zip', compression='zip', sep='\t')
data_2016 = pd.read_csv('data/raw/NSDUH-2016-DS0001-bndl-data-tsv.zip', compression='zip', sep='\t')
data_2017 = pd.read_csv('data/raw/NSDUH-2017-DS0001-bndl-data-tsv.zip', compression='zip', sep='\t')
data_2018 = pd.read_csv('data/raw/NSDUH-2018-DS0001-bndl-data-tsv.zip', compression='zip', sep='\t')
data_2019 = pd.read_csv('data/raw/NSDUH-2019-DS0001-bndl-data-tsv.zip', compression='zip', sep='\t')
data_2020 = pd.read_csv('data/raw/NSDUH-2020-DS0001-bndl-data-tsv.zip', compression='zip', sep='\t')

# %%
data_2015['MISUSE'] = np.where(data_2015['PNRNMREC'].isin([1, 2, 8]), 1, 0)
data_2016['MISUSE'] = np.where(data_2016['PNRNMREC'].isin([1, 2, 8]), 1, 0)
data_2017['MISUSE'] = np.where(data_2017['PNRNMREC'].isin([1, 2, 8]), 1, 0)
data_2018['MISUSE'] = np.where(data_2018['PNRNMREC'].isin([1, 2, 8]), 1, 0)
data_2019['MISUSE'] = np.where(data_2019['PNRNMREC'].isin([1, 2, 8]), 1, 0)
data_2020['MISUSE'] = np.where(data_2020['PNRNMREC'].isin([1, 2, 8]), 1, 0)

#%%
data_2018['FUCIG18'] = np.where(data_2018['CIGTRY']<18, 1, 0)
data_2019['FUCIG18'] = np.where(data_2019['CIGTRY']<18, 1, 0)
data_2020['FUCIG18'] = np.where(data_2020['CIGTRY']<18, 1, 0)

#%%
data_2018['FUMJ18'] = np.where(data_2018['MJAGE']<18, 1, 0)
data_2019['FUMJ18'] = np.where(data_2019['MJAGE']<18, 1, 0)
data_2020['FUMJ18'] = np.where(data_2020['MJAGE']<18, 1, 0)

# %%
data_2015 = data_2015[features]
data_2016 = data_2016[features]
data_2017 = data_2017[features]
data_2018 = data_2018[features]
data_2019 = data_2019[features]
data_2020 = data_2020[features]

# %%
data = pd.concat([data_2015, data_2016, data_2017, data_2018, data_2019, data_2020])

#%%
data = odp.preprocess(data)

# %%
data.to_csv('data/processed/processed.csv', index=False)
