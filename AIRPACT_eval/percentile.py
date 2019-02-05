# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 14:57:34 2019

@author: Jordan
"""
# =============================================================================
# Temp script to determine percentiles
# =============================================================================

# Import libraries
import pandas as pd

# Set directory
inputDir = r'E:/Research/AIRPACT_eval/'
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'

# Load stat functions
exec(open(stat_path).read())

# =============================================================================
# Load data
# =============================================================================
# Read model data
df_mod = pd.read_csv(inputDir + '/model_aqs.csv',sep=',')
df_mod['datetime'] = pd.to_datetime(df_mod['datetime']) #Must convert to date time to merge later
df_mod = df_mod.drop('Unnamed: 0',axis=1)

#Create AQSID Column form state code, county code, and site num
aqsid = pd.read_csv(inputDir+'aqs_sites.csv')
aqsid = aqsid.ix[:,['State Code','County Code','Site Number','Local Site Name','Location Setting']]

aqsid['County Code'] = ["%03d" % n for n in aqsid['County Code'] ]
aqsid['Site Number'] = ["%04d" % n for n in aqsid['Site Number'] ]

aqsid['AQSID'] = (aqsid['State Code']).astype(str) + (aqsid['County Code']).astype(str)+(aqsid['Site Number']).astype(str)

# Must force every cell in AQSID to be a string, otherwise lose most of data
aqsid['AQSID'] = aqsid['AQSID'].astype(str)
df_mod['AQSID'] = df_mod['AQSID'].astype(str)

df_mod = pd.merge(df_mod,aqsid) # Merge df_mod and aqsid so as to add names and such to the datafram

df_mod.loc[:,'O3_mod'] = pd.to_numeric(df_mod.loc[:,'O3_mod'], errors='coerce')
df_mod.loc[:,'PM2.5_mod'] = pd.to_numeric(df_mod.loc[:,'PM2.5_mod'], errors='coerce')

df_mod=df_mod.set_index('datetime')
print('Model data read')
#%%
# =============================================================================
# Manipulate data to be smaller and easier to work with
# =============================================================================
# Resample to get a smaller dataframe
d = df_mod.resample('M', convention='start').mean()

print(d.O3_mod.median())
print(d.O3_mod.quantile(0.5))
print(d.O3_mod.quantile(0.98))










