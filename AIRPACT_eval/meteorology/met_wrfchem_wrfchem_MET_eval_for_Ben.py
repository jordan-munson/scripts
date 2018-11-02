# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 18:06:15 2018

This script reads wrfout files and generates a dataframe for selected variables.

To run this script successfully, you needs "inputs" directory with all obs files and "outputs" where output files get saved. 

The followng parameters have to be modified before using: 
base_dir - a directory where python scripts and input subdirectory
datadir - a directory where wrfout is saved
start  - start date
end - end date

@author: yunhalee
"""
import matplotlib
#matplotlib.use('Agg')  # Uncomment this when using in Kamiak/Aeolus

# Set a directory containing python scripts and observation data
base_dir = "/Users/yunhalee/Desktop/worldbestpostprocessing/met/wrfchem/"

# set a directory containing wrfout files
datadir = "/Users/yunhalee/"

# all the functions are saved in AQS_evaluation_CE588.py
exec(open(base_dir +"Met_functions.py").read())

import pandas as pd
import numpy as np
import time
import datetime
from datetime import timedelta
import pytz
import os

# set start and end date
start = datetime.datetime(year=2017, month=8, day=29, hour=0)
end = datetime.datetime(year=2017, month=8, day=29, hour=23)
timezone = pytz.timezone("utc")
start = timezone.localize(start)
end = timezone.localize(end)

# open one of wrfout to read coordinate
modeloutput= datadir +"inputs/wrfout_d01_" +  start.strftime("%Y-%m-%d_00:00:00") # this is subset of wrfout for git repository

# open and read wrfout using netCDF function (Dataset)
if os.path.isfile(modeloutput):
    nc  = Dataset(modeloutput, 'r')
    print('reading ', modeloutput)
#elif os.path.isfile(modelrstoutput):
#    nc  = Dataset(modelrstoutput, 'r')
#    print('reading ', modelrstoutput)
else:
    print("no file")
    exit()

# x_dim and y_dim are the x (lon) and y (lat) dimensions of the model
x_dim = len(nc.dimensions['west_east'])
y_dim = len(nc.dimensions['south_north'])

# obtain model lat and lon - needed for AQS eval and basemap
lon = nc.variables['XLONG'][0]
lat  = nc.variables['XLAT'][0]

# Get the grid spacing
dx = float(nc.DX)
dy = float(nc.DY)
width_meters = dx * (int(x_dim) - 1)     #Domain Width
height_meters = dy * (int(y_dim) - 1)    #Domain Height

#more WRFCHEM map information needed for basemap
cen_lat = float(nc.CEN_LAT)
cen_lon = float(nc.CEN_LON)
truelat1 = float(nc.TRUELAT1)
truelat2 = float(nc.TRUELAT2)
standlon = float(nc.STAND_LON)

# close the wrfout
nc.close()

# reads WRF-Chem chemical tracers and saves them in a dictionary (wrf_3d)
wrf_3d = get_wrfchem_DF(datadir, start, end)


'''
#%%

## Ben - please feel free to use the code below as an example to create MET evaluation plots. Note that the code is for air qualtiy evaluation


############################################
# time-series plots with obs and model PM2.5
############################################

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
from matplotlib import dates
from matplotlib.dates import date2num, DayLocator, DateFormatter
import copy
import seaborn as sns

print("AQS evaluation begins") 

all_AQS = get_AQS_AIRPACT_data(base_dir, start, end) # PM2.5
all_AQS.rename(columns={'PM2.5_mod':'PM2.5_airpact'}, inplace=True)
all_AQS.rename(columns={'O3_mod':'O3_airpact'}, inplace=True)

# these info is used to download AQS data and more
wrfchem_sp = ['PM2.5_wrfchem', 'O3_wrfchem']
airpact_sp = ['PM2.5_airpact', 'O3_airpact']
obs_sp = ['PM2.5_obs', 'O3_obs']
ylabel_sp = ['PM2.5 [ug m-3]' , 'O3 [ppb]' ]

plt.style.use('seaborn-white')
plt.rcParams['xtick.major.size']  = 5
plt.rcParams['xtick.major.width'] = 1
plt.rcParams['xtick.minor.size']  = 4
plt.rcParams['xtick.minor.width'] = 1
plt.rcParams['ytick.major.size']  = 5
plt.rcParams['ytick.major.width'] = 1
plt.rcParams['ytick.minor.size']  = 4
plt.rcParams['ytick.minor.width'] = 1
plt.rcParams['ytick.direction']   = 'in'
plt.rcParams['xtick.direction']   = 'in'

# this is needed for x-axis label
dfmt = dates.DateFormatter('%m-%d %H')

for i, sp in enumerate(obs_sp): 
    
    AQS = all_AQS[pd.notnull(all_AQS[sp])]  #df.dropna(subset = ['column_name'])

    cnt = 0
    figs = plt.figure()
    plot_num = 321 # 6 plots in a single page
    fig = plt.figure(figsize=(10, 10)) # inches

    print("start date is "+ start.strftime("%Y%m%d") )
    print("end date is "+ end.strftime("%Y%m%d") )

    out_pdf = base_dir+'/outputs/'+ obs_sp[i] + '_'+ start.strftime("%Y%m%d") + '-' +  end.strftime("%Y%m%d") +"_wrfchem_eval.pdf"
    print(out_pdf)

    pdf = PdfPages(out_pdf)
    
    sites = np.array(list(set(AQS['AQSID'])))

    for sid in list(set(AQS['AQSID'])):
        #print(sid, cnt, plot_num)
        ax = plt.subplot(plot_num)
        d = AQS.loc[AQS['AQSID']==sid]
        d.Latitude = d.Latitude.astype(float)

        # check if there is enough data point
        if(d.shape[0] < 10):
            continue

        # get observation lat/lon
        inputlats = d['Latitude'].unique()[0]
        inputlons = d['Longitude'].unique()[0]

        mod_sample ={}
        
        # sample lat/lon grid information
        iy,ix = naive_fast(lat, lon, inputlats, inputlons)

        for k in wrf_3d.keys():
            mod_sample[k] = wrf_3d[k][:,iy,ix].flatten()

        # create new dataframe using the model sample data
        d_mod = pd.DataFrame(mod_sample)
        d_mod.rename(columns={'PM25':'PM2.5_wrfchem'}, inplace=True)
        d_mod.rename(columns={'o3':'O3_wrfchem'}, inplace=True)
        d_mod['DateTime'] = pd.to_datetime(d_mod['DateTime'])
        d_all = d.merge(d_mod, how='left')
        
        # hard-coded time zone conversion because of matplotlib
        d_all['DateTime']  = d_all['DateTime']  - timedelta(hours = 8)

        # compute statistics
        aq_stats = stats(d_all, wrfchem_sp[i], obs_sp[i])
        aq_stats.loc['model'] = ['wrfchem']
        airpact_stats = stats(d_all, airpact_sp[i], obs_sp[i])
        airpact_stats.loc['model'] = ['airpact']
        aq_stats = pd.concat([aq_stats, airpact_stats], axis=1, join_axes=[aq_stats.index] )
        aq_T = aq_stats.T
        aq_T['lat'] = inputlats
        aq_T['lon'] = inputlons
        aq_T['long_name'] = str(d['long_name'].unique())[1:-1]  # try to reduce [ ]

        if(cnt > 0):
            aq_stats_all = aq_stats_all.append(aq_T, ignore_index=True)
            aq_all_sites = aq_all_sites.append(d_all, ignore_index=True)
        else:
            aq_stats_all=copy.copy(aq_T)
            aq_all_sites=copy.copy(d_all)

        # plot profile, define styles
        plt.plot(d_all['DateTime'] ,d_all[obs_sp[i]],'b',marker='o', linestyle='solid',linewidth=1, label="obs")
        plt.plot(d_all['DateTime'] ,d_all[wrfchem_sp[i]],'r',linewidth=1, label="WRF-Chem")
        plt.plot(d_all['DateTime'] ,d_all[airpact_sp[i]],'r',linestyle='dashed',linewidth=1, label="AIRPACT")
        ax.xaxis.set_major_formatter(dfmt)
        fig.autofmt_xdate(rotation=60)
        ax.locator_params(axis='y', nbins=5)

        plt.ylabel(ylabel_sp[i])
        ax.legend(loc='upper left', prop={'size': 9})
        text='{:.2f}'.format(d['Latitude'].unique()[0]) + ', {:.2f}'.format(d['Longitude'].unique()[0])

        # some site has no long_name, so the below (nan check) is needed
        a = pd.Series(d['long_name'].unique())
        print(d['long_name'].unique())

        if(pd.isnull(a[0])):
            print("found")
            plt.title(text)
        else:
            b = str(d['long_name'].unique())[1:-1]
            plt.title(b[:20] +" " + text)

        plt.tight_layout()
        # Yunha - Don't change the order of the below code (plot_num, if, and cnt)
        plot_num += 1

        if(cnt > 0) & (np.remainder(cnt,6) == 5):
            print("saving at cnt :", cnt)
            pdf.savefig(fig)
            plot_num = 321
            fig = plt.figure(figsize=(10, 10)) # inches

        cnt += 1
    
    # save stats into an excel file
    writer = pd.ExcelWriter(base_dir + '/outputs/STATS_AQS_'+obs_sp[i] + '_'+ start.strftime("%Y%m%d") + '-' +  end.strftime("%Y%m%d") + '.xlsx')
    aq_stats_all.to_excel(writer,'Sheet1')
    writer.save()

    pdf.close()    
    plt.close('all')


#%%
############################################
# averaged diurnal cycle for obs and model PM2.5
############################################

plt.style.use('seaborn-white')
plt.rcParams['xtick.major.size']  = 5
plt.rcParams['xtick.major.width'] = 1
plt.rcParams['xtick.minor.size']  = 4
plt.rcParams['xtick.minor.width'] = 1
plt.rcParams['ytick.major.size']  = 5
plt.rcParams['ytick.major.width'] = 1
plt.rcParams['ytick.minor.size']  = 4
plt.rcParams['ytick.minor.width'] = 1
plt.rcParams['ytick.direction']   = 'in'
plt.rcParams['xtick.direction']   = 'in'

# this is needed for x-axis label
dfmt = dates.DateFormatter('%m-%d %H')

for i, sp in enumerate(obs_sp):
    
    # get rid of the rows with no observation ( commenting the line below will let two models compare)
    AQS = all_AQS[pd.notnull(all_AQS[sp])]  #df.dropna(subset = ['column_name'])
    cnt = 0
    figs = plt.figure()
    plot_num = 321 # 6 plots in a single page
    fig = plt.figure(figsize=(10, 10)) # inches

    out_pdf = base_dir+'/outputs/mean_Diurnal_'+ obs_sp[i] + '_'+ start.strftime("%Y%m%d") + '-' +  end.strftime("%Y%m%d") +"_wrfchem_eval.pdf"
    print(out_pdf)

    pdf = PdfPages(out_pdf)

    sites = np.array(list(set(AQS['AQSID'])))

    for sid in list(set(AQS['AQSID'])):

        ax = plt.subplot(plot_num)
        d = AQS.loc[AQS['AQSID']==sid]
        d.Latitude = d.Latitude.astype(float)
        # check if there is enough data point
        if(d.shape[0] < 10):
            continue

        # get observation lat/lon
        inputlats = d['Latitude'].unique()[0]
        inputlons = d['Longitude'].unique()[0]
        
        mod_sample ={}

        # sample lat/lon grid information
        iy,ix = naive_fast(lat, lon, inputlats, inputlons)

        for k in wrf_3d.keys():
            mod_sample[k] = wrf_3d[k][:,iy,ix].flatten()

        # create new dataframe using the model sample data
        d_mod = pd.DataFrame(mod_sample)
        d_mod.rename(columns={'PM25':'PM2.5_wrfchem'}, inplace=True)
        d_mod.rename(columns={'o3':'O3_wrfchem'}, inplace=True)
        d_mod['DateTime'] = pd.to_datetime(d_mod['DateTime'])
        d_all = d.merge(d_mod, how='left')
        d_all = d_all.set_index('DateTime')        
        
        # hard-coded time zone conversion because of matplotlib
        d_all.index  = d_all.index  - timedelta(hours = 8)
        d_all['hour_PST'] = d_all.index.hour

        # averaged diurnal data 
        #d_hourly = d_all.resample('H').mean()
        d_hourly = d_all.groupby(d_all.index.hour).mean()

        # compute statistics
        aq_stats = stats(d_hourly, wrfchem_sp[i], obs_sp[i])
        aq_stats.loc['model'] = ['wrfchem']
        airpact_stats = stats(d_hourly, airpact_sp[i], obs_sp[i])
        airpact_stats.loc['model'] = ['airpact']
        aq_stats = pd.concat([aq_stats, airpact_stats], axis=1, join_axes=[aq_stats.index] )
        aq_T = aq_stats.T
        aq_T['lat'] = inputlats
        aq_T['lon'] = inputlons
        aq_T['long_name'] = str(d['long_name'].unique())[1:-1]  # try to reduce [ ]

        if(cnt > 0):
            aq_stats_all = aq_stats_all.append(aq_T, ignore_index=True)
            aq_all_sites = aq_all_sites.append(d_hourly, ignore_index=True)
        else:
            aq_stats_all=copy.copy(aq_T)
            aq_all_sites=copy.copy(d_hourly)
      
        sns.boxplot(x= "hour_PST", y= wrfchem_sp[i], data=d_all, color="red", boxprops=dict(alpha=.3))
        sns.boxplot(x= "hour_PST", y= airpact_sp[i], data=d_all, color="green", boxprops=dict(alpha=.3))
        sns.boxplot(x= "hour_PST", y= obs_sp[i], data=d_all, color="blue", boxprops=dict(alpha=.3))
        plt.xlabel("hour [PST]")
        plt.ylabel(ylabel_sp[i])
        text='{:.2f}'.format(d['Latitude'].unique()[0]) + ', {:.2f}'.format(d['Longitude'].unique()[0])

        # some site has no long_name, so the below (nan check) is needed
        a = pd.Series(d['long_name'].unique())
        print(d['long_name'].unique())

        if(pd.isnull(a[0])):
            print("found")
            plt.title(text)
        else:
            b = str(d['long_name'].unique())[1:-1]
            plt.title(b[:20] +" " + text)

        plt.tight_layout()
        # Yunha - Don't change the order of the below code (plot_num, if, and cnt)
        plot_num += 1

        if(cnt > 0) & (np.remainder(cnt,6) == 5):
            print("saving at cnt :", cnt)
            pdf.savefig(fig)
            plot_num = 321
            fig = plt.figure(figsize=(10, 10)) # inches

        cnt += 1

    # save stats into an excel file
    writer = pd.ExcelWriter(base_dir + '/outputs/DIRUNAL_AQS_'+obs_sp[i] + '_'+ start.strftime("%Y%m%d") + '-' +  end.strftime("%Y%m%d") + '.xlsx')
    aq_stats_all.to_excel(writer,'Sheet1')
    aq_all_sites.to_excel(writer,'Sheet2')
    writer.save()

    pdf.close()

plt.close('all')

#%%
#########################################################
# Create pairplots betwen AQ and met variable at PM AQS sites
#########################################################
print("start pairplots for AQS")

temp = {}
#temp_list = ['PM25', 'o3', 'T2','PBLH','U10', 'V10', 'DateTime']
temp_list = ['PM25', 'o3', 'T2', 'DateTime']


AQS = all_AQS[pd.notnull(all_AQS['O3_obs'])] 
    
for sid in list(set(AQS['AQSID'])):
    print(sid)

    d = AQS.loc[AQS['AQSID']==sid]
    d.Latitude = d.Latitude.astype(float) # This column was object not float
    
    # check if there is enough data point
    if(d.shape[0] < 10):
        continue

    # get observation lat/lon
    inputlats = d['Latitude'].unique()[0]
    inputlons = d['Longitude'].unique()[0]

    mod_sample ={}
    
    # sample lat/lon grid information
    iy,ix = naive_fast(lat, lon, inputlats, inputlons)

    for k in temp_list:
        temp[k] = wrf_3d[k][:,iy,ix].flatten()

    # d_temp will have daily mean for Pres, TEMP2, winds, and RGRND and hourly TEMP2
    d_temp = pd.DataFrame(temp)
    d_temp['DateTime'] = pd.to_datetime(d_temp['DateTime'])
    d_temp = d_temp.set_index('DateTime')
    d_temp.describe()

    # site name and lat/lon
    text='{:.2f}'.format(d['Latitude'].unique()[0]) + '_{:.2f}'.format(d['Longitude'].unique()[0])

    # some site has no long_name, so the below (nan check) is needed
    a = pd.Series(d['long_name'].unique())
    print(d['long_name'].unique())

    if(pd.isnull(a[0])):
        print("found")
        b =text
    else:
        b = str(d['long_name'].unique())[1:-1]
        b = b[:20] +text

    g = sns.pairplot(d_temp[['PM25', 'o3', 'T2']], kind="reg" )
    for ax in g.axes.flat:
        plt.setp(ax.get_xticklabels(), rotation=45)
    g.savefig(base_dir + "outputs/AQ_vs_met_pairplot_" +b+ "_at_AQSsite.png")

    plt.close('all')
    del d_temp

#%%
###############################################
# create surface PM2.5 and O3 distribution map 
###############################################
print("basemap started")

# Draw the base map behind it with the lats and lons calculated earlier
m = Basemap(resolution='i',projection='lcc',width=width_meters,\
height=height_meters,lat_0=cen_lat,lon_0=cen_lon,lat_1=truelat1,lat_2=truelat2)

x,y = m(lon,lat)

#save maps into the pdf file (two maps in single page)
with PdfPages(base_dir+'outputs/WRFChem_PM25_O3_map_' + '_'+ start.strftime("%Y%m%d") + '-' +  end.strftime("%Y%m%d") + '.pdf') as pdf:
    fig = plt.figure(figsize=(14,10))
    ax = fig.add_subplot(121)
    k = "o3"
    ax.set_title(k)

    # compute auto color-scale using maximum concentrations
    up_scale = np.percentile(wrf_3d[k], 95)
    clevs = np.round(np.arange(0, up_scale, up_scale/10),3)
    print("debug clevs", clevs, k)

    cblabel = 'ppb'
    cbticks = True
    cs = m.contourf(x,y,wrf_3d[k].mean(axis=0),clevs,cmap=plt.get_cmap('jet'), extend='both')
    cs.cmap.set_under('cyan')
    cs.cmap.set_over('black')

    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()

    cbar = m.colorbar(location='bottom',pad="5%")
    cbar.set_label(cblabel)
    if cbticks:
        cbar.set_ticks(clevs)
        cbar.ax.tick_params(labelsize=9)
    
    # print the surface-layer mean on the map plot
    plt.annotate("mean: " + str(wrf_3d[k].mean(axis=0).mean()) +" ppb", xy=(0, 1.02), xycoords='axes fraction')

    # do the same plot setup but for PM2.5 
    ax = fig.add_subplot(122)
    k= "PM25"
    ax.set_title(k)

    # compute auto color-scale using maximum concentrations
    up_scale = np.percentile(wrf_3d[k], 95)
    clevs = np.round(np.arange(0, up_scale, up_scale/10),1)
    print("debug clevs", clevs, k)

    cblabel = 'ug/m3'
    cbticks = True
    cs = m.contourf(x,y, wrf_3d[k].mean(axis=0),clevs,cmap=plt.get_cmap('jet'), extend='both')
    cs.cmap.set_under('cyan')
    cs.cmap.set_over('black')

    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()

    cbar = m.colorbar(location='bottom',pad="5%")
    cbar.set_label(cblabel)
    if cbticks:
        cbar.set_ticks(clevs)
        cbar.ax.tick_params(labelsize=12)

    # plot mean
    plt.annotate("mean: " + str(wrf_3d[k].mean(axis=0).mean()) +" ug m-3", xy=(0, 1.02), xycoords='axes fraction')

    pdf.savefig(fig) #save image file
    plt.show()

'''
