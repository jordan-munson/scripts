# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:17:24 2019

@author: Jordan Munson
"""

import pandas as pd
import os.path

#PC
# =============================================================================
# inputDir = r'E:/Research/Urbanova_Jordan/Urbanova_ref_site_comparison/Urbanova/2018/'
# base_dir = inputDir
# =============================================================================

#AEOLUS
inputDir = '/data/lar/projects/Urbanova/2018/'
base_dir = '/data/lar/users/jmunson/'

date1 = '2018-01-12'
date2 = '2018-12-31'
mydates = pd.date_range(date1, date2, freq='D').tolist()
col_names_modeled = ['date', 'time', 'site_id', 'pollutant', 'concentration']

# read and save first day
df = inputDir+str(20180111)+'00/POST/CCTM/AIRNowSites_'+str(20180111)+'_v5.dat'
df_com  = pd.read_csv(df, header=None, names=col_names_modeled, sep='|',dtype='unicode')

with open(base_dir+'2018_Airnow_Urbanova_Forecasts.dat', 'w') as outfile:
    for date in mydates:
        time = date.strftime('%Y%m%d')
        df = inputDir+str(time)+'00/POST/CCTM/AIRNowSites_'+str(time)+'_v6.dat'
        if os.path.isfile(df):
            print('')
        
        else:
            df = inputDir+str(time)+'00/POST/CCTM/AIRNowSites_'+str(time)+'_v5.dat'
        try:
            df_base  = pd.read_csv(df, header=None, names=col_names_modeled, sep='|',dtype='unicode')
        except:
            continue
        df_com = df_com.append(df_base)

size=df_com.memory_usage(deep=True).sum()
if size < 20000000000:
    df_com.to_csv(base_dir +'merged_2018_Urb_airnow_forecasts.csv')   #Theoretically, this file should be about 1.7 GB for all the data
    print('data saved')
else:
    print('file too large, not saved')
    pass
