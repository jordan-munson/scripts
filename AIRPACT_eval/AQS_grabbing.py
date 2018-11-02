# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 09:09:58 2018

This process is not fast and should only be done while connected to ethernet

Script based off of Kai Fan
"""

import pandas as pd
import time
#Set state

latlon =  pd.read_csv(r'E:/Research/AIRPACT_eval/All_model-monitor_paired_daily_PM2.5_data.csv')
latlon = latlon.drop('date',axis=1)
latlon = latlon.drop('Parameter.Name',axis=1)
latlon = latlon.drop('Daily_mean_Conc',axis=1)
latlon = latlon.drop('AP4.PM2.5.Daily_mean_Conc',axis=1)

latlon = latlon.dropna()
latlon = latlon.drop_duplicates(subset = 'Sitename')



species = ['o3','pm_FRM/FEM','pm_non_FRM/FEM']
species_code = ['44201','88101','88502']

#species = ['Winds']#,'Temperature','Pressure','RH']
#species_code = ['WIND']#,'TEMP','PRESS','RH_DP']

def aqs(state,ac):
    AQS={}
    for i in range(0,3):
        print(species[i])
        for j in range(2009,2018):
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
   
    
    AQS_df.to_csv(r'E:/Research/AIRPACT_eval/AQS_data/'+state+'_met_aqs.csv')
    print(state + ' Done')

aqs('Washington','_WA')
aqs('Oregon','_OR')
aqs('Idaho','_ID')
aqs('Canada','_CC')









    