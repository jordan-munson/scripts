# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 10:44:28 2019

@author: riptu
"""

# =============================================================================
# format AIRPACT data for BenMAP
# =============================================================================
import pandas as pd

df = pd.read_csv(r'E:\Research\Benmap\output\airpact/2018_BASE_NARA_AIRPACT_benmap_PMIJ_D24HourMean.csv')

df_1 = df.query('136 <= Column < 166')
df_1 = df_1.query('186 <= Row < 216')

# =============================================================================
# df_1 = df.query('136 <= Row < 166')
# df_1 = df_1.query('186 <= Column < 216')
# =============================================================================



#%%
# =============================================================================
# Conversion to 30x30
# =============================================================================
# =============================================================================
# df_2 = pd.DataFrame()
# df_3 = pd.DataFrame()
# 
# Column = []
# Row = []
# for i in range(1,31):
#     for x in range(1,31):
#         Column.append(x)
#         Row.append(i)
# df_1['Column'] = Row
# df_1['Row'] = Column
# 
#     
#     
#     
# df_1.to_csv(r'E:\Research\Benmap\output\airpact/2018_30x30_BASE_NARA_AIRPACT_benmap_PMIJ_D24HourMean.csv',index=False)
# =============================================================================
    
#%%
# =============================================================================
# Make grid of zeros to compare against   
# =============================================================================
for value,aqi in zip([6,23.75,45.45,102.95,200.4,425.45],['good','moderate','usg','unhealthy','very_unhealthy','hazardous']):
    #df_1 = pd.read_csv(r'E:\Research\Benmap\output\Urbanova/2018_BASE_NARA_benmap_PMIJ_D24HourMean.csv')
    df_1=df
    empty = []
    #Blank value cell
    for x in range(0,365):
        if x == 364:
            empty.append(value)
        else:
            empty.append(value)
    empty = str(empty)
    
    Column = []
    Row = []
    for i in range(1,286):
        for x in range(1,259):
            Column.append(x)
            Row.append(i)
    df_1['Column'] = Row
    df_1['Row'] = Column
    
    df_1['Values'] = empty[1:-1]
        
        
    df_1.to_csv(r'E:\Research\Benmap\output\airpact/pm_aqi_'+aqi+'_AIRPACT_domain.csv',index=False)
    
    
    
    
    
    