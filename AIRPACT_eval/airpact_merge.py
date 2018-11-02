# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 09:33:24 2018

@author: riptu
"""
import pandas as pd

base_dir = r'E:\Research\AIRPACT_eval/'

co_dir = base_dir + 'All_model-monitor_paired_daily_CO_data.csv'
no2_dir = base_dir + 'All_model-monitor_paired_daily_NO2_data.csv'
o3_dir = base_dir + 'All_model-monitor_paired_daily_O3_data.csv'
pm2p5_dir = base_dir + 'All_model-monitor_paired_daily_PM2.5_data.csv'
pm10_dir = base_dir + 'All_model-monitor_paired_daily_PM10_data.csv'
so2_dir = base_dir + 'All_model-monitor_paired_daily_SO2_data.csv'

co   = pd.read_csv(co_dir, sep=',', dtype='unicode')
no2   = pd.read_csv(no2_dir, sep=',', dtype='unicode')
o3   = pd.read_csv(o3_dir, sep=',', dtype='unicode')
pm2p5   = pd.read_csv(pm2p5_dir, sep=',', dtype='unicode')
pm10   = pd.read_csv(pm10_dir, sep=',', dtype='unicode')
so2   = pd.read_csv(so2_dir, sep=',', dtype='unicode')

frames = [co,no2,o3,pm2p5,pm10,so2]
merged = pd.concat(frames)

col = ("XCell", "YCell", "date", "AP4.PM2.5.Daily_mean_Conc", "AP4.O3.Daily_8hrmax_Conc", "AP4.NO2.Daily_1hrmax_Conc", "AP4.NO2.Daily_mean_Conc", "AP4.SO2.Daily_mean_Conc", "AP4.SO2.Daily_1hrmax_Conc", "AP4.CO.Daily_1hrmax_Conc", "AP4.CO.Daily_8hrmax_Conc", "AP4.SO2.Daily_3hrmax_Conc", "AP4.PM10.Daily_mean_Conc", "Latitude", "Longitude")
merged = merged.reindex_axis(col, axis=1)
merged.loc[~(merged==0).all(axis=1)]
#merged = pd.concat(merged)
merged.to_csv(base_dir + '/All_Criteria_pollutant_obs_2014-2017_Yunha/alldata_4maps.csv',index=False)




