# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 12:15:21 2018

@author: riptu
"""

import pandas as pd

inputdir = r'E:\Research\AIRPACT_eval\meteorology/'
#inputdir = '/data/lar/users/jmunson/longterm_airpact/'

df_airpact = pd.read_csv(inputdir+'df_airpact.csv').drop(['Unnamed: 0','lat','lon'],axis=1)
df_obs = pd.read_csv(inputdir+'df_obs.csv').drop(['Unnamed: 0','Local Site Name'],axis=1).rename(columns={'datetime':'DateTime'})
df_aqsid = pd.read_csv(inputdir+'aqsid_waorid.csv').drop(['Unnamed: 0','County Code','State Code','Site Number','Local Site Name'],axis=1)

print('Dataframes read')

df_airpact=pd.merge(df_airpact,df_aqsid,how='outer')
df_airpact = df_airpact.dropna(subset=['Location Setting'])

df_all = pd.merge(df_airpact,df_obs,how ='outer',left_index=True,right_index=True, on = ['DateTime','AQS_ID'])

df_all.to_csv(inputdir+'/df_combined_aqs.csv')



#%%