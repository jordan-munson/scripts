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
#datadir = r'E:/Research/AIRPACT_eval/meteorology/example_met_days/'    # Actual data for plotting
#datadir = r'E:/Research/Urbanova_Jordan/Urbanova_ref_site_comparison/AIRPACT/2018/'    # test days
# all the functions are saved in Met_functions_for_Ben.py
exec(open(base_dir +"Met_functions_for_Ben.py").read())
print(base_dir +"Met_functions_for_Ben.py")

#exec(open(base_dir + "/airpact_functions.py").read())
'''
start_year = 2009    #2009
start_month = 5    #5
start_day = 1    #1

end_year = 2010
end_month = 8    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 18    #15

start_year = 2010    #2009
start_month = 9    #5
start_day = 1    #1

end_year = 2014
end_month = 7    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 1    #15

start_year = 2013    #2009
start_month = 3    #5
start_day = 26    #1

end_year = 2014
end_month = 7    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 1    #15

start_year = 2015    #2009
start_month = 1    #5
start_day = 11    #1

end_year = 2016
end_month = 12    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 10    #15

start_year = 2016    #2009
start_month = 12    #5
start_day = 11    #1

end_year = 2018
end_month = 8    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 1    #15

# Start of redesigned days

start_year = 2010    #2009
start_month = 9    #5
start_day = 1    #1

end_year = 2012
end_month = 10    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 20    #15

start_year = 2015    #2009
start_month = 1    #5
start_day = 1    #1

end_year = 2016
end_month = 1    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 12    #15

# Missing section of time here I accidently didnt put here, but I did run it.
'''
start_year = 2017    #2009
start_month = 1    #5
start_day = 2    #1

end_year = 2017
end_month = 5    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 31    #15
'''
start_year = 2018    #2009
start_month = 1    #5
start_day = 2    #1

end_year = 2018
end_month = 8    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 14    #15

start_year = 2017    #2009
start_month = 6    #5
start_day = 1    #1

end_year = 2018
end_month = 1    #8
#end_day = monthrange(end_year, end_month)[1]
end_day = 1    #15
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


df_latlon = pd.read_csv(base_dir+'aqs_latlon.csv').drop(['Unnamed: 0'],axis=1).rename(columns={'XCell':'ix','YCell':'iy','Sitename':'site_name'})

print('Starting airpact function')

#run airpact function
df_airpact = get_wrf_DF(datadir, start, end, x_dim, y_dim, lat, lon, layer)
df_airpact = df_airpact.reset_index().drop(['index'],axis=1)

# Add site names to the rows
df_airpact['iy'] = pd.to_numeric(df_airpact['iy'])
df_airpact['ix'] = pd.to_numeric(df_airpact['ix'])
#df_airpact1 = pd.concat([df_airpact,df_latlon], axis=1)
df_airpact = pd.merge(df_airpact,df_latlon).drop(['Latitude','Longitude'],axis=1) #Drop lat and lon values from sites. The lat lon info remaining are the points in the grid from airpact

#print(df_airpact.keys())
#print(df_airpact['DateTime'].shape)
#print(df_airpact['TEMP2'].shape)
#print(df_airpact['Q2'].shape)
#print(df_airpact['lat'].shape)
#print(df_airpact['lon'].shape)

print("Dictionary is done")
size=df_airpact.memory_usage(deep=True).sum()
if size < 20000000000:
    df_airpact.to_csv(base_dir +'/airpact_aqs_met_'+str(start_year)+str(start_month)+str(start_day)+'_'+str(end_year)+str(end_month)+str(end_day)+'.csv')   #Theoretically, this file should be about 1.7 GB for all the data
    print('Meteorology data saved')
else:
    print('Met file too large, not saved')
    pass

