# -*- coding: utf-8 -*-
"""
Created on Thu Jul 5 16:11:19 2018

@author: Benjamin Yang
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

# Set a directory containing python scripts
#base_dir = "/data/lar/projects/WRF_met_eval/"
base_dir = r'E:\Research\AIRPACT_eval\meteorology/'

# set a directory to save output files
#outputdir = '/data/lar/users/jmunson/longterm_airpact/outputs/'
outputdir = base_dir + '/outputs/'

#outputdir = "/home/byang/research/outputs/"

# all the functions are saved in Met_functions_for_Ben.py
exec(open(base_dir +"Met_functions_for_Ben.py").read())
print(base_dir +"Met_functions_for_Ben.py")
# set start and end date
start = datetime.datetime(year=2017, month=8, day=29, hour=0)
end = datetime.datetime(year=2017, month=9, day=10, hour=0)
#start = datetime.datetime(year=2017, month=9, day=5, hour=0)
#end = datetime.datetime(year=2017, month=9, day=7, hour=0)
timezone = pytz.timezone("utc")
start = timezone.localize(start)
end = timezone.localize(end)

# total hours (will be used to filter out stations with missing hour(s))
time_diff = end - start
tot_hours = time_diff.days*24 #+ time_diff.seconds/3600
print(tot_hours)

####################################
##########     UW WRF     ##########
####################################

# set a directory containing wrfout files
#datadir = "/data/lar/projects/UW_WRF_output/"
datadir = base_dir + '/UW_WRF_output/'

# open one of wrfout to read coordinate
modeloutput= datadir +"wrfout_d3_" +  start.strftime("%Y-%m-%d_00_00_00.nc") # this is subset of wrfout for git repository

# open and read wrfout using netCDF function (Dataset)
if os.path.isfile(modeloutput):
    nc  = Dataset(modeloutput, 'r')
    print('reading ', modeloutput)
else:
    print("no file")
    exit()

# x_dim and y_dim are the x (lon) and y (lat) dimensions of the model
x_dim1 = len(nc.dimensions['west_east'])
y_dim1 = len(nc.dimensions['south_north'])

# obtain model lat and lon - needed for AQS eval and basemap
lon1 = nc.variables['XLONG'][0]
lat1  = nc.variables['XLAT'][0]

# Get the grid spacing
#dx1 = float(nc.DX)
#dy1 = float(nc.DY)
#width_meters1 = dx1 * (int(x_dim1) - 1)     #Domain Width
#height_meters1 = dy1 * (int(y_dim1) - 1)    #Domain Height

# Get a variable (T2) from netCDF file for Basemap
t_basemap = wrf.getvar(nc, "T2")
print(t_basemap)
# close the wrfout
nc.close()

# reads UW WRF variables and saves them in a dictionary
wrf1 = met.get_wrf_DF('UW', datadir, start, end, x_dim1, y_dim1, lat1, lon1)

print("UW dictionary is done")
#%%
######################################
##########     WRF-CHEM     ##########  
######################################

# set a directory containing wrfout files
datadir = "/data/lar/projects/WRF_CHEM_output/SEP2017/"

# open one of wrfout to read coordinate
modeloutput= datadir +"wrfout_d01_" +  start.strftime("%Y-%m-%d_00:00:00") # this is subset of wrfout for git repository
print("WSU", modeloutput)

# open and read wrfout using netCDF function (Dataset)
if os.path.isfile(modeloutput):
    nc  = Dataset(modeloutput, 'r')
    print('reading ', modeloutput)
else:
    print("no file")
    exit()

# x_dim and y_dim are the x (lon) and y (lat) dimensions of the model
x_dim2 = len(nc.dimensions['west_east'])
y_dim2 = len(nc.dimensions['south_north'])

# obtain model lat and lon - needed for eval and basemap
lon2 = nc.variables['XLONG'][0]
lat2  = nc.variables['XLAT'][0]

# Get the grid spacing
#dx2 = float(nc.DX)
#dy2 = float(nc.DY)
#width_meters2 = dx2 * (int(x_dim2) - 1)     #Domain Width
#height_meters2 = dy2 * (int(y_dim2) - 1)    #Domain Height

# close the wrfout
nc.close()

# reads WRF-Chem chemical tracers and saves them in a dictionary
wrf2 = met.get_wrf_DF('WSU', datadir, start, end, x_dim2, y_dim2, lat2, lon2)

print("WRF_CHEM dictionary is done")

##################################
##########     HRRR     ##########
##################################

# set a directory containing wrfout files
datadir = "/data/lar/projects/HRRR_output/"  

# open one of wrfout to read coordinate
modeloutput= datadir +"wrfout_d5_" +  start.strftime("%Y-%m-%d_00_00_00.nc") # this is subset of wrfout for git repository

# open and read wrfout using netCDF function (Dataset)
if os.path.isfile(modeloutput):
    nc  = Dataset(modeloutput, 'r')
    print('reading ', modeloutput)
else:
    print("no file")
    exit()

# x_dim and y_dim are the x (lon) and y (lat) dimensions of the model
x_dim3 = len(nc.dimensions['x'])
y_dim3 = len(nc.dimensions['y'])

# obtain model lat and lon - needed for AQS eval and basemap
lon3 = nc.variables['longitude'][:,:] -360 # convert from degrees East to degrees
lat3  = nc.variables['latitude'][:,:] 

# Get the grid spacing
#dx3 = nc.variables['x'].grid_spacing
#dy3 = nc.variables['y'].grid_spacing
#width_meters3 = dx3 * (int(x_dim3) - 1)     #Domain Width
#height_meters3 = dy3 * (int(y_dim3) - 1)    #Domain Height

# close the wrfout
nc.close()

# reads UW WRF variables and saves them in a dictionary
wrf3 = met.get_wrf_DF('HRRR',datadir, start, end, x_dim3, y_dim3, lat3, lon3)

print("HRRR dictionary is done")

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
vname_2 = []
vname_3 = []
vlabel = []
mean_obs = []
mean1 = []
mean2 = []
mean3 = []

x_list = []
y_list = []

# Iterate over dictionary to make time series plots of each variable for each station
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
    print(st_name)
    st_id = str(x['STID'])
    lat_mw = float(x['LATITUDE']) # units = degrees
    lon_mw = float(x['LONGITUDE']) # units = degrees
    if x['ELEVATION'] is None:
        elev = 'N/A'
    else:
        elev = float(x['ELEVATION']) # units = feet
    
    # Sample lat/lon grid cell information
    iy1,ix1 = met.naive_fast(lat1, lon1, lat_mw, lon_mw)
    iy2,ix2 = met.naive_fast(lat2, lon2, lat_mw, lon_mw)
    iy3,ix3 = met.naive_fast(lat3, lon3, lat_mw, lon_mw)
    
    # Create new dictionary for WRF-Chem grid cell
    mod_sample1 = {}
    mod_sample2 = {}
    mod_sample3 = {}

    for k in wrf1.keys():
        #mod_sample1[k] = wrf.to_np(wrf1[k][:,iy,ix]).flatten()
        mod_sample1[k] = wrf1[k][:,iy1,ix1].flatten()
    for k in wrf2.keys():
        mod_sample2[k] = wrf2[k][:,iy2,ix2].flatten()
    for k in wrf3.keys():
        mod_sample3[k] = wrf3[k][:,iy3,ix3].flatten()
    
    # Convert dictionary to data frame    
    df_mod1 = pd.DataFrame(mod_sample1)
    df_mod2 = pd.DataFrame(mod_sample2)
    df_mod3 = pd.DataFrame(mod_sample3)
    #df_mod1 = df_mod1.drop(['DateTime','lat','lon'], axis=1)

    # Dates: Convert the strings to a python datetime object.mro
    o_dates = x['OBSERVATIONS']['date_time']
    
    # Store the data we will return in this new dictionary
    new_mw = {}
    
    converttime = np.vectorize(MWdate_to_datetime)
    new_mw['date_time'] = converttime(o_dates)
    
    # Dynamically create keys in the dictionary for each requested variable
    for v in new_list:
        # v represents all the variables, but each variable may have
        # more than one set. For now, just return the first set.
        key_name = str(v)
        set_num = 0

        grab_this_set = str(list(x['SENSOR_VARIABLES'][key_name])[set_num])

        # Always grab the first set (either _1 or _1d)
        # should make exceptions to this rule for certain stations and certain variables
        if grab_this_set[-1] != '1' and grab_this_set[-1] != 'd':
            grab_this_set = grab_this_set[0:-1]+'1'
        if grab_this_set[-1] == 'd':
            grab_this_set = grab_this_set[0:-2]+'1d'

        variable_data = np.array(x['OBSERVATIONS'][grab_this_set], dtype=np.float)
        new_mw[key_name] = variable_data   
    
    
    # Convert dictionary to data frame (dictionary must have same length
    # arrays, or else go down to the "except" block)
    df = pd.DataFrame(new_mw) 
    
    # Average data by each hour 
    df['NewDateTime'] = pd.to_datetime(df['date_time'])
    df.index = df['NewDateTime']
    df_h = df.resample('H').mean()
    df_h.insert(0,'date_time',df_h.index)
    df_h = df_h.reset_index(drop=True)

    # Skip station if it doesn't have 24 hours of data
    # CHANGE THIS NUMBER IF THERE ARE MORE DAYS (e.g. Aug 28-29 = 48 hours)
    if np.size(df_h['date_time']) != tot_hours:
        continue

    #########################################################
    ##########     CONVERT/CALCULATE VARIABLES     ##########
    #########################################################
    
    # Convert temperature from K to C°
    temp1 = df_mod1['T2'] - 273.15 
    temp2 = df_mod2['T2'] - 273.15
    temp3 = df_mod3['T2'] - 273.15
    
    # Convert pressure from Pa to hPa (mb)
    p1 = df_mod1['PSFC'] / 100
    p2 = df_mod2['PSFC'] / 100
    p3 = df_mod3['PSFC'] / 100
    
    # Calculate wind speed from u and v components
    u1 = df_mod1['U10']
    v1 = df_mod1['V10']
    u2 = df_mod2['U10']
    v2 = df_mod2['V10']
    u3 = df_mod3['U10']
    v3 = df_mod3['V10']
    
    ws1 = np.sqrt((u1**2)+(v1**2))
    ws2 = np.sqrt((u2**2)+(v2**2))
    ws3 = np.sqrt((u3**2)+(v3**2))
    
    # Calculate wind direction from u and v components
    ws1 = np.sqrt((u1**2)+(v1**2))
    ws2 = np.sqrt((u2**2)+(v2**2))
    ws3 = np.sqrt((u3**2)+(v3**2))
    
    wind_dir1 = np.arctan2(u1/ws1, v1/ws1) # Where wind is blowing TO
    wind_dir_degrees1 = wind_dir1 * 180/np.pi   
    wd1 = wind_dir_degrees1 + 180
    wind_dir2 = np.arctan2(u2/ws2, v2/ws2) 
    wind_dir_degrees2 = wind_dir2 * 180/np.pi   
    wd2 = wind_dir_degrees2 + 180 # Where wind is blowing FROM
    wind_dir3 = np.arctan2(u3/ws3, v3/ws3) 
    wind_dir_degrees3 = wind_dir3 * 180/np.pi   
    wd3 = wind_dir_degrees3 + 180 # Where wind is blowing FROM
    
    # Calculate 2-m (approximately) relative humidity using Q2, T2, PSFC, & constants
    # Formula taken from:
    # http://mailman.ucar.edu/pipermail/wrf-users/2012/002546.html
    pq0 = 379.90516
    a2 = 17.2693882
    a3 = 273.16
    a4 = 35.86
    
    rh1 = df_mod1['Q2'] / ( (pq0 / df_mod1['PSFC']) * np.exp(a2 * 
                   (df_mod1['T2'] - a3) / (df_mod1['T2'] - a4)) )
    rh2 = df_mod2['Q2'] / ( (pq0 / df_mod2['PSFC']) * np.exp(a2 * 
                   (df_mod2['T2'] - a3) / (df_mod2['T2'] - a4)) )
    
    rh_new1 = rh1 * 100 # convert from fraction to %    
    rh_new2 = rh2 * 100 # convert from fraction to %
    rh_new3 = df_mod3['Q2'] # already relativey humidity in %
    
    # Convert observed pressure from Pa to mb (if pressure exists)
    if 'pressure' in df_h:
        p_obs = df_h['pressure'] / 100
        df_h['pressure'] = p_obs
    
    # Create new data frame with all variables from WRF models
    df_models = pd.DataFrame({'T2_1': temp1, 'PSFC_1': p1, 'WS_1': ws1, 'WD_1': wd1, 
                              'RH_1': rh_new1, 'PRECIP_1': df_mod1['RAINNC'], 
                              'T2_2': temp2, 'PSFC_2': p2, 'WS_2': ws2, 'WD_2': wd2, 
                              'RH_2': rh_new2, 'PRECIP_2': df_mod2['RAINNC'],
                              'T2_3': temp3, 'PSFC_3': p3, 'WS_3': ws3, 'WD_3': wd3, 
                              'RH_3': rh_new3, 'PRECIP_3': df_mod3['RAINNC']})
    
    # Concatenating observation and model data frames
    df_all = pd.concat([df_h,df_models], axis=1)
    
    # Store x/y coordinates in lists
    y_list.append(lat_mw)
    x_list.append(lon_mw)
    
    # Select variables, specify labels, units and y-limits, and plot model 
    # variables based on MesoWest variable names
    for w in new_list:
        var_name = str(w)
        
        # Skip variable if all values are zeros or NaNs
        if df_h[var_name].isnull().all()==True or all(df_h[var_name]==0):
            continue
        
        #var_units = mw_data['UNITS'][var_name]
        if var_name=='air_temp':
            var_name_mod1 = 'T2_1'
            var_name_mod2 = 'T2_2'
            var_name_mod3 = 'T2_3'
            mod_var1 = temp1
            mod_var2 = temp2
            mod_var3 = temp3
 
            var_label = 'Temperature (C°)'
            var_units = 'C°'
            ymin = 0
            ymax = 40
            
        if var_name=='pressure':
            var_name_mod1 = 'PSFC_1'
            var_name_mod2 = 'PSFC_2'
            var_name_mod3 = 'PSFC_3'
            mod_var1 = p1
            mod_var2 = p2
            mod_var3 = p3
            
            var_label = 'Pressure (mb)'
            var_units = 'mb'
            ymin = 850
            ymax = 1050
            
        if var_name=='wind_speed':
            var_name_mod1 = 'WS_1'
            var_name_mod2 = 'WS_2'
            var_name_mod3 = 'WS_3'
            mod_var1 = ws1
            mod_var2 = ws2
            mod_var3 = ws3
            
            var_label = 'Wind Speed (m/s)'
            var_units = 'm/s'
            ymin = 0
            ymax = 15
            
        if var_name=='wind_direction':  
            var_name_mod1 = 'WD_1'
            var_name_mod2 = 'WD_2'
            var_name_mod3 = 'WD_3'
            mod_var1 = wd1   
            mod_var2 = wd2
            mod_var3 = wd3
            
            var_label = 'Wind Direction (°)'
            var_units = '°'
            ymin = -1
            ymax = 1
            
        if var_name=='relative_humidity':
            var_name_mod1 = 'RH_1'
            var_name_mod2 = 'RH_2'
            var_name_mod3 = 'RH_3'
            mod_var1 = rh_new1   
            mod_var2 = rh_new2
            mod_var3 = rh_new3
        
            var_label = 'Relative Humidity (%)'
            var_units = '%'
            ymin = 0
            ymax = 110
            
        if var_name=='precip_accum':
            var_name_mod1 = 'PRECIP_1'
            var_name_mod2 = 'PRECIP_2'
            var_name_mod3 = 'PRECIP_3'
            mod_var1 = df_mod1['RAINNC']
            mod_var2 = df_mod2['RAINNC']
            mod_var3 = df_mod3['RAINNC']
            
            var_label = 'Precipitation Accumulated (mm)'
            var_units = 'mm'
            ymin = 0 
            ymax = 10 
        
        
        ################################################
        ##########     COMPUTE STATISTICS     ##########
        ################################################
        
        var_units = 'var units'
        
        stats1 = met.stats(df_all, var_name_mod1, var_name, var_units)
        stats1.loc['model'] = ['UW WRF']
        stats2 = met.stats(df_all, var_name_mod2, var_name, var_units)
        stats2.loc['model'] = ['WSU WRF']
        stats3 = met.stats(df_all, var_name_mod3, var_name, var_units)
        stats3.loc['model'] = ['HRRR']
        stats_combined = pd.concat([stats1,stats2,stats3],axis=1,join_axes=[stats1.index])
        
        stats_T = stats_combined.T # transpose index and columns
        stats_T['lat'] = lat_mw
        stats_T['lon'] = lon_mw
        stats_T['station ID'] = st_id
        
        stats_all = stats_all.append(stats_T)
        
        # Fill data frame for computing overall statistics
        if var_name not in df_overall.columns:
            df_overall[[var_name_mod1,var_name_mod2,var_name_mod3,var_name]] \
            = df_all[[var_name_mod1,var_name_mod2,var_name_mod3,var_name]]
        else:
            df_overall = df_overall.append(df_all[[var_name_mod1,var_name_mod2,
                                                   var_name_mod3,var_name]],ignore_index=True)
        
        if var_name not in vname_obs:
            vname_obs.append(var_name)
            vname_1.append(var_name_mod1)
            vname_2.append(var_name_mod2)
            vname_3.append(var_name_mod3)
            vlabel.append(var_label)
        
        ###################################
        ##########     PLOTS     ##########
        ###################################
        
        # this is needed for x-axis label
        dfmt = dates.DateFormatter('%m-%d %H')
        #dfmt = dates.DateFormatter('%m-%d')
        
        # Create a time series plot of a meteorological parameter
        fig1, ax = plt.subplots(figsize=(8, 4))
        
        # MesoWest observations
        if var_name == 'wind_direction':
            ax.plot(df_h['date_time'],np.cos(df_h[var_name]*np.pi/180),c='k',label='Observations')
            # UW WRF model output        
            ax.plot(df_h['date_time'],np.cos(mod_var1*np.pi/180),c='b',label='UW WRF')
            # WRF-Chem model output
            ax.plot(df_h['date_time'],np.cos(mod_var2*np.pi/180),c='r',label='WSU WRF')
            # HRRR model output
            ax.plot(df_h['date_time'],np.cos(mod_var3*np.pi/180),c='g',label='HRRR')
            
            ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel='Cosine of Wind Direction',ylim=(ymin,ymax))
        else:
            ax.plot(df_h['date_time'],df_h[var_name],c='k',label='Observations')
            # UW WRF model output        
            ax.plot(df_h['date_time'],mod_var1,c='b',label='UW WRF')
            # WRF-Chem model output
            ax.plot(df_h['date_time'],mod_var2,c='r',label='WSU WRF')
            # HRRR model output
            ax.plot(df_h['date_time'],mod_var3,c='g',label='HRRR')
            
            ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel=var_label,ylim=(ymin,ymax))
        
        ax.xaxis.set_major_formatter(dfmt)
        fig1.autofmt_xdate(rotation=60)
        
        # Display r^2 on plot
        ax.text(1.15, 0.4,'UW WRF: $r^2$ = %s' %stats_T['R^2 [-]'][0], 
                fontsize = 11, ha='center', va='center', transform=ax.transAxes)
        ax.text(1.15, 0.3,'WSU WRF: $r^2$= %s' %stats_T['R^2 [-]'][1], 
                fontsize = 11, ha='center', va='center', transform=ax.transAxes)
        ax.text(1.15, 0.2,'HRRR: $r^2$= %s' %stats_T['R^2 [-]'][2], 
                fontsize = 11, ha='center', va='center', transform=ax.transAxes)
        
        ax.legend(loc='upper right', bbox_to_anchor=(1.27, 0.9))
        
        plt.show()
        fig1.savefig(outputdir + '%s_%s_timeseries.png' %(st_id, var_name),bbox_inches='tight')
        '''
        # Create a scatter plot with linear regression lines and 
        # correlation coefficients "r" (models vs. obs)
        fig2, ax = plt.subplots(figsize=(6, 4.5))
        
        ax.scatter(df_h[var_name], mod_var1, s=50, c='b', label='UW WRF')
        ax.scatter(df_h[var_name], mod_var2, s=50, c='r', label='WSU WRF')
        ax.scatter(df_h[var_name], mod_var3, s=50, c='g', label='HRRR') 
        
        # Perform linear regression
        m1, b1 = np.polyfit(df_h[var_name], mod_var1, deg=1)
        m2, b2 = np.polyfit(df_h[var_name], mod_var2, deg=1)
        m3, b3 = np.polyfit(df_h[var_name], mod_var3, deg=1)
        
        #ax.plot(df_h[var_name], m1*df_h[var_name] + b1, '--b', label='UW_WRF')
        #ax.plot(df_h[var_name], m2*df_h[var_name] + b2, ':r', label='WRF-Chem')
        #ax.plot(df_h[var_name], m3*df_h[var_name] + b3, '-.g', label='HRRR')
        
        
        # Get correlation coefficients
        cc1 = round(np.corrcoef(df_h[var_name], mod_var1)[0, 1],3)
        cc2 = round(np.corrcoef(df_h[var_name], mod_var2)[0, 1],3)
        cc3 = round(np.corrcoef(df_h[var_name], mod_var3)[0, 1],3)
        
        ax.text(1.15, 0.9,'UW WRF: r = %s' %cc1, fontsize = 11, ha='center', 
                va='center', transform=ax.transAxes)
        ax.text(1.15, 0.8,'WSU WRF: r = %s' %cc2, fontsize = 11, ha='center', 
                va='center', transform=ax.transAxes)
        ax.text(1.15, 0.7,'HRRR: r = %s' %cc3, fontsize = 11, ha='center', 
                va='center', transform=ax.transAxes)
        
        
        # Define x and y-limits
        xy_min = min(np.nanmin(df_h[var_name]),np.nanmin(mod_var1),np.nanmin(mod_var2),np.nanmin(mod_var3))
        xy_max = max(np.nanmax(df_h[var_name]),np.nanmax(mod_var1),np.nanmax(mod_var2),np.nanmax(mod_var3))

        # Add 1:1 line
        ax.plot([xy_min,xy_max], [xy_min,xy_max], '-k', label = '1:1 line')
        
        ax.set(title=st_name,xlabel='Observed %s' %var_label,
               ylabel='Predicted %s' %var_label,xlim=(xy_min,xy_max),ylim=(xy_min,xy_max))
        ax.legend(loc='center right', bbox_to_anchor=(1.3, 0.5))
        
        plt.show()
        fig2.savefig(outputdir + '%s_%s_regression.png' %(st_id, var_name),bbox_inches='tight')
        '''
########################################################
##########     COMPUTE OVERALL STATISTICS     ##########
########################################################

var_units = 'var units'

for n in np.arange(len(vname_obs)):
    stats1 = met.stats(df_overall, vname_1[n], vname_obs[n], var_units)
    #stats1.loc['model'] = ['UW WRF']
    stats2 = met.stats(df_overall, vname_2[n], vname_obs[n], var_units)
    #stats2.loc['model'] = ['WSU WRF']
    stats3 = met.stats(df_overall, vname_3[n], vname_obs[n], var_units)
    #stats3.loc['model'] = ['HRRR']
    stats_combined = pd.concat([stats1,stats2,stats3],axis=1,join_axes=[stats1.index])
    
    stats_T = stats_combined.T # transpose index and columns
    stats_T.insert(0, 'Variable', vlabel[n])
    stats_T.insert(1, 'OBS Mean [var units]', [mean_obs, mean_obs,mean_obs]) 
    stats_T.insert(2, 'Model', ['UW WRF','WSU WRF','HRRR'])
    

    # Finding mean (average) for observations and model values
    mean_obs = met.mean_stat(df_overall, vname_obs[n])
    mean1 = met.mean_stat(df_overall, vname_1[n])
    mean2 = met.mean_stat(df_overall, vname_2[n])
    mean3 = met.mean_stat(df_overall, vname_3[n])
    
    stats_T.insert(3, 'Mean [var units]', [mean1,mean2,mean3])

    stats_overall = stats_overall.append(stats_T)
'''
    # save stats into an Excel file
    writer = pd.ExcelWriter(outputdir + 'stats' + '_' + start_t  + '-' +  end_t + '.xlsx')
    stats_overall.to_excel(writer,'Sheet1',index=False)
    writer.save()
'''  
##############################################################
##########     BAR CHARTS OF OVERALL STATISTICS     ##########
##############################################################    
'''
ind = np.arange(len(vname_obs)) 
width = 0.2

for n in np.arange(3,7):   
    fig3, ax = plt.subplots(figsize=(8, 4))
    
    # Plot bars for each variable and model (group by variable name)    
    plt.bar(ind, stats_overall[stats_overall.values=='UW WRF'][list(stats_overall)[n]], width, color='royalblue', label='UW WRF')
    plt.bar(ind + width, stats_overall[stats_overall.values=='WSU WRF'][list(stats_overall)[n]], width, color='indianred', label='WSU WRF')
    plt.bar(ind + (width*2), stats_overall[stats_overall.values=='HRRR'][list(stats_overall)[n]], width, color='forestgreen', label='HRRR')
    
    if n == 6:
        plt.ylabel('$R^2$ [-]')
    else:
        plt.ylabel(list(stats_overall)[n])
    
    if n == 3: 
        plt.title('Normalized Mean Bias (NMB)')
        stat_name = 'NMB'
    if n == 4:
        plt.title('Normalized Mean Error (NME)')
        stat_name = 'NME'
    if n == 5:
        plt.title('Root Mean Square Error (RMSE)')
        stat_name = 'RMSE'
    if n == 6:
        plt.title('Coefficient of Determination ($R^2$)')
        stat_name = 'R^2'
    
    stats_var= list(stats_overall[stats_overall.values=='UW WRF'].index.values)
    for index,vname in enumerate(stats_var):
        if stats_var[index]=='T2_1':
            stats_var[index]='Temperature'
        if stats_var[index]=='PSFC_1':
            stats_var[index]='Pressure'
        if stats_var[index]=='WS_1':
            stats_var[index]='Wind Speed'
        if stats_var[index]=='WD_1':
            stats_var[index]='Wind Direction'
        if stats_var[index]=='RH_1':
            stats_var[index]='Relative Humidity'
        
    plt.xticks(ind + width, stats_var)
    
    plt.legend(loc='best')
    plt.show()
    fig3.savefig(outputdir + '%s_bar_chart.png' %stat_name, bbox_inches='tight')
''' 
#######################################
##########     BIAS MAPS     ##########
#######################################

# Create 2D map with points representing stations 
# (larger points = greater bias, blue = negative bias, red = positive bias)

# Get the basemap object
bm = wrf.get_basemap(t_basemap)

x, y = bm(x_list, y_list)

# Get x, y coordinates for each of 6 stations (KSEA,KPUW,KPDX,KLMT,KBOI,KMLP)
xlist_few = [-122.309,-117.11]
ylist_few = [47.449,46.744]
x_few, y_few = bm(xlist_few,ylist_few)
label_few = ['KSEA','KPUW']

# Make array with all variable names (for each model) in "stats_all" data frame 
stat_var = np.unique(stats_all.index)

for sv in stat_var: 
    # Create a figure
    fig4 = plt.figure(figsize=(12,9))
    
    # Add geographic outlines
    #bm.drawmapboundary(fill_color='navy')
    #bm.fillcontinents(color='peru', lake_color='navy')
                    
    bm.drawcoastlines(linewidth=0.25)
    bm.drawstates(linewidth=0.25)
    bm.drawcountries(linewidth=0.25)
    
    # Get NMB values
    nmb = list(stats_all.loc[sv,'NMB [%]']) 
    nme = list(stats_all.loc[sv,'NME [%]']) 
    
    #addsize = 70
    
    # Draw the contours and filled contours
    if sv in ['PSFC_1','PSFC_2','PSFC_3']:
      #addsize = 50
      #msizes = [51, 52, 53, 54, 55, 56]
      #nme_s = list(stats_all.loc[sv,'NME [%]'] + addsize)
      bm.scatter(x, y, s = 80, c = nmb, cmap='seismic', vmin = -10, vmax = 10)
      if sv=='PSFC_1':
        plt.title('Pressure: UW WRF', fontsize = 20)
      if sv=='PSFC_2':
        plt.title('Pressure: WSU WRF', fontsize = 20)  
      if sv=='PSFC_3':
        plt.title('Pressure: HRRR', fontsize = 20)
    if sv in ['RH_1','RH_2','RH_3']:
      #addsize = 30
      #msizes = [40, 50, 60, 70, 80]
      #nme_s = list(stats_all.loc[sv,'NME [%]'] + addsize)
      bm.scatter(x, y, s = 80, c = nmb, cmap='seismic', vmin = -100, vmax = 100)
      if sv=='RH_1':
        plt.title('Relative Humidity: UW WRF', fontsize = 20)
      if sv=='RH_2':
        plt.title('Relative Humidity: WSU WRF', fontsize = 20)  
      if sv=='RH_3':
        plt.title('Relative Humidity: HRRR', fontsize = 20)
    if sv in ['T2_1','T2_2','T2_3']:
      #addsize = 30
      #msizes = [40, 50, 60, 70, 80]
      #nme_s = list(stats_all.loc[sv,'NME [%]'] + addsize)
      bm.scatter(x, y, s = 80, c = nmb, cmap='seismic', vmin = -70, vmax = 70)
      if sv=='T2_1':
        plt.title('Temperature: UW WRF', fontsize = 20)
      if sv=='T2_2':
        plt.title('Temperature: WSU WRF', fontsize = 20)  
      if sv=='T2_3':
        plt.title('Temperature: HRRR', fontsize = 20)
    if sv in ['WD_1','WD_2','WD_3','WS_1','WS_2','WS_3']:
      #addsize = 10
      #msizes = [60, 110, 160, 210, 260]
      #nme_s = list(stats_all.loc[sv,'NME [%]'] + addsize)
      bm.scatter(x, y, s = 80, c = nmb, cmap='seismic', vmin = -500, vmax = 500)
      if sv=='WD_1':
        plt.title('Wind Direction: UW WRF', fontsize = 20)
      if sv=='WD_2':
        plt.title('Wind Direction: WSU WRF', fontsize = 20)  
      if sv=='WD_3':
        plt.title('Wind Direction: HRRR', fontsize = 20)
      if sv=='WS_1':
        plt.title('Wind Speed: UW WRF', fontsize = 20)
      if sv=='WS_2':
        plt.title('Wind Speed: WSU WRF', fontsize = 20)  
      if sv=='WS_3':
        plt.title('Wind Speed: HRRR', fontsize = 20)
    
    plt.title('%s Bias' %sv, fontsize = 18)
    plt.colorbar(label = 'NMB [%]', shrink = 0.75)
    
    '''
    labels = [str(a) for a in [b-addsize for b in msizes]]
    markers = []
    for size in msizes:
        markers.append(plt.scatter([],[], s=size, c='k', label=size))

    plt.legend(handles=markers, labels=labels, scatterpoints=1, ncol=1, title='NME [%]', loc='upper right')
    '''
  
    for label, xpt, ypt in zip(label_few, x_few, y_few):
        plt.text(xpt + 20000, ypt - 10000, label, size=10, zorder=2, weight='bold')
    
    plt.show()
    fig4.savefig(outputdir + '%s_bias.png' %sv, bbox_inches='tight')
    
'''        
# save stats table as a png file
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table

ax = plt.subplot(111, frame_on=False) # no visible frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

table(ax, stats_overall)  # where df is your data frame

plt.savefig('stats.png',bbox_inches='tight')
'''

