# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 21:26:16 2018

@author: riptu
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 5 16:11:19 2018

@author: Benjamin Yang
 - Modified by Jordan Munson for use in longterm evaluation of AIRPACT
"""

############################################
##########     IMPORT MODULES     ##########
############################################
import matplotlib
matplotlib.use('Agg')  # Uncomment this when using in Kamiak/Aeolus
import pandas as pd
import numpy as np
#import time
import datetime
from datetime import timedelta
from netCDF4 import Dataset
import pytz
import os
import Met_functions_for_Ben as met
from convert_MW_date import MWdate_to_datetime
import wrf
import matplotlib.pyplot as plt
from MesoPy import Meso
from matplotlib import dates
import time
starttime = time.time()
begin_time = time.time()

# Set a directory containing python scripts
base_dir = "/data/lar/users/jmunson/longterm_airpact/"
#base_dir = r'E:\Research\AIRPACT_eval\meteorology/'

# set a directory to save output files
outputdir = base_dir + 'outputs/'

# set a directory containing wrfout files
datadir = base_dir + 'linked_days/'
#datadir = r'E:/Research/AIRPACT_eval/meteorology/example_met_days/'

# all the functions are saved in Met_functions_for_Ben.py
exec(open(base_dir +"Met_functions_for_Ben.py").read())
print(base_dir +"Met_functions_for_Ben.py")

#exec(open(base_dir + "/airpact_functions.py").read())

start_year = 2015    #2009
start_month = 1    #5
start_day = 1    #1

end_year = 2018
end_month = 7    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 15    #15
'''
start_year = 2018    #2009
start_month = 1    #5
start_day = 11    #1

end_year = 2018
end_month = 1    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 13    #15
'''
# set start and end date
start = datetime.datetime(start_year, start_month, start_day, hour=0)
end = datetime.datetime(end_year, end_month, end_day, hour=0)

timezone = pytz.timezone("utc")
start = timezone.localize(start)
end = timezone.localize(end)
now=start
# total hours (will be used to filter out stations with missing hour(s))
time_diff = end - start
date_diff =end -start
date_diff =  int(round( date_diff.total_seconds()/60/60/24)) # total hour duration
tot_hours = time_diff.days*24 #+ time_diff.seconds/3600
#print(tot_hours)
date_diff_final = date_diff
print(date_diff)
####################################
#########     AIRPACT     ##########
####################################
if int(start.strftime('%Y%m%d')) < 20160425:
    grid = datadir + start.strftime('%Y%m%d')+'00/MCIP/GRIDCRO2D'
else:
    grid = datadir + start.strftime('%Y%m%d')+'00/MCIP37/GRIDCRO2D'


# open one of wrfout to read coordinate
modeloutputs = []

print(modeloutputs)

# Get accurate number of days
for t in range(0, date_diff):
    
    # Handles missing days
    if os.path.isfile(datadir + now.strftime('%Y%m%d')+'00/MCIP37/METCRO2D') or os.path.isfile(datadir + now.strftime('%Y%m%d')+'00/MCIP/METCRO2D'):
        #Changes day to next
        now += timedelta(hours=24)            
    else:
        date_diff_final = date_diff_final - 1
        #print('adding 24 hours')
        now += timedelta(hours=24)
        
print(date_diff_final)
now=start
'''
for t in range(0, date_diff_final):
    
    # Handles missing days
    if os.path.isfile(datadir + now.strftime('%Y%m%d')+'00/MCIP37/METCRO2D') or os.path.isfile(datadir + now.strftime('%Y%m%d')+'00/MCIP/METCRO2D'):
        # set a directory containing Urbanova data
        #print('Reading ' + now.strftime('%Y%m%d'))
        modeloutputs.append(datadir + now.strftime('%Y%m%d')+'00/MCIP37/METCRO2D')
        #Changes day to next
        now += timedelta(hours=24)            
    else:
        #print('adding 24 hours')
        now += timedelta(hours=24)
'''
if int(start.strftime('%Y%m%d')) < 20160425:  
    modeloutputs =  datadir + start.strftime('%Y%m%d')+'00/MCIP/METCRO2D'
else:
    modeloutputs =  datadir + start.strftime('%Y%m%d')+'00/MCIP37/METCRO2D'
print(int(start.strftime('%Y%m%d')) < 20160425)

# open and read wrfout using netCDF function (Dataset)
if os.path.isfile(modeloutputs):
    nc  = Dataset(modeloutputs, 'r')
    print('reading ', modeloutputs)
else:
    print("no file")
    exit()

# x_dim and y_dim are the x (lon) and y (lat) dimensions of the model
x_dim = len(nc.dimensions['COL'])
y_dim = len(nc.dimensions['ROW'])

# Get a variable (T2) from netCDF file for Basemap
#t_basemap = wrf.getvar(nc, "TEMP2")

nc.close()

# obtain model lat and lon - needed for AQS eval and basemap
latlon = grid
fin0 = Dataset(latlon, 'r')
lat = fin0.variables['LAT'][0,0]
lon = fin0.variables['LON'][0,0]
w = (fin0.NCOLS)*(fin0.XCELL)
h = (fin0.NROWS)*(fin0.YCELL)
lat_0 = fin0.YCENT
lon_0 = fin0.XCENT
fin0.close()

layer=0

#airpact_3d = get_airpact_DF(start, end, layer)



######################################
##########     MESOWEST     ##########  
######################################

# Enter MesoWest token (generate using API key)
m = Meso(token = '23fd1c019ccb4ec3a6946eb3a13c99ad')

# Convert the start and end time to the string format requried by the API
start_t = start.strftime("%Y%m%d%H%M")
end_t = (end - timedelta(hours=1)).strftime("%Y%m%d%H%M")
tz = 'utc'  # This is hard coded for now. Local time could be added later.

# String of some MesoWest variables available from this list:
# https://synopticlabs.org/api/mesonet/variables/
#variables = 'air_temp,pressure,wind_speed,wind_direction,relative_humidity,precip_accum'
variables = 'air_temp,pressure,wind_speed,wind_direction,relative_humidity'

var_list = variables.split(",")

# Bounding box (min lon, min lat, max lon, max lat)
# Lat/lon values taken from UW WRF output
#mw_data = m.timeseries(bbox=[-130.486771, 39.493988, -107.050415, 50.597836], 
#                    start=start_t, end=end_t,vars=var_list,obtimezone=tz)

# Stations in King County in Washington State matching at least one of the 
# variables provided
#mw_data = m.timeseries(state='WA',county='king',start=start_t,end=end_t,vars=var_list,obtimezone=tz)

# Specific stations (Sea-Tac Airport & Pullman-Moscow Airport)
# Return a time series from Aug 28 00z to Sep 9 23z for stations in Washington
#mw_data = m.timeseries(stid=['ksea','kpuw','cumw1'],start=start_t, end=end_t,vars=var_list,obtimezone=tz)

#print(mw_data)

# Make array of integers ("for" loop indices)
#stations = np.arange(0, np.size(mw_data['STATION']))

# Get metadata for all active stations within bounding box (UW WRF domain)
#all_mw_data = m.metadata(bbox=[np.min(lon1), np.min(lat1), np.max(lon1), np.max(lat1)], status='active')
#all_mw_data = m.metadata(state='WA')
#all_mw_data = m.metadata(stid=['ksea','kpuw'])
# All ASOS/AWOS station in WA, OR, ID in MesoWest
# Potential stations: https://www.faa.gov/air_traffic/weather/asos/

all_mw_data = m.metadata(stid=['KOKH','KAWO','KBLI','KPWT','KCLS','KDLS','KDEW',
'KORS','KELN','KEPH','KPAE','KFHR','KHQM','KKLS','KMWH','KOLM','KOMK','KEAT',
'KPSC','KNOW','KCLM','K0S9','KS40','KPUW','KPLU','KUIL','KRNT','KRLD','KBFI',
'KSEA','KSHN','KBVS','KGEG','KSFF','KSMP','K1S5','KTIW','KFCT','KVUO','KALW',
'K2S8','KS52','KYKM','KAST','KUAO','KBKE','KBDN','KBOK','KBNO','KCVO','KPDT',
'KEUG','K6S2','K4S1','KGCD','K3S8','KHRI','K77S','K4S2','KJSY','KLMT','KLGD',
'KLKV','K9S9','KS33','KMMV','KSLE','KMEH','KONP','KOTH','KONO','KHIO','KTTD',
'KPDX','K3S9','KRDM','KMFR','KRBG','KSPB','KSXT','KTMK','KBOI','K65S','KBYI',
'KEUL','KLLJ','KCOE','KDIJ','KSUN','KGIC','KIDA','KJER','KTWF','KLWS','KMYL',
'KMLP','KMAN','KPIH','KRXE','KSMN','KSZT'])

stations = []

# Make list of all station IDs 
for ind in np.arange(0, np.size(all_mw_data['STATION'])):
    stations.append(all_mw_data['STATION'][ind]['STID'])

# Create empty data frames
stats_all = pd.DataFrame() # statistics for each station
df_overall = pd.DataFrame() # data for each variable for each model
stats_overall = pd.DataFrame() # statistics for each variable for each model

# Create empty variable lists
vname_obs = []
vname_1 = []
vlabel = []
mean_obs = []
mean1 = []

x_list = []
y_list = []

iy = pd.DataFrame()
ix = pd.DataFrame()
# setup dataframe for combined
df_met_all = pd.DataFrame(columns=['DateTime','PRSFC','Q2','TEMP2','WDIR10','WSPD10','lat','lon'])

#This first for loop is to create dataframes of the lat/lon coordinates to pull from metcro files
iy = pd.DataFrame()
ix = pd.DataFrame()
# Iterate over dictionary to make time series plots of each variable for each station
print('Creating site list')
for i in stations:
    # Return a time series from Aug 28 00z to Sep 9 23z for each station
    mw_data = m.timeseries(stid=i,start=start_t, end=end_t,vars=var_list,obtimezone=tz)
    
    # Skip station if the data is NoneType
    if mw_data is None:
        continue
    
    # All data for a station
    x = mw_data['STATION'][0]

    # Only keep variables of interest
    all_var = list(x['SENSOR_VARIABLES'])
    new_list = []
    for item in all_var:
        if item in var_list:
            new_list.append(item)
    
    # Skip station if it doesn't have all the variables desired  
    if set(var_list).issubset(set(new_list))==False:
        continue

    # Get basic station information
    st_name = str(x['NAME'])
    #print(st_name)
    st_id = str(x['STID'])
    lat_mw = float(x['LATITUDE']) # units = degrees
    lon_mw = float(x['LONGITUDE']) # units = degrees
    if x['ELEVATION'] is None:
        elev = 'N/A'
    else:
        elev = float(x['ELEVATION']) # units = feet
    
    # Sample lat/lon grid cell information
    iy1,ix1 = met.naive_fast(lat, lon, lat_mw, lon_mw)
    #print(str(iy1)+','+str(ix1))
    
    site_name = pd.DataFrame([st_name],columns=['site_name'])
    ix1 = pd.concat([pd.DataFrame([ix1]),site_name], axis=1)
    iy1 = pd.concat([pd.DataFrame([iy1]),site_name], axis=1)
    
    iy = iy.append(iy1)
    ix = ix.append(ix1)

# Combine iy and ix
#iy = iy.set_index('site_name')
iy.columns = ['iy','site_name']
#ix = ix.set_index('site_name')
ix.columns = ['ix','site_name']
df_latlon = pd.merge(iy,ix, on='site_name')    
df_latlon = df_latlon.reset_index(drop=True)

print('Starting airpact function')

#run airpact function
df_airpact = get_wrf_DF(datadir, start, end, x_dim, y_dim, lat, lon, layer)
df_airpact = df_airpact.reset_index().drop(['index'],axis=1)

# Add site names to the rows
df_airpact['iy'] = pd.to_numeric(df_airpact['iy'])
df_airpact['ix'] = pd.to_numeric(df_airpact['ix'])
#df_airpact1 = pd.concat([df_airpact,df_latlon], axis=1)
df_airpact = pd.merge(df_airpact,df_latlon)

#print(df_airpact.keys())
#print(df_airpact['DateTime'].shape)
#print(df_airpact['TEMP2'].shape)
#print(df_airpact['Q2'].shape)
#print(df_airpact['lat'].shape)
#print(df_airpact['lon'].shape)

print("Dictionary is done")
size=df_airpact.memory_usage(deep=True).sum()
if size < 20000000000:
    df_airpact.to_csv(base_dir +'/airpact_met_'+str(start_year)+str(start_month)+str(start_day)+'_'+str(end_year)+str(end_month)+str(end_day)+'.csv')   #Theoretically, this file should be about 1.7 GB for all the data
    print('Meteorology data saved')
else:
    print('Met file too large, not saved')
    pass

