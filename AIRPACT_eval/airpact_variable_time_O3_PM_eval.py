# -*- coding: utf-8 -*-
"""


@author: Jordan Munson
"""
import matplotlib as mpl
#mpl.use('Agg') # Aeolus throws an error without this
import pandas as pd
import matplotlib.dates as mdates
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz
import numpy as np
import time
from subprocess import check_call 

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

starttime = time.time()
begin_time = time.time()

day='01'
month = '01' 
year  = '2018' 

endday = '31'
endmonth='12'
endyear='2018'

# =============================================================================
# # Aeolus directories
# inputDir = '/data/lar/users/jmunson/longterm_airpact/'
# stat_path = '/data/lar/users/jmunson/statistical_functions.py'
# aqsid = pd.read_csv(inputDir+'aqs_sites.csv')
# ben_path = inputDir + 'Met_functions_for_Ben.py'
# =============================================================================

#Set directory
inputDir = r'E:/Research/AIRPACT_eval/'
# Open statistics script
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'
ben_path = r'E:/Research/scripts/AIRPACT_eval/meteorology/Met_functions_for_Ben.py'
exec(open(stat_path).read())

##############################################################################
# Load model/obs data
##############################################################################

# Load saved AIRNOW data from R_apps site
df_1 = pd.read_csv('http://lar.wsu.edu/R_apps/2018ap5/data/hrly2018.csv', sep=',')  

# Convert to datetime and adjust to PST
print('Converting datetime, this may take a while')
df_1['datetime'] = pd.to_datetime(df_1['DateTime'], infer_datetime_format=True)
df_1["datetime"] = df_1["datetime"].apply(lambda x: x - dt.timedelta(hours=8)) #Adjust to PST
df_1 = df_1.drop(['DateTime'], axis=1)

print('Model data loaded')

#Create AQSID Column form state code, county code, and site num
aqsid = pd.read_csv(inputDir+'aqs_sites.csv')
aqsid = aqsid.ix[:,['State Code','County Code','Site Number','Local Site Name','Location Setting']]

aqsid['County Code'] = ["%03d" % n for n in aqsid['County Code'] ]
aqsid['Site Number'] = ["%04d" % n for n in aqsid['Site Number'] ]

aqsid['AQSID'] = (aqsid['State Code']).astype(str) + (aqsid['County Code']).astype(str)+(aqsid['Site Number']).astype(str)

# Must force every cell in AQSID to be a string, otherwise lose most of data
aqsid['AQSID'] = aqsid['AQSID'].astype(str)
df_1['AQSID'] = df_1['AQSID'].astype(str)

df_1 = pd.merge(df_1,aqsid) # Merge df_1 and aqsid so as to add names and such to the dataframe
df_1 = df_1.drop(['State Code','County Code', 'Site Number'], axis=1) # drop unecessary columns
print('Dataframe formatted with AQSID')
 
##############################################################################
# Manipulate dataframe to set up for plotting and create plot settings
##############################################################################

df_com = df_1 # original script used df_com past this point for everything

# Need to convert these to numeric
df_com.loc[:,'O3_mod'] = pd.to_numeric(df_com.loc[:,'O3_mod'], errors='coerce')
df_com.loc[:,'PM2.5_mod'] = pd.to_numeric(df_com.loc[:,'PM2.5_mod'], errors='coerce')
df_com.loc[:,'O3_obs'] = pd.to_numeric(df_com.loc[:,'O3_obs'], errors='coerce')
df_com.loc[:,'PM2.5_obs'] = pd.to_numeric(df_com.loc[:,'PM2.5_obs'], errors='coerce')

# Set plot parameters
mpl.rcParams['font.family'] = 'sans-serif'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 24.0
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

stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
stats_com = stats_com.drop(0,1)

#%%
##############################################################################
# Plot the data
##############################################################################


# =============================================================================
# # Scatter plots of modeled ozone vs pm
# for AQSID in list(set(df_com['AQSID'])):
#     #This section selects only data relevant to the aqs site
#     d = df_com.loc[df_com['AQSID']==AQSID]
#     d=d.reset_index()
#     site_nameinfo = d.loc[0,'Local Site Name'] #Gets the longname of the site to title the plot
#     d=d.ix[:,['PM2.5_mod','O3_mod','datetime']]
#     d['date'] = pd.to_datetime(d['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
#     d = d.set_index('datetime') 
#     d = d.resample('D').mean()
#     fig,ax=plt.subplots(1,1, figsize=(8,8)) #Set figure dimensions
#     #Find max values to set axis
#     #axismax = max(max(d['PM2.5_mod'],numeric_only=True),max(d['O3_mod']))     #This works on some PC's but not others
#     try:    #The axis max makes sure the x and y axis are the same
#         axismax= max(d.max(numeric_only=True))
#         ax.set_ylim(0,axismax)
#         ax.set_xlim(0,axismax)
#         plt.plot([0,axismax], [0,axismax], color='black')
#     except ValueError:
#         pass
#     
#     #Plot first section of year
#     mask = (d.index > '2014-7-1') & (d.index <= '2015-6-30')
#     da=d.loc[mask]
#     ax.scatter(da['PM2.5_mod'], da['O3_mod'], c='b', label = '07/14-07/15',linewidths=None, alpha=0.8) #Plotting the data
#     
#     #Plot first section of year
#     mask = (d.index > '2015-7-1') & (d.index <= '2016-6-30')
#     db=d.loc[mask]
#     ax.scatter(db['PM2.5_mod'], db['O3_mod'], c='r', label = '07/15-07/16',linewidths=None, alpha=0.7) #Plotting the data
#     
#     #Plot first section of year
#     mask = (d.index > '2016-7-1') & (d.index <= '2017-6-30')
#     dc=d.loc[mask]
#     ax.scatter(dc['PM2.5_mod'], dc['O3_mod'], c='g', label = '07/16-07/17',linewidths=None, alpha=0.7) #Plotting the data
#     
#     ax.set_aspect('equal', 'box')
#     plt.axis('equal')
#     ax.set_ylabel('Ozone')
#     ax.set_xlabel('$PM_{2.5}$')        
#     ax.set_title(site_nameinfo) 
#     plt.legend()
# 
#     plt.plot()
#     try:
#         if axismax>1:
#             plt.savefig(inputDir +'/plots/scatter/scatter_' + site_nameinfo+'.png', pad_inches=0.1, bbox_inches='tight')
#         else:
#             pass
#     except(FileNotFoundError):
#         pass
# =============================================================================

#%%        
# =============================================================================
# stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
# stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
# stats_com = stats_com.drop(0,1)
# 
# # Scatter plots of modeled vs observed
# pollutant = ['O3','PM2.5']
# for species in pollutant:
#     for AQSID in list(set(df_com['AQSID'])):
#         #This section selects only data relevant to the aqs site
#         d = df_com.loc[df_com['AQSID']==AQSID]
#         d=d.reset_index()
#         site_nameinfo = d.loc[0,'Local Site Name'] #Gets the longname of the site to title the plot
#         site_type = d.loc[0,'Location Setting']
#         d=d.ix[:,[species+'_obs',species+'_mod','datetime']]
#         d['date'] = pd.to_datetime(d['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
#         d = d.set_index('datetime') 
#         d = d.resample('D').mean()
#         fig,ax=plt.subplots(1,1, figsize=(8,8)) #Set figure dimensions
#         #Find max values to set axis
#         #axismax = max(max(d['PM2.5_mod'],numeric_only=True),max(d['O3_mod']))     #This works on some PC's but not others
#         try:    #The axis max makes sure the x and y axis are the same
#             axismax= max(d.max(numeric_only=True))
#             ax.set_ylim(0,axismax)
#             ax.set_xlim(0,axismax)
#             plt.plot([0,axismax], [0,axismax], color='black')
#         except ValueError:
#             pass
#     
#         #Plot first section of year
#         mask = (d.index > '2014-7-1') & (d.index <= '2015-6-30')
#         da=d.loc[mask]
#         ax.scatter(da[species+'_obs'], da[species+'_mod'], c='b', label = '07/14-07/15',linewidths=None, alpha=0.8) #Plotting the data
#     
#         #Plot first section of year
#         mask = (d.index > '2015-7-1') & (d.index <= '2016-6-30')
#         db=d.loc[mask]
#         ax.scatter(db[species+'_obs'], db[species+'_mod'], c='r', label = '07/15-07/16',linewidths=None, alpha=0.7) #Plotting the data
#     
#         #Plot first section of year
#         mask = (d.index > '2016-7-1') & (d.index <= '2017-6-30')
#         dc=d.loc[mask]
#         ax.scatter(dc[species+'_obs'], dc[species+'_mod'], c='g', label = '07/16-07/17',linewidths=None, alpha=0.7) #Plotting the data
#     
#         ax.set_aspect('equal', 'box')
#         plt.axis('equal')
#         if species =='PM2.5':
#             ax.set_ylabel('$PM_{2.5}$ Modeled')
#             ax.set_xlabel('$PM_{2.5}$ Observed')
#         else:
#             ax.set_ylabel('Ozone Modeled')
#             ax.set_xlabel('Ozone Observed')
#             
#         ax.set_title(str(site_nameinfo) +', Type: '+str(site_type)) 
#         plt.legend()
# 
#         #plt.plot()
#         try:
#             if species == 'PM2.5':
#                 if axismax>1:
#                     plt.savefig(inputDir +'/plots/scatter/scatter_PM_' + str(site_nameinfo)+'.png', pad_inches=0.1, bbox_inches='tight')
#                 else:
#                     pass
#             else:
#                 if axismax>1:
#                     plt.savefig(inputDir +'/plots/scatter/scatter_O3_' + str(site_nameinfo)+'.png', pad_inches=0.1, bbox_inches='tight')
#                 else:
#                     pass
#         except(FileNotFoundError):
#             pass
# 
# =============================================================================
#%%
stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
stats_com = stats_com.drop(0,1)
# =============================================================================
#         
# # Time series
# pollutant = ['O3','PM2.5']
# for species in pollutant:
#     for AQSID in list(set(df_com['AQSID'])):
#         #This section selects only data relevant to the aqs site
#         d = df_com.loc[df_com['AQSID']==AQSID]
#         d=d.reset_index()
#         site_nameinfo = d.loc[0,'Local Site Name'] #Gets the longname of the site to title the plot
#         site_type = d.loc[0,'Location Setting']
#         d=d.ix[:,[species+'_obs',species+'_mod','datetime']]
#         d['date'] = pd.to_datetime(d['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
#         dc = d.groupby(d.date.dt.year)
#         #print(dc)
#         
#         d = d.set_index('datetime') 
#         
#         #Calculate mb and fb
#         #for months in d:
#         #db=fb(d.groupby(d.index.month),species+'_mod', species+'_obs')#.rolling('24H').mean().ix[:,[species+'_mod', species+'_obs']]
#         
#         d = d.resample('M', convention='start').mean()
#         fig,ax=plt.subplots(1,1, figsize=(10,8)) #Set figure dimensions
# 
#         #Plot
#         d.ix[:,[species+'_obs', species+'_mod']].plot(kind='line', style='-', ax=ax, color=['black', 'blue'])
#         
#         if species == 'PM2.5':
#             ax.set_ylabel('$PM_{2.5} (ug/m^3)$')
#         else:
#             ax.set_ylabel('Ozone (ppb)')
#         ax.set_xlim('2009-1-1','2018-7-1')
#         ax.set_xlabel('DateTime')        
#         ax.set_title(str(site_nameinfo) +', Type: '+str(site_type))
#         #ax.text(0.95,1.03,'Site type: '+str(site_type),ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
#         plt.legend()
# 
#         #plt.plot()
#         print(species+ ' ' + site_nameinfo)
#         #Calculate Statistics
#         try:
#             #Run stats functions
#             aq_stats = stats(d, species+'_mod', species+'_obs')
#         
#         # aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
#    
#             # Merge stats into single dataframe
#             aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', species+' ' + site_nameinfo)    
#             stats_com = pd.merge(stats_com, aq_stats, how = 'inner', left_index = True, right_index = True)     
#             
#             #Drop some stats to put on plots
#             aq_stats = aq_stats.drop('MB',0)        
#             aq_stats = aq_stats.drop('ME',0)
#             aq_stats = aq_stats.drop('RMSE',0)
#             aq_stats = aq_stats.drop('NMB',0)
#             aq_stats = aq_stats.drop('NME',0)
#             
#             ax.text(0.15,-0.15, aq_stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
#             try:
#                 if species == 'O3':
#                     plt.savefig(inputDir+'/plots/monthly/ozone/'+'O3_diurnal_'+site_nameinfo+'.png',  pad_inches=0.1, bbox_inches='tight')
#                 else:
#                     plt.savefig(inputDir+'/plots/monthly/pm/'+'PM_diurnal_'+site_nameinfo+'.png',  pad_inches=0.1, bbox_inches='tight')
#             except(FileNotFoundError):
#                 pass
#             plt.close()
#         except (ZeroDivisionError):
#             pass
# stats_com.to_csv(inputDir + 'longterm_statistics.csv')
# 
# =============================================================================
# =============================================================================
# #%%
#     
# # Diurnal plots
# pollutant = ['O3','PM2.5']
# # Time series
# for species in pollutant:
#     for AQSID in list(set(df_com['AQSID'])):
#         d = df_com.loc[df_com['AQSID']==AQSID]
#     
#         d.loc[:,species+'_mod'] = pd.to_numeric(d.loc[:,species+'_mod'], errors='coerce')
#         d=d.reset_index()
#         site_nameinfo = d.loc[0,'Local Site Name'] #Gets the longname of the site to title the plot
#         site_type = d.loc[0,'Location Setting']        
#         d.drop('AQSID',1)
#         fig,ax=plt.subplots(1,1, figsize=(12,4))
#         d=d.set_index('datetime')
#         b=d.groupby(d.index.hour).std()
#         d.groupby(d.index.hour).mean().ix[:,[species+'_obs', species+'_mod']].plot(kind='line', style='-', ax=ax, color=['black', 'blue'], label=['Observation', 'Model'])
#         ax.set_title(str(site_nameinfo) +', Type: '+str(site_type))
#         
#         if species == 'PM2.5':
#             ax.set_ylabel('$PM_{2.5} (ug/m^3)$')
#         else:
#             ax.set_ylabel('Ozone (ppb)')
#             
#         ax.set_xlabel('Mean Diurnal (hours)')
#         d = d.groupby(d.index.hour).mean()
#         e = b
#         c = d-b
#         e = d+b
#         x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
#         ax.set_ylim(bottom=0)
#         #ax.text(0.95,1.03,'Site type: '+str(site_type),ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
#         plt.fill_between(x, c[species+'_mod'], e[species+'_mod'], facecolor='blue', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) 
#         ax.legend(['Observation', 'Model', 'Std. Dev.'], fontsize=12)
#         print(species+  ' ' + site_nameinfo)
#         
#         #Calculate Statistics
#         try:
#             #Run stats functions
#             aq_stats = stats(d, species+'_mod', species+'_obs')
#         
#         # aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
#    
#             #Clean up column names
#             #aq_stats.columns = aq_stats.columns.str.replace('4km ' + site_nameinfo, '4km')     
#         
#             #Drop some stats to put on plots
#             aq_stats = aq_stats.drop('MB',0)        
#             aq_stats = aq_stats.drop('ME',0)
#             aq_stats = aq_stats.drop('RMSE',0)
#             aq_stats = aq_stats.drop('NMB',0)
#             aq_stats = aq_stats.drop('NME',0)
# 
# #         ax.text(0,-0.25, aq_stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
#             try:
#                 if species == 'O3':
#                     plt.savefig(inputDir+'/plots/diurnal/ozone/'+'O3_diurnal_'+site_nameinfo+'.png',  pad_inches=0.1, bbox_inches='tight')
#                     plt.close()
#                 else:
#                     plt.savefig(inputDir+'/plots/diurnal/pm/'+'PM_diurnal_'+site_nameinfo+'.png',  pad_inches=0.1, bbox_inches='tight')
#                     plt.close()
#             except(FileNotFoundError):
#                 pass
# 
#         except (ZeroDivisionError):
#             pass
# =============================================================================

#%%

# =============================================================================
#  Monthly plots of averaged site types
# =============================================================================
stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
stats_com = stats_com.drop(0,1)
stats_com_8hour = stats_com
settings = ['RURAL', 'SUBURBAN', 'URBAN AND CENTER CITY']
            
pollutant = ['O3']#,'PM2.5']
for species in pollutant:
    da = df_com.dropna(subset=['Location Setting'])
    fig = plt.figure(figsize=(14,16))
    fig.suptitle('Daily Averaged '+str(species),y=0.94,fontsize=27,ha='center') # title
    fig.tight_layout() # spaces the plots out a bit
    
    for setting,i in zip(settings,[1,2,3]):    #list(set(da['Location Setting'])):
        #This section selects only data relevant to the aqs site
        print('Setting is ' + setting)
        d = da.loc[df_com['Location Setting']==setting]
        d=d.reset_index()
        site_type = d.loc[0,'Location Setting']
        
        # Determine how many sites are being used
        temp1 = d.loc[(d['Location Setting'] == setting)].dropna(subset=[species+'_obs'])
        temp1 = temp1.groupby(['Local Site Name']).count()
        temp1 = len(temp1.index.get_level_values(0))
        temp2 = d.loc[(d['Location Setting'] == setting)].dropna(subset=[species+'_mod'])
        temp2 = temp2.groupby(['Local Site Name']).count()
        temp2 = len(temp2.index.get_level_values(0))        
        d=d.ix[:,[species+'_obs',species+'_mod','datetime']]
        d['date'] = pd.to_datetime(d['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
        #print(dc)
        
        d = d.set_index('datetime') 

        if species == 'O3':
            fig.suptitle('Daily Averaged 8-Hr Max '+str(species),y=0.94,fontsize=27,ha='center') # title
            d = d.drop(['date'],axis=1)
            d = d.resample('H').mean()
            avg_8hr_o3 = (
                d.rolling(8, min_periods=6)
                .mean() )
            
            # By default, this takes the last timestamp in a rolling interval; i.e. the
            # timestamps correspond to the preceding 8 hours. We want them to refer to
            # the proeding 8 hours, so we can adjust them using datetime arithmetic
            times = avg_8hr_o3.index.values - pd.Timedelta('8h')
            avg_8hr_o3.index.values[:] = times
            
            # Finally, aggregate by calendar day and compute the maxima of the set of
            # 8-hour averages for each day
            avg_8hr_o3['date'] = avg_8hr_o3.index.strftime('%H')
            intervals = ['00','01','02','03','04','05','06','24'] # remove these hours as per EPA regulation
            for interval in intervals:
                avg_8hr_o3 = avg_8hr_o3[~avg_8hr_o3.date.str.contains(interval)]
                
            d_roll = avg_8hr_o3.resample('D').max().drop('date',axis=1)
            
            names = ['O3_8hour_obs','O3_8hour_mod']
            d_roll = d_roll.rename(columns = {'O3_obs':'O3_8hour_obs','O3_mod':'O3_8hour_mod'})
            d = d.rename(columns = {'O3_obs':'O3_ave_obs','O3_mod':'O3_ave_mod'})
            ylim = 65
            
            ax = fig.add_subplot(3,1,i) # set subplots
            
            d = d.resample('D', convention='start').max() # Daily value
            #d.ix[:,[species+'_ave_obs', species+'_ave_mod']].plot(kind='line', style='-', ax=ax, color=['black', 'blue'])
            d_roll.ix[:,[species+'_8hour_obs', species+'_8hour_mod']].plot(kind='line', style='-', ax=ax, color=['black', 'blue'])
            
            d_test = d['O3_ave_obs'] - d_roll['O3_8hour_obs']
            print(d_test.min())
        else:
            d = d.resample('D', convention='start').mean() # Daily value
        
        #Plot
            ax = fig.add_subplot(3,1,i) # set subplots
            d.ix[:,[species+'_obs', species+'_mod']].plot(kind='line', style='-', ax=ax, color=['black', 'blue'])
        
        if species == 'PM2.5':
            ax.set_ylabel('$PM_{2.5} (ug/m^3)$')
            ax.set_ylim(0,30)
            height = 20 # Height of annotations in graphs
            spc = 1.2 # Space the annotations are moved up and down
            plt.legend(prop={'size': 20},loc=2)
        else:
            ax.set_ylabel('Ozone (ppb)')
            ax.set_ylim(0,ylim) # ylim = 50
            height=10
            spc = 2
            plt.legend(prop={'size': 20},loc=3)
            print(d_test.min())
        
        ax.set_xlim(year+'-'+month+'-'+day,endyear+'-'+endmonth+'-'+endday)
        ax.set_xlabel(' ')        
        ax.set_title(str(site_type))
       # plt.legend(prop={'size': 20},loc=2)
        sze = 10 #size of annotation text
        
        plt.grid(True)    # Add grid lines to make graph interpretation easier
        
        #text_height = 0.061
        text_height = 0.05
        x1 = 0.429
        x2 = 0.689
        x3 = 0.95
        
        t1 = (x1-0.07)/2+0.07
        t2 = (x2-x1)/2+x1
        t3 = (x3-x2)/2+x2
        
# =============================================================================
#         if i == 3:
# 
#             ax.annotate('AP3',xy=(0.07,0.05),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(t1,text_height),va='center',color='red',size='x-small') # Left Arrow AP3 # previous height of 0.061 for the xytext
#             ax.annotate('AP3',xy=(x1,0.05),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(t1,text_height),va='center',color='red',size='x-small') # Right Arrow AP3
#             
#             ax.annotate('AP4',xy=(x1,0.05),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(t2,text_height),va='center',color='red',size='x-small') # Left Arrow AP4
#             ax.annotate('AP4',xy=(x2,0.05),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(t2,text_height),va='center',color='red',size='x-small') # Right Arrow AP4
#     
#             ax.annotate('AP5',xy=(x2,0.05),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(t3,text_height),va='center',color='red',size='x-small') # Left Arrow AP5
#             ax.annotate('AP5',xy=(x3,0.05),arrowprops=dict(facecolor='red',shrink=0.05),xycoords='figure fraction',xytext=(t3,text_height),va='center',color='red',size='x-small') # Right Arrow AP5
# 
# =============================================================================
        #ax.text(1.01, 0.4,'# of Observation sites '+str(temp1),fontsize = 12, ha='right', va='center', transform=ax.transAxes)  
        ax.text(0.98, 0.92,'# of Observation sites '+str(temp1),fontsize = 20, ha='right', va='center', transform=ax.transAxes)  

        #Calculate Statistics
        try:
            #Run stats functions
            if species == 'O3':
                aq_stats_8hour = stats(d_roll, species+'_8hour_mod', species+'_8hour_obs')
                aq_stats_8hour.columns = aq_stats_8hour.columns.str.replace(species+'_mod', species+' ' + site_type)
                stats_com_8hour = pd.merge(stats_com_8hour, aq_stats_8hour, how = 'inner', left_index = True, right_index = True)
                aq_stats = stats(d, species+'_ave_mod', species+'_ave_obs')
            else:
                aq_stats = stats(d, species+'_mod', species+'_obs')
            
        # aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
   
            # Merge stats into single dataframe
            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', species+' ' + site_type)
            stats_com = pd.merge(stats_com, aq_stats, how = 'inner', left_index = True, right_index = True)     
            

        except (ZeroDivisionError):
            pass
            
            #ax.text(0.15,-0.15, aq_stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
    try:
        if species == 'O3':
            print('Ozone')
            #plt.savefig(inputDir+'/plots/monthly/O3_monthly_sitetype.png',  pad_inches=0.1, bbox_inches='tight')
        else:
            #plt.savefig(inputDir+'/plots/monthly/PM_monthly_sitetype.png',  pad_inches=0.1, bbox_inches='tight')
            print('PM')
        plt.show()
        plt.close()
    except(FileNotFoundError):
        pass


        

#%%
            
exec(open(stat_path).read())
#Plot data
#Function to help move spines
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    
aq_stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
aq_stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
aq_stats_com = aq_stats_com.drop(0,1)      
stats_pm_rural = aq_stats_com
stats_pm_urban = aq_stats_com
stats_pm_suburban = aq_stats_com
stats_ozone_rural = aq_stats_com
stats_ozone_urban = aq_stats_com
stats_ozone_suburban = aq_stats_com

stats_pm_rural.name = 'PM2.5 Rural'
stats_pm_urban.name = 'PM2.5 Urban'
stats_pm_suburban.name = 'PM2.5 Suburban'
stats_ozone_rural.name = 'Ozone Rural'
stats_ozone_urban.name = 'Ozone Urban'
stats_ozone_suburban.name = 'Ozone Suburban'

# =============================================================================
# # Diurnal yearly plots
# =============================================================================
    
years = [endyear]    
pollutant = ['O3','PM2.5']

for species in pollutant:
    da = df_com.dropna(subset=['Location Setting'])
    for setting in settings:    #list(set(da['Location Setting'])):
        for year in years:       
            d = da.loc[df_com['Location Setting']==setting]
        
            d.loc[:,species+'_mod'] = pd.to_numeric(d.loc[:,species+'_mod'], errors='coerce')
            d=d.reset_index()
            site_type = d.loc[0,'Location Setting']
            site_type=site_type.replace(" ", "_")
            d.drop('AQSID',1)
            fig,ax=plt.subplots(1,1, figsize=(12,4))
            d=d.set_index('datetime')
            year = str(year)
            mask = (d.index > year+'-1-1') & (d.index <= year+'-12-31')
            d=d.loc[mask]
            df_stats=d
            
            # Set constant limits for plots
            if species == 'O3':
                ax.set_ylim(0,50)
            else:
                ax.set_ylim(0,20)
                
            b=d.groupby(d.index.hour).std()
            d.groupby(d.index.hour).mean().ix[:,[species+'_obs', species+'_mod']].plot(kind='line', style='-', ax=ax, color=['red', 'blue'], label=['Observation', 'Model'])
            ax.set_title(str(site_type) + ' '+year)
        
            if species == 'PM2.5':
                ax.set_ylabel('$PM_{2.5} (ug/m^3)$')
                ax.set_ylim(0,25)
            else:
                ax.set_ylabel('Ozone (ppb)')
                ax.set_ylim(0,55)
                
            ax.set_xlabel('Mean Diurnal (hours)')
            d = d.groupby(d.index.hour).mean()
            e = b
            c = d-b
            e = d+b
            x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
            #ax.text(0.95,1.03,'Site type: '+str(site_type),ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
            plt.fill_between(x, c[species+'_mod'], e[species+'_mod'], facecolor='blue', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) #Model
            plt.fill_between(x, c[species+'_obs'], e[species+'_obs'], facecolor='red', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) #Obs
            ax.legend(['Observation', 'Model', 'Std. Dev.'], fontsize=12)
            

             #Calculate Statistics. Organized the way they are so as to make plotting easier
            df_stats = df_stats.reset_index(drop=True)
            df_stats = df_stats.ix[:,[species+'_mod',species+'_obs','AQSID']]
            df_stats = df_stats.dropna()
            df_stats['diff'] = df_stats[species+'_obs'].abs()-df_stats[species+'_mod'].abs()
            df_stats = df_stats.drop(df_stats[df_stats['diff'] == 0].index)
            try:
                #Run stats functions
                #aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                #aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', year+'_'+species+'_'+site_type)     
                #aq_stats_com = pd.merge(aq_stats_com,aq_stats, how = 'inner', left_index = True, right_index = True) 
                
                if species == 'PM2.5':
                    if site_type == 'RURAL':
                        aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                        aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', year)     
                        stats_pm_rural = pd.merge(stats_pm_rural,aq_stats, how = 'inner', left_index = True, right_index = True)

                    elif site_type == 'URBAN AND CENTER CITY':
                        aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                        aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', year)     
                        stats_pm_urban = pd.merge(stats_pm_urban,aq_stats, how = 'inner', left_index = True, right_index = True)
               
                    elif site_type == 'SUBURBAN':
                        aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                        aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', year)     
                        stats_pm_suburban = pd.merge(stats_pm_suburban,aq_stats, how = 'inner', left_index = True, right_index = True)
                
                else:
                    if site_type == 'RURAL':
                        aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                        aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', year)     
                        stats_ozone_rural = pd.merge(stats_ozone_rural,aq_stats, how = 'inner', left_index = True, right_index = True)

                    elif site_type == 'URBAN AND CENTER CITY':
                        aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                        aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', year)     
                        stats_ozone_urban = pd.merge(stats_ozone_urban,aq_stats, how = 'inner', left_index = True, right_index = True)
               
                    elif site_type == 'SUBURBAN':
                        aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                        aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', year)     
                        stats_ozone_suburban = pd.merge(stats_ozone_suburban,aq_stats, how = 'inner', left_index = True, right_index = True)
                
                # Save diurnal plots
                try:
                    if species == 'O3':
                        print('')
                        #plt.savefig(inputDir+'/plots/diurnal/ozone/'+'O3_diurnal_'+site_type+'_'+year+'.png',  pad_inches=0.1, bbox_inches='tight')
                    else:
                        print('')
                        #plt.savefig(inputDir+'/plots/diurnal/pm/'+'PM_diurnal_'+site_type+'_'+year+'.png',  pad_inches=0.1, bbox_inches='tight')
                except(FileNotFoundError):
                    pass
                plt.close()

            except (ZeroDivisionError):
                pass
            
            print(species+  ' '+ year+' '+site_type)

# Save stats           
stats_pm_rural.to_csv(inputDir+'/stats/PM_rural.csv')   
stats_pm_urban.to_csv(inputDir+'/stats/PM_urban.csv')   
stats_pm_suburban.to_csv(inputDir+'/stats/PM_suburban.csv')   

stats_ozone_rural.to_csv(inputDir+'/stats/O3_rural.csv')   
stats_ozone_urban.to_csv(inputDir+'/stats/O3_urban.csv')   
stats_ozone_suburban.to_csv(inputDir+'/stats/O3_suburban.csv')     
#%%
            
# =============================================================================
# stats_pm_rural.name = 'PM2.5 Rural'
# stats_pm_urban.name = 'PM2.5 Urban'
# stats_pm_suburban.name = 'PM2.5 Suburban'
# stats_ozone_rural.name = 'Ozone Rural'
# stats_ozone_urban.name = 'Ozone Urban'
# stats_ozone_suburban.name = 'Ozone Suburban'
# 
# #Plot some statistics
# stat_list = [stats_ozone_rural,stats_ozone_urban,stats_ozone_suburban,stats_pm_rural,stats_pm_urban,stats_pm_suburban]
# for dataframe in stat_list:
#     d=dataframe.T
#     fig,ax=plt.subplots(1,1, figsize=(12,4))
#     ax.set_title(str(dataframe.name))
#            
#     #Start the extra axis
#     #par1 = ax.twinx()
#     par2 = ax.twinx()
#     par3 = ax.twinx()
# 
#     #Set the location of the extra axis
#     #par1.spines["right"].set_position(("axes", 1.1)) # red one
#     par2.spines["left"].set_position(("axes", -0.1)) # green one
#     par3.spines["right"].set_position(('axes',1))
# 
#     #make_patch_spines_invisible(par1)
#     make_patch_spines_invisible(par2)
#     make_patch_spines_invisible(par3)
#     
#     #Move spines
#     #par1.spines["right"].set_visible(True)
#     #par1.yaxis.set_label_position('right')
#     #par1.yaxis.set_ticks_position('right')
# 
#     par2.spines["left"].set_visible(True)
#     par2.yaxis.set_label_position('left')
#     par2.yaxis.set_ticks_position('left')
# 
#     par3.spines["right"].set_visible(True)
#     par3.yaxis.set_label_position('right')
#     par3.yaxis.set_ticks_position('right')
#     
#     #Select which data to plot, label, and color
#     p1, = ax.plot(d['FE'], 'b-', label = 'FE')
#     #p2, = par1.plot(d['RMSE'], 'r-', label = 'RMSE')
#     p3, = par2.plot(d['FB'], 'g-', label = 'FB')
#     p4, = par3.plot(d['r_squared'], 'darkorange', label = '$r^2$')
#     
#     #Set the y axis values
#     if dataframe.name in ['Ozone Rural','Ozone Urban','Ozone Suburban']: #Ozone
#         ax.set_ylim(0, 85)
#         #par1.set_ylim(0, 20)
#         par2.set_ylim(-20, 40)
#         par3.set_ylim(1, 0)
#     else:   #PM
#         ax.set_ylim(0, 100)
#         #par1.set_ylim(0, 40)
#         par2.set_ylim(-55, 55)
#         par3.set_ylim(1, 0)
#     
#     #Label the y axis
#     ax.set_ylabel('FE')
#     #par1.set_ylabel('RMSE')
#     par2.set_ylabel('FB')
#     par3.set_ylabel('$r^2$')
#     
#     #Sets color of labels
#     ax.yaxis.label.set_color(p1.get_color())
#     #par1.yaxis.label.set_color(p2.get_color())
#     par2.yaxis.label.set_color(p3.get_color())
#     par3.yaxis.label.set_color(p4.get_color())
#     
#     #Settings for the tics
#     tkw = dict(size=4, width=1.5)
#     ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
#     #par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
#     par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
#     par3.tick_params(axis='y', colors=p4.get_color(), **tkw)
#     ax.tick_params(axis='x', **tkw)
#     #plt.savefig(inputDir+'/plots/stats/'+dataframe.name+'_stats.png',  pad_inches=0.1, bbox_inches='tight')
#     plt.show()
#     plt.close()
# 
# 
# =============================================================================



#%%     

##############################################################################
#Run stats for duration of airpact
##############################################################################
exec(open(stat_path).read())
#Plot data
#Function to help move spines
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    
aq_stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
aq_stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
aq_stats_com = aq_stats_com.drop(0,1)      
stats_pm_rural = aq_stats_com
stats_pm_urban = aq_stats_com
stats_pm_suburban = aq_stats_com
stats_ozone_rural = aq_stats_com
stats_ozone_urban = aq_stats_com
stats_ozone_suburban = aq_stats_com

stats_pm_rural.name = 'PM2.5 Rural'
stats_pm_urban.name = 'PM2.5 Urban'
stats_pm_suburban.name = 'PM2.5 Suburban'
stats_ozone_rural.name = 'Ozone Rural'
stats_ozone_urban.name = 'Ozone Urban'
stats_ozone_suburban.name = 'Ozone Suburban'

# monthly stats
months = [1,2,3,4,5,6,7,8,9,10,11,12]    
pollutant = ['O3','PM2.5']

for species in pollutant:
    da = df_com.dropna(subset=['Location Setting'])
    for setting in settings:    #list(set(da['Location Setting'])):
        for year in years:  
            for month in months:
                d = da.loc[df_com['Location Setting']==setting]
                
                d.loc[:,species+'_mod'] = pd.to_numeric(d.loc[:,species+'_mod'], errors='coerce')
                d=d.reset_index()
                site_type = d.loc[0,'Location Setting']        
                d.drop('AQSID',1)
                d=d.set_index('datetime')
                year = str(year)
                month = str(month)
                mask = (d.index > year+'-'+month+'-1') & (d.index <= year+'-'+month+'-28')
                d=d.loc[mask]
                df_stats=d
    
                 #Calculate Statistics. Organized the way they are so as to make plotting easier
                df_stats = df_stats.reset_index(drop=True)
                df_stats = df_stats.ix[:,[species+'_mod',species+'_obs','AQSID']]
                df_stats = df_stats.dropna()
                df_stats['diff'] = df_stats[species+'_obs'].abs()-df_stats[species+'_mod'].abs()
                df_stats = df_stats.drop(df_stats[df_stats['diff'] == 0].index)
                try:
                    #Run stats functions
                    #aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                    #aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', year+'_'+species+'_'+site_type)     
                    #aq_stats_com = pd.merge(aq_stats_com,aq_stats, how = 'inner', left_index = True, right_index = True) 
                    name = str(year+'-'+month)
                    if species == 'PM2.5':
                        if site_type == 'RURAL':
                            aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', name)     
                            stats_pm_rural = pd.merge(stats_pm_rural,aq_stats, how = 'inner', left_index = True, right_index = True)
    
                        elif site_type == 'URBAN AND CENTER CITY':
                            aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', name)     
                            stats_pm_urban = pd.merge(stats_pm_urban,aq_stats, how = 'inner', left_index = True, right_index = True)
                   
                        elif site_type == 'SUBURBAN':
                            aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', name)     
                            stats_pm_suburban = pd.merge(stats_pm_suburban,aq_stats, how = 'inner', left_index = True, right_index = True)
                    
                    else:
                        if site_type == 'RURAL':
                            aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', name)     
                            stats_ozone_rural = pd.merge(stats_ozone_rural,aq_stats, how = 'inner', left_index = True, right_index = True)
    
                        elif site_type == 'URBAN AND CENTER CITY':
                            aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', name)     
                            stats_ozone_urban = pd.merge(stats_ozone_urban,aq_stats, how = 'inner', left_index = True, right_index = True)
                   
                        elif site_type == 'SUBURBAN':
                            aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', name)     
                            stats_ozone_suburban = pd.merge(stats_ozone_suburban,aq_stats, how = 'inner', left_index = True, right_index = True)
                    
    
                except (ZeroDivisionError):
                    pass
                
                print(species+  ' '+ year+' '+month+' '+site_type)
# Save stats           
stats_pm_rural.to_csv(inputDir+'/stats/PM_rural_monthly.csv')   
stats_pm_urban.to_csv(inputDir+'/stats/PM_urban_monthly.csv')   
stats_pm_suburban.to_csv(inputDir+'/stats/PM_suburban.csv')   

stats_ozone_rural.to_csv(inputDir+'/stats/O3_rural_monthly.csv')   
stats_ozone_urban.to_csv(inputDir+'/stats/O3_urban_monthly.csv')   
stats_ozone_suburban.to_csv(inputDir+'/stats/O3_suburban_monthly.csv')  

stats_pm_rural = stats_pm_rural.T
stats_pm_urban = stats_pm_urban.T
stats_pm_suburban = stats_pm_suburban.T
stats_ozone_rural = stats_ozone_rural.T
stats_ozone_urban = stats_ozone_urban.T
stats_ozone_suburban = stats_ozone_suburban.T

#%%
#########################
#Plot stats using monthly values
########################
stats_pm_rural.name = 'PM2.5 Rural'
stats_pm_urban.name = 'PM2.5 Urban'
stats_pm_suburban.name = 'PM2.5 Suburban'
stats_ozone_rural.name = 'Ozone Rural'
stats_ozone_urban.name = 'Ozone Urban'
stats_ozone_suburban.name = 'Ozone Suburban'

ozone_max_fe = max([max(stats_ozone_rural['FE']),max(stats_ozone_urban['FE']),max(stats_ozone_suburban['FE'])])
ozone_max_fb = max([max(stats_ozone_rural['FB']),max(stats_ozone_urban['FB']),max(stats_ozone_suburban['FB'])])
ozone_max_r2 = max([max(stats_ozone_rural['r_squared']),max(stats_ozone_urban['r_squared']),max(stats_ozone_suburban['r_squared'])])

pm_max_fe = max([max(stats_pm_rural['FE']),max(stats_pm_urban['FE']),max(stats_pm_suburban['FE'])])+5
pm_max_fb = max([max(stats_pm_rural['FB']),max(stats_pm_urban['FB']),max(stats_pm_suburban['FB'])])+10
pm_max_r2 = max([max(stats_pm_rural['r_squared']),max(stats_pm_urban['r_squared']),max(stats_pm_suburban['r_squared'])])
#Plot some statistics
stat_list = [stats_ozone_rural,stats_ozone_urban,stats_ozone_suburban,stats_pm_rural,stats_pm_urban,stats_pm_suburban]
for dataframe in stat_list:
    d=dataframe
    d.index= pd.to_datetime(d.index,yearfirst=True)
    fig,ax=plt.subplots(1,1, figsize=(12,4))
    ax.set_title(str(dataframe.name)+' FE and FB')
           
    # Identify which axis is what
    axis1 = 'FE'
    axis2 = 'nan'
    axis3 = 'FB'
    axis4 = 'r_squared'
    
    #Start the extra axis
    #par1 = ax.twinx()
    #par2 = ax.twinx()
    par3 = ax.twinx()

    #Set the location of the extra axis
    #par1.spines["right"].set_position(("axes", 1.1)) # red one
    #par2.spines["left"].set_position(("axes", -0.1)) # green one
    par3.spines["right"].set_position(('axes',1))

    #make_patch_spines_invisible(par1)
    #make_patch_spines_invisible(par2)
    make_patch_spines_invisible(par3)
    
    #Move spines
    #par1.spines["right"].set_visible(True)
    #par1.yaxis.set_label_position('right')
    #par1.yaxis.set_ticks_position('right')

    #par2.spines["left"].set_visible(True)
    #par2.yaxis.set_label_position('left')
    #par2.yaxis.set_ticks_position('left')

    par3.spines["right"].set_visible(True)
    par3.yaxis.set_label_position('right')
    par3.yaxis.set_ticks_position('right')
    
    #Select which data to plot, label, and color
    p1, = ax.plot(d[axis1], 'b-', label = axis1)
    #p2, = par1.plot(d['RMSE'], 'r-', label = 'RMSE')
   # p3, = par2.plot(d[axis3], 'g-', label = axis3)
    p4, = par3.plot(d[axis3], 'darkorange', label = axis3) #r^2 will always be this axis, and it's just easier to hard code the label
    
    #Set the y axis values
    if dataframe.name in ['Ozone Rural','Ozone Urban','Ozone Suburban']: #Ozone
        ax.set_ylim(0, ozone_max_fe)
        #par1.set_ylim(0, 20)
        par3.set_ylim(ozone_max_fb*-1, ozone_max_fb)
        #par3.set_ylim(1, 0)
    else:   #PM
        ax.set_ylim(0, pm_max_fe)
        #par1.set_ylim(0, 40)
        par3.set_ylim(pm_max_fb*-1, pm_max_fb)
        #par3.set_ylim(1, 0)
    
    #Label the y axis
    ax.set_ylabel(axis1)
    #par1.set_ylabel('RMSE')
    #par2.set_ylabel(axis3)
    par3.set_ylabel(axis3)
    
    #Sets color of labels
    ax.yaxis.label.set_color(p1.get_color())
    #par1.yaxis.label.set_color(p2.get_color())
    #par2.yaxis.label.set_color(p3.get_color())
    par3.yaxis.label.set_color(p4.get_color())
    
    #Settings for the tics
    tkw = dict(size=4, width=1.5)
    ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
    #par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    #par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    par3.tick_params(axis='y', colors=p4.get_color(), **tkw)
    ax.tick_params(axis='x', **tkw)
    plt.grid(True)
    #plt.savefig(inputDir+'/plots/stats/'+dataframe.name+'_monthly_stats.png',  pad_inches=0.1, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # Plot r^2
    fig,ax=plt.subplots(1,1, figsize=(12,4))
    ax.set_title(str(dataframe.name)+' $r^2$')
    p4, = ax.plot(d[axis4], 'g-', label = '$r^2$')
    ax.set_ylim(0,1)
    ax.set_ylabel('$r^2$')
    ax.yaxis.label.set_color(p4.get_color())
    ax.tick_params(axis='y', colors=p4.get_color(), **tkw)
    plt.grid(True)
    plt.savefig(inputDir+'/plots/stats/'+dataframe.name+'_monthly_r2_stats.png',  pad_inches=0.1, bbox_inches='tight')
    plt.show()
    plt.close()
end_time = time.time()
print("Run time was %s minutes"%(round((end_time-begin_time)/60)))
print('done')