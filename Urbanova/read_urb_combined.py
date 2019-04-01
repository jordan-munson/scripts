# -*- coding: utf-8 -*-
"""
Created on Nov 11, 2017

@author: yunhalee
Description - extract model output tracers, and run a machine learning 

"""
#%%
# import necessary modules
import numpy as np
from netCDF4 import Dataset
import datetime
import pickle
from datetime import timedelta
import pytz
import copy
 
# =============================================================================
# Functions the main script uses
# =============================================================================
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
    metlist = ['PRSFC','PBL','HFX','QFX','TEMP2','WSPD10','WDIR10','RGRND', 'CFRAC']
    modelmet = {}
    for k in metlist:
        modelmet[k] = infile.variables[k][:-1,0,:,:] # 0 is for vertical layer & :-1 is to omit last value
    return modelmet

def readmodelgas(infile):
    gaslist = ['PMIJ','NO2','SO2','O3','ISOP','CO','FORM']
    modelgas = {}
    for k in gaslist:
        modelgas[k] = infile.variables[k][:,0,:,:]
    return modelgas

def readmodelaerosol(infile):
    aerlist = ['ASO4','ANO3','ANH4', 'AEC', 'APOC']
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
      
#Main program starts here
inoutputDir    = '/data/lar/projects/Urbanova/'
outputDir = '/data/lar/users/jmunson/'

# =============================================================================
# inoutputDir = r'E:/Research/Urbanova_Jordan/Urbanova_ref_site_comparison/Urbanova/'
# outputDir = r'E:/Research/Urbanova_Jordan/'
# =============================================================================

start = datetime.datetime(year=2018, month=1, day=11, hour=0)
end = datetime.datetime(year=2018, month=12, day=31, hour=23)

# Urbanova dimensions are 90x90. Change if for AIRPACT
x_dim = 90
y_dim = 90

timezone = pytz.timezone("utc") #("America/Los_Angeles")
start = timezone.localize(start)
end = timezone.localize(end)
# in order to convert the time zone: start.astimezone(pytz.timezone("America/Los_Angeles")) 
inputlat=40
inputlon=-120


# read grid information
modelgrid = inoutputDir +start.strftime("%Y")+'/'+start.strftime("%Y%m%d")+"00/MCIP37/GRIDCRO2D"
nc  = Dataset(modelgrid, 'r')
lat = nc.variables['LAT'][0,0,:,:]
lon = nc.variables['LON'][0,0,:,:]
nc.close()
        
# sample lat/lon grid information 
iy,ix = naive_fast(lat, lon, inputlat, inputlon)


# prepare time loop to read AIRPACT output
date_diff =end -start
date_diff =  int(round( date_diff.total_seconds()/60/60/24)) # total hour duration

print("start date is "+ start.strftime("%Y%m%d") )

modelarray={}
hr=(end-start).total_seconds()/3600+1
hr=int(hr)

timearray = np.empty( ( int(24), y_dim, x_dim), '|U18')
     
# empty array
lonarray = {}
latarray = {}
hours = 0
modelarray={} 
modelarraytime={} 
modelarraylatlon = {}
model = {}
model['lat'] =  inputlat
model['lon'] =  inputlon
# now is the time variable used in the for loop
now = start
modelarraytime['DateTime'] = copy.copy(timearray)
#%%
for t in range(0, date_diff):
    print(t)
    # read combined 
    modeloutput= inoutputDir +now.strftime("%Y")+'/'+now.strftime("%Y%m%d")+"00/POST/CCTM/combined_" +  now.strftime("%Y%m%d") +".ncf"
    
    try:
        nc  = Dataset(modeloutput, 'r')
    except FileNotFoundError:
        now += timedelta(hours=24)
        continue
    print(modeloutput)
    #create time array for 24 hours
    dts = [dt.strftime('%Y%m%d %H:00 PST') for dt in 
           datetime_range(now, now+timedelta(hours=24), 
                          timedelta(hours=1))]
    
    
    if t<=0: 
        # Read surface gas and aerosols concentrations from combined
        modelarray = readmodelgas(nc)
        modelaer = readmodelaerosol(nc)
        modelarray.update(modelaer) # combine gas and aerosols, so all tracers are in model
        
        model['time'] = dts    
        
        # Run time loop that creates the first days dictionary of times
        for i in range(0, 24):
            timearray[i,:,:] = dts[int(i)]
            hours = hours+1

        modelarraytime['DateTime'] = copy.copy(timearray) # creates first days time. Needs copy.copy
    
        #for k in modelarray.keys(): 
        #    model[k] = modelarray[k][:,0, iy,ix]
            
    else:
        # Runs the different species grabbers and combines into a single thing
        gas = readmodelgas(nc)
        aer = readmodelaerosol(nc)
        gas.update(aer)
        
        # Run time loop that creates every other days time
        for i in range(0, 24):
            timearray[i,:,:] = dts[int(i)]
            hours = hours+1

        modelarraytime['DateTime'] = np.concatenate ( (modelarraytime['DateTime'], timearray))  # adds time values to array
            
        #gas.update(modelarraytime)
        # np.concatenate requires extra parenthesis 
        model['time'] = np.concatenate( (model['time'], dts ))  # accumulate time, but not useful.
        for k in modelarray.keys(): 
            modelarray[k] = np.concatenate((modelarray[k], gas[k]))
            
    # This here adds the time array to the overall dictionary
    if t == len(range(0,date_diff))-1:  
        modelarray.update(modelarraytime)
        
        # set lat/lon arrays to appropriate times
        latarray = np.zeros ( (hours,y_dim, x_dim) )
        lonarray = np.zeros ( (hours,y_dim, x_dim) )

        # Populate lat/lon dict
        for i in range(0,hours):
            latarray[i,:,:] = lat
            lonarray[i,:,:] = lon
            
        # Adds the lat/lon to dict
        modelarraylatlon['lat'] = copy.copy(latarray)
        modelarraylatlon['lon'] = copy.copy(lonarray)
            
        # add lat/lon to modelarray
        modelarray.update(modelarraylatlon)
        
    # How to accumulate modelarray over time
    now += timedelta(hours=24)
    print(now)
        
    nc.close()

# Save the dictionary to be used
def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    
name = outputDir+'1p33_'+start.strftime("%Y%m%d")+'_'+end.strftime("%Y%m%d")+'_PST'
save_obj(modelarray,name)