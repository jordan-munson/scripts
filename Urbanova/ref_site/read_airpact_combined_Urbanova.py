# -*- coding: utf-8 -*-
"""
Created on JAN 29, 2018

@author: yunhalee
Description - extract model output tracers

"""

###############################################################################

#Main program starts here

###############################################################################

# import necessary modules
# matplotlib
import matplotlib as mpl
mpl.use('Agg')
print('matplotlib: %s' % mpl.__version__)

# scipy
import scipy
print('scipy: %s' % scipy.__version__)
# numpy
import numpy as np
print('numpy: %s' % np.__version__)

import datetime
from datetime import timedelta
import pytz
import copy
from netCDF4 import Dataset

# pandas
import pandas as pd
print('pandas: %s' % pd.__version__)
# statsmodels
import statsmodels
print('statsmodels: %s' % statsmodels.__version__)



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


# setup model file path and file name

start = datetime.datetime(year=2018, month=1, day=19, hour=0)
end = datetime.datetime(year=2018, month=1, day=22, hour=23)
timezone = pytz.timezone("utc") #("America/Los_Angeles")
start = timezone.localize(start)
end = timezone.localize(end)
inputDir          = "/data/airpact5/rerun/Urbanova/"
plotDir           ='/data/lar/projects/Urbanova_output/'
# in order to convert the time zone: start.astimezone(pytz.timezone("America/Los_Angeles"))

#put observation site info 
inputlat=47.6608
inputlon=-117.4044


# read grid information
modelgrid = inputDir +start.strftime("%Y")+ "/"+start.strftime("%Y%m%d")+ "00/MCIP37/GRIDCRO2D"
print(modelgrid)
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

# empty array
modelarray={} 
#model directionary is no longer needed as modelarray contains lat, lon, and time information. 
#model = {}
#model['lat'] =  inputlat
#model['lon'] =  inputlon
# create a time array for modelarray 
import numpy as np
timearray = np.empty( ( 24, 90, 90), '|U18') # Grid coordinates
lonarray = np.zeros ( (24,90,90) )
latarray = np.zeros ( (24,90,90) )
# now is the time variable used in the for loop
now = start
for t in range(0, date_diff):
    # read combined 
    modeloutput= inputDir +now.strftime("%Y")+ "/"+now.strftime("%Y%m%d")+"00/POST/CCTM/combined_" +  now.strftime("%Y%m%d") +".ncf"
    print(modeloutput)
    nc  = Dataset(modeloutput, 'r')
    # read MCIP files
    modelmetin= inputDir +now.strftime("%Y")+ "/"+now.strftime("%Y%m%d")+"00/MCIP37/METCRO2D"
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
        aer = readmodelaerosol(nc)
        met = readmodelmet(mcip)
        gas.update(aer)
        gas.update(met)

        # loop over all keys excluding time 
        keys = set(modelarray.keys())
        excludes = set(['datetime','lat','lon'])

        for k in keys.difference(excludes): #modelarray.keys(): 
            modelarray[k] = np.concatenate((modelarray[k], gas[k]))

    # How to accumulate modelarray over time
    now += timedelta(hours=24)
    print("now time is", now)
    
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
    mod_sample[k] = modelarray[k][:,iy,ix].flatten() 
#            model[k].append(modelarray[k][:,j,i ].flatten() )

# convert model (iy,ix sampling data) to dataframe
d1 = pd.DataFrame(mod_sample)

# set a datetime column to index to better manipulate time series data
d1['datetime'] = pd.to_datetime(d1['datetime'])
d1 = d1.set_index('datetime')

# save sampled output to excel
writer = pd.ExcelWriter('AIRPACT1p33km_at_Urbanova_ref_site2.xlsx')
d1.to_excel(writer,'Sheet1')
writer.save()



