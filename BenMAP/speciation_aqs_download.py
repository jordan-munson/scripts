# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 14:34:44 2019

@author: Jordan Munson
"""


import pandas as pd
import time

base_dir = r'E:/Research/Benmap/'

species = ['pm2.5_speciation']# when changing bacl, don't forget to rename the save file line
species_code = ['SPEC']

# =============================================================================
# species = ['PM10_speciation']
# species_code = ['PM10SPEC']
# =============================================================================

#%%
# =============================================================================
# Hourly - takes long time
# =============================================================================
def aqs(begining,ending):
    AQS={}
    for i in range(0,1):
        print(species[i])
        for j in range(begining,ending):
            dataframename = species[i]+str(j)
            start = time.time()
            print(j)
            temp = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/hourly_'+species_code[i]+'_'+str(j)+'.zip',header=0,sep=',')
            temp['Date GMT'] = pd.to_datetime(temp['Date GMT'])
            #temp = temp[(temp['State Name']==state)]  
            AQS[dataframename] = temp
            end = time.time()
            print(round(end-start))       
            dict_AQS = AQS       
 
    AQS_df = pd.concat(dict_AQS)
    AQS_df = AQS_df.drop(['Parameter Code','POC','Datum','Time Local','Date Local','MDL','Uncertainty',
                          'Qualifier','Method Type','Method Code','Method Name','Date of Last Change'], axis=1)
   
    AQS_df.to_csv(base_dir+'AQS_data/speciation/aqs_'+species[0]+'_'+str(begining)+'.csv')

years = [2010,2011,2012,2013,2014,2015,2016,2017,2018] 

for year in years:
    start_year = year
    end_year = start_year+1
    aqs(start_year,end_year)
print('AQS Download done')







