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
#matplotlib.use('Agg')  # Uncomment this when using in Kamiak/Aeolus
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
#import wrf
import matplotlib.pyplot as plt
#from MesoPy import Meso
from matplotlib import dates
import time
import matplotlib.dates as mdates
starttime = time.time()
begin_time = time.time()
import matplotlib as mpl
 # Set a directory containing python scripts
#base_dir = "/data/lar/users/jmunson/longterm_airpact/"
base_dir = r'E:\Research\AIRPACT_eval\meteorology/'
aqs_dir = r'E:/Research/AIRPACT_eval/AQS_data/'
# set a directory to save output files
outputdir = base_dir + 'AQS_plots/'

# set a directory containing wrfout files
#datadir = base_dir + 'linked_days/'
datadir = r'E:\Research\Urbanova_Jordan\Urbanova_ref_site_comparison\AIRPACT\2018/'

# all the functions are saved in Met_functions_for_Ben.py
exec(open(r'E:\Research\scripts/AIRPACT_eval\meteorology/' +"Met_functions_for_Ben.py").read())
#print(base_dir +"Met_functions_for_Ben.py")

#df1 = pd.read_csv('airpact_met_200951_2012102.csv').drop(['Unnamed: 0'],axis=1)
#df2 = pd.read_csv('airpact_met_2012102_2016113.csv').drop(['Unnamed: 0'],axis=1)
#df3 = pd.read_csv('airpact_met_2016114_20161210.csv').drop(['Unnamed: 0'],axis=1)
#df4 = pd.read_csv('airpact_met_20161210_201871.csv').drop(['Unnamed: 0'],axis=1)

# The old df2 uses a 95x95 grid so will not work when combined. The grid cells will be off.

# Read the met data
df1 = pd.read_csv(base_dir + '/airpact_met_data/AQS/airpact_aqs_met_200951_2010818.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df2 = pd.read_csv(base_dir + '/airpact_met_data/AQS/airpact_aqs_met_201091_20121020.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df3 = pd.read_csv(base_dir + '/airpact_met_data/AQS/airpact_aqs_met_20121021_2013326.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df4 = pd.read_csv(base_dir + '/airpact_met_data/AQS/airpact_aqs_met_2013326_201471.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df5 = pd.read_csv(base_dir + '/airpact_met_data/AQS/airpact_aqs_met_201511_2016112.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df6 = pd.read_csv(base_dir + '/airpact_met_data/AQS/airpact_aqs_met_2016113_201711.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df7 = pd.read_csv(base_dir + '/airpact_met_data/AQS/airpact_aqs_met_201712_2017531.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df8 = pd.read_csv(base_dir + '/airpact_met_data/AQS/airpact_aqs_met_201761_201811.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df9 = pd.read_csv(base_dir + '/airpact_met_data/AQS/airpact_aqs_met_201812_2018814.csv').drop(['Unnamed: 0','ix','iy'],axis=1)

print('Met data read')

# Combine the met data
df_airpact = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9])

#df_airpact = pd.merge(df1,df2)

#df_list = [df1,df2,df3,df4]

#df_airpact = pd.concat(df_list)
df_airpact['DateTime'] = pd.to_datetime(df_airpact['DateTime'])
df_airpact['AQS_ID'] = df_airpact['AQS_ID'].astype(str)
print('Data concatenated')

#exec(open(base_dir + "/airpact_functions.py").read())

start_year = 2009    #2009
start_month = 5    #5
start_day = 1    #1

end_year = 2018   #2018
end_month = 7    #7
#end_day = monthrange(end_year, end_month)[1]
end_day = 1    #1

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
del([df1,df2,df3,df4,df5,df6,df7,df8,df9])

##############################################################################
# Read AQS data. csv's created from 'AQS_grabbing.py' script, and the model data from the previous lines of code
##############################################################################
# Read AQS data
df_wa = pd.read_csv(aqs_dir + 'AQS_data/Washington_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_or = pd.read_csv(aqs_dir + 'AQS_data/Oregon_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_id = pd.read_csv(aqs_dir + 'AQS_data/Idaho_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
#df_cc = pd.read_csv(aqs_dir + 'Canada_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_mt = pd.read_csv(aqs_dir + 'AQS_data/Montana_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_ca = pd.read_csv(aqs_dir + 'AQS_data/California_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_nv = pd.read_csv(aqs_dir + 'AQS_data/Nevada_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_ut = pd.read_csv(aqs_dir + 'AQS_data/Utah_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )

#df_wa_winds = pd.read_csv(base_dir + 'AQS_data/Washington_met_aqs_winds.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
#df_or_winds = pd.read_csv(base_dir + 'AQS_data/Oregon_met_aqs_winds.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
#df_id_winds = pd.read_csv(base_dir + 'AQS_data/Idaho_met_aqs_winds.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )

#  Combine AQS data
df_list = [df_wa,df_or,df_id,df_mt,df_ca,df_nv,df_ut]
df_obs = pd.concat(df_list)


#Create AQSID Column form state code, county code, and site num
df_obs['County Code'] = ["%03d" % n for n in df_obs['County Code'] ]
df_obs['Site Num'] = ["%04d" % n for n in df_obs['Site Num'] ]

df_obs['AQS_ID'] = (df_obs['State Code']).astype(str) + (df_obs['County Code']).astype(str)+(df_obs['Site Num']).astype(str)

# Drop columns of data we are not looking at so as to increase the speed of the script
df_obs = df_obs.drop(['Unnamed: 0','Unnamed: 1','State Name','County Name','State Code','County Code','Site Num','Units of Measure','Latitude','Longitude'],axis=1)
df_obs = df_obs.rename(columns={'Date Local_Time Local': 'datetime','Parameter Name':'Parameter_Name'})

# =============================================================================
# #Create AQSID Column form state code, county code, and site num
# aqsid = pd.read_csv(r'E:\Research\AIRPACT_eval/aqs_sites.csv')
# aqsid = aqsid.ix[:,['State Code','County Code','Site Number','Local Site Name','Location Setting']]
# 
# aqsid['County Code'] = ["%03d" % n for n in aqsid['County Code'] ]
# aqsid['Site Number'] = ["%04d" % n for n in aqsid['Site Number'] ]
# 
# aqsid['AQS_ID'] = (aqsid['State Code']).astype(str) + (aqsid['County Code']).astype(str)+(aqsid['Site Number']).astype(str)
# 
# # Must force every cell in AQSID to be a string, otherwise lose most of data
# aqsid['AQS_ID'] = aqsid['AQS_ID'].astype(str)
# =============================================================================
df_obs['AQS_ID'] = df_obs['AQS_ID'].astype(str)

#df_obs = pd.merge(df_obs,aqsid) # Merge df_mod and aqsid so as to add names and such to the datafram
df_obs = df_obs.drop(['State Code','County Code','Site Number'], axis=1)
print('Observed data read and combined')

# The obs data must be formatted so that the species are columns
df_obs_pres = df_obs.loc[(df_obs['Parameter_Name'] == 'Barometric pressure')].rename(columns={'Sample Measurement':'aqs_pressure'}).drop(['Parameter_Name'],axis=1)
df_obs_temp = df_obs.loc[(df_obs['Parameter_Name'] == 'Outdoor Temperature')].rename(columns={'Sample Measurement':'aqs_temp'}).drop(['Parameter_Name'],axis=1)
df_obs_rh = df_obs.loc[(df_obs['Parameter_Name'] == 'Relative Humidity ')].rename(columns={'Sample Measurement':'aqs_rh'}).drop(['Parameter_Name'],axis=1)
df_obs_wspd = df_obs.loc[(df_obs['Parameter_Name'] == 'Wind Speed - Resultant')].rename(columns={'Sample Measurement':'aqs_wspd'}).drop(['Parameter_Name'],axis=1)
df_obs_wdir = df_obs.loc[(df_obs['Parameter_Name'] == 'Wind Direction - Resultant')].rename(columns={'Sample Measurement':'aqs_wdir'}).drop(['Parameter_Name'],axis=1)

df_obs1 = pd.merge(df_obs_pres,df_obs_temp,how='outer')
df_obs = pd.merge(df_obs_wspd,df_obs_wdir,how='outer')
df_obs = pd.merge(df_obs,df_obs_rh,how='outer')
df_obs = pd.merge(df_obs,df_obs1,how='outer')

#df_obs2 = pd.concat([df_obs_pres,df_obs_temp,df_obs_rh,df_obs_wspd,df_obs_wdir],axis=1)
#df_com = pd.merge(df_obs, df_airpact, how='outer')


# =============================================================================
# # Create list of AQS_ID to run the for loop
# aqsid['AQS_ID']=aqsid['AQS_ID'].astype(str)
# site_list1= aqsid.loc[(aqsid['State Code'] == '16')]
# site_list2= aqsid.loc[(aqsid['State Code'] == '53')]
# site_list3= aqsid.loc[(aqsid['State Code'] == '41')]
# site_list=pd.concat([site_list1,site_list2,site_list3])
# site_list = site_list['AQS_ID'].tolist()
# stations = site_list
# =============================================================================

setting = ['URBAN AND CENTER CITY','SUBURBAN','RURAL']
# Save the data so that this process does not have to be done over and over again
#df_airpact.to_csv(base_dir+'/df_airpact.csv')
#df_obs.to_csv(base_dir+'/df_obs.csv')
#aqsid.to_csv(base_dir+'/aqsid_waorid.csv')
print('Data combined')

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
####################################
#########     AIRPACT     ##########
####################################
'''
if int(start.strftime('%Y%m%d')) < 20160425:
    grid = datadir + start.strftime('%Y%m%d')+'00/MCIP/GRIDCRO2D'
else:
    grid = datadir + start.strftime('%Y%m%d')+'00/MCIP37/GRIDCRO2D'
'''
# Delete the unecessary dataframes to avoid a memory error
#del([df_id,df_or,df_wa,df_obs_pres,df_obs_temp,df_obs_rh,df_obs1,df_obs_wspd,df_obs_wdir,df_id_winds,df_wa_winds,df_or_winds])
del(df_list)
grid = base_dir+'/2009050200/MCIP/GRIDCRO2D'
# open one of wrfout to read coordinate
modeloutputs = []

print(modeloutputs)
'''
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
'''
now=start

if int(start.strftime('%Y%m%d')) < 20160425:  
    #modeloutputs =  datadir + start.strftime('%Y%m%d')+'00/MCIP/METCRO2D'
    modeloutputs = base_dir+'/2009050200/MCIP/METCRO2D'
else:
    modeloutputs =  datadir + start.strftime('%Y%m%d')+'00/MCIP37/METCRO2D'
print(int(start.strftime('%Y%m%d')) < 20160425)
print(modeloutputs)
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

#%%
#stations = ['530090013']
'''
# Iterate over dictionary to make time series plots of each variable for each station
for i in stations:
    print('Attempting site '+str(i))
    # Locate correct site model data
    #df_mod1 = df_airpact.loc[(df_airpact['ix'] == ix1) & (df_airpact['iy'] == iy1)]
    df_mod1 = df_airpact.loc[(df_airpact['AQS_ID'] == str(i))]
    df_mod1 = df_mod1.reset_index(drop=True)
    
    # If there is no site data, this skips the site and moves to the next
    try:
        st_name = df_mod1.at[0,'site_name']
    except KeyError:
        continue
    
    df_h = df_obs.loc[(df_obs['AQS_ID'] == str(i))].rename(columns={'datetime':'date_time'})
    

    #df_com = pd.merge(df_mod1,df_h, how='outer')
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
    
    # Convert aqs data from F to C
    if 'aqs_temp' in df_h:
        df_h['aqs_temp'] = (df_h['aqs_temp']-32)*(5/9)
        
    #Try different way to create the dataframes, so as to retain all model data
    df_models=df_mod1
    df_models['TEMP2'] = df_models['TEMP2'] - 273.15
    df_models['PRSFC'] = df_models['PRSFC']/100
    df_models['rh1'] = rh_new1
    df_models = df_models.rename(columns = {'DateTime':'date_time','TEMP2':'TEMP2_1','PRSFC':'PRSFC_1','WSPD10':'WS_1','WDIR10':'WD_1','rh1':'RH_1'})
    
    # Create new data frame with all variables from WRF models
    #df_models = pd.DataFrame({'TEMP2_1': temp1, 'PRSFC_1': p1, 'WS_1': ws1, 'WD_1': wd1, 
     #                         'RH_1': rh_new1})#, 'PRECIP_1': df_mod1['RAINNC']})
    df_models = df_models.reset_index().drop(['index'],axis=1)
    
    df_models = df_models.set_index('date_time').drop(['ix','iy','lat','lon'],axis=1)  
    df_h = df_h.set_index('date_time').drop(['Local Site Name','AQS_ID'],axis=1)
    
    # Checks the size of the dataframes
    #mem_df_h=df_h.memory_usage(index=True).sum()
    #mem_df_models = df_models.memory_usage(index=True).sum()
    #print("df_h uses ",round(mem_df_h/ 1024**2)," MB")
    #print("df_models uses ",round(mem_df_models/ 1024**2)," MB")
    
    
    # Try and reset index so that concat can occur
    #df_models = df_models.reset_index()
    #df_h = df_h.reset_index()
    # Concatenating observation and model data frames
    #try:    # For some reason Portland, Portland International Airport throws this error "ValueError: Shape of passed values is (16, 103464), indices imply (16, 81096)", so this is my workaround
    #    df_all = pd.concat([df_models,df_h], axis=1)
    #    #df_all = df_h.join(df_models,how='outer')
    #except ValueError:
    #    continue
    df_all = pd.merge(df_models,df_h, how ='outer',left_index=True,right_index=True)

    # Select variables, specify labels, units and y-limits, and plot model 
    # variables based on MesoWest variable names
    new_list = ['aqs_temp','aqs_pressure','aqs_rh','aqs_wspd','aqs_wdir'] # Remember to add in winds here
    for w in new_list:
        var_name = str(w)
        
        # Skip variable if all values are zeros or NaNs
        if df_h[var_name].isnull().all()==True or all(df_h[var_name]==0):
            continue
        
        #var_units = mw_data['UNITS'][var_name]
        if var_name=='aqs_temp':
            var_name_mod1 = 'TEMP2_1'
            mod_var1 = temp1
 
            var_label = 'Temperature (C°)'
            var_units = 'C°'
            ymin = 0
            ymax = 40
            
        if var_name=='aqs_pressure':
            var_name_mod1 = 'PRSFC_1'
            mod_var1 = p1
            
            var_label = 'Pressure (mb)'
            var_units = 'mb'
            ymin = 850
            ymax = 1050
            
        if var_name=='aqs_wspd':
            var_name_mod1 = 'WS_1'
            mod_var1 = ws1
            
            var_label = 'Wind Speed (m/s)'
            var_units = 'm/s'
            ymin = 0
            ymax = 15
            
        if var_name=='aqs_wdir':  
            var_name_mod1 = 'WD_1'
            mod_var1 = wd1   
            
            var_label = 'Wind Direction (°)'
            var_units = '°'
            ymin = -1
            ymax = 1
            
        if var_name=='aqs_rh':
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
        #stats_T['lat'] = lat_mw
        #stats_T['lon'] = lon_mw
        stats_T['station ID'] = i
        
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
        dfmt = dates.DateFormatter('%Y')
        #dfmt = dates.DateFormatter('%m-%d')
        
        # Create a time series plot of a meteorological parameter
        fig1, ax = plt.subplots(figsize=(8, 4))

        #df_all = df_all.resample('D').mean()
        try:
            df_all = df_all.resample('M', convention='start').mean()
        except KeyError:
            pass
        
        # MesoWest observations
        if var_name == 'aqs_wdir':
            ax.plot(df_all.index,np.cos(df_all[var_name]*np.pi/180),c='k',label='Observations')
            # UW WRF model output        
            ax.plot(df_all.index,np.cos(df_all[var_name_mod1]*np.pi/180),c='b',label='Model')
            # WRF-Chem model output
            
            ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel='Cosine of Wind Direction',ylim=(ymin,ymax))
        else:
            ax.plot(df_all.index,df_all[var_name],c='k',label='Observations')
            # UW WRF model output        
            ax.plot(df_all.index,df_all[var_name_mod1],c='b',label='Model')
            # WRF-Chem model output
            
            ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel=var_label,ylim=(ymin,ymax))
            
        ax.set_xlim(str(start),str(end))
                    
        ax.xaxis.set_major_formatter(dfmt)
        fig1.autofmt_xdate(rotation=60)
        #df_all.plot(xticks=df_all.index)
        # Display r^2 on plot
        ax.text(1.15, 0.4,'$r^2$ = %s' %stats_T['R^2 [-]'][0], 
                 ha='center', va='center', transform=ax.transAxes)
        ax.text(1.15, 0.3,'RMSE= %s' %stats_T['RMSE [var units]'][0], 
                 ha='center', va='center', transform=ax.transAxes)
        
        ax.legend(loc='upper right', bbox_to_anchor=(1.27, 0.9))
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m')
        plt.show()
        
        fig1.savefig(outputdir + '/AQS/aqs_%s_%s_timeseries.png' %(st_name, var_name),bbox_inches='tight')
        plt.close()

    print(str(i) + ' plotted')

print('plots complete')    
'''
# =============================================================================
# df_airpact = df_airpact.drop(['lat','lon'],axis=1)
# df_airpact = pd.merge(df_airpact,aqsid).drop(['State Code','County Code','Site Number','Local Site Name'],axis=1)
# =============================================================================
#del(aqsid)
#%%
# =============================================================================
# stats_all = pd.DataFrame() # statistics for each station
# # Make Location Setting plots
# setting = ['URBAN AND CENTER CITY','SUBURBAN','RURAL']
# for i in setting:
#     print('Attempting setting '+str(i))
#     
#     # Locate correct site model data
#     df_mod1 = df_airpact.loc[(df_airpact['Location Setting'] == str(i))]
#     df_mod1 = df_mod1.reset_index(drop=True)
#     
#     # If there is no site data, this skips the site and moves to the next
#     try:
#         st_name = df_mod1.at[0,'Location Setting']
#     except KeyError:
#         continue
#     
#     df_h = df_obs.loc[(df_obs['Location Setting'] == str(i))].rename(columns={'datetime':'date_time'})
#     
# 
#     #df_com = pd.merge(df_mod1,df_h, how='outer')
#     #########################################################
#     ##########     CONVERT/CALCULATE VARIABLES     ##########
#     #########################################################
#     
#     # Convert temperature from K to C°
#     temp1 = df_mod1['TEMP2'] - 273.15 
#     
#     # Convert pressure from Pa to hPa (mb)
#     p1 = df_mod1['PRSFC'] / 100
#     
#     # Calculate wind speed from u and v components
#     
#     #u1 = df_mod1['U10']
#     #v1 = df_mod1['V10']
#     #ws1 = np.sqrt((u1**2)+(v1**2))
#     
#     ws1 = df_mod1['WSPD10']    # MCIP files record wind speed, no need to calculate
#     
#     # Calculate wind direction from u and v components 
#     
#     #wind_dir1 = np.arctan2(u1/ws1, v1/ws1) # Where wind is blowing TO
#     #wind_dir_degrees1 = wind_dir1 * 180/np.pi   
#     #wd1 = wind_dir_degrees1 + 180
#     
#     wd1 = df_mod1['WDIR10']    # MCIP files record wind speed, no need to calculate
#     
#     # Calculate 2-m (approximately) relative humidity using Q2, TEMP2, PRSFC, & constants
#     # Formula taken from:
#     # http://mailman.ucar.edu/pipermail/wrf-users/2012/002546.html
#     pq0 = 379.90516
#     a2 = 17.2693882
#     a3 = 273.16
#     a4 = 35.86
#     
#     rh1 = df_mod1['Q2'] / ( (pq0 / df_mod1['PRSFC']) * np.exp(a2 * 
#                    (df_mod1['TEMP2'] - a3) / (df_mod1['TEMP2'] - a4)) )
#     
#     rh_new1 = rh1 * 100 # convert from fraction to %    
#     #rh_new1  = df_mod1['Q2']/1000    #Do this to get the mixing ration instead of RH
#     # Convert aqs data from F to C
#     if 'aqs_temp' in df_h:
#         df_h['aqs_temp'] = (df_h['aqs_temp']-32)*(5/9)
#         
#     #Try different way to create the dataframes, so as to retain all model data
#     df_models=df_mod1
#     df_models['TEMP2'] = df_models['TEMP2'] - 273.15
#     df_models['PRSFC'] = df_models['PRSFC']/100
#     df_models['rh1'] = rh_new1
#     df_models = df_models.rename(columns = {'DateTime':'date_time','TEMP2':'TEMP2_1','PRSFC':'PRSFC_1','WSPD10':'WS_1','WDIR10':'WD_1','rh1':'RH_1'})
#     
#     # Create new data frame with all variables from WRF models
#     #df_models = pd.DataFrame({'TEMP2_1': temp1, 'PRSFC_1': p1, 'WS_1': ws1, 'WD_1': wd1, 
#      #                         'RH_1': rh_new1})#, 'PRECIP_1': df_mod1['RAINNC']})
#     df_models = df_models.reset_index().drop(['index'],axis=1)
#     
#     df_models = df_models.set_index('date_time').drop(['site_name'],axis=1)
#     df_h = df_h.set_index('date_time') #.drop(['Local Site Name'],axis=1)
#     
#     # Checks the size of the dataframes
#     #mem_df_h=df_h.memory_usage(index=True).sum()
#     #mem_df_models = df_models.memory_usage(index=True).sum()
#     #print("df_h uses ",round(mem_df_h/ 1024**2)," MB")
#     #print("df_models uses ",round(mem_df_models/ 1024**2)," MB")
#     
#     
#     # Try and reset index so that concat can occur
#     #df_models = df_models.reset_index()
#     #df_h = df_h.reset_index()
#     # Concatenating observation and model data frames
#     #try:    # For some reason Portland, Portland International Airport throws this error "ValueError: Shape of passed values is (16, 103464), indices imply (16, 81096)", so this is my workaround
#     #    df_all = pd.concat([df_models,df_h], axis=1)
#     #    #df_all = df_h.join(df_models,how='outer')
#     #except ValueError:
#     #    continue
#     
#     df_sitenum = df_h # Set this to later on determine number of sites
#     #Average the data monthly
#     df_models = df_models.resample('M', convention='start').mean()
#     df_h = df_h.resample('M', convention='start').mean()
#     
#     del(df_mod1)
#     df_all = pd.merge(df_models,df_h, how ='outer',left_index=True,right_index=True)
#     del(df_models)
#     
#     # Select variables, specify labels, units and y-limits, and plot model 
#     # variables based on MesoWest variable names
#     new_list = ['aqs_temp','aqs_pressure','aqs_rh','aqs_wspd','aqs_wdir'] # Remember to add in winds here
#     for w in new_list:
#         var_name = str(w)
#         
#         temp1 = df_sitenum.loc[(df_sitenum['Location Setting'] == i)]
#         temp1 = temp1.groupby(['Local Site Name']).count()
#         temp1 = len(temp1.index.get_level_values(0))
#         # Skip variable if all values are zeros or NaNs
#         if df_h[var_name].isnull().all()==True or all(df_h[var_name]==0):
#             continue
#         
#         #var_units = mw_data['UNITS'][var_name]
#         if var_name=='aqs_temp':
#             var_name_mod1 = 'TEMP2_1'
#             mod_var1 = temp1
#  
#             var_label = 'Temperature (C°)'
#             var_units = 'C°'
#             ymin = 0
#             ymax = 40
#             
#         if var_name=='aqs_pressure':
#             var_name_mod1 = 'PRSFC_1'
#             mod_var1 = p1
#             
#             var_label = 'Pressure (mb)'
#             var_units = 'mb'
#             ymin = 850
#             ymax = 1050
#             
#         if var_name=='aqs_wspd':
#             var_name_mod1 = 'WS_1'
#             mod_var1 = ws1
#             
#             var_label = 'Wind Speed (m/s)'
#             var_units = 'm/s'
#             ymin = 0
#             ymax = 6
#             
#         if var_name=='aqs_wdir':  
#             var_name_mod1 = 'WD_1'
#             mod_var1 = wd1   
#             
#             var_label = 'Wind Direction (°)'
#             var_units = '°'
#             ymin = -1
#             ymax = 1
#             
#         if var_name=='aqs_rh':
#             var_name_mod1 = 'RH_1'
#             mod_var1 = rh_new1   
#         
#             var_label = 'Relative Humidity (%)'
#             var_units = '%'
#             ymin = 0
#             ymax = 110
#             
#        # if var_name=='precip_accum':
#         #    var_name_mod1 = 'PRECIP_1'
#          #   mod_var1 = df_mod1['RAINNC']
#             
#           #  var_label = 'Precipitation Accumulated (mm)'
#            # var_units = 'mm'
#             #ymin = 0 
#             #ymax = 10 
#         
#         
#         ################################################
#         ##########     COMPUTE STATISTICS     ##########
#         ################################################
#         
#         var_units = 'var units'
#         
#         stats1 = met.stats(df_all, var_name_mod1, var_name, var_units)
#         stats1.loc['model'] = ['AIRPACT']
#         stats_combined = pd.concat([stats1],axis=1,join_axes=[stats1.index])
#         
#         stats_T = stats_combined.T # transpose index and columns
#         #stats_T['lat'] = lat_mw
#         #stats_T['lon'] = lon_mw
#         stats_T['station ID'] = i
#         
#         stats_all = stats_all.append(stats_T)
#         
#         # Fill data frame for computing overall statistics
#         if var_name not in df_overall.columns:
#             df_overall[[var_name_mod1,var_name]] \
#             = df_all[[var_name_mod1,var_name]]
#         else:
#             df_overall = df_overall.append(df_all[[var_name_mod1,
#                                                    var_name]],ignore_index=True)
#         
#         if var_name not in vname_obs:
#             vname_obs.append(var_name)
#             vname_1.append(var_name_mod1)
#             vlabel.append(var_label)
#         
#         ###################################
#         ##########     PLOTS     ##########
#         ###################################
#         # this is needed for x-axis label
#         dfmt = dates.DateFormatter('%Y')
#         #dfmt = dates.DateFormatter('%m-%d')
#         
#         # Create a time series plot of a meteorological parameter
#         fig1, ax = plt.subplots(figsize=(8, 4))
# 
#         '''
#         # MesoWest observations
#         if var_name == 'wind_direction':
#             ax.plot(df_h['date_time'],np.cos(df_h[var_name]*np.pi/180),c='k',label='Observations')
#             # UW WRF model output        
#             ax.plot(df_h['date_time'],np.cos(mod_var1*np.pi/180),c='b',label='Model')
#             # WRF-Chem model output
#             
#             ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel='Cosine of Wind Direction',ylim=(ymin,ymax))
#         else:
#             ax.plot(df_h['date_time'],df_h[var_name],c='k',label='Observations')
#             # UW WRF model output        
#             ax.plot(df_h['date_time'],mod_var1,c='b',label='Model')
#             # WRF-Chem model output
#             
#             ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel=var_label,ylim=(ymin,ymax))
#         '''
#         #df_all = df_all.resample('D').mean()
# 
#      
#         # MesoWest observations
#         if var_name == 'aqs_wdir':
#             ax.plot(df_all.index,np.cos(df_all[var_name]*np.pi/180),c='k',label='Observations')
#             # UW WRF model output        
#             ax.plot(df_all.index,np.cos(df_all[var_name_mod1]*np.pi/180),c='b',label='Model')
#             # WRF-Chem model output
#             
#             ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel='Cosine of Wind Direction',ylim=(ymin,ymax))
#         else:
#             ax.plot(df_all.index,df_all[var_name],c='k',label='Observations')
#             # UW WRF model output        
#             ax.plot(df_all.index,df_all[var_name_mod1],c='b',label='Model')
#             # WRF-Chem model output
#             
#             ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel=var_label,ylim=(ymin,ymax))
#             
#         ax.set_xlim(str(start),str(end))
#                     
#         ax.xaxis.set_major_formatter(dfmt)
#         fig1.autofmt_xdate(rotation=60)
#         #df_all.plot(xticks=df_all.index)
#         # Display r^2 on plot
#         ax.text(1.15, 0.4,'$r^2$ = %s' %stats_T['R^2 [-]'][0], 
#                  ha='center', va='center', transform=ax.transAxes)
#         ax.text(1.15, 0.3,'RMSE= %s' %stats_T['RMSE [var units]'][0], 
#                  ha='center', va='center', transform=ax.transAxes)
#         ax.text(1.15, 0.2,'# of sites '+str(temp1), 
#                  ha='center', va='center', transform=ax.transAxes)        # Plot number of sites
#         ax.legend(loc='upper right', bbox_to_anchor=(1.27, 0.9))
#         ax.fmt_xdata = mdates.DateFormatter('%Y-%m')
#         
#         yax = 0.02
#         yax2 = yax +0.011
#         size = 'medium'
#         # Create Airpact version change annotation
#         ax.annotate('AP3',xy=(0.09,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.2,yax2),color='red',size=size) # Left Arrow AP3
#         ax.annotate('AP3',xy=(0.33,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.2,yax2),color='red',size=size) # Right Arrow AP3
#  
#         ax.annotate('AP4',xy=(0.33,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.421,yax2),color='red',size=size) # Left Arrow AP4       
#         ax.annotate('AP4',xy=(0.512,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.421,yax2),color='red',size=size) # Right Arrow AP4
#         
#         ax.annotate('AP5',xy=(0.512,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.646,yax2),color='red',size=size) # Left Arrow AP5
#         ax.annotate('AP5',xy=(0.8,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.646,yax2),color='red',size=size) # Right Arrow AP5
#         '''
#         ax.annotate('AP3',xy=(0.09,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.235,yax2),color='red',size=size) # Left Arrow AP3
#         ax.annotate('AP3',xy=(0.405,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.235,yax2),color='red',size=size) # Right Arrow AP3
#         
#         ax.annotate('AP4',xy=(0.632,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.512,yax2),color='red',size=size) # Right Arrow AP4
#         ax.annotate('AP4',xy=(0.405,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.512,yax2),color='red',size=size) # Left Arrow AP4
#         
#         ax.annotate('AP5',xy=(0.632,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.78,yax2),color='red',size=size) # Left Arrow AP5
#         ax.annotate('AP5',xy=(0.94,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.78,yax2),color='red',size=size) # Right Arrow AP5
#         '''
#         # Add significant event annotations to plots
#         #ax.annotate('12km to 4km',xy=(0.405,0.75),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(0.405,.8),color='red',size='x-small') # Right Arrow AP3
#         
#         plt.show()
#         fig1.savefig(outputdir + '/time_series/type/aqs_%s_%s_timeseries_site.png' %(st_name, var_name),bbox_inches='tight')
#         plt.close()
#         
# 
#         
#         '''
#         # Create a scatter plot with linear regression lines and 
#         # correlation coefficients "r" (models vs. obs)
#         fig2, ax = plt.subplots(figsize=(6, 4.5))
#         
#         ax.scatter(df_h[var_name], mod_var1, s=50, c='b', label='UW WRF')
#         ax.scatter(df_h[var_name], mod_var2, s=50, c='r', label='WSU WRF')
#         ax.scatter(df_h[var_name], mod_var3, s=50, c='g', label='HRRR') 
#         
#         # Perform linear regression
#         m1, b1 = np.polyfit(df_h[var_name], mod_var1, deg=1)
#         m2, b2 = np.polyfit(df_h[var_name], mod_var2, deg=1)
#         m3, b3 = np.polyfit(df_h[var_name], mod_var3, deg=1)
#         
#         #ax.plot(df_h[var_name], m1*df_h[var_name] + b1, '--b', label='UW_WRF')
#         #ax.plot(df_h[var_name], m2*df_h[var_name] + b2, ':r', label='WRF-Chem')
#         #ax.plot(df_h[var_name], m3*df_h[var_name] + b3, '-.g', label='HRRR')
#         
#         
#         # Get correlation coefficients
#         cc1 = round(np.corrcoef(df_h[var_name], mod_var1)[0, 1],3)
#         cc2 = round(np.corrcoef(df_h[var_name], mod_var2)[0, 1],3)
#         cc3 = round(np.corrcoef(df_h[var_name], mod_var3)[0, 1],3)
#         
#         ax.text(1.15, 0.9,'UW WRF: r = %s' %cc1,  ha='center', 
#                 va='center', transform=ax.transAxes)
#         ax.text(1.15, 0.8,'WSU WRF: r = %s' %cc2,  ha='center', 
#                 va='center', transform=ax.transAxes)
#         ax.text(1.15, 0.7,'HRRR: r = %s' %cc3,  ha='center', 
#                 va='center', transform=ax.transAxes)
#         
#         
#         # Define x and y-limits
#         xy_min = min(np.nanmin(df_h[var_name]),np.nanmin(mod_var1),np.nanmin(mod_var2),np.nanmin(mod_var3))
#         xy_max = max(np.nanmax(df_h[var_name]),np.nanmax(mod_var1),np.nanmax(mod_var2),np.nanmax(mod_var3))
# 
#         # Add 1:1 line
#         ax.plot([xy_min,xy_max], [xy_min,xy_max], '-k', label = '1:1 line')
#         
#         ax.set(title=st_name,xlabel='Observed %s' %var_label,
#                ylabel='Predicted %s' %var_label,xlim=(xy_min,xy_max),ylim=(xy_min,xy_max))
#         ax.legend(loc='center right', bbox_to_anchor=(1.3, 0.5))
#         
#         plt.show()
#         fig2.savefig(outputdir + '%s_%s_regression.png' %(st_id, var_name),bbox_inches='tight')
#         '''
#     print(str(i) + ' plotted')
#     
#     #Create large dataframe with all the model data
#     #df_mod1 = df_mod1.reset_index(drop=True)
#     #site_name = pd.DataFrame([st_name],columns=['site_name'])
#     #df_mod2 = pd.concat([df_h,site_name], axis=1)
#     #df_mod2 = df_mod2.rename(columns={'date_time':'DateTime'})
#     #df_mod2.site_name = df_mod2.site_name.fillna(st_name)
#     #df_temp = pd.merge(df_mod1,df_mod2, on='DateTime', how='outer')
#     #df_met_all = pd.concat([df_met_all,df_temp])
#     
#     #ix1 = pd.concat([pd.DataFrame([ix1]),site_name], axis=1)
#     #iy1 = pd.concat([pd.DataFrame([iy1]),site_name], axis=1)
#     
#     #iy = iy.append(iy1)
#     #ix = ix.append(ix1)
#     #df_met_all = pd.concat([df_met_all,df_mod1])
# print('plots complete')    
# stats_all = stats_all.reset_index()
# stats_all.to_csv(base_dir+'/AQS_stats/aqs_stats.csv')
# =============================================================================
#%%
# Make plots and do stats for the different versions of AIRPACT (3,4,5)
versions = ['ap3','ap4','ap5'] #List versions
for version in versions:
    stats_all = pd.DataFrame() # statistics for each station

    for i in setting:
        print('Attempting setting '+str(i))
        
        # Set date range used based of versions
        if version == 'ap3':
            start_date ='2009-05-01'
            end_date = '2012-12-31'
        elif version == 'ap4':
            start_date ='2013-01-01'
            end_date = '2015-12-31'
        elif version == 'ap5':
            start_date ='2016-01-01'
            end_date = '2018-12-31'
            
        # Locate correct site model data
        mask = (df_airpact['DateTime'] > start_date) & (df_airpact['DateTime'] <= end_date) # Create a mask to determine the date range used
    
        df_mod1 = df_airpact.loc[mask]        
        df_mod1 = df_mod1.loc[(df_mod1['Location Setting'] == str(i))]
        df_mod1 = df_mod1.reset_index(drop=True)
        
        # If there is no site data, this skips the site and moves to the next
        try:
            st_name = str(df_mod1.at[0,'Location Setting']) + '_' + version
        except KeyError:
            continue
        
        df_h = df_obs.loc[(df_obs['Location Setting'] == str(i))].rename(columns={'datetime':'date_time'})
        
    
        #df_com = pd.merge(df_mod1,df_h, how='outer')
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
        #rh_new1  = df_mod1['Q2']/1000    #Do this to get the mixing ration instead of RH
        # Convert aqs data from F to C
        if 'aqs_temp' in df_h:
            df_h['aqs_temp'] = (df_h['aqs_temp']-32)*(5/9)
            
        #Try different way to create the dataframes, so as to retain all model data
        df_models=df_mod1
        df_models['TEMP2'] = df_models['TEMP2'] - 273.15
        df_models['PRSFC'] = df_models['PRSFC']/100
        df_models['rh1'] = rh_new1
        df_models = df_models.rename(columns = {'DateTime':'date_time','TEMP2':'TEMP2_1','PRSFC':'PRSFC_1','WSPD10':'WS_1','WDIR10':'WD_1','rh1':'RH_1'})
        
        # Create new data frame with all variables from WRF models
        #df_models = pd.DataFrame({'TEMP2_1': temp1, 'PRSFC_1': p1, 'WS_1': ws1, 'WD_1': wd1, 
         #                         'RH_1': rh_new1})#, 'PRECIP_1': df_mod1['RAINNC']})
        df_models = df_models.reset_index().drop(['index'],axis=1)
        
        df_models = df_models.set_index('date_time').drop(['site_name'],axis=1)
        df_h = df_h.set_index('date_time').drop(['Local Site Name'],axis=1)
        
        # Checks the size of the dataframes
        #mem_df_h=df_h.memory_usage(index=True).sum()
        #mem_df_models = df_models.memory_usage(index=True).sum()
        #print("df_h uses ",round(mem_df_h/ 1024**2)," MB")
        #print("df_models uses ",round(mem_df_models/ 1024**2)," MB")
        
        
        # Try and reset index so that concat can occur
        #df_models = df_models.reset_index()
        #df_h = df_h.reset_index()
        # Concatenating observation and model data frames
        #try:    # For some reason Portland, Portland International Airport throws this error "ValueError: Shape of passed values is (16, 103464), indices imply (16, 81096)", so this is my workaround
        #    df_all = pd.concat([df_models,df_h], axis=1)
        #    #df_all = df_h.join(df_models,how='outer')
        #except ValueError:
        #    continue
        
        #Average the data monthly
        df_models = df_models.resample('M', convention='start').mean()
        df_h = df_h.resample('M', convention='start').mean()
    
        del(df_mod1)
        df_all = pd.merge(df_models,df_h, how ='outer',left_index=True,right_index=True)
        del(df_models)
        
        # Select variables, specify labels, units and y-limits, and plot model 
        # variables based on MesoWest variable names
        new_list = ['aqs_temp','aqs_pressure','aqs_rh','aqs_wspd','aqs_wdir'] # Remember to add in winds here
        for w in new_list:
            var_name = str(w)
            
            # Skip variable if all values are zeros or NaNs
            if df_h[var_name].isnull().all()==True or all(df_h[var_name]==0):
                continue
            
            #var_units = mw_data['UNITS'][var_name]
            if var_name=='aqs_temp':
                var_name_mod1 = 'TEMP2_1'
                mod_var1 = temp1
     
                var_label = 'Temperature (C°)'
                var_units = 'C°'
                ymin = 0
                ymax = 40
                
            if var_name=='aqs_pressure':
                var_name_mod1 = 'PRSFC_1'
                mod_var1 = p1
                
                var_label = 'Pressure (mb)'
                var_units = 'mb'
                ymin = 850
                ymax = 1050
                
            if var_name=='aqs_wspd':
                var_name_mod1 = 'WS_1'
                mod_var1 = ws1
                
                var_label = 'Wind Speed (m/s)'
                var_units = 'm/s'
                ymin = 0
                ymax = 6
                
            if var_name=='aqs_wdir':  
                var_name_mod1 = 'WD_1'
                mod_var1 = wd1   
                
                var_label = 'Wind Direction (°)'
                var_units = '°'
                ymin = -1
                ymax = 1
                
            if var_name=='aqs_rh':
                var_name_mod1 = 'RH_1'
                mod_var1 = rh_new1   
            
                var_label = 'Relative Humidity (%)'
                var_units = '%'
                ymin = 0
                ymax = 110
                
           # if var_name=='precip_accum':
            #    var_name_mod1 = 'PRECIP_1'
             #   mod_var1 = df_mod1['RAINNC']
                
              #  var_label = 'Precipitation Accumulated (mm)'
               # var_units = 'mm'
                #ymin = 0 
                #ymax = 10 
            
            
            ################################################
            ##########     COMPUTE STATISTICS     ##########
            ################################################
            
            var_units = 'var units'
            
            stats1 = met.stats(df_all, var_name_mod1, var_name, var_units)
            stats1.loc['model'] = ['AIRPACT']
            stats_combined = pd.concat([stats1],axis=1,join_axes=[stats1.index])
            
            stats_T = stats_combined.T # transpose index and columns
            #stats_T['lat'] = lat_mw
            #stats_T['lon'] = lon_mw
            stats_T['station ID'] = i
            
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
            dfmt = dates.DateFormatter('%Y')
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
            #df_all = df_all.resample('D').mean()
    
         
            # MesoWest observations
            if var_name == 'aqs_wdir':
                ax.plot(df_all.index,np.cos(df_all[var_name]*np.pi/180),c='k',label='Observations')
                # UW WRF model output        
                ax.plot(df_all.index,np.cos(df_all[var_name_mod1]*np.pi/180),c='b',label='Model')
                # WRF-Chem model output
                
                ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel='Cosine of Wind Direction',ylim=(ymin,ymax))
            else:
                ax.plot(df_all.index,df_all[var_name],c='k',label='Observations')
                # UW WRF model output        
                ax.plot(df_all.index,df_all[var_name_mod1],c='b',label='Model')
                # WRF-Chem model output
                
                ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel=var_label,ylim=(ymin,ymax))
                
            ax.set_xlim(str(start),str(end))
                        
            ax.xaxis.set_major_formatter(dfmt)
            fig1.autofmt_xdate(rotation=60)
            #df_all.plot(xticks=df_all.index)
            # Display r^2 on plot
            ax.text(1.15, 0.4,'$r^2$ = %s' %stats_T['R^2 [-]'][0], 
                     ha='center', va='center', transform=ax.transAxes)
            ax.text(1.15, 0.3,'RMSE= %s' %stats_T['RMSE [var units]'][0], 
                     ha='center', va='center', transform=ax.transAxes)
            
            ax.legend(loc='upper right', bbox_to_anchor=(1.27, 0.9))
            ax.fmt_xdata = mdates.DateFormatter('%Y-%m')
            plt.show()
            
            fig1.savefig(outputdir + '/time_series/type/aqs_%s_%s_timeseries_site.png' %(st_name, var_name),bbox_inches='tight')
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
            
            ax.text(1.15, 0.9,'UW WRF: r = %s' %cc1,  ha='center', 
                    va='center', transform=ax.transAxes)
            ax.text(1.15, 0.8,'WSU WRF: r = %s' %cc2,  ha='center', 
                    va='center', transform=ax.transAxes)
            ax.text(1.15, 0.7,'HRRR: r = %s' %cc3,  ha='center', 
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
        print(str(i) + ' plotted')
        
        #Create large dataframe with all the model data
        #df_mod1 = df_mod1.reset_index(drop=True)
        #site_name = pd.DataFrame([st_name],columns=['site_name'])
        #df_mod2 = pd.concat([df_h,site_name], axis=1)
        #df_mod2 = df_mod2.rename(columns={'date_time':'DateTime'})
        #df_mod2.site_name = df_mod2.site_name.fillna(st_name)
        #df_temp = pd.merge(df_mod1,df_mod2, on='DateTime', how='outer')
        #df_met_all = pd.concat([df_met_all,df_temp])
        
        #ix1 = pd.concat([pd.DataFrame([ix1]),site_name], axis=1)
        #iy1 = pd.concat([pd.DataFrame([iy1]),site_name], axis=1)
        
        #iy = iy.append(iy1)
        #ix = ix.append(ix1)
        #df_met_all = pd.concat([df_met_all,df_mod1])
    stats_all = stats_all.reset_index()
    stats_all.to_csv(base_dir+'/AQS_stats/aqs_stats_%s.csv' %(version))
print('plots complete')    

#%%
# Make plots that cover all of airpact, regardless of site or type
setting =['total']
versions = ['ap3','ap4','ap5'] #List versions
df_airpact['tot'] = 'total'
df_obs['tot'] = 'total'
i='total'
stats_all = pd.DataFrame() # statistics for each station
for version in versions:

    print('Attempting setting '+str(i))
    
    # Set date range used based of versions
    if version == 'ap3':
        start_date ='2009-05-01'
        end_date = '2014-07-01'
    elif version == 'ap4':
        start_date ='2014-07-01'
        end_date = '2015-12-01'
    elif version == 'ap5':
        start_date ='2015-12-01'
        end_date = '2018-07-01'
        
    # Locate correct site model data
    mask = (df_airpact['DateTime'] > start_date) & (df_airpact['DateTime'] <= end_date) # Create a mask to determine the date range used

    df_mod1 = df_airpact.loc[mask]        
    df_mod1 = df_mod1.loc[(df_mod1['tot'] == str(i))]
    df_mod1 = df_mod1.reset_index(drop=True)
    df_mod1['version'] = version
    # If there is no site data, this skips the site and moves to the next
    try:
        st_name = str(df_mod1.at[0,'tot']) + '_' + version
    except KeyError:
        continue
    
    df_h = df_obs.loc[(df_obs['tot'] == str(i))].rename(columns={'datetime':'date_time'})
    

    #df_com = pd.merge(df_mod1,df_h, how='outer')
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
    
    #Q2 is the water vapor mixing ratio at 2m. kg/kg
    rh1 = df_mod1['Q2'] / ( (pq0 / df_mod1['PRSFC']) * np.exp(a2 * 
                   (df_mod1['TEMP2'] - a3) / (df_mod1['TEMP2'] - a4)) )
    
    rh_new1 = rh1 * 100 # convert from fraction to %    
    mix_ratio  = df_mod1['Q2']/1000    #Do this to get the mixing ration instead of RH in g/kg
    # Convert aqs data from F to C
    if 'aqs_temp' in df_h:
        df_h['aqs_temp'] = (df_h['aqs_temp']-32)*(5/9)
        
    #Try different way to create the dataframes, so as to retain all model data
    df_models=df_mod1
    df_models['TEMP2'] = df_models['TEMP2'] - 273.15
    df_models['PRSFC'] = df_models['PRSFC']/100
    df_models['rh1'] = rh_new1
    df_models['mix_ratio'] = mix_ratio
    df_models = df_models.rename(columns = {'DateTime':'date_time','TEMP2':'TEMP2_1','PRSFC':'PRSFC_1','WSPD10':'WS_1','WDIR10':'WD_1','rh1':'RH_1'})
    
    # Create new data frame with all variables from WRF models
    #df_models = pd.DataFrame({'TEMP2_1': temp1, 'PRSFC_1': p1, 'WS_1': ws1, 'WD_1': wd1, 
     #                         'RH_1': rh_new1})#, 'PRECIP_1': df_mod1['RAINNC']})
    df_models = df_models.reset_index().drop(['index'],axis=1)
    
    df_models = df_models.set_index('date_time').drop(['site_name'],axis=1)
    df_h = df_h.set_index('date_time').drop(['Local Site Name'],axis=1)
    
    # Checks the size of the dataframes
    #mem_df_h=df_h.memory_usage(index=True).sum()
    #mem_df_models = df_models.memory_usage(index=True).sum()
    #print("df_h uses ",round(mem_df_h/ 1024**2)," MB")
    #print("df_models uses ",round(mem_df_models/ 1024**2)," MB")
    
    
    # Try and reset index so that concat can occur
    #df_models = df_models.reset_index()
    #df_h = df_h.reset_index()
    # Concatenating observation and model data frames
    #try:    # For some reason Portland, Portland International Airport throws this error "ValueError: Shape of passed values is (16, 103464), indices imply (16, 81096)", so this is my workaround
    #    df_all = pd.concat([df_models,df_h], axis=1)
    #    #df_all = df_h.join(df_models,how='outer')
    #except ValueError:
    #    continue
    
    #Average the data monthly
    df_models = df_models.resample('M', convention='start').mean()
    df_h = df_h.resample('M', convention='start').mean()

    del(df_mod1)
    df_all = pd.merge(df_models,df_h, how ='outer',left_index=True,right_index=True)
    df_all['version'] = 'version'
    del(df_models)
    
    # Select variables, specify labels, units and y-limits, and plot model 
    # variables based on MesoWest variable names
    new_list = ['aqs_temp','aqs_pressure','aqs_rh','aqs_wspd','aqs_wdir'] # Remember to add in winds here
    for w in new_list:
        var_name = str(w)
        
        # Skip variable if all values are zeros or NaNs
        if df_h[var_name].isnull().all()==True or all(df_h[var_name]==0):
            continue
        
        #var_units = mw_data['UNITS'][var_name]
        if var_name=='aqs_temp':
            var_name_mod1 = 'TEMP2_1'
            mod_var1 = temp1
 
            var_label = 'Temperature (C°)'
            var_units = 'C°'
            ymin = 0
            ymax = 40
            
        if var_name=='aqs_pressure':
            var_name_mod1 = 'PRSFC_1'
            mod_var1 = p1
            
            var_label = 'Pressure (mb)'
            var_units = 'mb'
            ymin = 850
            ymax = 1050
            
        if var_name=='aqs_wspd':
            var_name_mod1 = 'WS_1'
            mod_var1 = ws1
            
            var_label = 'Wind Speed (m/s)'
            var_units = 'm/s'
            ymin = 0
            ymax = 6
            
        if var_name=='aqs_wdir':  
            var_name_mod1 = 'WD_1'
            mod_var1 = wd1   
            
            var_label = 'Wind Direction (°)'
            var_units = '°'
            ymin = -1
            ymax = 1
            
        if var_name=='aqs_rh':
            var_name_mod1 = 'RH_1'
            mod_var1 = rh_new1   
        
            var_label = 'Relative Humidity (%)'
            var_units = '%'
            ymin = 0
            ymax = 110
            
       # if var_name=='precip_accum':
        #    var_name_mod1 = 'PRECIP_1'
         #   mod_var1 = df_mod1['RAINNC']
            
          #  var_label = 'Precipitation Accumulated (mm)'
           # var_units = 'mm'
            #ymin = 0 
            #ymax = 10 
        
        
        ################################################
        ##########     COMPUTE STATISTICS     ##########
        ################################################
        
        var_units = 'var units'
        
        stats1 = met.stats(df_all, var_name_mod1, var_name, var_units)
        stats1.loc['model'] = ['AIRPACT']

        stats_combined = pd.concat([stats1],axis=1,join_axes=[stats1.index])
        
        stats_T = stats_combined.T # transpose index and columns
        #stats_T['lat'] = lat_mw
        #stats_T['lon'] = lon_mw
        stats_T['station ID'] = i
        stats_T['version'] = version
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
        dfmt = dates.DateFormatter('%Y')
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
        #df_all = df_all.resample('D').mean()

     
        # MesoWest observations
        if var_name == 'aqs_wdir':
            ax.plot(df_all.index,np.cos(df_all[var_name]*np.pi/180),c='k',label='Observations')
            # UW WRF model output        
            ax.plot(df_all.index,np.cos(df_all[var_name_mod1]*np.pi/180),c='b',label='Model')
            # WRF-Chem model output
            
            ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel='Cosine of Wind Direction',ylim=(ymin,ymax))
        else:
            ax.plot(df_all.index,df_all[var_name],c='k',label='Observations')
            # UW WRF model output        
            ax.plot(df_all.index,df_all[var_name_mod1],c='b',label='Model')
            # WRF-Chem model output
            
            ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel=var_label,ylim=(ymin,ymax))
            
        ax.set_xlim(str(start),str(end))
                    
        ax.xaxis.set_major_formatter(dfmt)
        fig1.autofmt_xdate(rotation=60)
        #df_all.plot(xticks=df_all.index)
        # Display r^2 on plot
        ax.text(1.15, 0.4,'$r^2$ = %s' %stats_T['R^2 [-]'][0], 
                 ha='center', va='center', transform=ax.transAxes)
        ax.text(1.15, 0.3,'RMSE= %s' %stats_T['RMSE [var units]'][0], 
                 ha='center', va='center', transform=ax.transAxes)
        
        ax.legend(loc='upper right', bbox_to_anchor=(1.27, 0.9))
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m')
        #plt.show()
        
        fig1.savefig(outputdir + '/time_series/type/aqs_%s_%s_total_timeseries.png' %(st_name, var_name),bbox_inches='tight')
        plt.show()
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
        
        ax.text(1.15, 0.9,'UW WRF: r = %s' %cc1,  ha='center', 
                va='center', transform=ax.transAxes)
        ax.text(1.15, 0.8,'WSU WRF: r = %s' %cc2,  ha='center', 
                va='center', transform=ax.transAxes)
        ax.text(1.15, 0.7,'HRRR: r = %s' %cc3,  ha='enter', 
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
    print(str(i) + ' plotted')
    
    #Create large dataframe with all the model data
    #df_mod1 = df_mod1.reset_index(drop=True)
    #site_name = pd.DataFrame([st_name],columns=['site_name'])
    #df_mod2 = pd.concat([df_h,site_name], axis=1)
    #df_mod2 = df_mod2.rename(columns={'date_time':'DateTime'})
    #df_mod2.site_name = df_mod2.site_name.fillna(st_name)
    #df_temp = pd.merge(df_mod1,df_mod2, on='DateTime', how='outer')
    #df_met_all = pd.concat([df_met_all,df_temp])
    
    #ix1 = pd.concat([pd.DataFrame([ix1]),site_name], axis=1)
    #iy1 = pd.concat([pd.DataFrame([iy1]),site_name], axis=1)
    
    #iy = iy.append(iy1)
    #ix = ix.append(ix1)
    #df_met_all = pd.concat([df_met_all,df_mod1])
stats_all = stats_all.reset_index()
stats_all.to_csv(base_dir+'/AQS_stats/aqs_stats_%s.csv' %('total'))
    
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
    
    writer = pd.ExcelWriter(outputdir + 'stats' + '_' + start.strftime('%Y%m%d')  + '-' +  end.strftime('%Y%m%d') + '.xlsx')
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
#%%
stats_all = pd.DataFrame() # statistics for each station
# Make Location Setting plots
setting = ['URBAN AND CENTER CITY','SUBURBAN','RURAL']

print('Attempting setting '+str(i))

# Locate correct site model data
#df_mod1 = df_airpact.loc[(df_airpact['Location Setting'] == str(i))]
df_mod1 = df_airpact
df_mod1 = df_mod1.reset_index(drop=True)

df_h = df_obs.rename(columns={'datetime':'date_time'})

#df_com = pd.merge(df_mod1,df_h, how='outer')
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
#rh_new1  = df_mod1['Q2']/1000    #Do this to get the mixing ration instead of RH
# Convert aqs data from F to C
if 'aqs_temp' in df_h:
    df_h['aqs_temp'] = (df_h['aqs_temp']-32)*(5/9)
    
#Try different way to create the dataframes, so as to retain all model data
df_models=df_mod1
df_models['TEMP2'] = df_models['TEMP2'] - 273.15
df_models['PRSFC'] = df_models['PRSFC']/100
df_models['rh1'] = rh_new1
df_models = df_models.rename(columns = {'DateTime':'date_time','TEMP2':'TEMP2_1','PRSFC':'PRSFC_1','WSPD10':'WS_1','WDIR10':'WD_1','rh1':'RH_1'})

# Create new data frame with all variables from WRF models
#df_models = pd.DataFrame({'TEMP2_1': temp1, 'PRSFC_1': p1, 'WS_1': ws1, 'WD_1': wd1, 
 #                         'RH_1': rh_new1})#, 'PRECIP_1': df_mod1['RAINNC']})
df_models = df_models.reset_index().drop(['index'],axis=1)

df_models = df_models.set_index('date_time').drop(['site_name'],axis=1)
df_h = df_h.set_index('date_time') #.drop(['Local Site Name'],axis=1)

# Checks the size of the dataframes
#mem_df_h=df_h.memory_usage(index=True).sum()
#mem_df_models = df_models.memory_usage(index=True).sum()
#print("df_h uses ",round(mem_df_h/ 1024**2)," MB")
#print("df_models uses ",round(mem_df_models/ 1024**2)," MB")


# Try and reset index so that concat can occur
#df_models = df_models.reset_index()
#df_h = df_h.reset_index()
# Concatenating observation and model data frames
#try:    # For some reason Portland, Portland International Airport throws this error "ValueError: Shape of passed values is (16, 103464), indices imply (16, 81096)", so this is my workaround
#    df_all = pd.concat([df_models,df_h], axis=1)
#    #df_all = df_h.join(df_models,how='outer')
#except ValueError:
#    continue

df_sitenum = df_h # Set this to later on determine number of sites
#Average the data monthly
df_models = df_models.resample('M', convention='start').mean()
df_h = df_h.resample('M', convention='start').mean()

del(df_mod1)
df_all = pd.merge(df_models,df_h, how ='outer',left_index=True,right_index=True)
del(df_models)

# Select variables, specify labels, units and y-limits, and plot model 
# variables based on MesoWest variable names
new_list = ['aqs_temp','aqs_pressure','aqs_rh','aqs_wspd']#,'aqs_wdir'] # Remember to add in winds here
for w in new_list:
    var_name = str(w)
    
    temp1 = df_sitenum
    temp1 = temp1.groupby(['Local Site Name']).count()
    temp1 = len(temp1.index.get_level_values(0))
    # Skip variable if all values are zeros or NaNs
    if df_h[var_name].isnull().all()==True or all(df_h[var_name]==0):
        continue
    
    #var_units = mw_data['UNITS'][var_name]
    if var_name=='aqs_temp':
        var_name_mod1 = 'TEMP2_1'
        mod_var1 = temp1
        st_name = 'AIRPACT Monthly Temperature'
 
        var_label = 'Temperature (C°)'
        var_units = 'C°'
        ymin = 0
        ymax = 40
        
    if var_name=='aqs_pressure':
        var_name_mod1 = 'PRSFC_1'
        mod_var1 = p1
        st_name = 'AIRPACT Monthly Pressure'
        
        var_label = 'Pressure (mb)'
        var_units = 'mb'
        ymin = 850
        ymax = 1050
        
    if var_name=='aqs_wspd':
        var_name_mod1 = 'WS_1'
        mod_var1 = ws1
        st_name = 'AIRPACT Monthly Wind Speed'
        
        var_label = 'Wind Speed (m/s)'
        var_units = 'm/s'
        ymin = 0
        ymax = 6
        
    if var_name=='aqs_wdir':  
        var_name_mod1 = 'WD_1'
        mod_var1 = wd1   
        st_name = 'AIRPACT Monthly Wind Direction'

        var_label = 'Wind Direction (°)'
        var_units = '°'
        ymin = -1
        ymax = 1
        
    if var_name=='aqs_rh':
        var_name_mod1 = 'RH_1'
        mod_var1 = rh_new1   
        st_name = 'AIRPACT Monthly Relative Humidity'
        
        var_label = 'Relative Humidity (%)'
        var_units = '%'
        ymin = 0
        ymax = 110
        
   # if var_name=='precip_accum':
    #    var_name_mod1 = 'PRECIP_1'
     #   mod_var1 = df_mod1['RAINNC']
        
      #  var_label = 'Precipitation Accumulated (mm)'
       # var_units = 'mm'
        #ymin = 0 
        #ymax = 10 
    
    
    ################################################
    ##########     COMPUTE STATISTICS     ##########
    ################################################
    
    var_units = 'var units'
    
    stats1 = met.stats(df_all, var_name_mod1, var_name, var_units)
    stats1.loc['model'] = ['AIRPACT']
    stats_combined = pd.concat([stats1],axis=1,join_axes=[stats1.index])
    
    stats_T = stats_combined.T # transpose index and columns
    #stats_T['lat'] = lat_mw
    #stats_T['lon'] = lon_mw

    
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
    dfmt = dates.DateFormatter('%Y')
    #dfmt = dates.DateFormatter('%m-%d')
    
    # Create a time series plot of a meteorological parameter
    fig1, ax = plt.subplots(figsize=(8, 5))

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
    #df_all = df_all.resample('D').mean()

 
    # MesoWest observations
    if var_name == 'aqs_wdir':
        ax.plot(df_all.index,np.cos(df_all[var_name]*np.pi/180),c='k',label='Observations')
        # UW WRF model output        
        ax.plot(df_all.index,np.cos(df_all[var_name_mod1]*np.pi/180),c='b',label='Model')
        # WRF-Chem model output
        
        ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel='Cosine of Wind Direction',ylim=(ymin,ymax))
    else:
        ax.plot(df_all.index,df_all[var_name],c='k',label='Observations')
        # UW WRF model output        
        ax.plot(df_all.index,df_all[var_name_mod1],c='b',label='Model')
        # WRF-Chem model output
        
        ax.set(title=st_name,xlabel='Date / Time (UTC)',ylabel=var_label,ylim=(ymin,ymax))
        
    ax.set_xlim(str(start),str(end))
                
    ax.xaxis.set_major_formatter(dfmt)
    fig1.autofmt_xdate(rotation=25)
    #df_all.plot(xticks=df_all.index)
    # Display r^2 on plot
    ax.text(1.17, 0.44,'$r^2$ = %s' %stats_T['R^2 [-]'][0], 
             ha='center', va='center', transform=ax.transAxes)
    ax.text(1.17, 0.32,'RMSE= %s' %stats_T['RMSE [var units]'][0], 
             ha='center', va='center', transform=ax.transAxes)
    ax.text(1.17, 0.2,'# of sites '+str(temp1), 
             ha='center', va='center', transform=ax.transAxes)        # Plot number of sites
    ax.legend(loc='upper right',fontsize=16, bbox_to_anchor=(1.4, 0.9))
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m')
    
    yax = 0.015
    yax2 = yax +0.015
    size = 'medium'
    
    mod = 0.05
    
    xax1 = .2-mod
    xax2 = .421-mod
    xax3 = .646-mod
    
    xax4 = 0.33-mod
    xax5 = 0.512-mod
    xax6 = 0.8-mod
    
    
    # Create Airpact version change annotation
    ax.annotate('AP3',xy=(0.09,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(xax1,yax2),color='red',size=size) # Left Arrow AP3
    ax.annotate('AP3',xy=(xax4,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(xax1,yax2),color='red',size=size) # Right Arrow AP3
 
    ax.annotate('AP4',xy=(xax4,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(xax2,yax2),color='red',size=size) # Left Arrow AP4       
    ax.annotate('AP4',xy=(xax5,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(xax2,yax2),color='red',size=size) # Right Arrow AP4
    
    ax.annotate('AP5',xy=(xax5,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(xax3,yax2),color='red',size=size) # Left Arrow AP5
    ax.annotate('AP5',xy=(xax6,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(xax3,yax2),color='red',size=size) # Right Arrow AP5
    '''
    ax.annotate('AP3',xy=(0.09,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.235,yax2),color='red',size=size) # Left Arrow AP3
    ax.annotate('AP3',xy=(0.405,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.235,yax2),color='red',size=size) # Right Arrow AP3
    
    ax.annotate('AP4',xy=(0.632,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.512,yax2),color='red',size=size) # Right Arrow AP4
    ax.annotate('AP4',xy=(0.405,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.512,yax2),color='red',size=size) # Left Arrow AP4
    
    ax.annotate('AP5',xy=(0.632,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.78,yax2),color='red',size=size) # Left Arrow AP5
    ax.annotate('AP5',xy=(0.94,yax),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(.78,yax2),color='red',size=size) # Right Arrow AP5
    '''
    # Add significant event annotations to plots
    #ax.annotate('12km to 4km',xy=(0.405,0.75),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(0.405,.8),color='red',size='x-small') # Right Arrow AP3
    ax.set_xlabel('')
    plt.show()
    fig1.savefig(outputdir + '/time_series/type/aqs_%s_timeseries_site.png' %(var_name),bbox_inches='tight')
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
    
    ax.text(1.15, 0.9,'UW WRF: r = %s' %cc1,  ha='center', 
            va='center', transform=ax.transAxes)
    ax.text(1.15, 0.8,'WSU WRF: r = %s' %cc2,  ha='center', 
            va='center', transform=ax.transAxes)
    ax.text(1.15, 0.7,'HRRR: r = %s' %cc3,  ha='center', 
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
#df_mod1 = df_mod1.reset_index(drop=True)
#site_name = pd.DataFrame([st_name],columns=['site_name'])
#df_mod2 = pd.concat([df_h,site_name], axis=1)
#df_mod2 = df_mod2.rename(columns={'date_time':'DateTime'})
#df_mod2.site_name = df_mod2.site_name.fillna(st_name)
#df_temp = pd.merge(df_mod1,df_mod2, on='DateTime', how='outer')
#df_met_all = pd.concat([df_met_all,df_temp])

#ix1 = pd.concat([pd.DataFrame([ix1]),site_name], axis=1)
#iy1 = pd.concat([pd.DataFrame([iy1]),site_name], axis=1)

#iy = iy.append(iy1)
#ix = ix.append(ix1)
#df_met_all = pd.concat([df_met_all,df_mod1])
print('plots complete')    
stats_all = stats_all.reset_index()
stats_all.to_csv(base_dir+'/AQS_stats/aqs_stats.csv')
#%%
# List how many sites are used for each type
temp1 = df_obs.loc[(df_obs['Location Setting'] == 'RURAL')].rename(columns={'Location Setting': 'type'})
temp2 = df_obs.loc[(df_obs['Location Setting'] == 'SUBURBAN')].rename(columns={'Location Setting': 'type'})
temp3 = df_obs.loc[(df_obs['Location Setting'] == 'URBAN AND CENTER CITY')].rename(columns={'Location Setting': 'type'})

temp1 = temp1['Local Site Name'].unique()
temp2 = temp2['Local Site Name'].unique()
temp3 = temp3['Local Site Name'].unique()

end_time = time.time()
print("Run time was %s minutes"%(round((end_time-begin_time)/60)))

