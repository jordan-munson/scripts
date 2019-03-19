# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 08:51:54 2018

@author: Jordan
"""

import matplotlib as mpl
mpl.use('Agg')
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

inputDir          = r'E:\Research\Urbanova_Jordan/'
plotDir           =r'E:\Research\Urbanova_Jordan\output/'
stats_dir = r'E:/Research/scripts/Urbanova/'
urb_path = inputDir +  'Urbanova_ref_site_comparison/Urbanova/'
air_path = inputDir + 'Urbanova_ref_site_comparison/AIRPACT/'


# Set file paths
file_modelled_base = inputDir +'/airnow/merged_2018_Urb_airnow_forecasts.csv'
print(file_modelled_base)
file_airnowsites  = inputDir+ '/aqsid.csv'
#file_airnowsites  = '/data/lar/projects/Urbanova/2018/2018040400/POST/CCTM/aqsid.csv' # Hard coded as some aqsid files do not include all site ID's, this one does.
print(file_airnowsites)
exec(open(stats_dir +"statistical_functions.py").read()) 

df_aqsid = pd.read_csv(file_airnowsites, skiprows=[1])

g = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
g.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
g = g.drop(0,1)

col_names_modeled = ['date', 'time', 'site_id', 'pollutant', 'concentration']
col_names_observed= ['datetime', 'site_id', 'O3_AP5_4km', 'PM2.5_AP5_4km', 'O3_obs', 'PM2.5_obs']
df_base_1  = pd.read_csv(file_modelled_base).drop('Unnamed: 0',axis=1) # new method
df_obs_1   = pd.read_csv('http://lar.wsu.edu/R_apps/2018ap5/data/hrly2018.csv', sep=',', names=col_names_observed, skiprows=[0],dtype='unicode')

col_names_observed= ['datetime', 'site_id','CO_AP5_4km', 'NOX_AP5_4km','NO_AP5_4km', 'NO2_AP5_4km','CO_obs', 'NOX_obs','NO_obs','NO2_obs']
df_base_2  = pd.read_csv(file_modelled_base).drop('Unnamed: 0',axis=1) # new method
df_obs_2   = pd.read_csv('http://lar.wsu.edu/R_apps/2018ap5/data/hrly2018_conoxnono2.csv', sep=',', names=col_names_observed, skiprows=[0],dtype='unicode')
df_sites = pd.read_csv(file_airnowsites, skiprows=[1],dtype='unicode') # skip 2nd row which is blank


df_base = pd.merge(df_base_1,df_base_2, how='inner')
df_obs = pd.merge(df_obs_1,df_obs_2,how='inner')
    
df_urb = pd.DataFrame()
species = ['PM2.5', 'OZONE','CO','NO2']
for pollutant in species:
    if pollutant == 'PM2.5':
        abrv = 'PM2.5'
        unit = '($ug/m^3$)'
        y_max = 30
        t_title = 'Daily Mean '+pollutant
        s_title = t_title
    if pollutant == 'OZONE':
        abrv = 'O3'
        unit = '(ppb)'
        y_max = 60
        t_title = ' O3 Max Daily 8-Hour Average'
        s_title = t_title
    if pollutant == 'CO':
        abrv = 'CO'
        unit = '(ppb)'
        y_max = 500
        t_title = 'CO Max Daily 8-Hour Average'
        s_title = t_title  
    if pollutant == 'NO2':
        abrv = 'NO2'
        unit = '(ppb)'
        y_max = 200
        t_title = 'NO2 Max Daily Hour Average'
        s_title = t_title

   
    # extract only abrv data
    df_temp = df_base.loc[df_base['pollutant']==pollutant, df_base.columns]
    # Renames the abrv to concentration
    df_temp.columns = df_temp.columns.str.replace('concentration',abrv+ '_AP5_1.33km')
    
    # convert object to numeric (This is required to plot these columns)
    df_obs[abrv+'_AP5_4km'] = pd.to_numeric(df_obs[abrv+'_AP5_4km'])
    df_temp[abrv+'_AP5_1.33km'] = pd.to_numeric(df_temp[abrv+'_AP5_1.33km'])
    df_obs[abrv+'_obs'] = pd.to_numeric(df_obs[abrv+'_obs'])
    
    df_urb = df_urb.append(df_temp)


# convert datatime colume to time data (This conversion is so slow)
print('Executing datetime conversion, this takes a while')
df_urb['datetime'] = pd.to_datetime(df_urb['date'] + ' ' + df_urb['time'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
df_obs['datetime'] = pd.to_datetime(df_obs['datetime'], infer_datetime_format=True)
print('datetime conversion complete')

#Convert model data to PST from UTC (PST = UTC-8)
df_urb["datetime"] = df_urb["datetime"].apply(lambda x: x - dt.timedelta(hours=8))
df_obs["datetime"] = df_obs["datetime"].apply(lambda x: x - dt.timedelta(hours=8))
df_urb = df_urb.drop('date',axis=1)
df_urb = df_urb.drop('time',axis=1)
# sites which are common between base and Observations
sites_common = set(df_obs['site_id']).intersection(set(df_base['site_id']))


df_obs_mod = pd.merge(df_obs,df_urb, how='outer')
# get rid of rows if abrv base is not available
#df_obs_mod = df_obs_mod[pd.notnull(df_obs_mod[abrv+'_AP5_1.33km'])]


df_com = df_obs_mod.copy() 
#df_com = df_com.dropna(subset = ['pollutant'])
df_com.columns = df_com.columns.str.replace('site_id','AQSID')

df_com = pd.merge(df_com,df_aqsid, how = 'inner')
print('Combined dataframe finished')

# Set plot parameters
mpl.rcParams['font.family'] = 'sans-serif'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 24.0
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

#%%
# create lits to use in calcs of site ids
used_AQSID = list(set(df_com['AQSID']))

stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
stats_com = stats_com.drop(0,1)
lats = []
lons = []

m = Basemap(projection='merc',
              #lat_0=lat, lon_0=lon,
              llcrnrlat=46.9, urcrnrlat=48.5,
              llcrnrlon=-118.7, urcrnrlon=-116,
              area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold

# Calculate stats for each site and add to list
pollutant = ['O3','PM2.5','NO2']
for species in pollutant:
    plt.figure(figsize=(10,11))
#    if species == 'O3':
    unit_list = 'FB (%)'
#    else:
#        unit_list = '$ug/m^3$'
    m.drawcounties()
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    cmap = plt.get_cmap('jet')
    
    #used_AQSID = ['410050004','530090013'] # to test map
    for AQSID in used_AQSID:
        
        #This section selects only data relevant to the aqs site
        d = df_com.loc[df_com['AQSID']==AQSID]
        d=d.reset_index()
        site_nameinfo = d.loc[0,'long_name'] #Gets the longname of the site to title the plot
        
        lat = d.loc[0,'Latitude']
        lon = d.loc[0,'Longitude']
        #lats.append(lat)
        #lons.append(lon)
        
        #site_type = d.loc[0,'Location Setting']
        d=d.ix[:,[species+'_obs',species+'_AP5_1.33km','datetime']]
        #d['date'] = pd.to_datetime(d['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
        d['date'] = d['datetime'] #format="%m/%d/%y %H:%M")
        
        
        #d = d.set_index('datetime') 
        
        #print(species+ ' ' + str(site_nameinfo))
        #Calculate Statistics
        try:
            #Run stats functions
            aq_stats = stats(d, species+'_AP5_1.33km', species+'_obs')
            
                    #Mapping
            x, y = m(lon, lat)
            marker_shape = 'o'
            #marker_color = 'r'
            sp = 3 # Fractional Bias
            spp = 4 # FE # Change this if you want the size to correlate to a different statistic
            size = abs(6*aq_stats[species+'_AP5_1.33km'][spp])
            m.scatter(x, y, marker=marker_shape,c = aq_stats[species+'_AP5_1.33km'][sp], s = size, alpha = 0.7,cmap=cmap)
            print(AQSID,aq_stats[species+'_AP5_1.33km'][sp])
            plt.clim(-100,100)
            #print(aq_stats[species+'_mod'][sp])
        # aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
   
            # Merge stats into single dataframe
            aq_stats.columns = aq_stats.columns.str.replace(species+'_AP5_1.33km', species+' ' + str(site_nameinfo))    
            stats_com = pd.merge(stats_com, aq_stats, how = 'inner', left_index = True, right_index = True)     
            #print('Stats check okay')
            

            
        except (ZeroDivisionError):
            pass
    


    cbticks = True
    cbar = m.colorbar(location='bottom')#,pad="-12%")    # Disable this for the moment
    cbar.set_label(unit_list)
    plt.title(species + ' Fractional Bias/Error Map')
    
    # Circle size chart
    msizes = [0,30,150,300,450,600]
    labels = ['FE (%)',5,25,50,75,100]
    markers = []
    for size,label in zip(msizes,labels):
        markers.append(plt.scatter([],[], s=size, label=label,c='black',alpha = 0.7))
    plt.legend(bbox_to_anchor=(1.0, 1), loc='upper left',handles=markers)    
    
    plt.savefig(inputDir+'/airnow/bias_maps/'+species+'_bias_map.png',  pad_inches=0.1, bbox_inches='tight')
    plt.show()
    plt.close()
end_time = time.time()
print("Run time was %s minutes"%(round((end_time-begin_time)/60)))
print('done')
#stats_com.to_csv(inputDir + 'stats/bias_map_stats.csv')



























