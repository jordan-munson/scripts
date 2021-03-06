# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 08:33:10 2018

@author: Jordan Munson
"""
import matplotlib as mpl
mpl.use('Agg')
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

# =============================================================================
# #Set directorys
# inputDir = r'E:/Research/AIRPACT_eval/'
# stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'
# aqsid = pd.read_csv(r'E:\Research\AIRPACT_eval/aqs_sites.csv')
# =============================================================================

# Aeolus directories
inputDir = '/data/lar/users/jmunson/longterm_airpact/'
stat_path = '/data/lar/users/jmunson/statistical_functions.py'
aqsid = pd.read_csv(inputDir+'aqs_sites.csv')

# Open statistics script
exec(open(stat_path).read())
#aqsid = aqsid.drop(['Unnamed: 4','Unnamed: 5','Unnamed: 6','Latitude','Longitude'], axis=1)
#aqsid = aqsid.drop([0,0], axis=0)


##############################################################################
# Read AQS data. csv's created from 'AQS_grabbing.py' script, and the model data from the previous lines of code
##############################################################################
# Read model data
df_mod = pd.read_csv(inputDir + '/model_aqs.csv',sep=',')
df_mod['datetime'] = pd.to_datetime(df_mod['datetime']) #Must convert to date time to merge later
df_mod = df_mod.drop('Unnamed: 0',axis=1)

#Create AQSID Column form state code, county code, and site num
aqsid = aqsid.ix[:,['State Code','County Code','Site Number','Local Site Name','Location Setting']]

aqsid['County Code'] = ["%03d" % n for n in aqsid['County Code'] ]
aqsid['Site Number'] = ["%04d" % n for n in aqsid['Site Number'] ]

aqsid['AQSID'] = (aqsid['State Code']).astype(str) + (aqsid['County Code']).astype(str)+(aqsid['Site Number']).astype(str)

# Must force every cell in AQSID to be a string, otherwise lose most of data
aqsid['AQSID'] = aqsid['AQSID'].astype(str)
df_mod['AQSID'] = df_mod['AQSID'].astype(str)

df_mod = pd.merge(df_mod,aqsid) # Merge df_mod and aqsid so as to add names and such to the datafram

print('Model data read')

# Read AQS data
df_wa = pd.read_csv(inputDir + 'AQS_data/Washington_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_or = pd.read_csv(inputDir + 'AQS_data/Oregon_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_id = pd.read_csv(inputDir + 'AQS_data/Idaho_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
#df_cc = pd.read_csv(inputDir + 'Canada_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_mt = pd.read_csv(inputDir + 'AQS_data/Montana_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_ca = pd.read_csv(inputDir + 'AQS_data/California_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_nv = pd.read_csv(inputDir + 'AQS_data/Nevada_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_ut = pd.read_csv(inputDir + 'AQS_data/Utah_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )

#  Combine AQS data
df_list = [df_wa,df_or,df_id,df_mt,df_ca,df_nv,df_ut]
df_obs = pd.concat(df_list)


#Create AQSID Column form state code, county code, and site num
df_obs['County Code'] = ["%03d" % n for n in df_obs['County Code'] ]
df_obs['Site Num'] = ["%04d" % n for n in df_obs['Site Num'] ]

df_obs['AQSID'] = (df_obs['State Code']).astype(str) + (df_obs['County Code']).astype(str)+(df_obs['Site Num']).astype(str)

# Drop columns of data we are not looking at so as to increase the speed of the script
df_obs = df_obs.drop(['Unnamed: 0','Unnamed: 1','State Name','County Name','State Code','County Code','Site Num','Units of Measure','Latitude','Longitude'],axis=1)
df_obs = df_obs.rename(columns={'Date Local_Time Local': 'datetime','Parameter Name':'Parameter_Name'})
print('Observed data read and combined')

# Only pulls ozone/pm data
df_obs_o3 = df_obs.loc[df_obs['Parameter_Name']=='Ozone']
df_obs_pm = df_obs.loc[df_obs['Parameter_Name']=='PM2.5 - Local Conditions']
df_obs_pm2 = df_obs.loc[df_obs['Parameter_Name']=='Acceptable PM2.5 AQI & Speciation Mass']
df_obs_pm = pd.concat([df_obs_pm,df_obs_pm2])

df_obs_o3 = df_obs_o3.rename(columns={'Sample Measurement':'O3_obs'})
df_obs_pm = df_obs_pm.rename(columns={'Sample Measurement':'PM2.5_obs'})

df_obs_o3 = df_obs_o3.drop(['Parameter_Name'],axis=1)
df_obs_pm = df_obs_pm.drop(['Parameter_Name'],axis=1)
df_obs = pd.merge(df_obs_o3, df_obs_pm, on =['datetime','AQSID'], how='outer')

df_obs = pd.merge(df_obs,aqsid, how='outer') 
#df_obs = df_obs.drop(['Latitude_x','Latitude_y','Longitude_x','Longitude_y'], axis=1)
  
##############################################################################
# Manipulate obs and mod dataframes to set them up to plot
##############################################################################
#df_com = pd.concat([df_obs,df_mod])
'''
# sites which are common between base and Observations
sites_common = set(df_obs['AQSID']).intersection(set(df_mod['AQSID']))

## take only the data which is for common sites
df_obs_new = pd.DataFrame(columns=df_obs.columns)
df_mod_new = pd.DataFrame(columns=df_mod.columns)
for sites in sites_common:
    #    print sites
    dfa = df_obs.loc[df_obs['AQSID']==sites, df_obs.columns]
    dfb = df_mod.loc[df_mod['AQSID']==sites, df_mod.columns]
    df_obs_new = pd.concat([df_obs_new, dfa], join='outer', ignore_index=True)
    df_mod_new = pd.concat([df_mod_new, dfb], join='outer', ignore_index=True)
'''
# merge now
print('Merging large dataframes, this may take a while')
#df_com = pd.merge(df_obs_new, df_mod_new, on=['datetime', 'AQSID','long_name'], how='outer')
df_com = pd.merge(df_obs, df_mod, how='outer')

#df_com = pd.concat([df_obs,df_mod])


# Need to convert these to numeric
df_com.loc[:,'O3_mod'] = pd.to_numeric(df_com.loc[:,'O3_mod'], errors='coerce')
df_com.loc[:,'PM2.5_mod'] = pd.to_numeric(df_com.loc[:,'PM2.5_mod'], errors='coerce')
#df_com.loc[:,'AQSID'] = pd.to_numeric(df_com.loc[:,'AQSID'], errors='coerce')

#df_com = df_com.drop(['AQSID_x','AQSID_y'],axis=1)
df_com['datetime'] = pd.to_datetime(df_com['datetime'], infer_datetime_format=True)

#df_com = pd.merge(df_com,aqsid, on=['AQSID','long_name'], how='outer')   
#df_com = df_com.set_index('datetime')

df_com.loc[:,'O3_mod'] = pd.to_numeric(df_com.loc[:,'O3_mod'], errors='coerce')
df_com.loc[:,'PM2.5_mod'] = pd.to_numeric(df_com.loc[:,'PM2.5_mod'], errors='coerce')
df_com.loc[:,'O3_obs'] = pd.to_numeric(df_com.loc[:,'O3_obs'], errors='coerce')
df_com['O3_obs'] = df_com['O3_obs']*1000
df_obs['O3_obs'] = df_obs['O3_obs']*1000
df_com.loc[:,'PM2.5_obs'] = pd.to_numeric(df_com.loc[:,'PM2.5_obs'], errors='coerce')
df_com = df_com.drop(['State Code','County Code','Site Number'],axis=1) # drop unecessary columns
print('Combined dataframe finished')

# Set plot parameters
mpl.rcParams['font.family'] = 'calibri'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 10.0
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


df_mod.loc[:,'O3_mod'] = pd.to_numeric(df_mod.loc[:,'O3_mod'], errors='coerce')
df_mod.loc[:,'PM2.5_mod'] = pd.to_numeric(df_mod.loc[:,'PM2.5_mod'], errors='coerce')

stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
stats_com = stats_com.drop(0,1)
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

#pollutant = ['PM2.5','O3']

pollutant = ['O3']
pollutant = ['PM2.5']

versions = ['AP3','AP4','AP5']

# Short version to make running on pc faster
#pollutant = ['O3']

for species in pollutant:
    print(species)
    da = df_com.dropna(subset=['Location Setting'])
    # Create the overal plot and its settings
    fig = plt.figure(figsize=(6,3),dpi=300)#8,4)) # seems to do nothing here really
    if species == 'PM2.5':
        #fig.set_ylabel('$PM_{2.5} (ug/m^3)$')
        fig.text(-0.015, 0.5, '$PM_{2.5} [ug/m^3]$', va='center', rotation='vertical')
# =============================================================================
#         fig.suptitle('Daily Averaged Seasonal Variations',y=1.06) # title
# =============================================================================
    else:
        #fig.set_ylabel('Ozone (ppb)') 
        fig.text(-0.015, 0.5, 'Ozone [ppb]', va='center', rotation='vertical')
# =============================================================================
#         fig.suptitle('Daily Max 8-Hr Ozone Seasonal Variations',y=1.06) # title
# =============================================================================
        
    
    fig.tight_layout() # spaces the plots out a bit

    #Annotate versions in
# =============================================================================
#     fig.text(0.5, 0.99, 'AIRPACT 3', va='center',ha='center')
#     fig.text(0.5, 0.66, 'AIRPACT 4', va='center',ha='center')
#     fig.text(0.5, 0.33, 'AIRPACT 5', va='center',ha='center')
# =============================================================================
    fig.text(0.202, 1, 'AP-3', va='center',ha='center') # 0.98
    fig.text(0.520, 1, 'AP-4', va='center',ha='center')
    fig.text(0.842, 1, 'AP-5', va='center',ha='center')
    # seasons
# =============================================================================
#     fig.text(0.013,0.78,'Winter',va='center',ha='center', rotation='vertical')
#     fig.text(0.013,0.3,'Summer',va='center',ha='center', rotation='vertical')
# =============================================================================
    
    for version,i in zip(versions,[0,1,2]):#[0,4,8]):
        print(version)
    # Set date range used based of versions
        if version == 'AP3':
# =============================================================================
#             start_date ='2009-05-01'
#             #end_date = '2014-07-01'
#             end_date = '2014-06-30'
# =============================================================================
            years = [2009,2010,2011,2012]
        elif version == 'AP4':
# =============================================================================
#             start_date ='2014-07-01'
#             #end_date = '2015-12-01'
#             end_date = '2015-11-30'
# =============================================================================
            years = [2013,2014,2015]
        elif version == 'AP5':
# =============================================================================
#             start_date ='2015-12-01'
#             #end_date = '2018-07-01'
#             end_date = '2018-06-30'
# =============================================================================
            years = [2016,2017,2018]
        
# =============================================================================
#         # Locate correct site model data
#         mask = (df_com['datetime'] > start_date) & (df_com['datetime'] <= end_date) # Create a mask to determine the date range used
#         dc = da.loc[mask]
# =============================================================================
        

        
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
                    e = '11/30/2009'
                    if species == 'O3':
                        e = '11/29/2010' 
                    else:
                        e = '11/30/2010'
                    dates = pd.date_range(start=s,end=e)
                    #ax = fig.add_subplot(6,2,4+i)
                    
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
                    s = '3/1/2009'
                    e = '5/31/2009'
                    if species == 'O3':
                        e = '5/30/2010' 
                    else:
                        e = '5/31/2010'
                    dates = pd.date_range(start=s,end=e)
                    #ax = fig.add_subplot(6,2,2+i)

                    
            #plt.rcParams["figure.figsize"] = (8,4)
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
            if season == 'Summer' or season == 'Winter':
                # Plotting section
                #ax = fig.add_subplot(1,i,1)
                #Plot
                db.ix[:,[species+'_obs', species+'_mod']].plot(kind='line', style='-', ax=ax, color=['black', 'red'])
                ax.set_xlim(s,e) # set limits in the hopes of removing doubled last label
                plt.setp(ax.get_xticklabels())#, horizontalalignment='right') # angle x axis labels
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
    # =============================================================================
    #             ax.set_title(str(season),fontsize=12) # sets the titles of individ plots as the season, and makes the font smaller
    # =============================================================================
                #plt.legend(['Observation','Forecast'],prop={'size': 8})
                sze = 10 #size of annotation text            
                
                # Set letter denoting plot
                if i ==0:
                    if season == 'Winter':
                        abc = '(a)'
                        plt.legend(['Observation','Forecast'],prop={'size': 8})
                    else:
                        abc = '(d)'
                        ax.get_legend().remove()
                if i ==1:
                    ax.get_legend().remove()
                    if season == 'Winter':
                        abc = '(b)'
                    else:
                        abc = '(e)'
                if i ==2:
                    ax.get_legend().remove()
                    if season == 'Winter':
                        abc = '(c)'
                    else:
                        abc = '(f)'
                #ax.text(0.5, 1.1,abc, ha='right', va='center', transform=ax.transAxes)
                ax.set_title(abc)
        
                plt.grid(True)    # Add grid lines to make graph interpretation easier
            
            #Calculate Statistics
            try:
                #Run stats functions
                aq_stats = stats(d, species+'_mod', species+'_obs')
            
            # aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
       
                # Merge stats into single dataframe
                aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', species)    
                stats_com = pd.merge(stats_com, aq_stats, how = 'inner', left_index = True, right_index = True)     
                

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
# grab some data to test script with
apples = d[:][0:100]
apples = apples.drop('date',axis=1)

# compute 8-hour rolling averages
avg_8hr_o3 = apples.rolling(8,min_periods=6).mean()

# By default, this takes the last timestamp in a rolling interval; i.e. the
# timestamps correspond to the preceding 8 hours. We want them to refer to
# the proeding 8 hours, so we can adjust them using datetime arithmetic
times = avg_8hr_o3.index.values - pd.Timedelta('8h')
avg_8hr_o3.index.values[:] = times

# Finally, aggregate by calendar day and compute the maxima of the set of
# 8-hour averages for each day
mda8_o3 = avg_8hr_o3.resample('D').max()

# Plot just one year of data
ax = mda8_o3.plot(figsize=(8, 4), color='k')
ax.set_ylabel("MDA8 O$_3$ [ppb]")
plt.show()












