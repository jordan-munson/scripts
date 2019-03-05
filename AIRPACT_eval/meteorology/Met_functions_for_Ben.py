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
#from mpl_toolkits.basemap import Basemap
import datetime
from datetime import timedelta
import pytz
import copy
import time
import os
import sys
#import wrf


# read the following functions
# Read met data
def readWRFmet(infile):
    metlist = ['TEMP2','PRSFC','WDIR10','WSPD10','Q2']
 #   metlist = ['T2']
 # if model==1:
 #       for k in metlist:
 #           wrfmet[k] = wrf.combine_files(infile,k,wrf.ALL_TIMES)
    wrfmet = {}
    for k in metlist:
        wrfmet[k] = infile.variables[k][:,:,:]
    return wrfmet

def readAIRPACTmet(infile,layer):
    metlist = ['PRSFC','TEMP2','Q2','WSPD10','WDIR10']
    airpactmet = {}
    for k in metlist:
        try:
            airpactmet[k] = infile.variables[k][:,layer,:,:]
        except KeyError:
            continue
    return airpactmet

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
    NMB=round((df_new['dif_var'].sum()/df_new[name_var2].sum())*100,2)
    return NMB
#Normalized Mean Error - NME
def nme(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']= abs(df_new[name_var1]-df_new[name_var2])
    NME=round((df_new['dif_var'].sum()/df_new[name_var2].sum())*100,2)
    return NME

#Root Mean Squared Error - RMSE
def rmse(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']= (df_new[name_var1]-df_new[name_var2])**(2)
    RMSE=round((df_new['dif_var'].sum()/len(df_new.index))**(0.5),2)
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

#Fractional bias - FB
def fb(df,name_var1,name_var2):  #var1 is model var2 is observed    
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']=df_new[name_var1]-df_new[name_var2]
    df_new['sum_var']=df_new[name_var1]+df_new[name_var2]
    df_new = df_new.drop(df_new[df_new.sum_var<=0].index) # Drop cells that are zero. These values cause infinity results
    df_new = df_new.drop(df_new[df_new.dif_var==0].index) # Drop cells that are zero. These values cause infinity results 
    df_new = df_new.dropna()
    FB= round((df_new['dif_var']/df_new['sum_var']).sum()*(2/len(df_new.index))*100,2)
    return FB

#Fractional error - FE
def fe(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']=abs(df_new[name_var1]-df_new[name_var2])
    df_new['sum_var']=df_new[name_var1]+df_new[name_var2]
    df_new = df_new.drop(df_new[df_new.sum_var<=0].index) # Drop cells that are zero. These values cause infinity results
    df_new = df_new.drop(df_new[df_new.dif_var==0].index) # Drop cells that are zero. These values cause infinity results
    df_new = df_new.dropna()
    FE= round((df_new['dif_var']/df_new['sum_var']).sum()*(2/len(df_new.index))*100,2)
    return FE
    
#Mean bias - MB
def mb(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']=df_new[name_var1]-df_new[name_var2]
    MB=round((df_new['dif_var'].sum())/len(df_new.index),2)
    return MB

#Mean error - ME
def me(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']=df_new[name_var1]-df_new[name_var2]
    ME=round(abs(df_new['dif_var']).sum()/len(df_new.index),2)
    return ME

# The Mean - Mean model concentration
def mean(df,name_var1,name_var2):  #var1 is model var2 is observed)
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    MEAN = df_new[name_var1].mean()
    return MEAN

def percentile(df,name_var1,name_var2):
    df_new=pd.DataFrame()
    percentile_98=pd.DataFrame()
    name1 = name_var1+' 98th'
    name2 = name_var2+' 98th'
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    percentile_98[name1] = [df_new[name_var1].quantile(0.98)]
    percentile_98[name2] = [df_new[name_var2].quantile(0.98)]
    return percentile_98
    
#Calculates and combines into a labeled dataframe
def stats(df,name_var1,name_var2,var_units):
    MB = mb(df,name_var1,name_var2)
    ME = me(df,name_var1,name_var2)
    FB = fb(df,name_var1,name_var2)
    FE = fe(df,name_var1,name_var2)
    NMB = nmb(df,name_var1,name_var2)
    NME = nme(df,name_var1,name_var2)
    RMSE = rmse(df,name_var1,name_var2)
    r_squared = r2(df,name_var1,name_var2)
    MEAN = mean(df,name_var1,name_var2)
    percentile_98 = percentile(df,name_var1,name_var2)
    name1 = name_var1+' 98th'
    name2 = name_var2+' 98th'
    
    g = pd.DataFrame([MEAN,MB,ME,FB,FE,NMB,NME,RMSE,r_squared, percentile_98[name1][0],percentile_98[name2][0]])
    g.index = ['Mean','MB','ME','FB','FE',"NMB [%]", "NME [%]", "RMSE [%s]" %var_units, "R^2 [-]",'Model 98th','Observation 98th']
    g.columns = [name_var1]
    return g

# =============================================================================
# #Create a test dataframe to ensure the functions are correct
# df_test=pd.DataFrame()
# df_test['M']= [7,6,5,11]
# df_test['O']= [6,8,6,12]
# df_test_results = stats(df_test,'M','O','test')    # Comment out when not debugging to avoid pointless dataframes
# =============================================================================

# Calculate mean
def mean_stat(df,name_var):   
    mean_value = np.nanmean(df[name_var])
    return mean_value

# Save WRF output into dictionary
def get_wrf_DF(datadir, start, end, x_dim, y_dim, lat, lon, layer):
    
    # prepare time loop to read model output
    date_diff =end -start
    date_diff =  int(round( date_diff.total_seconds()/60/60/24)) # total hour duration

    print("start date is "+ start.strftime("%Y%m%d") )
    now = start
    df_mod2 = pd.DataFrame()
    modelarray={}
    # create a time array for modelarray
    timearray = np.empty( ( 24, y_dim, x_dim), '|U18') # I have to hard_coded the length of time string
    lonarray = np.zeros ( (24,y_dim, x_dim) )
    latarray = np.zeros ( (24,y_dim, x_dim) )




    date_diff_final = date_diff
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
        
    now=start

    for t in range(0, date_diff_final):
        if int(now.strftime('%Y%m%d')) < 20160425:  
            modeloutputs =  datadir + now.strftime('%Y%m%d')+'00/MCIP/METCRO2D'
        else:
            modeloutputs =  datadir + now.strftime('%Y%m%d')+'00/MCIP37/METCRO2D'
        # open and read wrfout using netCDF function (Dataset)
        if os.path.isfile(modeloutputs):
            nc  = Dataset(modeloutputs, 'r')
            print('reading ', modeloutputs)
        else:
            now += timedelta(hours=24)
            continue
            #print("no file")
            #sys.exit()

        # create time array for 24 hours
        dts = [dt.strftime('%Y%m%d %H:00 UTC') for dt in
               DateTime_range(now, now+timedelta(hours=24),
                              timedelta(hours=1))]
        #if t<=0:
            # Read gas, aerosols, and met predictions
        
        modelarray = readAIRPACTmet(nc,layer)
        try:
            modelarray['TEMP2'] = modelarray['TEMP2'][0:24,:,:]
        except KeyError:
            pass
        try:
            modelarray['PRSFC'] = modelarray['PRSFC'][0:24,:,:]
        except KeyError:
            pass
        try:
            modelarray['Q2'] = modelarray['Q2'][0:24,:,:]
        except KeyError:
            pass         
        try:
            modelarray['WSPD10'] = modelarray['WSPD10'][0:24,:,:]
        except KeyError:
            pass        
        try:
            modelarray['WDIR10'] = modelarray['WDIR10'][0:24,:,:]
        except KeyError:
            pass        

        print(modelarray['TEMP2'].shape)

# add time variable to modelarray
        for i in range(0, 24):
            timearray[i,:,:] = dts[i]
            latarray[i,:,:] = lat
            lonarray[i,:,:] = lon
        modelarray['DateTime'] = copy.copy(timearray)  ## without copy.copy, this will become pointer
        modelarray['lat'] = latarray
        modelarray['lon']= lonarray

#        else:
#            # add time variable to modelarray
#            for i in range(0, 24):
#                timearray[i,:,:] = dts[i]
#
#            modelarray['DateTime'] = np.concatenate ( (modelarray['DateTime'], timearray))
#            modelarray['lat'] = np.concatenate ( (modelarray['lat'], latarray))
#            modelarray['lon'] = np.concatenate ( (modelarray['lon'], lonarray))
#
#            met = readAIRPACTmet(nc,layer)
#            met['TEMP2'] = met['TEMP2'][0:24,:,:]
#            met['PRSFC'] = met['PRSFC'][0:24,:,:]
#            met['Q2'] = met['Q2'][0:24,:,:]
#            met['WSPD10'] = met['WSPD10'][0:24,:,:]
#            met['WDIR10'] = met['WDIR10'][0:24,:,:]
#            #print(met['TEMP2'].shape)
#            
#            # loop over all keys excluding time
#            keys = set(modelarray.keys())
#            excludes = set(['DateTime','lat','lon'])
#
#            for k in keys.difference(excludes): #modelarray.keys():
#                modelarray[k] = np.concatenate((modelarray[k], met[k]))
#
#            del met
        


        mod_sample1 = {}
        for i in df_latlon.index:
                #print(iy2+','+ix2)
                #print (df_latlon['iy'][i], df_latlon['ix'][i])
                iy2 = df_latlon['iy'][i]
                ix2 = df_latlon['ix'][i]
                #print('Coords being read = '+str(iy2)+','+str(ix2))
                for k in modelarray.keys():
                    #mod_sample1[k] = wrf.to_np(wrf1[k][:,iy,ix]).flatten()
                    try:
                        mod_sample1[k] = modelarray[k][:,iy2,ix2].flatten()
                    except IndexError:
                        pass
                # Convert dictionary to data frame  
                df_mod1 = pd.DataFrame(mod_sample1)
                df_mod1['iy']=str(iy2)
                df_mod1['ix']=str(ix2)
                df_mod2 = pd.concat([df_mod2,df_mod1])
                
                #location_iy = pd.DataFrame([str(iy2)],columns=['iy'])
                #location_ix = pd.DataFrame([str(ix2)],columns=['ix'])
                #df_mod2 = df_mod2.append(location_iy)
                #df_mod2 = df_mod2.append(location_ix)
                
        # How to accumulate modelarray over time
        now += timedelta(hours=24)
        print("now time is", now)
        del modelarray
        nc.close()

    del timearray
    del latarray
    del lonarray
    
    return df_mod2
