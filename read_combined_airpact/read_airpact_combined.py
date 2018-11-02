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
import matplotlib as mpl
mpl.use('Agg')
import datetime

#%%  
def naive_fast(latvar,lonvar,lat0,lon0):
    # Read latitude and longitude from file into numpy arrays
    latvals = latvar[:]
    lonvals = lonvar[:]
    ny,nx = latvals.shape
    dist_sq = (latvals-lat0)**2 + (lonvals-lon0)**2
    minindex_flattened = dist_sq.argmin()  # 1D index of min element
    iy_min,ix_min = np.unravel_index(minindex_flattened, latvals.shape)
    return int(iy_min),int(ix_min)
 
#%%
def readmodelmet(infile):
    metlist = ['PRSFC','PBL','HFX','QFX','TEMP2','WSPD10','WDIR10','RGRND', 'CFRAC']
    modelmet = {}
    for k in metlist:
        modelmet[k] = infile.variables[k][:-1,0,:,:] # 0 is for vertical layer & :-1 is to omit last value
    return modelmet
#%%
def readmodelgas(infile):
    gaslist = ['NO','NO2','SO2','O3','ISOP','CO','NH3','FORM']
    modelgas = {}
    for k in gaslist:
        modelgas[k] = infile.variables[k][:,0,:,:]
    return modelgas
#%%
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
#%%

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta
#%%        
#Main program starts here

# For now I am going to map the PBL concentrations and Free tropospheric concentrations
# Later I will do sample the PBL/FT concentrations along the air trajectory
# setup model file path and file name

from datetime import timedelta
import pytz

inoutputDir    = r"E:\Research\read_combined_airpact/AIRPACT_output/"
modeloutroot = r"E:\Research\read_combined_airpact/AIRPACT_output/tracers"

start = datetime.datetime(year=2017, month=8, day=10, hour=0)
end = datetime.datetime(year=2017, month=8, day=12, hour=23)
timezone = pytz.timezone("utc") #("America/Los_Angeles")
start = timezone.localize(start)
end = timezone.localize(end)
# in order to convert the time zone: start.astimezone(pytz.timezone("America/Los_Angeles"))

inputlat=40
inputlon=-120


# read grid information
modelgrid = inoutputDir +"/GRIDCRO2D"
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
model = {}
model['lat'] =  inputlat
model['lon'] =  inputlon
# now is the time variable used in the for loop
now = start
for t in range(0, date_diff):
    # read combined 
    modeloutput= modeloutroot +"/combined_" +  now.strftime("%Y%m%d") +".ncf"
    print(modeloutput)
    nc  = Dataset(modeloutput, 'r')

    
    # read MCIP files
    modelmetin= inoutputDir +"/mcip/METCRO2D_" +  now.strftime("%Y%m%d")
    print(modelmetin)
    mcip  = Dataset(modelmetin, 'r')
    #print(mcip)
    
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
       
        model['time'] = dts    
        #for k in modelarray.keys(): 
        #    model[k] = modelarray[k][:,0, iy,ix]
            
    else:
        gas = readmodelgas(nc)
        aer = readmodelaerosol(nc)
        met = readmodelmet(mcip)
        gas.update(aer)
        gas.update(met)
        # np.concatenate requires extra parenthesis 
        model['time'] = np.concatenate( (model['time'], dts ))  # accumulate time
        for k in modelarray.keys(): 
            modelarray[k] = np.concatenate((modelarray[k], gas[k]))
            
    # How to accumulate modelarray over time
    now += timedelta(hours=24)
    print(now)
        
    nc.close()
    mcip.close()

# delete unused variables
del gas
del aer
del met
del modelaer
del modelmet

#%%
#end of time loop

# sample at given lat and lon
for k in modelarray.keys(): 
    model[k] = modelarray[k][:,iy,ix]
    
#%%    
# reshape the modelarray to create 2D list for machine learning functions
for k in modelarray.keys(): 
    modelarray[k] = modelarray[k][:,:,:].flatten()

#%%
# SVR takes so long - so I gave up. 
#from sklearn import svm, datasets
# all met variables (trainingset) except PBL (target)
#metlist_woPBL = ['PRSFC','HFX','QFX','TEMP2','WSPD10','WDIR10','RGRND', 'CFRAC']
    
#METlist = np.concatenate([ modelarray[k].reshape((len(modelarray[k]),1)) for k in metlist_woPBL ], axis=1 )
#PBL =modelarray['PBL'][:]
#clf = svm.SVR()
#clf.fit(METlist[0:1000000], PBL[0:1000000])

#%%
from sklearn import decomposition

#metlist = ['PBL','PRSFC','HFX','QFX','TEMP2','WSPD10','WDIR10','RGRND', 'CFRAC']
metlist_woPBL = ['PRSFC','HFX','QFX','TEMP2','WSPD10','WDIR10','RGRND', 'CFRAC']

METlist = np.concatenate([ modelarray[k].reshape((len(modelarray[k]),1)) for k in metlist_woPBL ], axis=1 )

pca = decomposition.PCA()
pca.fit(METlist)

print(pca.explained_variance_) 

