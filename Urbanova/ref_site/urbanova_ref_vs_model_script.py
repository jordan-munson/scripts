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

#Setup to pull AIRPACT data
start = dt.datetime(year=int(year), month=int(month), day=int(day), hour=0)
end = dt.datetime(year=int(endyear), month=int(endmonth), day=int(endday), hour=23)
timezone = pytz.timezone("utc") #("America/Los_Angeles")
start = timezone.localize(start)
end = timezone.localize(end)

#Site coordinates
inputlat = 47.6608
inputlon = -117.4044

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
        mod_sample[k] = modelarray[k][:,iy,ix].flatten() 
        #            model[k].append(modelarray[k][:,j,i ].flatten() )

    # convert model (iy,ix sampling data) to dataframe
    d1 = pd.DataFrame(mod_sample)

    # set a datetime column to index to better manipulate time series data
    d1['datetime'] = pd.to_datetime(d1['datetime'])
    d1 = d1.set_index('datetime')

    # save sampled output to excel in current folder
    if x == '4km':
        writer = pd.ExcelWriter('AIRPACT4km_at_Urbanova_reference_site.xlsx')
        d1.to_excel(writer,'Sheet1')
        writer.save()
    if x == '1p33km':
        writer = pd.ExcelWriter('AIRPACT1p33km_at_Urbanova_reference_site.xlsx')
        d1.to_excel(writer,'Sheet1')
        writer.save()   

#Run the function for 4km and then 1p33km
x='1p33km'
airpact(x)

x='4km'
airpact(x)

#End of function

#File Directories
file_1p33km = inputDir + '/AIRPACT1p33km_at_Urbanova_reference_site.xlsx'
print(file_1p33km)
file_4km = inputDir + '/AIRPACT4km_at_Urbanova_reference_site.xlsx'
print(file_4km)
#file_ref = 'http://134.121.20.103/Urbanova_AQRS_stats.xlsx'   #No data at this link currently
file_ref = inputDir + '/Urbanova_AQRS_stats.xlsx'
print(file_4km)

#Read data files
df_1p33km = pd.read_excel(file_1p33km, sep =',')
df_4km = pd.read_excel(file_4km, sep =',')
df_ref = pd.read_excel(file_ref, sep =',', skiprows = [0,2,3,4,5])

#Rename some columns to make the script work
df_1p33km.rename(columns={'O3':'1p33km_O3'}, inplace=True)
df_1p33km.rename(columns={'NO':'1p33km_NO'}, inplace=True)
df_1p33km.rename(columns={'NO2':'1p33km_NO2'}, inplace=True)
df_1p33km.rename(columns={'SO2':'1p33km_SO2'}, inplace=True)

df_4km.rename(columns={'O3':'4km_O3'}, inplace=True)
df_4km.rename(columns={'NO':'4km_NO'}, inplace=True)
df_4km.rename(columns={'NO2':'4km_NO2'}, inplace=True)
df_4km.rename(columns={'SO2':'4km_SO2'}, inplace=True)

df_ref.rename(columns={'TIMESTAMP':'datetime'}, inplace=True)    #Necessary so that df_ref will plot. Replaces TIMESTAMP with datetime

#Convert datatime column to time data
df_1p33km['datetime'] = pd.to_datetime(df_1p33km['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M"
df_4km['datetime'] = pd.to_datetime(df_4km['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M"
df_ref['datetime'] = pd.to_datetime(df_ref['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M"

#Convert model data to PST from UTC (PST = UTC-8)
df_1p33km["datetime"] = df_1p33km["datetime"].apply(lambda x: x - dt.timedelta(hours=8))
df_4km["datetime"] = df_4km["datetime"].apply(lambda x: x - dt.timedelta(hours=8))

#Convert object to numeric, otherwise these columns will not resample or plot
df_ref.loc[:,'m405_NO2_Avg'] = pd.to_numeric(df_ref.loc[:,'m405_NO2_Avg'], errors='coerce')
df_ref.loc[:,'m405_NO_Avg'] = pd.to_numeric(df_ref.loc[:,'m405_NO_Avg'], errors='coerce')
df_ref.loc[:,'m205_O3_Avg'] = pd.to_numeric(df_ref.loc[:,'m405_NO_Avg'], errors='coerce')

#Convert df_ref to hourly data
df_ref['datetime'] = pd.to_datetime(df_ref['datetime'])
df_ref = df_ref.set_index('datetime')
#dropna(): df_ref.dropna().describe()    #Needed for Urbanova
df_ref = df_ref.resample('H').mean()
df_ref = df_ref.reset_index()

#Merge data into a single table
combined = pd.merge(df_1p33km, df_4km, on=['datetime'], how='inner')
combined1 = pd.merge(combined, df_ref, on=['datetime'], how='inner')

#%%
#Calculate some statistics
# Open statistics script
exec(open(inputDir +"/statistical_functions_ref_site.py").read())

#Create a test dataframe to ensure the functions are correct
df_test=pd.DataFrame()
df_test['M']= [5,6,5,11]
df_test['O']= [6,8,6,12]

#Run the stats function for the desired data
Test_stats = stats(df_test,'M', 'O')
O3_1p33km_stats = stats(combined1, '1p33km_O3', 'm205_O3_Avg')
O3_4km_stats = stats(combined1, '4km_O3', 'm205_O3_Avg')
NO2_1p33km_stats = stats(combined1, '1p33km_NO2', 'm405_NO2_Avg')
NO2_4km_stats = stats(combined1, '4km_NO2', 'm405_NO2_Avg')
NO_1p33km_stats = stats(combined1, '1p33km_NO', 'm405_NO_Avg')
NO_4km_stats = stats(combined1, '4km_NO', 'm405_NO_Avg')
SO2_1p33km_stats = stats(combined1, '1p33km_SO2', 't100u_so2_Avg')
SO2_4km_stats = stats(combined1, '4km_SO2', 't100u_so2_Avg')

#Calculate stats for regression plots
O3_regression_stats = stats(combined1, '4km_O3', '1p33km_O3')
NO2_regression_stats = stats(combined1, '4km_NO2', '1p33km_NO2')
NO_regression_stats = stats(combined1, '4km_NO', '1p33km_NO')
SO2_regression_stats = stats(combined1, '4km_SO2', '1p33km_SO2')

#Combine the statistics
O3_stats = pd.merge(O3_1p33km_stats,O3_4km_stats, how = 'inner', left_index = True, right_index = True)
NO2_stats = pd.merge(NO2_1p33km_stats,NO2_4km_stats, how = 'inner', left_index = True, right_index = True)
NO_stats = pd.merge(NO_1p33km_stats,NO_4km_stats, how = 'inner', left_index = True, right_index = True)
SO2_stats = pd.merge(SO2_1p33km_stats,SO2_4km_stats, how = 'inner', left_index = True, right_index = True)
O3_NO2 = pd.merge(O3_stats,NO2_stats, how = 'inner', left_index = True, right_index = True)
SO2_NO = pd.merge(SO2_stats,NO_stats, how = 'inner', left_index = True, right_index = True)
Statistics = pd.merge(O3_NO2,SO2_NO, how = 'inner', left_index = True, right_index = True)

#Save Statistics to excel file
writer = pd.ExcelWriter('reference_site_statistics.xlsx')
Statistics.to_excel(writer, 'Sheet1')
writer.save()

#%%

#Some more formatting
beginning = month+'-'+day+'-'+year
print(beginning)
#endday = str(int(endday) + 10) #Attempt to manually extend the graph to appropriate date length
ending = endmonth+'-'+endday+'-'+endyear
idx = pd.date_range(beginning + ' 00:00:00', ending + ' 00:00:00', freq = 'H')
#idx = pd.date_range('01-11-2018 00:00:00', '01-15-2018 00:00:00', freq = 'H')
combined1.set_index('datetime', inplace =True)
combined1 = combined1.reindex(idx)

#Clean NaN values up for regression plots
combined2 = combined1.dropna()

# Calculate diurnal mean
diurnal = combined1.groupby(combined1.index.hour).mean()

#%%
#Set plot parameters
mpl.rcParams['font.family'] = 'sans-serif'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 20.0
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

g = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
g.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
g = g.drop(0,1)

#Plot data
# Hourly plots function

def hourly_ref(df,name_var1,name_var2,name_var3,stats,y_label,title, diurnal):
    fig,ax=plt.subplots(1,1, figsize=(12,4))
    df.ix[:,[name_var1, name_var2,name_var3]].plot(kind='line', style='-', ax=ax, color=['black', 'blue', 'red'])
    stats = stats.drop('MB',0)        
    stats = stats.drop('ME',0)
    stats = stats.drop('RMSE',0)
    stats = stats.drop('NMB',0)
    stats = stats.drop('NME',0)
    #ax.text(0,-0.25, stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
    ax.set_title(title+ ' Comparison')
    ax.set_ylabel(y_label)
    ax.legend(['Ref Site', 'AP5_4km', 'AP5_1.33km'], fontsize=12)
    if diurnal == 'yes':
        ax.set_xlabel('Mean Diurnal (hours)')
        b=combined1.groupby(combined1.index.hour).std()
        e = b
        c = df-b
        e = df+b
        x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        plt.fill_between(x, c[name_var1], e[name_var1], facecolor='blue', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) 
        plt.fill_between(x, c[name_var2], e[name_var2],facecolor='red', edgecolor='black',alpha = 0.1, label=['Std. Dev.'])   
    else:
        ax.set_xlabel('PST')
    plt.savefig(outputDir +'/'+title+'_ref_site_comparison_'+ year +month +day+ '-' + endyear + endmonth + endday+'.pdf', pad_inches=0.1, bbox_inches='tight')

def diurnal_plot(df,name_var1,name_var2,name_var3,stats,y_label,title, diurnal):
    fig,ax=plt.subplots(1,1, figsize=(12,4))
    d=df
    #d=d.set_index('datetime')
    b=d.groupby(d.index.hour).std()
    d.groupby(d.index.hour).mean().ix[:,[name_var1, name_var2, name_var3]].plot(kind='line', style='-', ax=ax, color=['black', 'blue', 'red'], label=['OBS', 'sens', 'base'])
    ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.set_xlabel('Mean Diurnal (hours)')
    d = d.groupby(d.index.hour).mean()
    e = b
    c = d-b
    e = d+b
    x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    plt.fill_between(x, c[name_var2], e[name_var2], facecolor='blue', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) 
    plt.fill_between(x, c[name_var3], e[name_var3],facecolor='red', edgecolor='black',alpha = 0.1, label=['Std. Dev.'])     
    ax.legend(['OBS', 'AP5_4km', 'AP5_1.33km', 'Std. Dev.'], fontsize=12)
    plt.savefig(outputDir +'/'+title+'_ref_site_comparison_'+ year +month +day+ '-' + endyear + endmonth + endday+'.pdf', pad_inches=0.1, bbox_inches='tight')
# Regression plot function, includes statistics, best-fit line,
def regression(df,name_var1,name_var2,name_var3,stats,title,save,label):
    fig,ax=plt.subplots(1,1, figsize=(8,8))
    ax.scatter(df[name_var3],df[name_var1], c='b', label='4km')
    ax.scatter(df[name_var3],df[name_var2], c='r',marker='s', label='1.33km')
    axismax = max(max(df[name_var1]),max(df[name_var2]))
    plt.plot([0,axismax], [0,axismax], color='black')
    stats = stats.drop('MB',0)        
    stats = stats.drop('ME',0)
    stats = stats.drop('RMSE',0)
    stats = stats.drop('NMB',0)
    stats = stats.drop('NME',0) 
    ax.set_ylabel('Modeled ' +label)
    ax.set_xlabel('Observed '+label) 
    ax.set_ylim(0,axismax)
    ax.set_xlim(0,axismax)
    
    #ax.text(0,-0.25, stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
    ax.set_title(title + ' Scatter') 
    plt.legend()
    plt.savefig(outputDir +'/'+save+'_'+ year +month +day+ '-' + endyear + endmonth + endday+'.pdf', pad_inches=0.1, bbox_inches='tight')
    
# Run hourly plots
hourly_ref(combined1,'m205_O3_Avg','4km_O3','1p33km_O3', O3_stats,'O3, ppbv','O3_Hourly','no')
hourly_ref(combined1,'m405_NO2_Avg','4km_NO2','1p33km_NO2', NO2_stats,'NO2, ppb','NO2_Hourly','no')
hourly_ref(combined1,'m405_NO_Avg','4km_NO','1p33km_NO', NO_stats,'NO, ppbv','NO_Hourly','no')
hourly_ref(combined1,'t100u_so2_Avg','4km_SO2','1p33km_SO2', SO2_stats,'SO2, ppbv','SO2_Hourly','no')

# Run mean diurnal
diurnal_plot(combined1,'m205_O3_Avg','4km_O3','1p33km_O3', O3_stats,'O3, ppb','O3_Diurnal','yes')
diurnal_plot(combined1,'m405_NO2_Avg','4km_NO2','1p33km_NO2', NO2_stats,'NO2, ppb','NO2_Diurnal','yes')
diurnal_plot(combined1,'m405_NO_Avg','4km_NO','1p33km_NO', NO_stats,'NO, ppb','NO_Diurnal','yes')
diurnal_plot(combined1,'t100u_so2_Avg','4km_SO2','1p33km_SO2', SO2_stats,'SO2, ppb','SO2_Diurnal','yes')

# Run regression functions to compare models to eachother 
regression(combined2,'4km_O3','1p33km_O3','m205_O3_Avg', O3_regression_stats, 'O3', 'O3_regression', 'O3 (ppb)')
regression(combined2,'4km_NO2','1p33km_NO2','m405_NO2_Avg', NO2_regression_stats, 'NO2', 'NO2_regression', 'NO2 (ppb)')
regression(combined2,'4km_NO','1p33km_NO','m405_NO_Avg', NO_regression_stats, 'NO', 'NO_regression', 'NO (ppb)')
regression(combined2,'4km_SO2','1p33km_SO2','t100u_so2_Avg', SO2_regression_stats, 'SO2', 'SO2_regression', 'SO2 (ppb)')

end_time = time.time()
print("Run time was %s seconds"%(end_time-begin_time))
print('End of Script')
