# -*- coding: utf-8 -*-
"""
Program to compare AIRPACT 1.33km/4km to the Urbanova reference site
Created - 1/31/2018
"""

print('Start of Script')

#Import necessary libraries
import matplotlib as mpl
mpl.use('Agg')              #without this, errors in Aeolus may occur
import pandas as pd
import time
import datetime as dt
import numpy as np
from datetime import timedelta
import pytz
import copy
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from calendar import monthrange
pd.show_versions()

#Specify directories
#inputDir = '/data/lar/users/jmunson/'     # Aeolus
#air_path = '/data/airpact5/AIRRUN/'
#urb_path = '/data/lar/projects/Urbanova/'
#air_saved_path = '/data/airpact5/saved/'

inputDir = r'E:/Research/Urbanova_Jordan/Urbanova_ref_site_comparison'      #PC
air_path = inputDir + '/AIRPACT/'
urb_path = inputDir + '/Urbanova/'
air_saved_path = air_path

outputDir = inputDir +'/timeseries_plot'

#Set day/month/year
starttime = time.time()
day = '11'
month = '01'
year = '2018'

endday = '13'
endmonth = '01'
endyear = '2018'

#end_year=int(endyear)
#end_month=int(endmonth) 
#endday = str(monthrange(end_year, end_month)[1])  #Automatically finds last day of the month

begin_time = time.time()
# user-defined functions 

def naive_fast(latvar,lonvar,lat0,lon0):
    # Read latitude and longitude from file into numpy arrays
    latvals = latvar[:]
    lonvals = lonvar[:]
    ny,nx = latvals.shape
    dist_sq = (latvals-lat0)**2 + (lonvals-lon0)**2
    minindex_flattened = dist_sq.argmin()  # 1D index of min element
    iy_min,ix_min = np.unravel_index(minindex_flattened, latvals.shape)
    return int(iy_min),int(ix_min)

def readmodelmet(infile):
    metlist = ['PRSFC','PBL','HFX','TEMP2','WSPD10','WDIR10','RGRND', 'CFRAC']
    modelmet = {}
    for k in metlist:
        modelmet[k] = infile.variables[k][:-1,0,:,:] # 0 is for vertical layer & :-1 is to omit last value that is 25 hr
    return modelmet

def readmodelgas(infile):
    gaslist = ['NO','NO2','SO2','O3','ISOP','CO','NH3','FORM']
    modelgas = {}
    for k in gaslist:
        modelgas[k] = infile.variables[k][:,0,:,:]
    return modelgas

def readmodelaerosol(infile):
    aerlist = ['ASO4','ANO3','ANH4', 'AEC', 'APOC','PM']
    sizemode =['IJ']  # K is excluded for now. Adding K, this will be PM10 - AEC and POC don't have K mode though
    
    #soalist should be considered later. 
    modelaerosol = {}
    for k in aerlist:
        for i in sizemode:
            t=k+i
            if i == 'IJ':
                modelaerosol[k] = infile.variables[t][:,0,:,:]
            else:
                 modelaerosol[k] =  modelaerosol[k] +  infile.variables[t][:,0,:,:]

    return modelaerosol

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta
        
# Get dataframe to get lat/lon
latlon =  pd.read_csv(r'E:/Research/AIRPACT_eval/All_model-monitor_paired_daily_PM2.5_data.csv')
latlon = latlon.drop('date',axis=1)
latlon = latlon.drop('Parameter.Name',axis=1)
latlon = latlon.drop('Daily_mean_Conc',axis=1)
latlon = latlon.drop('AP4.PM2.5.Daily_mean_Conc',axis=1)

latlon = latlon.dropna()
latlon = latlon.drop_duplicates(subset = 'Sitename')

#Setup to pull AIRPACT data
start = dt.datetime(year=int(year), month=int(month), day=int(day), hour=0)
end = dt.datetime(year=int(endyear), month=int(endmonth), day=int(endday), hour=23)
timezone = pytz.timezone("utc") #("America/Los_Angeles")
start = timezone.localize(start)
end = timezone.localize(end)

#Site coordinates
inputlat = 47.6608
inputlon = -117.4044
#%%
print("Start date is "+ start.strftime("%Y%m%d") )


#Start of Function

def airpact(x):
    now=start
    
    # read grid information
    if x == '4km':
       modelgrid =  air_path +start.strftime("%Y")+ "/"+start.strftime("%Y%m%d")+ "00/MCIP37/GRIDCRO2D"
    if x == '1p33km':
       modelgrid = urb_path +start.strftime("%Y")+ "/"+start.strftime("%Y%m%d")+ "00/MCIP37/GRIDCRO2D"
    print(modelgrid)
    nc  = Dataset(modelgrid, 'r')
    lat = nc.variables['LAT'][0,0,:,:]
    lon = nc.variables['LON'][0,0,:,:]
    nc.close()
        
    # sample lat/lon grid information 
    iy,ix = naive_fast(lat, lon, inputlat, inputlon)
    print(iy,ix)
    # prepare time loop to read AIRPACT output
    date_diff =end -start
    date_diff =  int(round( date_diff.total_seconds()/60/60/24)) # total hour duration
    print('date_diff is '+str(date_diff))
 
    #empty array
    modelarray={} 
    # create a time array for modelarray 
    if x == '4km':
        timearray = np.empty( ( 24, 258, 285), '|U18') # Grid Coordinates
        lonarray = np.zeros ( (24,258,285) )
        latarray = np.zeros ( (24,258,285) )
    if x == '1p33km':
        timearray = np.empty( ( 24, 90, 90), '|U18') # Grid coordinates
        lonarray = np.zeros ( (24,90,90) )
        latarray = np.zeros ( (24,90,90) )
    # now is the time variable used in the for loop
    now = start
    for t in range(0, date_diff):
        # read combined 
        if x =='4km':
            modeloutput= air_saved_path +now.strftime("%Y")+ "/"+now.strftime("%m")+"/aconc/combined_" +  now.strftime("%Y%m%d") +".ncf"
        if x =='1p33km':
            modeloutput= urb_path +now.strftime("%Y")+ "/"+now.strftime("%Y%m%d")+"00/POST/CCTM/combined_" +  now.strftime("%Y%m%d") +".ncf"
        print(modeloutput)
        nc  = Dataset(modeloutput, 'r')
        # read MCIP files
        if x == '4km':
            modelmetin =  air_path +start.strftime("%Y")+ "/"+start.strftime("%Y%m%d")+ "00/MCIP37/METCRO2D"
        if x == '1p33km':
            modelmetin =  urb_path +start.strftime("%Y")+ "/"+start.strftime("%Y%m%d")+ "00/MCIP37/METCRO2D"
        print(modelmetin)
        mcip  = Dataset(modelmetin, 'r')
        #create time array for 24 hours
        dts = [dt.strftime('%Y%m%d %H:00 UTC') for dt in 
               datetime_range(now, now+timedelta(hours=24), 
                              timedelta(hours=1))]

        if t<=0: 
            # Read surface gas and aerosols concentrations from combined
            modelarray = readmodelgas(nc)
            modelaer = readmodelaerosol(nc)
            modelarray.update(modelaer) # combine gas and aerosols, so all tracers are in model
            
            modelmet = readmodelmet(mcip) # read mcip
            modelarray.update(modelmet) # add met variable to modelarray
        
            # add time variable to modelarray 
            for i in range(0, 24):
                timearray[i,:,:] = dts[i]
                latarray[i,:,:] = lat
                lonarray[i,:,:] = lon
                modelarray['datetime'] = copy.copy(timearray)  ## without copy.copy, this will become pointer
                modelarray['lat'] = latarray
                modelarray['lon']= lonarray       
        else:
        # add time variable to modelarray 
            for i in range(0, 24):
                timearray[i,:,:] = dts[i]

            modelarray['datetime'] = np.concatenate ( (modelarray['datetime'], timearray)) 
            modelarray['lat'] = np.concatenate ( (modelarray['lat'], latarray)) 
            modelarray['lon'] = np.concatenate ( (modelarray['lon'], lonarray))

            gas = readmodelgas(nc)
            #print(gas['NO'][0])
            aer = readmodelaerosol(nc)
            met = readmodelmet(mcip)
            gas.update(aer)
            gas.update(met)

            # loop over all keys excluding time 
            keys = set(modelarray.keys())
            excludes = set(['datetime','lat','lon'])

            for k in keys.difference(excludes): #modelarray.keys(): 
                modelarray[k] = np.concatenate((modelarray[k], gas[k]))

    # How to accumulate modelarray over time and skip missing days
        now += timedelta(hours=24)
      
#        try:
 #           modeloutput= urb_path +now.strftime("%Y")+ "/"+now.strftime("%Y%m%d")+"00/POST/CCTM/combined_" +  now.strftime("%Y%m%d") +".ncf"
  #          nc  = Dataset(modeloutput, 'r')
   #         modeloutput= air_saved_path +now.strftime("%Y")+ "/"+now.strftime("%m")+"/aconc/combined_" +  now.strftime("%Y%m%d") +".ncf"
    #        nc  = Dataset(modeloutput, 'r')
     #   except:
      #      print('adding 24 hours')
       #     now += timedelta(hours=24)
            
        #try:
         #   modeloutput= urb_path +now.strftime("%Y")+ "/"+now.strftime("%Y%m%d")+"00/POST/CCTM/combined_" +  now.strftime("%Y%m%d") +".ncf"
          #  nc  = Dataset(modeloutput, 'r')
           # modeloutput= air_saved_path +now.strftime("%Y")+ "/"+now.strftime("%m")+"/aconc/combined_" +  now.strftime("%Y%m%d") +".ncf"
            #nc  = Dataset(modeloutput, 'r')
        #except:
         #   print('adding another 24 hours')
          #  now += timedelta(hours=24)

        nc.close()
        mcip.close()

# delete unused variables
    del gas
    del aer
    del met
    del modelaer
    del modelmet
    del timearray
    del latarray
    del lonarray

    mod_sample = {}

    for k in modelarray.keys():      
        for Sitename in latlon:
              ix = latlon['XCell']
              iy = latlon['YCell']
        mod_sample[k] = modelarray[k][:,iy,ix].flatten() 
        #            model[k].append(modelarray[k][:,j,i ].flatten() )

    # convert model (iy,ix sampling data) to dataframe
    d1 = pd.DataFrame(mod_sample)

    # set a datetime column to index to better manipulate time series data
    d1['datetime'] = pd.to_datetime(d1['datetime'])
    d1 = d1.set_index('datetime') 

    return d1
#Run the function for 4km and then 1p33km
x='4km'
df = airpact(x)

#%%


























