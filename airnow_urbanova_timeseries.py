
# This script is modifed based on Vikram Ravi's python code
# program for evaluation of PM2.5 for airpact 5 using airnow data
# author - vikram ravi
# dated - 2016-02-10

############################################################################################################################
# import some libraries
import matplotlib as mpl
mpl.use('Agg')
import pandas as pd
import numpy as np
import time
import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
import os
from netCDF4 import Dataset
from matplotlib.backends.backend_pdf import PdfPages
from calendar import monthrange

print('Start of airnow Analysis')


starttime = time.time()
day='01'
month = '04' 
year  = '2018' 

endday = '31'
endmonth='05'
endyear='2018'

#end_year=int(endyear)
#end_month=int(endmonth) 
#endday = str(monthrange(end_year, end_month)[1])

inputDir          = r'E:\Research\Urbanova_Jordan/'
plotDir           =r'E:\Research\Urbanova_Jordan\output/'
urb_path = inputDir +  'Urbanova_ref_site_comparison/Urbanova/'
air_path = inputDir + 'Urbanova_refEsite_comparison/AIRPACT/'

#inputDir = '/data/lar/users/jmunson'       #Aeolus
#urb_path = '/data/lar/projects/Urbanova' + '/'   #Aeolus
#air_path = '/data/airpact5/AIRRUN' + '/'    #Aeolus

# Set file paths
file_modelled_base = inputDir +'/merged.csv'
print(file_modelled_base)
file_airnowsites  = inputDir+ '/aqsid.csv'
#file_airnowsites  = '/data/lar/projects/Urbanova/2018/2018040400/POST/CCTM/aqsid.csv' # Hard coded as some aqsid files do not include all site ID's, this one does.
print(file_airnowsites)

begin_time = time.time()

#Setup time to pull AIRPACT data
start = dt.datetime(year=int(year), month=int(month), day=int(day), hour=0)
end = dt.datetime(year=int(endyear), month=int(endmonth), day=int(endday), hour=23)
timezone = pytz.timezone("utc") #("America/Los_Angeles")
start = timezone.localize(start)
end = timezone.localize(end)
'''
print("Start date is "+ start.strftime("%Y%m%d") )

## Pull AIRNow data and concatenate
# prepare time loop to read model output
date_diff =end -start
date_diff =  int(round( date_diff.total_seconds()/60/60/24)) # total hour duration

print("start date is "+ start.strftime("%Y%m%d") )
now = start

merged = []

# For loop to find the AIRNOW dat files for specified time period
for t in range(0, date_diff):
    
    # set a directory containing Urbanova AIRNOW data
    datadir = urb_path + now.strftime("%Y") + "/" + now.strftime("%Y%m%d")+"00/POST/CCTM/" 

    # Complete file path to data 
    f= datadir +"AIRNowSites_" +  now.strftime("%Y%m%d") + "_v6.dat"
    print(t, f)
    
    read = pd.read_csv(f)
    merged.append(read)
    
    #Changes day to next
    now += timedelta(hours=24)
    
    # Handles missing days
    try:
        datadir = urb_path + now.strftime("%Y") + "/" + now.strftime("%Y%m%d")+"00/POST/CCTM/" 
        f= datadir +"AIRNowSites_" +  now.strftime("%Y%m%d") + "_v6.dat" 
        read = pd.read_csv(f)
    except:
        print('adding 24 hours')
        now += timedelta(hours=24)
    try:
        datadir = urb_path + now.strftime("%Y") + "/" + now.strftime("%Y%m%d")+"00/POST/CCTM/" 
        f= datadir +"AIRNowSites_" +  now.strftime("%Y%m%d") + "_v6.dat"
        read = pd.read_csv(f)
    except:
        print('adding another 24 hours')
        now += timedelta(hours=24)
     
result = pd.concat(merged)
result.to_csv(inputDir + '/merged.csv',index=False)

print('AIRNOW data concatenated')
'''
# Open statistics script
exec(open(inputDir +"/statistical_functions.py").read()) 
#%%
def airnow(pollutant, abrv, unit):
    print('Running ' + abrv)
    global df_base
    # Read files
    if abrv == 'O3' or abrv == 'PM2.5':
        col_names_modeled = ['date', 'time', 'site_id', 'pollutant', 'concentration']
        col_names_observed= ['datetime', 'site_id', 'O3_AP5_4km', 'PM2.5_AP5_4km', 'O3_obs', 'PM2.5_obs']
        df_base  = pd.read_csv(file_modelled_base, header=None, names=col_names_modeled, sep='|',dtype='unicode')   #AIRNOW data is seperated by |, thus it has to be specified here
        df_obs   = pd.read_csv('http://lar.wsu.edu/R_apps/2018ap5/data/hrly2018.csv', sep=',', names=col_names_observed, skiprows=[0],dtype='unicode')
        df_sites = pd.read_csv(file_airnowsites, skiprows=[1],dtype='unicode') # skip 2nd row which is blank
        df_sites.rename(columns={'AQSID':'site_id'}, inplace=True)
        print('O3/PM2.5 files read')
    elif abrv == 'CO' or abrv == 'NOX':
        col_names_modeled = ['date', 'time', 'site_id', 'pollutant', 'concentration']
        col_names_observed= ['datetime', 'site_id', 'CO_AP5_4km', 'NOX_AP5_4km', 'CO_obs', 'NOX_obs']
        df_base   = pd.read_csv(file_modelled_base, header=None, names=col_names_modeled, sep='|',dtype='unicode')   #AIRNOW data is seperated by |, thus it has to be specified here
        df_obs   = pd.read_csv('http://lar.wsu.edu/R_apps/2018ap5/data/hrly2018_conox.csv', sep=',', names=col_names_observed, skiprows=[0],dtype='unicode')
        df_sites = pd.read_csv(file_airnowsites, skiprows=[1],dtype='unicode') # skip 2nd row which is blank
        df_sites.rename(columns={'AQSID':'site_id'}, inplace=True)
        print('CO/NOX files read')  
    else:
        col_names_modeled = ['date', 'time', 'site_id', 'pollutant', 'concentration']
        col_names_observed= ['datetime', 'site_id', 'SO2_AP5_4km', 'SO2_obs']
        df_base   = pd.read_csv(file_modelled_base, header=None, names=col_names_modeled, sep='|',dtype='unicode')   #AIRNOW data is seperated by |, thus it has to be specified here
        df_obs   = pd.read_csv('http://lar.wsu.edu/R_apps/2018ap5/data/hrly2018_so2.csv', sep=',', names=col_names_observed, skiprows=[0],dtype='unicode')
        df_sites = pd.read_csv(file_airnowsites, skiprows=[1],dtype='unicode') # skip 2nd row which is blank
        df_sites.rename(columns={'AQSID':'site_id'}, inplace=True)
        print('SO2 files read')        
    # extract only abrv data
    df_base = df_base.loc[df_base['pollutant']==pollutant, df_base.columns]
    # Renames the abrv to concentration
    df_base.columns = df_base.columns.str.replace('concentration',abrv+ '_AP5_1.33km')

    # convert datatime colume to time data (This conversion is so slow)
    print('Executing datetime conversion, this takes a while')
    df_base['datetime'] = pd.to_datetime(df_base['date'] + ' ' + df_base['time'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
    df_obs['datetime'] = pd.to_datetime(df_obs['datetime'], infer_datetime_format=True)
    print('datetime conversion complete')

    #Convert model data to PST from UTC (PST = UTC-8)
    df_base["datetime"] = df_base["datetime"].apply(lambda x: x - dt.timedelta(hours=8))
    df_obs["datetime"] = df_obs["datetime"].apply(lambda x: x - dt.timedelta(hours=8))
    df_base = df_base.drop('date',axis=1)
    df_base = df_base.drop('time',axis=1)
    # sites which are common between base and Observations
    sites_common = set(df_obs['site_id']).intersection(set(df_base['site_id']))


    ## take only the data which is for common sites
    df_obs_new = pd.DataFrame(columns=df_obs.columns)
    df_base_new = pd.DataFrame(columns=df_base.columns)
    for sites in sites_common:
        #    print sites
        df1 = df_obs.loc[df_obs['site_id']==sites, df_obs.columns]
        df3 = df_base.loc[df_base['site_id']==sites, df_base.columns]
        df_obs_new = pd.concat([df_obs_new, df1], join='outer', ignore_index=True)
        df_base_new = pd.concat([df_base_new, df3], join='outer', ignore_index=True)

    # merge now
    df_obs_mod = pd.merge(df_obs_new, df_base_new, on=['datetime', 'site_id'], how='outer')

    # get rid of rows if abrv base is not available
    df_obs_mod = df_obs_mod[pd.notnull(df_obs_mod[abrv+'_AP5_1.33km'])]



    df_tseries = df_obs_mod.copy() 
    df_siteinfo = df_sites.set_index('site_id')

# convert object to numeric (This is required to plot these columns)
    df_tseries.loc[:,abrv+'_AP5_4km'] = pd.to_numeric(df_tseries.loc[:,abrv+'_AP5_4km'])
    df_tseries.loc[:,abrv+'_AP5_1.33km'] = pd.to_numeric(df_tseries.loc[:,abrv+'_AP5_1.33km'])
    df_tseries.loc[:,abrv+'_obs'] = pd.to_numeric(df_tseries.loc[:,abrv+'_obs'])

    df_tseries['datetime'] = df_tseries['datetime'].dt.tz_localize('UTC').dt.tz_convert('US/Pacific')
    print(set(df_tseries['site_id']))
#%%
    # Set plot parameters
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
    #print(df_tseries)
#Plot
    for sid in list(set(df_tseries['site_id'])):
        d = df_tseries.loc[df_tseries['site_id']==sid]
        site_nameinfo = df_siteinfo.ix[sid, 'long_name']
        d.drop('site_id',1)
        fig,ax=plt.subplots(1,1, figsize=(12,4))
        d.set_index('datetime').ix[:,[abrv+'_obs', abrv+'_AP5_4km', abrv+'_AP5_1.33km']].plot(kind='line', style='-', ax=ax, color=['black', 'blue', 'red'], label=['OBS', 'sens', 'base'])
        ax.set_title(site_nameinfo)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.set_ylabel(abrv+' '+unit)
        ax.set_xlabel('PST')        
        ax.legend(['OBS', 'AP5_4km', 'AP5_1.33km'], fontsize=12)
    
    #Calculate Statistics
        try:
            #Run stats functions
            aq_stats_4km = stats(d, abrv+'_AP5_4km', abrv+'_obs')
            aq_stats_1p33km = stats(d, abrv+'_AP5_1.33km', abrv+'_obs')
            aq_stats = pd.merge(aq_stats_1p33km, aq_stats_4km, how = 'inner', left_index = True, right_index = True)
        
            aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_1.33km', '1.33km ' + site_nameinfo)    
            aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
            g = pd.merge(g, aq_stats, how = 'inner', left_index = True, right_index = True)
   
        #Clean up column names
            aq_stats.columns = aq_stats.columns.str.replace('1.33km ' + site_nameinfo, '1.33km')    
            aq_stats.columns = aq_stats.columns.str.replace('4km ' + site_nameinfo, '4km')     
        
        #Drop some stats to put on plots
            aq_stats = aq_stats.drop('MB',0)        
            aq_stats = aq_stats.drop('ME',0)
            aq_stats = aq_stats.drop('RMSE',0)
            aq_stats = aq_stats.drop('NMB',0)
            aq_stats = aq_stats.drop('NME',0)

#            ax.text(0,-0.25, aq_stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
        
        except (ZeroDivisionError):
            print('No observed data, statistics cannot be calculated')
        plt.savefig(inputDir +'/airnow/'+month+'/timeseries_plot/hourly_'+abrv+'_'+site_nameinfo+'_'+ year +month +day+ '-' + endyear + endmonth + endday+'.pdf', pad_inches=0.1, bbox_inches='tight')
    g.to_csv(inputDir +'/airnow/'+month+ '/airnow_'+abrv+'_stats.csv')
    print(df_tseries)
# Scatter plots
    for sid in list(set(df_tseries['site_id'])):
        fig,ax=plt.subplots(1,1, figsize=(8,8))
        d = df_tseries.loc[df_tseries['site_id']==sid]
        site_nameinfo = df_siteinfo.ix[sid, 'long_name']
        d.drop('site_id',1)
        d=d.set_index('datetime')
        d=d.groupby(d.index.hour).rolling('24H').mean().ix[:,[abrv+'_obs', abrv+'_AP5_4km', abrv+'_AP5_1.33km']]
        ax.scatter(d[abrv+'_obs'], d[abrv+'_AP5_4km'], c='b', label = '4km',linewidths=None, alpha=0.8)
        ax.scatter(d[abrv+'_obs'], d[abrv+'_AP5_1.33km'], c='r', marker='s', label = '1.33km',linewidths=None,alpha=0.8)        
        axismax = max(max(d[abrv+'_AP5_4km']),max(d[abrv+'_AP5_1.33km']))
        plt.plot([0,axismax], [0,axismax], color='black')
        ax.set_aspect('equal', 'box')
        plt.axis('equal')
        ax.set_ylabel('Modeled '+abrv+' '+unit)
        ax.set_xlabel('Observed '+abrv+' '+unit)        
        ax.set_title(site_nameinfo) 
        plt.legend()
        ax.set_ylim(0,axismax)
        ax.set_xlim(0,axismax)
       # print(d)

#Calculate Statistics
        try:
            #Run stats functions
            aq_stats_4km = stats(d, abrv+'_AP5_4km', abrv+'_obs')
            aq_stats_1p33km = stats(d, abrv+'_AP5_1.33km', abrv+'_obs')
            aq_stats = pd.merge(aq_stats_1p33km, aq_stats_4km, how = 'inner', left_index = True, right_index = True)
        
            aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_1.33km', '1.33km ' + site_nameinfo)    
            aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
   
        #Clean up column names
            aq_stats.columns = aq_stats.columns.str.replace('1.33km ' + site_nameinfo, '1.33km')    
            aq_stats.columns = aq_stats.columns.str.replace('4km ' + site_nameinfo, '4km')     
        
        #Drop some stats to put on plots
            aq_stats = aq_stats.drop('MB',0)        
            aq_stats = aq_stats.drop('ME',0)
            aq_stats = aq_stats.drop('RMSE',0)
            aq_stats = aq_stats.drop('NMB',0)
            aq_stats = aq_stats.drop('NME',0)

#            ax.text(0,-0.12, aq_stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
            plt.savefig(inputDir +'/airnow/'+month+'/scatter_plots/scatter_'+abrv+'_'+site_nameinfo+'_'+ year +month +day+ '-' + endyear + endmonth + endday+'.pdf', pad_inches=0.1, bbox_inches='tight') #Placed this here so that if there is no oberved data, it won't save an empty plot

        except (ZeroDivisionError):
            pass
        plt.savefig(inputDir +'/airnow/'+month+'/scatter_plots/scatter_'+abrv+'_'+site_nameinfo+'_'+ year +month +day+ '-' + endyear + endmonth + endday+'.pdf', pad_inches=0.1, bbox_inches='tight')
# Diurnal plots
    for sid in list(set(df_tseries['site_id'])):
        d = df_tseries.loc[df_tseries['site_id']==sid]
        site_nameinfo = df_siteinfo.ix[sid, 'long_name']
        d.drop('site_id',1)
        fig,ax=plt.subplots(1,1, figsize=(12,4))
        d=d.set_index('datetime')
        b=d.groupby(d.index.hour).std()
        d.groupby(d.index.hour).mean().ix[:,[abrv+'_obs', abrv+'_AP5_4km', abrv+'_AP5_1.33km']].plot(kind='line', style='-', ax=ax, color=['black', 'blue', 'red'], label=['OBS', 'sens', 'base'])
        ax.set_title(site_nameinfo)
        ax.set_ylabel(abrv+' '+unit)
        ax.set_xlabel('Mean Diurnal (hours)')
        d = d.groupby(d.index.hour).mean()
        e = b
        c = d-b
        e = d+b
        x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        ax.set_ylim(bottom=0)
        plt.fill_between(x, c[abrv+'_AP5_4km'], e[abrv+'_AP5_4km'], facecolor='blue', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) 
        plt.fill_between(x, c[abrv+'_AP5_1.33km'], e[abrv+'_AP5_1.33km'],facecolor='red', edgecolor='black',alpha = 0.1, label=['Std. Dev.'])     
        ax.legend(['OBS', 'AP5_4km', 'AP5_1.33km', 'Std. Dev.'], fontsize=12)
        print('Plotted ' + site_nameinfo)
        
#Calculate Statistics
        try:
            #Run stats functions
            aq_stats_4km = stats(d, abrv+'_AP5_4km', abrv+'_obs')
            aq_stats_1p33km = stats(d, abrv+'_AP5_1.33km', abrv+'_obs')
            aq_stats = pd.merge(aq_stats_1p33km, aq_stats_4km, how = 'inner', left_index = True, right_index = True)
        
            aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_1.33km', '1.33km ' + site_nameinfo)    
            aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
   
        #Clean up column names
            aq_stats.columns = aq_stats.columns.str.replace('1.33km ' + site_nameinfo, '1.33km')    
            aq_stats.columns = aq_stats.columns.str.replace('4km ' + site_nameinfo, '4km')     
        
        #Drop some stats to put on plots
            aq_stats = aq_stats.drop('MB',0)        
            aq_stats = aq_stats.drop('ME',0)
            aq_stats = aq_stats.drop('RMSE',0)
            aq_stats = aq_stats.drop('NMB',0)
            aq_stats = aq_stats.drop('NME',0)

#            ax.text(0,-0.25, aq_stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
        
        except (ZeroDivisionError):
            pass
        plt.savefig(inputDir+'/airnow/'+month+'/diurnal_plot/'+abrv+'_'+site_nameinfo+'_'+ year +month +day+ '-' + endyear + endmonth + endday+'.pdf',  pad_inches=0.1, bbox_inches='tight')

#%%
# Run the function
#airnow('OZONE','O3','($ppb$)')
airnow('PM2.5','PM2.5','($ug/m^3$)')
#airnow('CO','CO','($ppb$)')
#airnow('NOX','NOX','($ppb$)')
#airnow('SO2','SO2','($ppb$)')     No SO2 data in airnow v5


end_time = time.time()
print("Run time was %s seconds"%(end_time-begin_time))
print("End of airnow Analysis")











