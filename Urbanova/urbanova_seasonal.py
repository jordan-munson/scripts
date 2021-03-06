# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 08:33:10 2018

@author: Jordan Munson
"""
import matplotlib as mpl
#mpl.use('Agg')
import pandas as pd
import matplotlib.dates as mdates
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz
import numpy as np
import time
from subprocess import check_call 
from datetime import timedelta
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
from matplotlib.backends.backend_pdf import PdfPages
from calendar import monthrange
from matplotlib.dates import DateFormatter

starttime = time.time()
begin_time = time.time()



day='01'
month = '01' 
year  = '2018' 

endday = '31'
endmonth='12'
endyear='2018'

#end_year=int(endyear)
#end_month=int(endmonth) 
#endday = str(monthrange(end_year, end_month)[1])

inputDir          = r'E:\Research\Urbanova_Jordan/'
plotDir           =r'E:\Research\Urbanova_Jordan\output/'
stats_dir         = r'E:/Research/scripts/Urbanova/'
aqsid = pd.read_csv(r'E:/Research/AIRPACT_eval/aqs_sites.csv')
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'
urb_path = inputDir +  'Urbanova_ref_site_comparison/Urbanova/'
air_path = inputDir + 'Urbanova_ref_site_comparison/AIRPACT/'
file_airnowsites  = inputDir+ '/aqsid.csv'
# Open statistics script
exec(open(stat_path).read())


# load data
file_modelled_base = inputDir +'/airnow/merged_2018_Urb_airnow_forecasts.csv'


col_names_modeled = ['date', 'time', 'site_id', 'pollutant', 'concentration']
col_names_observed= ['datetime', 'site_id', 'O3_AP5_4km', 'PM2.5_AP5_4km', 'O3_obs', 'PM2.5_obs']
df_base  = pd.read_csv(file_modelled_base, header=None, sep='|',dtype='unicode', names=col_names_modeled)   #AIRNOW data is seperated by |, thus it has to be specified here
df_base  = pd.read_csv(file_modelled_base).drop('Unnamed: 0',axis=1) # new method
df_obs_o3_pm   = pd.read_csv('http://lar.wsu.edu/R_apps/2018ap5/data/hrly2018.csv', sep=',',skiprows=[0],dtype='unicode', names=col_names_observed)
df_obs_o3_pm['datetime'] = pd.to_datetime(df_obs_o3_pm['datetime'], infer_datetime_format=True)
df_sites = pd.read_csv(file_airnowsites, skiprows=[1],dtype='unicode') # skip 2nd row which is blank
df_sites.rename(columns={'AQSID':'site_id'}, inplace=True)

# Weed out non-spokane sites from airpact
df_obs_o3_pm = pd.merge(df_obs_o3_pm,df_sites,how='inner')
df_base = pd.merge(df_base,df_sites,how='inner')

aqsid_spokane = pd.DataFrame()
aqsid_spokane['long_name'] = df_base['long_name'].unique()

df_obs_o3_pm = pd.merge(df_obs_o3_pm,aqsid_spokane,how='inner')
#df_com = pd.merge(df_base,df_obs_o3_pm,how='outer')
print('O3/PM2.5 files read')
        
# Set plot parameters
mpl.rcParams['font.family'] = 'sans-serif'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 28.0
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
# =============================================================================
#  The section below makes seasonal plots irregardless of site type
# =============================================================================
stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
stats_com = stats_com.drop(0,1)
settings = ['RURAL', 'SUBURBAN', 'URBAN AND CENTER CITY']
#seasons = ['Summer','Fall','Winter','Spring'] 
seasons = ['Summer','Winter'] 

pollutant = ['O3','PM2.5']
#pollutant = ['O3']
versions = ['AP3','AP4','AP5']

# Short version to make running on pc faster
#pollutant = ['O3']

for species in pollutant:
    print(species)
    if species == 'O3':
        pollutant = 'OZONE'
    
    if species == 'PM2.5':
        pollutant = species
    # extract only abrv data
    df_base_1 = df_base.loc[df_base['pollutant']==pollutant, df_base.columns]
    # Renames the abrv to concentration
    df_base_1.columns = df_base_1.columns.str.replace('concentration',species+ '_AP5_1.33km')

    # convert datatime colume to time data (This conversion is so slow)
    print('Executing datetime conversion, this takes a while')
    df_base_1['datetime'] = pd.to_datetime(df_base_1['date'] + ' ' + df_base_1['time'], infer_datetime_format=True)#.drop(['date','time'],axis=1) #format="%m/%d/%y %H:%M")
    df_base_1 = df_base_1.drop('date',axis=1)
    df_base_1 = df_base_1.drop('time',axis=1)    
    
    df_com = pd.merge(df_obs_o3_pm,df_base_1, how='outer')
    print('datetime conversion complete')
    da = df_com.copy()
    #da = df_com.dropna(subset=['Location Setting'])
    # Create the overal plot and its settings
    fig = plt.figure(figsize=(26,10))#10,18)) # seems to do nothing here really
    if species == 'PM2.5':
        #fig.set_ylabel('$PM_{2.5} (ug/m^3)$')
        fig.text(-0.01, 0.5, '$PM_{2.5} (ug/m^3)$', va='center', rotation='vertical')
        fig.suptitle('Daily Averaged Seasonal Variations',y=1.06) # title
    else:
        #fig.set_ylabel('Ozone (ppb)') 
        fig.text(-0.01, 0.5, 'Ozone (ppb)', va='center', rotation='vertical')
        fig.suptitle('Daily Max 8-Hr Ozone Seasonal Variations',y=1.06) # title
        
    
    fig.tight_layout() # spaces the plots out a bit

    #Annotate versions in
# =============================================================================
#     fig.text(0.5, 0.99, 'AIRPACT 3', va='center',ha='center')
#     fig.text(0.5, 0.66, 'AIRPACT 4', va='center',ha='center')
#     fig.text(0.5, 0.33, 'AIRPACT 5', va='center',ha='center')
# =============================================================================
    fig.text(0.179, .98, 'AP-3', va='center',ha='center')
    fig.text(0.5051, 0.98, 'AP-4', va='center',ha='center')
    fig.text(0.833, 0.98, 'AP-5', va='center',ha='center')
    for version,i in zip(versions,[0,1,2]):#[0,4,8]):
        print(version)
    # Set date range used based of versions
        if version == 'AP3':
            start_date ='2009-05-01'
            #end_date = '2014-07-01'
            end_date = '2014-06-30'
            years = [2009,2010,2011,2012]
        elif version == 'AP4':
            start_date ='2014-07-01'
            #end_date = '2015-12-01'
            end_date = '2015-11-30'
            years = [2013,2014,2015]
        elif version == 'AP5':
            start_date ='2015-12-01'
            #end_date = '2018-07-01'
            end_date = '2018-06-30'
            years = [2016,2017]
        
        # Locate correct site model data
        mask = (df_com['datetime'] > start_date) & (df_com['datetime'] <= end_date) # Create a mask to determine the date range used
        dc = da.loc[mask]
        

        
        for season in seasons:
            print(season)
            db=pd.DataFrame()       #reset empty
            #This section selects only data relevant to the aqs site
 
            # set dataframe maybe
            d=df_com.copy()
            d=d.ix[:,[species+'_obs',species+'_mod','datetime']]
            #print('starting datetime conversion')
            d['date'] = pd.to_datetime(d['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
            #print('datetime conversion finished')
            
            d = d.set_index('datetime') # Set datetime column as index
            d1=pd.DataFrame()
            d2=pd.DataFrame()
            d3=pd.DataFrame()
            for year in years:
            # Select seasons
                if season == 'Summer':
                    year = str(year)
                    mask = (d.index > year+'-6-1') & (d.index <= year+'-6-30')
                    d11=d.loc[mask]
                    d1 = d1.append(d11)
                    mask = (d.index > year+'-7-1') & (d.index <= year+'-7-31')
                    d22=d.loc[mask]
                    d2 = d2.append(d22)
                    mask = (d.index > year+'-8-1') & (d.index <= year+'-8-31')
                    d33=d.loc[mask]
                    d3 = d3.append(d33)
                    s = '6/1/2009'
                    if species == 'O3':    
                        e = '8/30/2009'
                    else:
                        e = '8/31/2009'
                    dates = pd.date_range(start=s,end=e) 
                    ax = fig.add_subplot(2,3,4+i)#(6,2,3+i)
                    
                if season == 'Fall':
                    year = str(year)
                    mask = (d.index > year+'-9-1') & (d.index <= year+'-9-30')
                    d11=d.loc[mask]
                    d1 = d1.append(d11)
                    mask = (d.index > year+'-10-1') & (d.index <= year+'-10-31')
                    d22=d.loc[mask]
                    d2 = d2.append(d22)
                    mask = (d.index > year+'-11-1') & (d.index <= year+'-11-30')
                    d33=d.loc[mask]
                    d3 = d3.append(d33)
                    s = '9/1/2009'
                    e = '11/20/2009'
                    dates = pd.date_range(start=s,end=e)
                    ax = fig.add_subplot(6,2,4+i)
                    
                if season == 'Winter':
                    if year == 2009:   # Don't have 2008 data, so have to skip first iteration
                        continue
                    mask = (d.index > str(year-1)+'-12-1') & (d.index <= str(year-1)+'-12-31')
                    d11=d.loc[mask]
                    d1 = d1.append(d11)
                    year = str(year)
                    mask = (d.index > year+'-1-1') & (d.index <= year+'-1-31')
                    d22=d.loc[mask]
                    d2 = d2.append(d22)
                    mask = (d.index > year+'-2-1') & (d.index <= year+'-2-28')
                    d33=d.loc[mask]
                    d3 = d3.append(d33)
                    s = '12/1/2009'
                    if species == 'O3':
                        e = '2/27/2010' 
                    else:
                        e = '2/28/2010'
                    dates = pd.date_range(start=s,end=e)
                    ax = fig.add_subplot(2,3,1+i)#(6,2,1+i)

                    
                if season == 'Spring':
                    if year == 2009:   # Don't have 2008 data, so have to skip first iteration
                        continue
                    year = str(year)
                    mask = (d.index > year+'-3-1') & (d.index <= year+'-3-31')
                    d11=d.loc[mask]
                    d1 = d1.append(d11)
                    mask = (d.index > year+'-4-1') & (d.index <= year+'-4-30')
                    d22=d.loc[mask]
                    d2 = d2.append(d22)
                    mask = (d.index > year+'-5-1') & (d.index <= year+'-5-31')
                    d33=d.loc[mask]
                    d3 = d3.append(d33)
                    dates = pd.date_range(start='3/1/2009',end='5/31/2009')
                    ax = fig.add_subplot(6,2,2+i)

                    
            plt.rcParams["figure.figsize"] = (8,4)
            plt.tight_layout() # spaces the plots out a bit

            # Change data to monthly averages
            if species == 'O3':
                # 8-hour ozone script from http://danielrothenberg.com/gcpy/examples/timeseries/calc_mda8_timeseries.html
                cat = [d1,d2,d3]
                db = pd.concat(cat).reset_index(drop=True).set_index('date')

                # find daily max 8 hour average
                dbc = pd.DataFrame()
                for x in cat:
                    x = x.drop('date',axis=1)
                    x = x.resample('H').mean()
                    avg_8hr_o3 = x.rolling(8,min_periods=6).mean()
                    times = avg_8hr_o3.index.values - pd.Timedelta('8h')
                    avg_8hr_o3.index.values[:] = times
                    
                    avg_8hr_o3['date'] = avg_8hr_o3.index.strftime('%H')
                    intervals = ['00','01','02','03','04','05','06','24'] # remove these hours as per EPA regulation
                    for interval in intervals:
                        avg_8hr_o3 = avg_8hr_o3[~avg_8hr_o3.date.str.contains(interval)]
                        
                    x1 = avg_8hr_o3.resample('D').max().drop('date',axis=1)
# =============================================================================
#                     # this way performs the calc like Joe suggested 2/6/19
#                     x = x.drop('date',axis=1)
#                     avg_8hr_o3 = x.rolling(8,min_periods=6).mean()
#                     times = avg_8hr_o3.index.values - pd.Timedelta('8h')
#                     avg_8hr_o3.index.values[:] = times
#                     avg_8hr_o3 = avg_8hr_o3.resample('H').mean()
#                     x1 = avg_8hr_o3.resample('D').max().dropna()
# =============================================================================
                    
                    dbc = dbc.append(x1.groupby(x1.index.day).mean())
                db = dbc.dropna()
                
                db['datetime'] = dates
                db = db.set_index('datetime')
            else:
                d1 = d1.groupby(d1.index.day).mean()
                d2 = d2.groupby(d2.index.day).mean()
                d3 = d3.groupby(d3.index.day).mean()
                cat = [d1,d2,d3]
                db = pd.concat(cat).reset_index(drop=True)
                db['datetime'] = dates
                db = db.set_index('datetime')
            #db = db.resample('D', convention='start').mean()
            
            # Plotting section
            #ax = fig.add_subplot(1,i,1)
            #Plot
            db.ix[:,[species+'_obs', species+'_mod']].plot(kind='line', style='-', ax=ax, color=['black', 'blue'])
            ax.set_xlim(s,e) # set limits in the hopes of removing doubled last label
            plt.setp(ax.get_xticklabels(), rotation=30)#, horizontalalignment='right') # angle x axis labels
            if species == 'PM2.5':
                #ax.set_ylabel('$PM_{2.5} (ug/m^3)$')
                ax.set_ylim(0,30)
                height = 20 # Height of annotations in graphs
                spc = 1.2 # Space the annotations are moved up and down
            else:
                #ax.set_ylabel('Ozone (ppb)')
                ax.set_ylim(20,75)
                #ax.set_ylim(0,120) # for use with 8 hour max ave
                height=10
                spc = 2
            
            #ax.set_xlim('2009-1-1','2018-7-1')
            myFmt = DateFormatter("%b")
            months = mdates.MonthLocator() 
            days = mdates.DayLocator(bymonthday=(1,1))  
            ax.xaxis.set_major_formatter(myFmt)
            ax.xaxis.set_major_locator(months)
            ax.xaxis.set_minor_locator(days)
            ax.set_xlabel('')        # Gets rid of the 'DateTime' x label and replaces with a space
            ax.set_title(str(season),fontsize=28) # sets the titles of individ plots as the season, and makes the font smaller
            plt.legend(prop={'size': 16})#,loc=3) # Places the legend in the lower left corner at a size of 10
            sze = 10 #size of annotation text            
            
            # Set letter denoting plot
            if i ==0:
                if season == 'Winter':
                    abc = 'A'
                else:
                    abc = 'D'
            if i ==1:
                if season == 'Winter':
                    abc = 'B'
                else:
                    abc = 'E'
            if i ==2:
                if season == 'Winter':
                    abc = 'C'
                else:
                    abc = 'F'
            ax.text(-0.02, 1.08,abc,fontsize = 20, ha='right', va='center', transform=ax.transAxes)
    
            plt.grid(True)    # Add grid lines to make graph interpretation easier
            
            #Calculate Statistics
            try:
                #Run stats functions
                aq_stats = stats(d, species+'_mod', species+'_obs')
            
            # aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
       
                # Merge stats into single dataframe
                aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', species)    
                stats_com = pd.merge(stats_com, aq_stats, how = 'inner', left_index = True, right_index = True)     
                
                #Drop some stats to put on plots
                aq_stats = aq_stats.drop('MB',0)        
                aq_stats = aq_stats.drop('ME',0)
                aq_stats = aq_stats.drop('RMSE',0)
                aq_stats = aq_stats.drop('NMB',0)
                aq_stats = aq_stats.drop('NME',0)
            except (ZeroDivisionError):
                pass
                
                #ax.text(0.15,-0.15, aq_stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
    try:
        if species == 'O3':
            print('O3')
            plt.savefig(inputDir+'/plots/seasons/'+'O3_8hr_seasons.png',  pad_inches=0.1, bbox_inches='tight')
        else:
            print('PM')
            plt.savefig(inputDir+'/plots/seasons/'+'PM_seasons.png',  pad_inches=0.1, bbox_inches='tight')
        #plt.show()
        #plt.close()
    except(FileNotFoundError):
        pass
end_time = time.time()
print("Run time was %s minutes"%(round((end_time-begin_time)/60)))
print('done')


#%%
# =============================================================================
# # grab some data to test script with
# apples = d[:][0:100]
# apples = apples.drop('date',axis=1)
# 
# # compute 8-hour rolling averages
# avg_8hr_o3 = apples.rolling(8,min_periods=6).mean()
# 
# # By default, this takes the last timestamp in a rolling interval; i.e. the
# # timestamps correspond to the preceding 8 hours. We want them to refer to
# # the proeding 8 hours, so we can adjust them using datetime arithmetic
# times = avg_8hr_o3.index.values - pd.Timedelta('8h')
# avg_8hr_o3.index.values[:] = times
# 
# # Finally, aggregate by calendar day and compute the maxima of the set of
# # 8-hour averages for each day
# mda8_o3 = avg_8hr_o3.resample('D').max()
# 
# # Plot just one year of data
# ax = mda8_o3.plot(figsize=(8, 4), color='k')
# ax.set_ylabel("MDA8 O$_3$ [ppb]")
# plt.show()
# =============================================================================


#%%
# =============================================================================
# # =============================================================================
# #  Monthly plots of averaged site types
# # =============================================================================
# stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
# stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
# stats_com = stats_com.drop(0,1)
# settings = ['RURAL', 'SUBURBAN', 'URBAN AND CENTER CITY']
# seasons = ['Summer','Fall','Winter','Spring'] 
# pollutant = ['O3','PM2.5']
# versions = ['AP3','AP4','AP5']
# 
# for species in pollutant:
#     da = df_com.dropna(subset=['Location Setting'])
# 
#     for version in versions:
#         print(version)
#     # Set date range used based of versions
#         if version == 'AP3':
#             start_date ='2009-05-01'
#             end_date = '2014-07-01'
#             years = [2009,2010,2011,2012,2013,2014]
#         elif version == 'AP4':
#             start_date ='2014-07-01'
#             end_date = '2015-12-01'
#             years = [2014,2015]
#         elif version == 'AP5':
#             start_date ='2015-12-01'
#             end_date = '2018-07-01'
#             years = [2016,2017]
#         
#         # Locate correct site model data
#         mask = (df_com['datetime'] > start_date) & (df_com['datetime'] <= end_date) # Create a mask to determine the date range used
#         dc = da.loc[mask]
#         
#         for setting in settings:    #list(set(da['Location Setting'])):
#             # Create the overal plot and its settings
#             fig = plt.figure(figsize=(10,6))
#             if species == 'PM2.5':
#                 #fig.set_ylabel('$PM_{2.5} (ug/m^3)$')
#                 fig.text(0, 0.5, '$PM_{2.5} (ug/m^3)$', va='center', rotation='vertical')
#                
#             else:
#                 #fig.set_ylabel('Ozone (ppb)') 
#                 fig.text(0, 0.5, 'Ozone (ppb)', va='center', rotation='vertical')
#             fig.suptitle(str(version)+' '+str(setting),y=1) # title
#             fig.tight_layout() # spaces the plots out a bit
#             
#             for season in seasons:
#                 db=pd.DataFrame()       #reset empty
#                 #This section selects only data relevant to the aqs site
#                 print('Setting is ' + setting,season)
#                 d = dc.loc[df_com['Location Setting']==setting]
#                 d=d.reset_index()
#                 site_type = d.loc[0,'Location Setting']
#                 
#                 # Determine how many sites are being used
#                 temp1 = d.loc[(d['Location Setting'] == setting)].dropna(subset=[species+'_obs'])
#                 temp1 = temp1.groupby(['Local Site Name']).count()
#                 temp1 = len(temp1.index.get_level_values(0))
#                 temp2 = d.loc[(d['Location Setting'] == setting)].dropna(subset=[species+'_mod'])
#                 temp2 = temp2.groupby(['Local Site Name']).count()
#                 temp2 = len(temp2.index.get_level_values(0))        
#                 d=d.ix[:,[species+'_obs',species+'_mod','datetime']]
#                 d['date'] = pd.to_datetime(d['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
#                 
#                 d = d.set_index('datetime') # Set datetime column as index
#                 d1=pd.DataFrame()
#                 d2=pd.DataFrame()
#                 d3=pd.DataFrame()
#                 for year in years:
#                 # Select seasons
#                     if season == 'Summer':
#                         year = str(year)
#                         mask = (d.index > year+'-6-1') & (d.index <= year+'-6-30')
#                         d11=d.loc[mask]
#                         d1 = d1.append(d11)
#                         mask = (d.index > year+'-7-1') & (d.index <= year+'-7-31')
#                         d22=d.loc[mask]
#                         d2 = d2.append(d22)
#                         mask = (d.index > year+'-8-1') & (d.index <= year+'-8-31')
#                         d33=d.loc[mask]
#                         d3 = d3.append(d33)
#                         dates = pd.date_range(start='6/1/2009',end='8/31/2009')
#                         ax = fig.add_subplot(223)
#                         
#                     if season == 'Fall':
#                         year = str(year)
#                         mask = (d.index > year+'-9-1') & (d.index <= year+'-9-30')
#                         d11=d.loc[mask]
#                         d1 = d1.append(d11)
#                         mask = (d.index > year+'-10-1') & (d.index <= year+'-10-31')
#                         d22=d.loc[mask]
#                         d2 = d2.append(d22)
#                         mask = (d.index > year+'-11-1') & (d.index <= year+'-11-30')
#                         d33=d.loc[mask]
#                         d3 = d3.append(d33)
#                         dates = pd.date_range(start='9/1/2009',end='11/30/2009')
#                         ax = fig.add_subplot(224)
#                         
#                     if season == 'Winter':
#                         if year == 2009:   # Don't have 2008 data, so have to skip first iteration
#                             continue
#                         mask = (d.index > str(year-1)+'-12-1') & (d.index <= str(year-1)+'-12-31')
#                         d11=d.loc[mask]
#                         d1 = d1.append(d11)
#                         year = str(year)
#                         mask = (d.index > year+'-1-1') & (d.index <= year+'-1-31')
#                         d22=d.loc[mask]
#                         d2 = d2.append(d22)
#                         mask = (d.index > year+'-2-1') & (d.index <= year+'-2-28')
#                         d33=d.loc[mask]
#                         d3 = d3.append(d33)
#                         dates = pd.date_range(start='12/1/2009',end='2/28/2010')
#                         ax = fig.add_subplot(221)
# 
#                         
#                     if season == 'Spring':
#                         if year == 2009:   # Don't have 2008 data, so have to skip first iteration
#                             continue
#                         year = str(year)
#                         mask = (d.index > year+'-3-1') & (d.index <= year+'-3-31')
#                         d11=d.loc[mask]
#                         d1 = d1.append(d11)
#                         mask = (d.index > year+'-4-1') & (d.index <= year+'-4-30')
#                         d22=d.loc[mask]
#                         d2 = d2.append(d22)
#                         mask = (d.index > year+'-5-1') & (d.index <= year+'-5-31')
#                         d33=d.loc[mask]
#                         d3 = d3.append(d33)
#                         dates = pd.date_range(start='3/1/2009',end='5/31/2009')
#                         ax = fig.add_subplot(222)
# 
#                         
#                 plt.rcParams["figure.figsize"] = (8,4)
#                 plt.tight_layout() # spaces the plots out a bit
# 
#                 # Change data to monthly averages
#                 d1 = d1.groupby(d1.index.day).mean()
#                 d2 = d2.groupby(d2.index.day).mean()
#                 d3 = d3.groupby(d3.index.day).mean()
#                 cat = [d1,d2,d3]
#                 db = pd.concat(cat).reset_index(drop=True)
#                 db['datetime'] = dates
#                 db = db.set_index('datetime')
#                 #db = db.resample('D', convention='start').mean()
#                 
#                 # Plotting section
#                 #ax = fig.add_subplot(1,i,1)
#                 #Plot
#                 db.ix[:,[species+'_obs', species+'_mod']].plot(kind='line', style='-', ax=ax, color=['black', 'blue'])
#                     
#                 if species == 'PM2.5':
#                     #ax.set_ylabel('$PM_{2.5} (ug/m^3)$')
#                     ax.set_ylim(0,30)
#                     height = 20 # Height of annotations in graphs
#                     spc = 1.2 # Space the annotations are moved up and down
#                 else:
#                     #ax.set_ylabel('Ozone (ppb)')
#                     ax.set_ylim(0,55)
#                     height=10
#                     spc = 2
#                 
#                 #ax.set_xlim('2009-1-1','2018-7-1')
#                 myFmt = DateFormatter("%m")
#                 ax.xaxis.set_major_formatter(myFmt)
#                 ax.set_xlabel('')        # Gets rid of the 'DateTime' x label and replaces with a space
#                 ax.set_title(str(season),fontsize=12) # sets the titles of individ plots as the season, and makes the font smaller
#                 plt.legend(prop={'size': 10},loc=3) # Places the legend in the lower left corner at a size of 10
#                 sze = 10 #size of annotation text
#                 
#                 plt.grid(True)    # Add grid lines to make graph interpretation easier
#                 
#                 #Calculate Statistics
#                 try:
#                     #Run stats functions
#                     aq_stats = stats(d, species+'_mod', species+'_obs')
#                 
#                 # aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
#            
#                     # Merge stats into single dataframe
#                     aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', species+' ' + site_type)    
#                     stats_com = pd.merge(stats_com, aq_stats, how = 'inner', left_index = True, right_index = True)     
#                     
#                     #Drop some stats to put on plots
#                     aq_stats = aq_stats.drop('MB',0)        
#                     aq_stats = aq_stats.drop('ME',0)
#                     aq_stats = aq_stats.drop('RMSE',0)
#                     aq_stats = aq_stats.drop('NMB',0)
#                     aq_stats = aq_stats.drop('NME',0)
#                 except (ZeroDivisionError):
#                     pass
#                     
#                     #ax.text(0.15,-0.15, aq_stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
#             try:
#                 if species == 'O3':
#                     print('O3')
#                     plt.savefig(inputDir+'/plots/seasons/'+'O3_seasons_sitetype_'+site_type+'_'+version+'.png',  pad_inches=0.1, bbox_inches='tight')
#                 else:
#                     print('PM')
#                     plt.savefig(inputDir+'/plots/seasons/'+'PM_seasons_sitetype_'+site_type+'_'+version+'.png',  pad_inches=0.1, bbox_inches='tight')
#                 #plt.show()
#                 #plt.close()
#             except(FileNotFoundError):
#                 pass
#         
# 
# =============================================================================


