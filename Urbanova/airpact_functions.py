import pandas as pd
# numpy has a lots of useful math related modules
import numpy as np
# Helpful function to display intermittent result
#from IPython.display import display

from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
import datetime
from datetime import timedelta
import pytz
import copy
import time
import os

#Read AIRPACT gas species
def readAIRPACTgas(infile,layer):
    #gaslist = ['NO','NO2','SO2','O3','ISOP','CO','NH3','FORM']  # Feb 16 2017 - add more VOC species to evaluate MOSAIC

    if filetype == 'aconc':
        gaslist = ["O3",'BENZENE','CO','NH3','NO','NO2','SO2']
    else:
        gaslist = ['O3']
    airpactgas = {}
    for k in gaslist:
        airpactgas[k] = infile.variables[k][:,layer,:,:]
    return airpactgas

def readAIRPACTaerosol(infile, layer):
    #aerlist = ['ASO4I','ASO4J','ASO4K','ANO3I','ANO3J','ANO3K','ANH4I','ANH4J','ANH4K','AECI','AECJ','APOCI','APOCJ','APNCOMI','APNCOMJ']
    aerlist = ['PMIJ']
    airpactaerosol = {}
    #airpactaero = {}
    for k in aerlist:
        airpactaerosol[k] = infile.variables[k][:,layer,:,:] # 0 is for surface layer
    #airpactaero['ASO4IJ'] = np.add(airpactaerosol['ASO4I'],airpactaerosol['ASO4J'])
    #airpactaero['ANO3IJ'] = np.add(airpactaerosol['ANO3I'], airpactaerosol['ASO4J'])
    #airpactaero['ANH4IJ'] = np.add(airpactaerosol['ANH4I'], airpactaerosol['ASO4J'])
    #airpactaero['ASO4'] = np.add(np.add(airpactaerosol['ASO4I'], airpactaerosol['ASO4J']), airpactaerosol['ASO4K'])
    #airpactaero['ANO3'] = np.add(np.add(airpactaerosol['ANO3I'], airpactaerosol['ASO4J']), airpactaerosol['ANO3K'])
    #airpactaero['ANH4'] = np.add(np.add(airpactaerosol['ANH4I'], airpactaerosol['ASO4J']), airpactaerosol['ANH4K'])
    #airpactaero['AEC'] = np.add(airpactaerosol['AECI'], airpactaerosol['AECJ'])
    #airpactaero['APOA'] = np.add(np.add(np.add(airpactaerosol['APOCI'], airpactaerosol['APOCJ']), airpactaerosol['APNCOMI']), airpactaerosol['APNCOMJ'])
    #return airpactaero
    return airpactaerosol

def DateTime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

# save airpact output into dataframe
def get_airpact_DF(start, end, layer):
    # prepare time loop to read model output
    date_diff =end -start
    date_diff =  int(round( date_diff.total_seconds()/60/60/24)) # total hour duration
    print('date diff is '+ str(date_diff))
    print("start date is "+ start.strftime("%Y%m%d") )
    now = start
    
    modelarray={}
    hr=(end-start).total_seconds()/3600+1
    hr=int(hr)
    print('Hours in df are ' + str(hr))
    lonarray = np.zeros ( (hr,y_dim, x_dim) )
    latarray = np.zeros ( (hr,y_dim, x_dim) )
    for i in range(0,hr):
        latarray[i,:,:] = lat
        lonarray[i,:,:] = lon
    
    for t in range(0, len(modeloutputs)):
        #modeloutput= datadir +"input/wrfout_d01_" +  now.strftime("%Y-%m-%d_00:00:00_subset")
        # open and read wrfout using netCDF function (Dataset)
        if os.path.isfile(modeloutputs[t]):
            nc  = Dataset(modeloutputs[t], 'r')
            print('reading ', modeloutputs[t])
        else:
            print("no file")
            #exit() 
            continue # Try this instead to avoid an exit
       #create time array for 24 hours
        dts = [dt.strftime('%Y%m%d %H:00 UTC') for dt in
               DateTime_range(now, now+timedelta(hours=hr),
                              timedelta(hours=1))]
               
        if t==0:   # if the run is on the first day
            # Read gas, aerosols, and met predictions
            modelarray0 = readAIRPACTgas(nc,layer)
            modelaer0 = readAIRPACTaerosol(nc,layer)
            modelarray0.update(modelaer0) # combine gas and aerosols, so all tracers are in airpact
            modelarray={}
            if start.hour<8:
                h=start.hour+16
            else:
                h=start.hour-8
            for i in list(modelarray0.keys()):
                modelarray[i]=modelarray0[i][h:,:,:]
            #modelmet = readairpactmet(nc)
            #modelarray.update(modelmet)
            
            # create a time array for modelarray
            timearray = np.empty( ( int(24-h), y_dim, x_dim), '|U18')
            
            # add time variable to modelarray
            j=0
            for i in range(h, 24):
                timearray[j,:,:] = dts[i]
                j=j+1
            
            modelarray['DateTime'] = copy.copy(timearray)  ## without copy.copy, this will become pointer
            modelarray['lat'] = latarray
            modelarray['lon']= lonarray
        elif t==len(modeloutputs)-1:   # If the run is on the last day
            if end.hour<8:
                h=end.hour+16
            else:
                h=end.hour-8
            # create a time array for modelarray
            timearray = np.empty( ( h+1, y_dim, x_dim), '|U18')
            # add time variable to modelarray
            for i in range(0, h):
                #timearray[i,:,:] = dts[int(hr-h-1+i)]
                timearray[i,:,:] = dts[int(hr-h-1+i)]
            modelarray['DateTime'] = np.concatenate ( (modelarray['DateTime'], timearray))
            #modelarray['lat'] = np.concatenate ( (modelarray['lat'], latarray))
            #modelarray['lon'] = np.concatenate ( (modelarray['lon'], lonarray))
            
            gas0 = readAIRPACTgas(nc,layer)
            aer0 = readAIRPACTaerosol(nc,layer)
            #met = readairpactmet(nc)
            gas0.update(aer0)
            gas={}
            for i in list(gas0.keys()):
                gas[i]=gas0[i][:(h+1),:,:]
            #gas.update(met)
            
            # loop over all keys excluding time
            keys = set(modelarray.keys())
            excludes = set(['DateTime','lat','lon'])
            
            for k in keys.difference(excludes): #modelarray.keys():
                modelarray[k] = np.concatenate((modelarray[k], gas[k]))
            
            del gas
            del gas0
            del aer0
        else:   # every day other than the first or last
            # create a time array for modelarray
            timearray = np.empty( ( 24, y_dim, x_dim), '|U18')
            # add time variable to modelarray
            h_first_day=24-start.hour
            for i in range(0, 24):
                timearray[i,:,:] = dts[h_first_day+(t-2)*24+i]
                          
            modelarray['DateTime'] = np.concatenate ( (modelarray['DateTime'], timearray))
            #modelarray['lat'] = np.concatenate ( (modelarray['lat'], latarray))
            #modelarray['lon'] = np.concatenate ( (modelarray['lon'], lonarray))
            
            gas0 = readAIRPACTgas(nc,layer)
            aer0 = readAIRPACTaerosol(nc,layer)
            #met = readairpactmet(nc)
            gas0.update(aer0)
            gas={}
            for i in list(gas0.keys()):
                gas[i]=gas0[i][:,:,:]
            #gas.update(met)
            
            # loop over all keys excluding time
            keys = set(modelarray.keys())
            excludes = set(['DateTime','lat','lon'])
            
            for k in keys.difference(excludes): #modelarray.keys():
                modelarray[k] = np.concatenate((modelarray[k], gas[k]))
            
            del gas
            del gas0
            del aer0
            #del met
        
        # How to accumulate modelarray over time
        now += timedelta(hours=24)
        print("now time is", now)
        
        nc.close()
    
    del modelaer0
    #del modelmet
    del timearray
    del latarray
    del lonarray
    return modelarray

def get_AQS_AIRPACT_data(start, end):
    startyr=start.strftime("%Y")
    startmon=start.strftime("%m")
    endyr=end.strftime("%Y")
    endmon=start.strftime("%m")
    
    # get aqsstie information
    url = 'http://lar.wsu.edu/airpact/airnow_sites/aqsid' +start.strftime("%Y%m%d") + '.csv'
    print(url)
    aqs_sites = pd.read_csv(url)
    
    # drop the first row where jen left a comment
    aqs_sites.drop(0, inplace=True)
    
    # read AIRNOW observation
    
    # This doesn't work in Kamiak AQS_file = 'https://aqs.epa.gov/aqsweb/airdata/hourly_'+species_code[i]+'_'+startyr+'.zip'
    #PM_file = "/Users/yunhalee/Desktop/WSU_work/AIRPACT/Smoke_Forecast_intercomparison/AQS_eval/hourly_88101_2017.csv" # e.g ~/cs564/p5/AQI.csv"
    #url = 'http://lar.wsu.edu/R_apps/' + start.strftime("%Y") +'ap5/data/hrly'+start.strftime("%Y")+'.csv' 
    url = 'http://lar.wsu.edu/R_apps/2018ap5/data/hrly2018.csv'
    print(url)
    AQS_obs =  pd.read_csv(url)
    
    AQS_obs['DateTime'] = pd.to_datetime(AQS_obs['DateTime'],format='%m/%d/%y %H:%M') #add format can reduce running time
    
    # subset the result dataframe using target time period
    mask = (AQS_obs['DateTime'] > start) & (AQS_obs['DateTime'] <= end)
    AQS_obs = AQS_obs.loc[mask]
    print("AQS observation final length", AQS_obs.shape)
    
    # merge the AQS_obs using matching SiteNumber
    AQS_obs =AQS_obs.merge(aqs_sites, on='AQSID')
    
    return AQS_obs

def naive_fast(latvar,lonvar,lat0,lon0):
    latvals = latvar[:]
    lonvals = lonvar[:]
    ny,nx = latvals.shape
    dist_sq = (latvals-lat0)**2 + (lonvals-lon0)**2
    minindex_flattened = dist_sq.argmin()  # 1D index of min element
    iy_min,ix_min = np.unravel_index(minindex_flattened, latvals.shape)
    return int(iy_min),int(ix_min)

#Fractional Bias - FB
def fb(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']=df_new[name_var1]-df_new[name_var2]
    df_new['sum_var']=df_new[name_var1]+df_new[name_var2]
    FB=round((df_new['dif_var']/df_new['sum_var']).sum()*2/len(df[name_var1])*100)
    return FB
#Test = nmb(combined1, '1p33km_O3', 'm205_O3_Avg')
#Fractional Error - FE
def fe(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']= abs(df_new[name_var1]-df_new[name_var2])
    df_new['sum_var']=df_new[name_var1]+df_new[name_var2]
    FE=round((df_new['dif_var']/df_new['sum_var']).sum()*2/len(df[name_var1])*100)
    return FE

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
    FB = fb(df,name_var1,name_var2)
    FE = fe(df,name_var1,name_var2)
    NMB = nmb(df,name_var1,name_var2)
    NME = nme(df,name_var1,name_var2)
    RMSE = rmse(df,name_var1,name_var2)
    r_squared = r2(df,name_var1,name_var2)
    g = pd.DataFrame([FB,FE,NMB,NME,RMSE,r_squared])
    g.index = ["FB","FE","NMB", "NME", "RMSE", "r_squared"]
    g.columns = [name_var1]
    return g
#%%


# save aconc output into dataframe
def get_aconc_DF(start, end, layer):
    # prepare time loop to read model output
    filetype='aconc'
    date_diff =end -start
    date_diff =  int(round( date_diff.total_seconds()/60/60/24)) # total hour duration
    print('date diff is '+ str(date_diff))
    print("start date is "+ start.strftime("%Y%m%d") )
    now = start
    
    modelarray={}
    hr=(end-start).total_seconds()/3600+1
    hr=int(hr)
    print('Hours in df are ' + str(hr))
    lonarray = np.zeros ( (hr,y_dim, x_dim) )
    latarray = np.zeros ( (hr,y_dim, x_dim) )
    for i in range(0,hr):
        latarray[i,:,:] = lat
        lonarray[i,:,:] = lon
    
    for t in range(0, len(modeloutputs)):
        #modeloutput= datadir +"input/wrfout_d01_" +  now.strftime("%Y-%m-%d_00:00:00_subset")
        # open and read wrfout using netCDF function (Dataset)
        if os.path.isfile(modeloutputs[t]):
            nc  = Dataset(modeloutputs[t], 'r')
            print('reading ', modeloutputs[t])
        else:
            print("no file")
            #exit() 
            continue # Try this instead to avoid an exit
       #create time array for 24 hours
        dts = [dt.strftime('%Y%m%d %H:00 UTC') for dt in
               DateTime_range(now, now+timedelta(hours=hr),
                              timedelta(hours=1))]
               
        if t==0:   # if the run is on the first day
            # Read gas, aerosols, and met predictions
            modelarray0 = readAIRPACTgas(nc,layer)
            #modelaer0 = readAIRPACTaerosol(nc,layer)
            #modelarray0.update(modelaer0) # combine gas and aerosols, so all tracers are in airpact
            modelarray={}
            if start.hour<8:
                h=start.hour+16
            else:
                h=start.hour-8
            for i in list(modelarray0.keys()):
                modelarray[i]=modelarray0[i][0:,:,:]
            #modelmet = readairpactmet(nc)
            #modelarray.update(modelmet)
            
            # create a time array for modelarray
            timearray = np.empty( ( int(24), y_dim, x_dim), '|U18')
            
            # add time variable to modelarray
            j=0
            for i in range(0, 24):
                timearray[j,:,:] = dts[i]
                j=j+1
            
            modelarray['DateTime'] = copy.copy(timearray)  ## without copy.copy, this will become pointer
            modelarray['lat'] = latarray
            modelarray['lon']= lonarray
        elif t==len(modeloutputs)-1:   # If the run is on the last day
            if end.hour<8:
                h=end.hour+16
            else:
                h=end.hour-8
            # create a time array for modelarray
            #timearray = np.empty( ( h+1, y_dim, x_dim), '|U18')
            timearray = np.empty( ( 24, y_dim, x_dim), '|U18') # for use with single days data

            # add time variable to modelarray
            for i in range(0, 24):
                #timearray[i,:,:] = dts[int(hr-h-1+i)]
                timearray[i,:,:] = dts[int(24)]
            modelarray['DateTime'] = np.concatenate ( (modelarray['DateTime'], timearray))
            #modelarray['lat'] = np.concatenate ( (modelarray['lat'], latarray))
            #modelarray['lon'] = np.concatenate ( (modelarray['lon'], lonarray))
            
            gas0 = readAIRPACTgas(nc,layer)
            aer0 = readAIRPACTaerosol(nc,layer)
            #met = readairpactmet(nc)
            gas0.update(aer0)
            gas={}
            for i in list(gas0.keys()):
                gas[i]=gas0[i][:(h+1),:,:]
            #gas.update(met)
            
            # loop over all keys excluding time
            keys = set(modelarray.keys())
            excludes = set(['DateTime','lat','lon'])
            
            for k in keys.difference(excludes): #modelarray.keys():
                modelarray[k] = np.concatenate((modelarray[k], gas[k]))
            
            del gas
            del gas0
            del aer0
        else:   # every day other than the first or last
            # create a time array for modelarray
            timearray = np.empty( ( 24, y_dim, x_dim), '|U18')
            # add time variable to modelarray
            h_first_day=24-start.hour
            for i in range(0, 24):
                timearray[i,:,:] = dts[h_first_day+(t-2)*24+i]
                          
            modelarray['DateTime'] = np.concatenate ( (modelarray['DateTime'], timearray))
            #modelarray['lat'] = np.concatenate ( (modelarray['lat'], latarray))
            #modelarray['lon'] = np.concatenate ( (modelarray['lon'], lonarray))
            
            gas0 = readAIRPACTgas(nc,layer)
            aer0 = readAIRPACTaerosol(nc,layer)
            #met = readairpactmet(nc)
            gas0.update(aer0)
            gas={}
            for i in list(gas0.keys()):
                gas[i]=gas0[i][:,:,:]
            #gas.update(met)
            
            # loop over all keys excluding time
            keys = set(modelarray.keys())
            excludes = set(['DateTime','lat','lon'])
            
            for k in keys.difference(excludes): #modelarray.keys():
                modelarray[k] = np.concatenate((modelarray[k], gas[k]))
            
            del gas
            del gas0
            del aer0
            #del met
        
        # How to accumulate modelarray over time
        now += timedelta(hours=24)
        print("now time is", now)
        
        nc.close()
    
    #del modelaer0
    #del modelmet
    del timearray
    del latarray
    del lonarray
    return modelarray


#urbanova_old = get_aconc_DF(start, end, layer)