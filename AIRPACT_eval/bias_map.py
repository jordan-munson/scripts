# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 08:51:54 2018

@author: Jordan
"""

import matplotlib as mpl
#mpl.use('Agg')
import pandas as pd
import matplotlib.dates as mdates
import datetime as dt
import matplotlib.pyplot as plt
import pytz
import numpy as np
import time
from subprocess import check_call 
import os
from datetime import timedelta
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap

starttime = time.time()
begin_time = time.time()

day='01'
month = '04' 
year  = '2018' 

endday = '31'
endmonth='05'
endyear='2018'

#Set directory
inputDir = r'E:/Research/AIRPACT_eval/'
# Open statistics script
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'
ben_path = r'E:/Research/scripts/AIRPACT_eval/meteorology/Met_functions_for_Ben.py'
exec(open(stat_path).read())
#aqsidd = pd.read_csv(r'G:\Research\Urbanova_Jordan\Urbanova_ref_site_comparison/Aqsid.csv')
#aqsidd = aqsidd.drop(['Unnamed: 4','Unnamed: 5','Unnamed: 6','Latitude','Longitude'], axis=1)
#aqsidd = aqsidd.drop([0,0], axis=0)

##############################################################################
# Read AQS data. csv's created from 'AQS_grabbing.py' script, and the model data from the previous lines of code
##############################################################################
# Read model data
df_mod = pd.read_csv(inputDir + '/model_aqs.csv',sep=',')
df_mod['datetime'] = pd.to_datetime(df_mod['datetime']) #Must convert to date time to merge later
df_mod = df_mod.drop('Unnamed: 0',axis=1)

#Create AQSID Column form state code, county code, and site num
aqsid = pd.read_csv(inputDir+'aqs_sites.csv')
aqsid = aqsid.ix[:,['State Code','County Code','Site Number','Local Site Name','Location Setting','Latitude','Longitude']]

aqsid['County Code'] = ["%03d" % n for n in aqsid['County Code'] ]
aqsid['Site Number'] = ["%04d" % n for n in aqsid['Site Number'] ]

aqsid['AQSID'] = (aqsid['State Code']).astype(str) + (aqsid['County Code']).astype(str)+(aqsid['Site Number']).astype(str)

# Must force every cell in AQSID to be a string, otherwise lose most of data
aqsid['AQSID'] = aqsid['AQSID'].astype(str)
df_mod['AQSID'] = df_mod['AQSID'].astype(str)

df_mod = pd.merge(df_mod,aqsid) # Merge df_mod and aqsid so as to add names and such to the datafram

print('Model data read')

# Read AQS data
df_wa = pd.read_csv(inputDir + 'AQS_data/Washington_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_or = pd.read_csv(inputDir + 'AQS_data/Oregon_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_id = pd.read_csv(inputDir + 'AQS_data/Idaho_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
#df_cc = pd.read_csv(inputDir + 'Canada_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )

#  Combine AQS data
df_list = [df_wa,df_or,df_id]
df_obs = pd.concat(df_list)


#Create AQSID Column form state code, county code, and site num
df_obs['County Code'] = ["%03d" % n for n in df_obs['County Code'] ]
df_obs['Site Num'] = ["%04d" % n for n in df_obs['Site Num'] ]

df_obs['AQSID'] = (df_obs['State Code']).astype(str) + (df_obs['County Code']).astype(str)+(df_obs['Site Num']).astype(str)

# Drop columns of data we are not looking at so as to increase the speed of the script
df_obs = df_obs.drop(['Unnamed: 0','Unnamed: 1','State Name','County Name','State Code','County Code','Site Num','Units of Measure'],axis=1)
df_obs = df_obs.rename(columns={'Date Local_Time Local': 'datetime','Parameter Name':'Parameter_Name'})
print('Observed data read and combined')

# Only pulls ozone/pm data
df_obs_o3 = df_obs.loc[df_obs['Parameter_Name']=='Ozone']
df_obs_pm = df_obs.loc[df_obs['Parameter_Name']=='PM2.5 - Local Conditions']
df_obs_pm2 = df_obs.loc[df_obs['Parameter_Name']=='Acceptable PM2.5 AQI & Speciation Mass']
df_obs_pm = pd.concat([df_obs_pm,df_obs_pm2])

df_obs_o3 = df_obs_o3.rename(columns={'Sample Measurement':'O3_obs'})
df_obs_pm = df_obs_pm.rename(columns={'Sample Measurement':'PM2.5_obs'})

df_obs_o3 = df_obs_o3.drop(['Parameter_Name'],axis=1)
df_obs_pm = df_obs_pm.drop(['Parameter_Name'],axis=1)
df_obs = pd.merge(df_obs_o3, df_obs_pm, on =['datetime','AQSID'], how='outer')

df_obs = pd.merge(df_obs,aqsid, how='outer') 
#df_obs = df_obs.drop(['Latitude_x','Latitude_y','Longitude_x','Longitude_y'], axis=1)
  
##############################################################################
# Manipulate obs and mod dataframes to set them up to plot
##############################################################################
#df_com = pd.concat([df_obs,df_mod])

# merge now
print('Merging large dataframes, this may take a while')
#df_com = pd.merge(df_obs_new, df_mod_new, on=['datetime', 'AQSID','long_name'], how='outer')
df_com = pd.merge(df_obs, df_mod, how='outer')

#df_com = pd.concat([df_obs,df_mod])


# Need to convert these to numeric
df_com.loc[:,'O3_mod'] = pd.to_numeric(df_com.loc[:,'O3_mod'], errors='coerce')
df_com.loc[:,'PM2.5_mod'] = pd.to_numeric(df_com.loc[:,'PM2.5_mod'], errors='coerce')
#df_com.loc[:,'AQSID'] = pd.to_numeric(df_com.loc[:,'AQSID'], errors='coerce')

#df_com = df_com.drop(['AQSID_x','AQSID_y'],axis=1)
df_com['datetime'] = pd.to_datetime(df_com['datetime'], infer_datetime_format=True)

#df_com = pd.merge(df_com,aqsid, on=['AQSID','long_name'], how='outer')   
#df_com = df_com.set_index('datetime')

df_com.loc[:,'O3_mod'] = pd.to_numeric(df_com.loc[:,'O3_mod'], errors='coerce')
df_com.loc[:,'PM2.5_mod'] = pd.to_numeric(df_com.loc[:,'PM2.5_mod'], errors='coerce')
df_com.loc[:,'O3_obs'] = pd.to_numeric(df_com.loc[:,'O3_obs'], errors='coerce')
df_com['O3_obs'] = df_com['O3_obs']*1000
df_obs['O3_obs'] = df_obs['O3_obs']*1000
df_com.loc[:,'PM2.5_obs'] = pd.to_numeric(df_com.loc[:,'PM2.5_obs'], errors='coerce')
df_com = df_com.drop(['State Code','County Code','Site Number'],axis=1) # drop unecessary columns
print('Combined dataframe finished')

# Set plot parameters
mpl.rcParams['font.family'] = 'sans-serif'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 20.0
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


df_mod.loc[:,'O3_mod'] = pd.to_numeric(df_mod.loc[:,'O3_mod'], errors='coerce')
df_mod.loc[:,'PM2.5_mod'] = pd.to_numeric(df_mod.loc[:,'PM2.5_mod'], errors='coerce')

df_com = df_com.dropna()
#%%
stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
stats_com = stats_com.drop(0,1)
lats = []
lons = []

m = Basemap(projection='merc',
              #lat_0=lat, lon_0=lon,
              llcrnrlat=40.5, urcrnrlat=49.5,
              llcrnrlon=-125, urcrnrlon=-109,
              area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold

# Calculate stats for each site and add to list
pollutant = ['O3','PM2.5']
for species in pollutant:
    m.drawcounties()
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    for AQSID in list(set(df_com['AQSID'])):

        #This section selects only data relevant to the aqs site
        d = df_com.loc[df_com['AQSID']==AQSID]
        d=d.reset_index()
        site_nameinfo = d.loc[0,'Local Site Name'] #Gets the longname of the site to title the plot
        
        lat = d.loc[0,'Latitude']
        lon = d.loc[0,'Longitude']
        lats.append(lat)
        lons.append(lon)
        
        site_type = d.loc[0,'Location Setting']
        d=d.ix[:,[species+'_obs',species+'_mod','datetime']]
        d['date'] = pd.to_datetime(d['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
        dc = d.groupby(d.date.dt.year)
        #print(dc)
        
        #d = d.set_index('datetime') 
        
        #print(species+ ' ' + str(site_nameinfo))
        #Calculate Statistics
        try:
            #Run stats functions
            aq_stats = stats(d, species+'_mod', species+'_obs')
            
                    #Mapping
            x, y = m(lon, lat)
            marker_shape = 'o'
            marker_color = 'r'
            size = 10*aq_stats[species+'_mod'][3] # Fractional Bias
            m.scatter(x, y, marker=marker_shape,color=marker_color, s = size)

        # aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
   
            # Merge stats into single dataframe
            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', species+' ' + site_nameinfo)    
            stats_com = pd.merge(stats_com, aq_stats, how = 'inner', left_index = True, right_index = True)     
            #print('Stats check okay')
        except (ZeroDivisionError):
            pass
    plt.show()

#stats_com.to_csv(inputDir + 'stats/bias_map_stats.csv')



























