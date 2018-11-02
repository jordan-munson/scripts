# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 13:43:28 2018

@author: yunhalee

"""

import pandas as pd
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap

import datetime
from datetime import timedelta
import pytz
import copy
import time

# read the following functions
# Read met data
def readWRFmet(infile):
    metlist = ['PSFC','T2','Q2', 'RAINC','RAINNC','PBLH','U10', 'V10']
 #   metlist = ['T2']
    wrfmet = {}
    for k in metlist:
        wrfmet[k] = infile.variables[k][:,:,:] # 0 is for vertical layer & :-1 is to omit last value that is 25 hr
    return wrfmet

# Read latitude and longitude from file into numpy arrays
def naive_fast(latvar,lonvar,lat0,lon0):
    latvals = latvar[:]
    lonvals = lonvar[:]
    ny,nx = latvals.shape
    dist_sq = (latvals-lat0)**2 + (lonvals-lon0)**2
    minindex_flattened = dist_sq.argmin()  # 1D index of min element
    iy_min,ix_min = np.unravel_index(minindex_flattened, latvals.shape)
    return int(iy_min),int(ix_min)

def DateTime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

#Normalized Mean Bias - NMB
def nmb(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']=df_new[name_var1]-df_new[name_var2]
    NMB=round((df_new['dif_var'].sum()/df_new[name_var2].sum())*100)
    return NMB
#Test = nmb(combined1, '1p33km_O3', 'm205_O3_Avg')
#Normalized Mean Error - NME
def nme(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']= abs(df_new[name_var1]-df_new[name_var2])
    NME=round((df_new['dif_var'].sum()/df_new[name_var2].sum())*100)
    return NME

#Root Mean Squared Error - RMSE
def rmse(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']= (df_new[name_var1]-df_new[name_var2])**(2)
    RMSE=round((df_new['dif_var'].sum()/len(df_new.index))**(0.5))
    return RMSE

#Coefficient of Determination - r^2
def r2(df,name_var1,name_var2):
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    top_var= ((df_new[name_var1]-np.mean(df_new[name_var1])) * (df_new[name_var2]-np.mean(df_new[name_var2]))).sum()
    bot_var= (((df_new[name_var1]-np.mean(df_new[name_var1]))**2).sum() * ((df_new[name_var2]-np.mean(df_new[name_var2]))**2).sum())**(.5)
    r_squared=round(((top_var/bot_var)**2),2)
    return r_squared

#Calculates and combines into a labeled dataframe
def stats(df,name_var1,name_var2):
    NMB = nmb(df,name_var1,name_var2)
    NME = nme(df,name_var1,name_var2)
    RMSE = rmse(df,name_var1,name_var2)
    r_squared = r2(df,name_var1,name_var2)
    g = pd.DataFrame([NMB,NME,RMSE,r_squared])
    g.index = ["NMB", "NME", "RMSE", "r_squared"]
    g.columns = [name_var1]
    return g

# save wrfchem output into dataframe
def get_wrfchem_DF(datadir, start, end):

    # prepare time loop to read model output
    date_diff =end -start
    date_diff =  int(round( date_diff.total_seconds()/60/60/24)) # total hour duration

    print("start date is "+ start.strftime("%Y%m%d") )
    now = start

    modelarray={}
    # create a time array for modelarray
    timearray = np.empty( ( 24, y_dim, x_dim), '|U18') # I have to hard_coded the length of time string
    lonarray = np.zeros ( (24,y_dim, x_dim) )
    latarray = np.zeros ( (24,y_dim, x_dim) )

    for t in range(0, date_diff):

        # Note that "_subset" in modeloutput name should be removed for real application 
        modeloutput= datadir +"inputs/wrfout_d01_" +  now.strftime("%Y-%m-%d_00:00:00")

        # open and read wrfout using netCDF function (Dataset)
        if os.path.isfile(modeloutput):
            nc  = Dataset(modeloutput, 'r')
            print('reading ', modeloutput)
        else:
            print("no file")
            exit() 

       #create time array for 24 hours
        dts = [dt.strftime('%Y%m%d %H:00 UTC') for dt in
               DateTime_range(now, now+timedelta(hours=24),
                              timedelta(hours=1))]
        if t<=0:
            # Read gas, aerosols, and met predictions
            modelarray = readWRFmet(nc)

            # add time variable to modelarray
            for i in range(0, 24):
                timearray[i,:,:] = dts[i]
                latarray[i,:,:] = lat
                lonarray[i,:,:] = lon
            modelarray['DateTime'] = copy.copy(timearray)  ## without copy.copy, this will become pointer
            modelarray['lat'] = latarray
            modelarray['lon']= lonarray
        else:
            # add time variable to modelarray
            for i in range(0, 24):
                timearray[i,:,:] = dts[i]

            modelarray['DateTime'] = np.concatenate ( (modelarray['DateTime'], timearray))
            modelarray['lat'] = np.concatenate ( (modelarray['lat'], latarray))
            modelarray['lon'] = np.concatenate ( (modelarray['lon'], lonarray))

            met = readWRFmet(nc)

            # loop over all keys excluding time
            keys = set(modelarray.keys())
            excludes = set(['DateTime','lat','lon'])

            for k in keys.difference(excludes): #modelarray.keys():
                modelarray[k] = np.concatenate((modelarray[k], met[k]))

            del met

        # How to accumulate modelarray over time
        now += timedelta(hours=24)
        print("now time is", now)

        nc.close()

    del timearray
    del latarray
    del lonarray

    return modelarray
