# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 09:09:58 2018

This process is not fast and should only be done while connected to ethernet

Script based off of Kai Fan
"""

import pandas as pd
import time
#Set state

# =============================================================================
# species = ['o3','pm_FRM/FEM','pm_non_FRM/FEM']
# species_code = ['44201','88101','88502']
# name = ''
# num = 3
# =============================================================================

species = ['Winds','Temperature','Pressure','RH']
species_code = ['WIND','TEMP','PRESS','RH_DP']
name = '_met'
num = 4

def aqs(state,ac):
    AQS={}
    for i in range(0,num):
        print(species[i])
        for j in range(2009,2019):
            dataframename = species[i]+ac+str(j)
            start = time.time()
            print(j)
            temp = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/hourly_'+species_code[i]+'_'+str(j)+'.zip',header=0,sep=',')
            temp['Date GMT'] = pd.to_datetime(temp['Date GMT'])
            temp = temp[(temp['State Name']==state)]  
            AQS[dataframename] = temp
            end = time.time()
            print(round(end-start))       
            dict_AQS = AQS       
 
    AQS_df = pd.concat(dict_AQS)
    AQS_df = AQS_df.drop(['Parameter Code','POC','Datum','Date GMT','Time GMT','MDL','Uncertainty',
                          'Qualifier','Method Type','Method Code','Method Name','Date of Last Change'], axis=1)
   
    AQS_df.to_csv(r'E:/Research/AIRPACT_eval/AQS_data/'+state+'_aqs'+name+'.csv')
    print(state + ' Done')

aqs('Washington','_WA')
aqs('Oregon','_OR')
aqs('Idaho','_ID')
aqs('Montana','_MT')
aqs('California','_CA')
aqs('Utah','_UT')
aqs('Nevada','_NV')
aqs('Canada','_CC')
