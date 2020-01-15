# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:47:35 2019

@author: riptu
"""

import matplotlib as mpl
#mpl.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

starttime = time.time()
begin_time = time.time()


# =============================================================================
# #Set directorys
# =============================================================================
inputDir = r'E:/Research/AIRPACT_eval/'
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'
ben_path = r'E:/Research/scripts/AIRPACT_eval/meteorology/Met_functions_for_Ben.py'

exec(open(stat_path).read())

# =============================================================================
# # Set plot parameters
# =============================================================================
mpl.rcParams['font.family'] = 'arial'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 10 # 10 for paper. 28 for presentations
mpl.rcParams['xtick.major.size']  = 10
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['xtick.minor.size']  = 5
mpl.rcParams['xtick.minor.width'] = 1
mpl.rcParams['ytick.major.size']  = 10
mpl.rcParams['ytick.major.width'] = 2
mpl.rcParams['ytick.minor.size']  = 5
mpl.rcParams['ytick.minor.width'] = 1
mpl.rcParams['ytick.direction']   = 'in'
mpl.rcParams['xtick.direction']   = 'in'

# =============================================================================
# # load data
# =============================================================================
df_com = pd.read_csv(inputDir+'AQS_data/df_com_aplong.csv').drop('Unnamed: 0', axis=1)
df_com.loc[:,'O3_mod'] = pd.to_numeric(df_com.loc[:,'O3_mod'], errors='coerce')
df_com.loc[:,'PM2.5_mod'] = pd.to_numeric(df_com.loc[:,'PM2.5_mod'], errors='coerce')
df_com.loc[:,'O3_obs'] = pd.to_numeric(df_com.loc[:,'O3_obs'], errors='coerce')
df_com.loc[:,'PM2.5_obs'] = pd.to_numeric(df_com.loc[:,'PM2.5_obs'], errors='coerce')
df_com['datetime'] = pd.to_datetime(df_com['datetime'])
print('Data loading section done')

stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
stats_com = stats_com.drop(0,1)

versions = ['AP3','AP4','AP5']
pollutant = ['PM2.5','O3']

#%%
# =============================================================================
# Calc DMA8 and DAily ave
# =============================================================================
for species in pollutant:
    x = df_com.copy()
    x = x.set_index('datetime')
    dbc = pd.DataFrame()
    
    if species == 'O3':       
        x = x.resample('H').mean()
        avg_8hr_o3 = x.rolling(8,min_periods=6).mean()
        times = avg_8hr_o3.index.values - pd.Timedelta('8h')
        avg_8hr_o3.index.values[:] = times
        
        avg_8hr_o3['date'] = avg_8hr_o3.index.strftime('%H')
        intervals = ['00','01','02','03','04','05','06','24'] # remove these hours as per EPA regulation
        for interval in intervals:
            avg_8hr_o3 = avg_8hr_o3[~avg_8hr_o3.date.str.contains(interval)]
            
        df_ozone = avg_8hr_o3.resample('D').max().drop(['date','PM2.5_obs','PM2.5_mod'],axis=1)
        
        #dbc = dbc.append(x1.groupby(x1.index.day).mean())
        #db = dbc.dropna()
        
        #db['datetime'] = dates
        #df_ozone = db.set_index('datetime')
        
    else:
        #df_pm = x.groupby(x.index.day).mean()

        #df_pm['datetime'] = dates
        #df_pm = df_pm.set_index('datetime')
        df_pm = x.resample('D', convention='start').mean().drop(['O3_obs','O3_mod'],axis=1)
#%%
# =============================================================================
#         Do AQI calculations
# =============================================================================
# AQI determination
df_ozone['O3_mod_AQI'] = df_ozone['O3_mod'].map(lambda x: "Good" if x<=54 else "Moderate" if 54<x<=70 else "USG" if 70<x<=85 else "Unhealthy" if 85<x<=105 else "Very_Unhealthy" if 105<x<=200 else "Hazardous" if x>200 else "")
df_ozone['O3_obs_AQI'] = df_ozone['O3_obs'].map(lambda x: "Good" if x<=54 else "Moderate" if 54<x<=70 else "USG" if 70<x<=85 else "Unhealthy" if 85<x<=105 else "Very_Unhealthy" if 105<x<=200 else "Hazardous" if x>200 else "")

df_pm['PM2.5_mod_AQI'] = df_pm['PM2.5_mod'].map(lambda x: "Good" if x<=12 else "Moderate" if 12<x<=35.4 else "USG" if 35.4<x<=55.4 else "Unhealthy" if 55.4<x<=150.4 else "Very_Unhealthy" if 150.4<x<=250.4 else "Hazardous" if x>250.4 else "")
df_pm['PM2.5_obs_AQI'] = df_pm['PM2.5_obs'].map(lambda x: "Good" if x<=12 else "Moderate" if 12<x<=35.4 else "USG" if 35.4<x<=55.4 else "Unhealthy" if 55.4<x<=150.4 else "Very_Unhealthy" if 150.4<x<=250.4 else "Hazardous" if x>250.4 else "")

# set a value of 1,2,3,4,5 along with the aqi so as to plot them
df_ozone['O3_mod_AQI#'] = df_ozone['O3_mod'].map(lambda x: 1 if x<=54 else 2 if 54<x<=70 else 3 if 70<x<=85 else 4 if 85<x<=105 else 5 if 105<x<=200 else 6 if x>200 else "")
df_ozone['O3_obs_AQI#'] = df_ozone['O3_obs'].map(lambda x: 1 if x<=54 else 2 if 54<x<=70 else 3 if 70<x<=85 else 4 if 85<x<=105 else 5 if 105<x<=200 else 6 if x>200 else "")

df_pm['PM2.5_mod_AQI#'] = pd.to_numeric(df_pm['PM2.5_mod']).map(lambda x: 1 if x<=12 else 2 if 12<x<=35.4 else 3 if 35.4<x<=55.4 else 4 if 55.4<x<=150.4 else 5 if 150.4<x<=250.4 else 6 if x>250.4 else 0)
df_pm['PM2.5_obs_AQI#'] = pd.to_numeric(df_pm['PM2.5_obs']).map(lambda x: 1 if x<=12 else 2 if 12<x<=35.4 else 3 if 35.4<x<=55.4 else 4 if 55.4<x<=150.4 else 5 if 150.4<x<=250.4 else 6 if x>250.4 else 0)
 
      # try to assign values for the contingency table
df_pm['comb'] = df_pm['PM2.5_mod_AQI'] + df_pm['PM2.5_obs_AQI'] # combine

# =============================================================================
# PM aqi
# =============================================================================
# Determines "a", or the amount of agreements
a = sum(np.where(df_pm['PM2.5_mod_AQI'] == df_pm['PM2.5_obs_AQI'],1,0))

# Determines "b", or the amount of false alarms
b=0
for aqi in ['Moderate','USG','Unhealthy','Very_Unhealthy','Hazardous']:
    b1 = sum(np.where((df_pm['PM2.5_obs_AQI'] == 'Good') & (df_pm['PM2.5_mod_AQI'] == aqi),1,0))
    b = b+b1

for aqi in ['USG','Unhealthy','Very_Unhealthy','Hazardous']:
    b1 = sum(np.where((df_pm['PM2.5_obs_AQI'] == 'Moderate') & (df_pm['PM2.5_mod_AQI'] == aqi),1,0))
    b = b+b1

for aqi in ['Unhealthy','Very_Unhealthy','Hazardous']:
    b1 = sum(np.where((df_pm['PM2.5_obs_AQI'] == 'USG') & (df_pm['PM2.5_mod_AQI'] == aqi),1,0))
    b = b+b1

for aqi in ['Very_Unhealthy','Hazardous']:
    b1 = sum(np.where((df_pm['PM2.5_obs_AQI'] == 'Unhealthy') & (df_pm['PM2.5_mod_AQI'] == aqi),1,0))
    b = b+b1
  
for aqi in ['Hazardous']:
    b1 = sum(np.where((df_pm['PM2.5_obs_AQI'] == 'Very_Unhealthy') & (df_pm['PM2.5_mod_AQI'] == aqi),1,0))
    b = b+b1

# Determines "c", or the amount of false negatives
c=0
for aqi in ['Moderate','USG','Unhealthy','Very_Unhealthy','Hazardous']:
    c1 = sum(np.where((df_pm['PM2.5_mod_AQI'] == 'Good') & (df_pm['PM2.5_obs_AQI'] == aqi),1,0))
    c = c+c1

for aqi in ['USG','Unhealthy','Very_Unhealthy','Hazardous']:
    c1 = sum(np.where((df_pm['PM2.5_mod_AQI'] == 'Moderate') & (df_pm['PM2.5_obs_AQI'] == aqi),1,0))
    c = c+c1

for aqi in ['Unhealthy','Very_Unhealthy','Hazardous']:
    c1 = sum(np.where((df_pm['PM2.5_mod_AQI'] == 'USG') & (df_pm['PM2.5_obs_AQI'] == aqi),1,0))
    c = c+c1

for aqi in ['Very_Unhealthy','Hazardous']:
    c1 = sum(np.where((df_pm['PM2.5_mod_AQI'] == 'Unhealthy') & (df_pm['PM2.5_obs_AQI'] == aqi),1,0))
    c = c+c1
  
for aqi in ['Hazardous']:
    c1 = sum(np.where((df_pm['PM2.5_mod_AQI'] == 'Very_Unhealthy') & (df_pm['PM2.5_obs_AQI'] == aqi),1,0))
    c = c+c1
    
print(len(df_pm))
print(a+b+c) # The difference of 50 is the result of a missing 50 days of model data. Nothing to worry about.

# =============================================================================
#  Ozone aqi
# =============================================================================
# Determines "a", or the amount of agreements
a_ozone = sum(np.where(df_ozone['O3_mod_AQI'] == df_ozone['O3_obs_AQI'],1,0))

# Determines "b", or the amount of false alarms
b_ozone=0
for aqi in ['Moderate','USG','Unhealthy','Very_Unhealthy','Hazardous']:
    b1 = sum(np.where((df_ozone['O3_obs_AQI'] == 'Good') & (df_ozone['O3_mod_AQI'] == aqi),1,0))
    b_ozone = b_ozone+b1

for aqi in ['USG','Unhealthy','Very_Unhealthy','Hazardous']:
    b1 = sum(np.where((df_ozone['O3_obs_AQI'] == 'Moderate') & (df_ozone['O3_mod_AQI'] == aqi),1,0))
    b_ozone = b_ozone+b1

for aqi in ['Unhealthy','Very_Unhealthy','Hazardous']:
    b1 = sum(np.where((df_ozone['O3_obs_AQI'] == 'USG') & (df_ozone['O3_mod_AQI'] == aqi),1,0))
    b_ozone = b_ozone+b1

for aqi in ['Very_Unhealthy','Hazardous']:
    b1 = sum(np.where((df_ozone['O3_obs_AQI'] == 'Unhealthy') & (df_ozone['O3_mod_AQI'] == aqi),1,0))
    b_ozone = b_ozone+b1
  
for aqi in ['Hazardous']:
    b1 = sum(np.where((df_ozone['O3_obs_AQI'] == 'Very_Unhealthy') & (df_ozone['O3_mod_AQI'] == aqi),1,0))
    b_ozone = b_ozone+b1

# Determines "c", or the amount of false negatives
c_ozone=0
for aqi in ['Moderate','USG','Unhealthy','Very_Unhealthy','Hazardous']:
    c1 = sum(np.where((df_ozone['O3_mod_AQI'] == 'Good') & (df_ozone['O3_obs_AQI'] == aqi),1,0))
    c_ozone = c_ozone+c1

for aqi in ['USG','Unhealthy','Very_Unhealthy','Hazardous']:
    c1 = sum(np.where((df_ozone['O3_mod_AQI'] == 'Moderate') & (df_ozone['O3_obs_AQI'] == aqi),1,0))
    c_ozone = c_ozone+c1

for aqi in ['Unhealthy','Very_Unhealthy','Hazardous']:
    c1 = sum(np.where((df_ozone['O3_mod_AQI'] == 'USG') & (df_ozone['O3_obs_AQI'] == aqi),1,0))
    c_ozone = c_ozone+c1

for aqi in ['Very_Unhealthy','Hazardous']:
    c1 = sum(np.where((df_ozone['O3_mod_AQI'] == 'Unhealthy') & (df_ozone['O3_obs_AQI'] == aqi),1,0))
    c_ozone = c_ozone+c1
  
for aqi in ['Hazardous']:
    c1 = sum(np.where((df_ozone['O3_mod_AQI'] == 'Very_Unhealthy') & (df_ozone['O3_obs_AQI'] == aqi),1,0))
    c_ozone = c_ozone+c1
    
print(len(df_pm))
print(a+b+c) # The difference of 50 is the result of a missing 50 days of model data. Nothing to worry about.
#%%
# =============================================================================
# Combine contingency and
# =============================================================================
rounder = 3

for species in pollutant:
    contingency = pd.DataFrame([0,0,0])

    if species == 'O3':
        df = df_ozone
    else:
        df = df_pm
    for version in versions:
        if version == 'AP3':
            start_date = '2009-01-01'
            end_date = '2012-12-31'
        if version == 'AP4':
            start_date = '2013-01-01'
            end_date = '2015-12-31'
        if version == 'AP5':
            start_date = '2016-01-01'
            end_date = '2018-12-31'
            
        mask = (df.index > start_date) & (df.index <= end_date)
        d=df.loc[mask]
        print(len(d))
        # plot AQI values
        #d.plot(y=['PM2.5_mod_AQI#','PM2.5_obs_AQI#'],figsize = (8,8),kind='kde',xlim=(0,5))#,ylim=(0,5)
                  
        # Determines "a", or the amount of agreements
        a = sum(np.where(d[species+'_mod_AQI'] == d[species+'_obs_AQI'],1,0))
        
        # Determines "b", or the amount of false alarms
        b=0
        for aqi in ['Moderate','USG','Unhealthy','Very_Unhealthy','Hazardous']:
            b1 = sum(np.where((d[species+'_obs_AQI'] == 'Good') & (d[species+'_mod_AQI'] == aqi),1,0))
            b = b+b1
        
        for aqi in ['USG','Unhealthy','Very_Unhealthy','Hazardous']:
            b1 = sum(np.where((d[species+'_obs_AQI'] == 'Moderate') & (d[species+'_mod_AQI'] == aqi),1,0))
            b = b+b1
        
        for aqi in ['Unhealthy','Very_Unhealthy','Hazardous']:
            b1 = sum(np.where((d[species+'_obs_AQI'] == 'USG') & (d[species+'_mod_AQI'] == aqi),1,0))
            b = b+b1
        
        for aqi in ['Very_Unhealthy','Hazardous']:
            b1 = sum(np.where((d[species+'_obs_AQI'] == 'Unhealthy') & (d[species+'_mod_AQI'] == aqi),1,0))
            b = b+b1
          
        for aqi in ['Hazardous']:
            b1 = sum(np.where((d[species+'_obs_AQI'] == 'Very_Unhealthy') & (d[species+'_mod_AQI'] == aqi),1,0))
            b = b+b1
        
        # Determines "c", or the amount of false negatives
        c=0
        for aqi in ['Moderate','USG','Unhealthy','Very_Unhealthy','Hazardous']:
            c1 = sum(np.where((d[species+'_mod_AQI'] == 'Good') & (d[species+'_obs_AQI'] == aqi),1,0))
            c = c+c1
        
        for aqi in ['USG','Unhealthy','Very_Unhealthy','Hazardous']:
            c1 = sum(np.where((d[species+'_mod_AQI'] == 'Moderate') & (d[species+'_obs_AQI'] == aqi),1,0))
            c = c+c1
        
        for aqi in ['Unhealthy','Very_Unhealthy','Hazardous']:
            c1 = sum(np.where((d[species+'_mod_AQI'] == 'USG') & (d[species+'_obs_AQI'] == aqi),1,0))
            c = c+c1
        
        for aqi in ['Very_Unhealthy','Hazardous']:
            c1 = sum(np.where((d[species+'_mod_AQI'] == 'Unhealthy') & (d[species+'_obs_AQI'] == aqi),1,0))
            c = c+c1
          
        for aqi in ['Hazardous']:
            c1 = sum(np.where((d[species+'_mod_AQI'] == 'Very_Unhealthy') & (d[species+'_obs_AQI'] == aqi),1,0))
            c = c+c1
        cont = pd.DataFrame([a,b,c],columns=[version])
        contingency = pd.merge(contingency,cont, left_index = True, right_index = True)
    contingency = contingency.drop(0,axis=1)
    
    if species == 'O3':
        contingency_aqi_ozone = contingency.T.rename(columns={0:'a',1:'b',2:'c'})
        table_ozone = pd.DataFrame()
        table_ozone['BIAS'] = round((contingency_aqi_ozone['a'] + contingency_aqi_ozone['b'])/(contingency_aqi_ozone['a']+contingency_aqi_ozone['c']),rounder) # Perfect score is one
        table_ozone['FAR'] = round(contingency_aqi_ozone['b']/(contingency_aqi_ozone['a']+contingency_aqi_ozone['b']),rounder) # Perfect score is one
        table_ozone['POD'] = round(contingency_aqi_ozone['a']/(contingency_aqi_ozone['a']+contingency_aqi_ozone['c']),rounder) # Perfect score is one
        table_ozone = table_ozone.T
    else:
        contingency_aqi_pm = contingency.T.rename(columns={0:'a',1:'b',2:'c'})   
        table_pm = pd.DataFrame()
        table_pm['BIAS'] = round((contingency_aqi_pm['a'] + contingency_aqi_pm['b'])/(contingency_aqi_pm['a']+contingency_aqi_pm['c']),rounder) # Perfect score is one
        table_pm['FAR'] = round(contingency_aqi_pm['b']/(contingency_aqi_pm['a']+contingency_aqi_pm['b']),rounder) # Perfect score is one
        table_pm['POD'] = round(contingency_aqi_pm['a']/(contingency_aqi_pm['a']+contingency_aqi_pm['c']),rounder) # Perfect score is one
        table_pm = table_pm.T
contingency_aqi_pm = contingency_aqi_pm.T
contingency_aqi_ozone = contingency_aqi_ozone.T
#%%
# =============================================================================
# Forecast evaluation metrics
# =============================================================================
# =============================================================================
# table = pd.DataFrame()
# 
# # Contingency table
# table['BIAS'] = round((contingency_aqi['a'] + contingency_aqi['b'])/(contingency_aqi['a']+contingency_aqi['c']),2) # Perfect score is one
# table['FAR'] = round(contingency_aqi['a']/(contingency_aqi['a']+contingency_aqi['b']),2) # Perfect score is one
# table['POD'] = round(contingency_aqi['a']/(contingency_aqi['a']+contingency_aqi['c']),2) # Perfect score is one
# 
# 
# =============================================================================



#%%
# =============================================================================
# EPA standards section
# =============================================================================

for species in pollutant:
    contingency = pd.DataFrame([0,0,0])
    if species =='O3':
        level = 27 # from https://www.epa.gov/sites/production/files/2015-10/documents/20151001_air_quality_index_updates.pdf
        df = df_ozone
    else:
        level = 6 # Point that AQ goes from Good to moderate
        df = df_pm
    for version in versions:
        if version == 'AP3':
            start_date = '2009-01-01'
            end_date = '2012-12-31'
        if version == 'AP4':
            start_date = '2013-01-01'
            end_date = '2015-12-31'
        if version == 'AP5':
            start_date = '2016-01-01'
            end_date = '2018-12-31'
            
        mask = (df.index > start_date) & (df.index <= end_date)
        d=df.loc[mask]
        print(len(d))
        # plot AQI values
        #d.plot(y=['PM2.5_mod_AQI#','PM2.5_obs_AQI#'],figsize = (8,8),kind='kde',xlim=(0,5))#,ylim=(0,5)
                  
        # Determines "a", or the amount of agreements
        a = sum(np.where((d[species+'_mod'] <level) &  (d[species+'_obs'] <level),1,0))
        
        # Determines "b", or the amount of false alarms
        b = sum(np.where((d[species+'_mod'] >=level) & (d[species+'_obs'] <level),1,0))
        # C is false negatives
        c = sum(np.where((d[species+'_mod'] <level) & (d[species+'_obs'] >=level),1,0))
        cont = pd.DataFrame([a,b,c],columns=[version])
        contingency = pd.merge(contingency,cont, left_index = True, right_index = True)
    contingency = contingency.drop(0,axis=1)
    contingency_epa = contingency.T.rename(columns={0:'a',1:'b',2:'c'})  
    
    if species == 'O3':
        table_ozone_epa = pd.DataFrame()
        table_ozone_epa['BIAS'] = round((contingency_epa['a'] + contingency_epa['b'])/(contingency_epa['a']+contingency_epa['c']),rounder) # Perfect score is one
        table_ozone_epa['FAR'] = round(contingency_epa['b']/(contingency_epa['a']+contingency_epa['b']),rounder) # Perfect score is one
        table_ozone_epa['POD'] = round(contingency_epa['a']/(contingency_epa['a']+contingency_epa['c']),rounder) # Perfect score is one
        table_ozone_epa = table_ozone_epa.T
        table_ozone_epa = contingency_epa.rename(columns={'a':'Hits','b':'False Alarms','c':'Misses'}).T.append(table_ozone_epa)
    else:
        table_pm_epa = pd.DataFrame()
        table_pm_epa['BIAS'] = round((contingency_epa['a'] + contingency_epa['b'])/(contingency_epa['a']+contingency_epa['c']),rounder) # Perfect score is one
        table_pm_epa['FAR'] = round(contingency_epa['b']/(contingency_epa['a']+contingency_epa['b']),rounder) # Perfect score is one
        table_pm_epa['POD'] = round(contingency_epa['a']/(contingency_epa['a']+contingency_epa['c']),rounder) # Perfect score is one
        table_pm_epa = table_pm_epa.T
        table_pm_epa = contingency_epa.rename(columns={'a':'Hits','b':'False Alarms','c':'Misses'}).T.append(table_pm_epa)
        
#%%
for species in pollutant:
    print(species)
    if species =='O3':
        df = df_ozone
    else:
        df = df_pm
    for version in versions:
        if version == 'AP3':
            start_date = '2009-01-01'
            end_date = '2012-12-31'
        if version == 'AP4':
            start_date = '2013-01-01'
            end_date = '2015-12-31'
        if version == 'AP5':
            start_date = '2016-01-01'
            end_date = '2018-12-31'
            
        mask = (df.index > start_date) & (df.index <= end_date)
        d=df.loc[mask]
        
        d_good = d.loc[d[species+'_obs_AQI#'] == 1]
        d_good = d_good[species+'_obs_AQI#'].sum()
        
        d_moderate = d.loc[d[species+'_obs_AQI#'] == 2]
        d_moderate = d_moderate[species+'_obs_AQI#'].sum()
                                
        d_usg = d.loc[d[species+'_obs_AQI#'] == 3]
        d_usg = d_usg[species+'_obs_AQI#'].sum()    
                                
        print(d_good,d_moderate, d_usg)










