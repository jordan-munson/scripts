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
#base_dir = "/data/lar/users/jmunson/longterm_airpact/"
base_dir = r'E:\Research\AIRPACT_eval\meteorology/'

# set a directory to save output files
outputdir = base_dir + 'outputs/'

# set a directory containing wrfout files
#datadir = base_dir + 'linked_days/'
datadir = r'E:\Research\Urbanova_Jordan\Urbanova_ref_site_comparison\AIRPACT\2018/'

# all the functions are saved in Met_functions_for_Ben.py
exec(open(base_dir +"Met_functions_for_Ben.py").read())
print(base_dir +"Met_functions_for_Ben.py")

#exec(open(base_dir + "/airpact_functions.py").read())

start_year = 2018    #2009
start_month = 1    #5
start_day = 11    #1

end_year = 2018
end_month = 1    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 13    #15

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

print('Starting airpact function')
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
    print(str(iy1)+','+str(ix1))
    
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

#run airpact function
df_airpact = get_wrf_DF(datadir, start, end, x_dim, y_dim, lat, lon, layer)
df_airpact = df_airpact.reset_index().drop(['index'],axis=1)
print(df_airpact.keys())
print(df_airpact['DateTime'].shape)
print(df_airpact['TEMP2'].shape)
print(df_airpact['Q2'].shape)
print(df_airpact['lat'].shape)
print(df_airpact['lon'].shape)

print("Dictionary is done")

#%%
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
    iy1,ix1 = met.naive_fast(lat, lon, lat_mw, lon_mw)
    #print(str(iy1)+' , '+str(ix1))


    #iy = pd.concat([iy,pd.DataFrame([iy1])])
    #ix = pd.concat([ix,pd.DataFrame([ix1])])
    
    # Create new dictionary for WRF-Chem grid cell
    mod_sample1 = {}

 #   for k in df_airpact.keys():
        #mod_sample1[k] = wrf.to_np(wrf1[k][:,iy,ix]).flatten()
#        mod_sample1[k] = df_airpact[k][:,iy1,ix1].flatten()
    
    # Convert dictionary to data frame    
    #df_mod1 = pd.DataFrame(mod_sample1)
    df_airpact['iy'] = pd.to_numeric(df_airpact['iy'])
    df_airpact['ix'] = pd.to_numeric(df_airpact['ix'])

    df_mod1 = df_airpact.loc[(df_airpact['ix'] == ix1) & (df_airpact['iy'] == iy1)]

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
    temp1 = df_mod1['TEMP2'] - 273.15 
    
    # Convert pressure from Pa to hPa (mb)
    p1 = df_mod1['PRSFC'] / 100
    
    # Calculate wind speed from u and v components
    
    #u1 = df_mod1['U10']
    #v1 = df_mod1['V10']
    #ws1 = np.sqrt((u1**2)+(v1**2))
    
    ws1 = df_mod1['WSPD10']    # MCIP files record wind speed, no need to calculate
    
    # Calculate wind direction from u and v components 
    
    #wind_dir1 = np.arctan2(u1/ws1, v1/ws1) # Where wind is blowing TO
    #wind_dir_degrees1 = wind_dir1 * 180/np.pi   
    #wd1 = wind_dir_degrees1 + 180
    
    wd1 = df_mod1['WDIR10']    # MCIP files record wind speed, no need to calculate
    
    # Calculate 2-m (approximately) relative humidity using Q2, TEMP2, PRSFC, & constants
    # Formula taken from:
    # http://mailman.ucar.edu/pipermail/wrf-users/2012/002546.html
    pq0 = 379.90516
    a2 = 17.2693882
    a3 = 273.16
    a4 = 35.86
    
    rh1 = df_mod1['Q2'] / ( (pq0 / df_mod1['PRSFC']) * np.exp(a2 * 
                   (df_mod1['TEMP2'] - a3) / (df_mod1['TEMP2'] - a4)) )
    
    rh_new1 = rh1 * 100 # convert from fraction to %    
    
    # Convert observed pressure from Pa to mb (if pressure exists)
    if 'pressure' in df_h:
        p_obs = df_h['pressure'] / 100
        df_h['pressure'] = p_obs
    
    # Create new data frame with all variables from WRF models
    df_models = pd.DataFrame({'TEMP2_1': temp1, 'PRSFC_1': p1, 'WS_1': ws1, 'WD_1': wd1, 
                              'RH_1': rh_new1})#, 'PRECIP_1': df_mod1['RAINNC']})
    df_models = df_models.reset_index().drop(['index'],axis=1)
    # Concatenating observation and model data frames
    df_all = pd.concat([df_h,df_models], axis=1).dropna()
    
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
            var_name_mod1 = 'TEMP2_1'
            mod_var1 = temp1
 
            var_label = 'Temperature (C°)'
            var_units = 'C°'
            ymin = 0
            ymax = 40
            
        if var_name=='pressure':
            var_name_mod1 = 'PRSFC_1'
            mod_var1 = p1
            
            var_label = 'Pressure (mb)'
            var_units = 'mb'
            ymin = 850
            ymax = 1050
            
        if var_name=='wind_speed':
            var_name_mod1 = 'WS_1'
            mod_var1 = ws1
            
            var_label = 'Wind Speed (m/s)'
            var_units = 'm/s'
            ymin = 0
            ymax = 15
            
        if var_name=='wind_direction':  
            var_name_mod1 = 'WD_1'
            mod_var1 = wd1   
            
            var_label = 'Wind Direction (°)'
            var_units = '°'
            ymin = -1
            ymax = 1
            
        if var_name=='relative_humidity':
            var_name_mod1 = 'RH_1'
            mod_var1 = rh_new1   
        
            var_label = 'Relative Humidity (%)'
            var_units = '%'
            ymin = 0
            ymax = 110
            
        if var_name=='precip_accum':
            var_name_mod1 = 'PRECIP_1'
            mod_var1 = df_mod1['RAINNC']
            
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
        stats_combined = pd.concat([stats1],axis=1,join_axes=[stats1.index])
        
        stats_T = stats_combined.T # transpose index and columns
        stats_T['lat'] = lat_mw
        stats_T['lon'] = lon_mw
        stats_T['station ID'] = st_id
        
        stats_all = stats_all.append(stats_T)
        
        # Fill data frame for computing overall statistics
        if var_name not in df_overall.columns:
            df_overall[[var_name_mod1,var_name]] \
            = df_all[[var_name_mod1,var_name]]
        else:
            df_overall = df_overall.append(df_all[[var_name_mod1,
                                                   var_name]],ignore_index=True)
        
        if var_name not in vname_obs:
            vname_obs.append(var_name)
            vname_1.append(var_name_mod1)
            vlabel.append(var_label)
        
        ###################################
        ##########     PLOTS     ##########
        ###################################
        # this is needed for x-axis label
        dfmt = dates.DateFormatter('%m-%d %H')
        #dfmt = dates.DateFormatter('%m-%d')
        
        # Create a time series plot of a meteorological parameter
        fig1, ax = plt.subplots(figsize=(8, 4))

        '''
        # MesoWest observations
        if var_name == 'wind_direction':
            ax.plot(df_h['date_time'],np.cos(df_h[var_name]*np.pi/180),c='k',label='Observations')
            # UW WRF model output        
            ax.plot(df_h['date_time'],np.cos(mod_var1*np.pi/180),c='b',label='Model')
            # WRF-Chem model output
            
            ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel='Cosine of Wind Direction',ylim=(ymin,ymax))
        else:
            ax.plot(df_h['date_time'],df_h[var_name],c='k',label='Observations')
            # UW WRF model output        
            ax.plot(df_h['date_time'],mod_var1,c='b',label='Model')
            # WRF-Chem model output
            
            ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel=var_label,ylim=(ymin,ymax))
        '''
        
        # MesoWest observations
        if var_name == 'wind_direction':
            ax.plot(df_all['date_time'],np.cos(df_all[var_name]*np.pi/180),c='k',label='Observations')
            # UW WRF model output        
            ax.plot(df_all['date_time'],np.cos(df_all[var_name_mod1]*np.pi/180),c='b',label='Model')
            # WRF-Chem model output
            
            ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel='Cosine of Wind Direction',ylim=(ymin,ymax))
        else:
            ax.plot(df_all['date_time'],df_all[var_name],c='k',label='Observations')
            # UW WRF model output        
            ax.plot(df_all['date_time'],df_all[var_name_mod1],c='b',label='Model')
            # WRF-Chem model output
            
            ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel=var_label,ylim=(ymin,ymax))
        ax.xaxis.set_major_formatter(dfmt)
        fig1.autofmt_xdate(rotation=60)
        
        # Display r^2 on plot
        ax.text(1.15, 0.4,'$r^2$ = %s' %stats_T['R^2 [-]'][0], 
                fontsize = 11, ha='center', va='center', transform=ax.transAxes)
        ax.text(1.15, 0.3,'RMSE= %s' %stats_T['RMSE [var units]'][0], 
                fontsize = 11, ha='center', va='center', transform=ax.transAxes)
        
        ax.legend(loc='upper right', bbox_to_anchor=(1.27, 0.9))
        
        plt.show()
        fig1.savefig(outputdir + '%s_%s_timeseries.png' %(st_id, var_name),bbox_inches='tight')
        plt.close()

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
    #Create large dataframe with all the model data
    site_name = pd.DataFrame([st_name],columns=['site_name'])
    df_mod2 = pd.concat([df_h,site_name], axis=1)
    df_mod2.site_name = df_mod2.site_name.fillna(st_name)
    df_temp = pd.concat([df_mod1,df_mod2], axis=1)
    df_met_all = pd.concat([df_met_all,df_temp])
    
    ix1 = pd.concat([pd.DataFrame([ix1]),site_name], axis=1)
    iy1 = pd.concat([pd.DataFrame([iy1]),site_name], axis=1)
    
    iy = iy.append(iy1)
    ix = ix.append(ix1)
    #df_met_all = pd.concat([df_met_all,df_mod1])
    
# Save the model meteorology data
cols = ['date_time','site_name','PRSFC','Q2','TEMP2','WDIR10','WSPD10','air_temp','pressure','relative_humidity','wind_direction','wind_speed','lat','lon']
df_met_all = df_met_all.drop('DateTime',axis=1)
df_met_all = df_met_all[cols]
size=df_met_all.memory_usage(deep=True).sum()

print('df_met_all dataframe is '+str(size)+' bytes')
if size < 20000000000:
    df_met_all.to_csv(base_dir +'/df_met_all.csv')   #Theoretically, this file should be about 1.7 GB for all the data
    print('Meteorology data saved')
else:
    print('Met file too large, not saved')
    pass

        
#%%
########################################################
##########     COMPUTE OVERALL STATISTICS     ##########
########################################################

var_units = 'var units'

for n in np.arange(len(vname_obs)):
    stats1 = met.stats(df_overall, vname_1[n], vname_obs[n], var_units)
    #stats1.loc['model'] = ['UW WRF']
    #stats2.loc['model'] = ['WSU WRF']
    
    stats_T = stats_combined.T # transpose index and columns
    stats_T.insert(0, 'Variable', vlabel[n])
    stats_T.insert(1, 'OBS Mean [var units]', [mean_obs]) 
    stats_T.insert(2, 'Model', ['AIRPACT'])
    

    # Finding mean (average) for observations and model values
    mean_obs = met.mean_stat(df_overall, vname_obs[n])
    mean1 = met.mean_stat(df_overall, vname_1[n])
    
    stats_T.insert(1, 'Mean [var units]', [mean1])

    stats_overall = stats_overall.append(stats_T)

    # save stats into an Excel file
    
    writer = pd.ExcelWriter(outputdir + 'stats' + '_' + start_t  + '-' +  end_t + '.xlsx')
    stats_overall.to_excel(writer,'Sheet1',index=False)
    writer.save()

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
        if stats_var[index]=='TEMP2_1':
            stats_var[index]='Temperature'
        if stats_var[index]=='PRSFC_1':
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
#%%
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
    if sv in ['PRSFC_1','PRSFC_2']:
      #addsize = 50
      #msizes = [51, 52, 53, 54, 55, 56]
      #nme_s = list(stats_all.loc[sv,'NME [%]'] + addsize)
      bm.scatter(x, y, s = 80, c = nmb, cmap='seismic', vmin = -10, vmax = 10)
      if sv=='PRSFC_1':
        plt.title('Pressure: UW WRF', fontsize = 20)
      if sv=='PRSFC_2':
        plt.title('Pressure: WSU WRF', fontsize = 20)  
    if sv in ['RH_1','RH_2']:
      #addsize = 30
      #msizes = [40, 50, 60, 70, 80]
      #nme_s = list(stats_all.loc[sv,'NME [%]'] + addsize)
      bm.scatter(x, y, s = 80, c = nmb, cmap='seismic', vmin = -100, vmax = 100)
      if sv=='RH_1':
        plt.title('Relative Humidity: UW WRF', fontsize = 20)
      if sv=='RH_2':
        plt.title('Relative Humidity: WSU WRF', fontsize = 20)  
    if sv in ['TEMP2_1','TEMP2_2']:
      #addsize = 30
      #msizes = [40, 50, 60, 70, 80]
      #nme_s = list(stats_all.loc[sv,'NME [%]'] + addsize)
      bm.scatter(x, y, s = 80, c = nmb, cmap='seismic', vmin = -70, vmax = 70)
      if sv=='TEMP2_1':
        plt.title('Temperature: UW WRF', fontsize = 20)
      if sv=='TEMP2_2':
        plt.title('Temperature: WSU WRF', fontsize = 20)  
    if sv in ['WD_1','WD_2','WS_1','WS_2']:
      #addsize = 10
      #msizes = [60, 110, 160, 210, 260]
      #nme_s = list(stats_all.loc[sv,'NME [%]'] + addsize)
      bm.scatter(x, y, s = 80, c = nmb, cmap='seismic', vmin = -500, vmax = 500)
      if sv=='WD_1':
        plt.title('Wind Direction: UW WRF', fontsize = 20)
      if sv=='WD_2':
        plt.title('Wind Direction: WSU WRF', fontsize = 20)  
      if sv=='WS_1':
        plt.title('Wind Speed: UW WRF', fontsize = 20)
      if sv=='WS_2':
        plt.title('Wind Speed: WSU WRF', fontsize = 20)  
    plt.title('%s Bias' %sv, fontsize = 18)
    plt.colorbar(label = 'NMB [%]', shrink = 0.75)
    

  
    for label, xpt, ypt in zip(label_few, x_few, y_few):
        plt.text(xpt + 20000, ypt - 10000, label, size=10, zorder=2, weight='bold')
    
    plt.show()
    fig4.savefig(outputdir + '%s_bias.png' %sv, bbox_inches='tight')
    
    
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

#df_combined_all = pd.DataFrame.from_dict(df_airpact, orient='index')


end_time = time.time()
print("Run time was %s seconds"%(round(end_time-begin_time)))

