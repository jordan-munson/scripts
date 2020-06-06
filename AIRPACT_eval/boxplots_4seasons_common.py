# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 14:19:07 2019

@author: Jordan Munson
"""
import matplotlib as mpl
#mpl.use('Agg')
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import time
import numpy as np

starttime = time.time()
begin_time = time.time()

day='01'
month = '04' 
year  = '2018' 

endday = '31'
#endmonth='05'
endmonth='12'
endyear='2018'

# =============================================================================
# # Aeolus directories
# inputDir = '/data/lar/users/jmunson/longterm_airpact/'
# stat_path = '/data/lar/users/jmunson/statistical_functions.py'
# ben_path = inputDir + 'Met_functions_for_Ben.py'
# =============================================================================

#Set directory
inputDir = r'G:/Research/AIRPACT_eval/'
stat_path = r'G:/Research/scripts/Urbanova/statistical_functions.py'
ben_path = r'G:/Research/scripts/AIRPACT_eval/meteorology/Met_functions_for_Ben.py'

exec(open(stat_path).read())

# Set plot parameters
mpl.rcParams['font.family'] = 'Calibri'  # the font used for all labelling/text
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

# load data
df_com = pd.read_csv(inputDir+'AQS_data/df_com.csv').drop('Unnamed: 0', axis=1)
df_com.loc[:,'O3_mod'] = pd.to_numeric(df_com.loc[:,'O3_mod'], errors='coerce')
df_com.loc[:,'PM2.5_mod'] = pd.to_numeric(df_com.loc[:,'PM2.5_mod'], errors='coerce')
df_com.loc[:,'O3_obs'] = pd.to_numeric(df_com.loc[:,'O3_obs'], errors='coerce')
df_com.loc[:,'PM2.5_obs'] = pd.to_numeric(df_com.loc[:,'PM2.5_obs'], errors='coerce')
df_com['datetime'] = pd.to_datetime(df_com['datetime'])
df_com['AQSID'] = df_com['AQSID'].astype(str)

# read in common sites
df_aqsid_o3 = pd.read_csv(inputDir+'/o3_aqsid.csv',dtype=str).drop('Unnamed: 0', axis=1) # load in AQSID that are present for all versions of AIRPACT. This is created later in the script.
df_aqsid_pm = pd.read_csv(inputDir+'/pm_aqsid.csv',dtype=str).drop('Unnamed: 0', axis=1) # load in AQSID that are present for all versions of AIRPACT. This is created later in the script.

print('Data loading section done')

# Set variables for for loops
pollutant = ['O3','PM2.5']
versions = ['AP3','AP4','AP5']
seasons = ['Spring','Summer','Fall','Winter'] 

#%%
# =============================================================================
# for species in pollutant:
#     data=[]
#     data1=[]
#     data2=[]
#     data3=[]
#     data_obs = []
#     data_obs1 = []
#     data_obs2=[]
#     data_obs3=[]
#     names=versions
#     sites=[]
#     if species == 'O3':
#         unit_list = 'ppb'
#     else:
#         unit_list = '$\u03BCg m^-3$'
#         
#     
#     for version in versions:
#         if version == 'AP3':
#             xlabel = 'AP-3'
# 
#             years = [2009,2010,2011,2012]
#         elif version == 'AP4':
#             xlabel = 'AP-4'
# 
#             years = [2013,2014,2015]
#         elif version == 'AP5':
#             xlabel = 'AP-5'
# 
#             years = [2016,2017,2018]
#         
#         for season in seasons:
#             print(season)
#             db=pd.DataFrame()       #reset empty
#             #This section selects only data relevant to the aqs site
#  
#             # set dataframe maybe
#             d=df_com.copy()
#             
#             d['AQSID'] = d['AQSID'].astype(str)
#             if species == 'O3': # only use sites common
#                 d = pd.merge(d,df_aqsid_o3,on='AQSID')
#             else:
#                 d = pd.merge(d,df_aqsid_pm,on='AQSID')
#             
#             d=d.ix[:,[species+'_obs',species+'_mod','datetime']]
#             #print('starting datetime conversion')
#             d['date'] = pd.to_datetime(d['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
#             #print('datetime conversion finished')
#             
#             d = d.set_index('datetime') # Set datetime column as index
#             d1=pd.DataFrame()
#             d2=pd.DataFrame()
#             d3=pd.DataFrame()
#             for year in years:
#             # Select seasons
#                 if season == 'Summer':
#                     year = str(year)
#                     mask = (d.index > year+'-6-1') & (d.index <= year+'-6-30')
#                     d11=d.loc[mask]
#                     d1 = d1.append(d11)
#                     mask = (d.index > year+'-7-1') & (d.index <= year+'-7-31')
#                     d22=d.loc[mask]
#                     d2 = d2.append(d22)
#                     mask = (d.index > year+'-8-1') & (d.index <= year+'-8-31')
#                     d33=d.loc[mask]
#                     d3 = d3.append(d33)
#                     s = '6/1/2009'
#                     if species == 'O3':    
#                         e = '8/30/2009'
#                     else:
#                         e = '8/31/2009'
#                     dates = pd.date_range(start=s,end=e) 
#                     
#                 if season == 'Fall':
#                     year = str(year)
#                     mask = (d.index > year+'-9-1') & (d.index <= year+'-9-30')
#                     d11=d.loc[mask]
#                     d1 = d1.append(d11)
#                     mask = (d.index > year+'-10-1') & (d.index <= year+'-10-31')
#                     d22=d.loc[mask]
#                     d2 = d2.append(d22)
#                     mask = (d.index > year+'-11-1') & (d.index <= year+'-11-30')
#                     d33=d.loc[mask]
#                     d3 = d3.append(d33)
#                     s = '9/1/2009'
#                     e = '11/30/2009'
#                     if species == 'O3':
#                         e = '11/29/2009' 
#                     else:
#                         e = '11/30/2009'
#                     dates = pd.date_range(start=s,end=e)
#                     #ax = fig.add_subplot(6,2,4+i)
#                     
#                 if season == 'Winter':
#                     if year == 2009:   # Don't have 2008 data, so have to skip first iteration
#                         continue
#                     mask = (d.index > str(year-1)+'-12-1') & (d.index <= str(year-1)+'-12-31')
#                     d11=d.loc[mask]
#                     d1 = d1.append(d11)
#                     year = str(year)
#                     mask = (d.index > year+'-1-1') & (d.index <= year+'-1-31')
#                     d22=d.loc[mask]
#                     d2 = d2.append(d22)
#                     mask = (d.index > year+'-2-1') & (d.index <= year+'-2-28')
#                     d33=d.loc[mask]
#                     d3 = d3.append(d33)
#                     s = '12/1/2009'
#                     if species == 'O3':
#                         e = '2/27/2010' 
#                     else:
#                         e = '2/28/2010'
#                     dates = pd.date_range(start=s,end=e)
# 
#                     
#                 if season == 'Spring':
#                     if year == 2009:   # Don't have 2008 data, so have to skip first iteration
#                         continue
#                     year = str(year)
#                     mask = (d.index > year+'-3-1') & (d.index <= year+'-3-31')
#                     d11=d.loc[mask]
#                     d1 = d1.append(d11)
#                     mask = (d.index > year+'-4-1') & (d.index <= year+'-4-30')
#                     d22=d.loc[mask]
#                     d2 = d2.append(d22)
#                     mask = (d.index > year+'-5-1') & (d.index <= year+'-5-31')
#                     d33=d.loc[mask]
#                     d3 = d3.append(d33)
#                     s = '3/1/2009'
#                     e = '5/31/2009'
#                     if species == 'O3':
#                         e = '5/29/2009' 
#                     else:
#                         e = '5/31/2009'
#                     dates = pd.date_range(start=s,end=e)
# 
#                     
#             plt.rcParams["figure.figsize"] = (6,3)
#             plt.tight_layout() # spaces the plots out a bit
# 
#             # Change data to monthly averages
#             if species == 'O3':
#                 ylim = (10,65)
#                 ylabel = 'Ozone [ppb]'
#                 # 8-hour ozone script from http://danielrothenberg.com/gcpy/examples/timeseries/calc_mda8_timeseries.html
#                 cat = [d1,d2,d3]
#                 db = pd.concat(cat).reset_index(drop=True).set_index('date')
# 
#                 # find daily max 8 hour average
#                 dbc = pd.DataFrame()
#                 for x in cat:
#                     x = x.drop('date',axis=1)
#                     x = x.resample('H').mean()
#                     avg_8hr_o3 = x.rolling(8,min_periods=6).mean()
#                     times = avg_8hr_o3.index.values - pd.Timedelta('8h')
#                     avg_8hr_o3.index.values[:] = times
#                     
#                     avg_8hr_o3['date'] = avg_8hr_o3.index.strftime('%H')
#                     intervals = ['00','01','02','03','04','05','06','24'] # remove these hours as per EPA regulation
#                     for interval in intervals:
#                         avg_8hr_o3 = avg_8hr_o3[~avg_8hr_o3.date.str.contains(interval)]
#                         
#                     x1 = avg_8hr_o3.resample('D').max().drop('date',axis=1)             
#                     
#                     dbc = dbc.append(x1.groupby(x1.index.day).mean()) # This bit unnecessary. Averages over the whole timeframe into a single month
#                     #dbc = x1
#                 db = dbc.dropna()
#                 
#                 db['datetime'] = dates
#                 db = db.set_index('datetime')
#             else:
#                 ylim = (0,25)
#                 ylabel = 'PM$_{2.5}$ [\u03BCg m$^{-3}$]'
#                 d1 = d1.groupby(d1.index.day).mean()
#                 d2 = d2.groupby(d2.index.day).mean()
#                 d3 = d3.groupby(d3.index.day).mean()
#                 cat = [d1,d2,d3]
#                 db = pd.concat(cat).reset_index(drop=True)
#                 db['datetime'] = dates
#                 db = db.set_index('datetime')
#             #db = db.resample('D', convention='start').mean()
#             
#             if season == 'Spring':
#                 data.append(list(db[species+'_mod'].dropna()))
#                 data_obs.append(list(db[species+'_obs'].dropna()))
#             if season == 'Summer':
#                 data1.append(list(db[species+'_mod'].dropna()))
#                 data_obs1.append(list(db[species+'_obs'].dropna()))
#             if season == 'Fall':
#                 data2.append(list(db[species+'_mod'].dropna()))
#                 data_obs2.append(list(db[species+'_obs'].dropna()))
#             if season == 'Winter':
#                 data3.append(list(db[species+'_mod'].dropna()))
#                 data_obs3.append(list(db[species+'_obs'].dropna()))
# 
#             #names.append(version)
#             
#     # Plotting section
#     fig = plt.figure(figsize=(6,4),dpi=300)
#     fig.tight_layout()
#     label = 10
#     
#     print(names)
#     names = ['AP-3','AP-4','AP-5']
# # =============================================================================
# #     if species == 'O3':
# #         fig.suptitle('Summer 8-Hour Max Average Ozone ',ha='center') # title
# #         fig.text(0.03, 0.5, 'Ozone (ppb)', va='center', rotation='vertical')
# #     else:
# #         fig.suptitle('Summer Daily Average PM2.5',ha='center') # title        
# #         fig.text(0, 0.5, '$PM_{2.5} (ug/m^3)$', va='center', rotation='vertical')
# # =============================================================================
#     sites = len(data)
#     
#     def set_box_color(bp, color):
#         plt.setp(bp['boxes'], color=color)
#         plt.setp(bp['whiskers'], color=color)
#         plt.setp(bp['caps'], color=color)
#         plt.setp(bp['medians'], color=color)
#     
#     
#     ax = fig.add_subplot(2,2,1)
#     ax.set_title('(a) Spring',fontsize = label)
#     bpl =ax.boxplot(data, positions=np.array(range(len(data)))*2.0-0.35, sym='', widths=0.6)
#     bpr =ax.boxplot(data_obs, positions=np.array(range(len(data_obs)))*2.0+0.35, sym='', widths=0.6)
#     ax.set_xlim(-1,5)
#     plt.xticks([],[])
#     ax.yaxis.set_ticks_position('none') 
#     plt.grid(True,alpha=0.7,axis='y')
#     ax.set_ylabel(ylabel) 
#     ax.set_ylim(ylim)
#     set_box_color(bpl, 'red')
#     set_box_color(bpr, 'black')
#     ax.grid(False)
#     plt.plot([], c='Red', label='Forecast')
#     plt.plot([], c='Black', label='Observation')
#     plt.legend()
#     
#     
#     
#     ax = fig.add_subplot(2,2,2)
#     ax.set_title('(b) Summer', fontsize = label)
#     bpl = ax.boxplot(data1, positions=np.array(range(len(data1)))*2.0-0.35, sym='', widths=0.6)
#     bpr = ax.boxplot(data_obs1, positions=np.array(range(len(data_obs1)))*2.0+0.35, sym='', widths=0.6)  
#     ax.set_xlim(-1,5)
#     plt.xticks([],[])
#     ax.yaxis.set_ticks_position('none') 
#     plt.grid(True,alpha=0.7,axis='y')
#     #ax.set_ylabel(species+' '+'['+unit_list+']') 
#     ax.set_ylim(ylim)
#     set_box_color(bpl, 'red')
#     set_box_color(bpr, 'black')
#     ax.grid(False)
#     
#     ax = fig.add_subplot(2,2,3)
#     ax.set_title('(c) Fall', fontsize = label)
#     bpl = ax.boxplot(data2, positions=np.array(range(len(data2)))*2.0-0.35, sym='', widths=0.6)
#     bpr = ax.boxplot(data_obs2, positions=np.array(range(len(data_obs2)))*2.0+0.35, sym='', widths=0.6)    
#     ax.set_xlim(-1,5)
#     ax.yaxis.set_ticks_position('none') 
#     plt.grid(True,alpha=0.7,axis='y')
#     ax.set_ylabel(ylabel) 
#     ax.set_ylim(ylim)
#     plt.xticks([0,2,4],names)
#     set_box_color(bpl, 'red')
#     set_box_color(bpr, 'black')
#     
#     plt.tick_params(
#     axis='x',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom=False,      # ticks along the bottom edge are off
#     top=False)         # ticks along the top edge are off
#     #labelbottom=False) # labels along the bottom edge are off
#     ax.grid(False)
#     
#     ax = fig.add_subplot(2,2,4)
#     ax.set_title('(d) Winter', fontsize = label)
#     #ax.set_ylabel(species+' '+'['+unit_list+']') 
#     ax.set_ylim(ylim)
#     bpl = ax.boxplot(data3, positions=np.array(range(len(data3)))*2.0-0.35, sym='', widths=0.6)
#     bpr = ax.boxplot(data_obs3, positions=np.array(range(len(data_obs3)))*2.0+0.35, sym='', widths=0.6)    
#     ax.set_xlim(-1,5)
#     ax.yaxis.set_ticks_position('none') 
#     plt.grid(True,alpha=0.7,axis='y')
#     plt.xticks([0,2,4],names)
#     set_box_color(bpl, 'red')
#     set_box_color(bpr, 'black')
#     plt.plot([], c='Red', label='Forecast')
#     plt.plot([], c='Black', label='Observation')
#     
#     
#     # Removex ticks
#     plt.tick_params(
#     axis='x',          # changes apply to the x-axis
#     which='both',      # both major and minor ticks are affected
#     bottom=False,      # ticks along the bottom edge are off
#     top=False,         # ticks along the top edge are off
#     labelbottom=True) # labels along the bottom edge are off
#     
#     #ax.set_ylabel(species+' '+'('+unit_list+')') 
#     plt.grid(True,alpha=0.7,axis='y')
#     ax.grid(False)
#     
# # =============================================================================
# #     # place letters 
# #     ax.text(1.09, 1.72,'A', ha='right', va='center', transform=ax.transAxes,fontsize=20)
# #     ax.text(1.09, 0.5,'B', ha='right', va='center', transform=ax.transAxes,fontsize=20)
# # =============================================================================
#     
#     plt.savefig(inputDir+'/plots/boxplot/'+species+'boxplot_4seasons_common.png',  pad_inches=0.1, bbox_inches='tight')
#     plt.show()
#     plt.close()
#     
# =============================================================================
#%%  
# =============================================================================
# Swap seasonal plots so that there are 3 subplots, one for each AIRPACT version
# =============================================================================
    
for species in pollutant:
    data=[]
    data1=[]
    data2=[]
    data3=[]
    data_obs = []
    data_obs1 = []
    data_obs2=[]
    data_obs3=[]
    names=versions
    sites=[]
    if species == 'O3':
        unit_list = 'ppb'
    else:
        unit_list = '$\u03BCg m^-3$'
        
    
    for version in versions:
        if version == 'AP3':
            xlabel = 'AP-3'

            years = [2009,2010,2011,2012]
        elif version == 'AP4':
            xlabel = 'AP-4'

            years = [2013,2014,2015]
        elif version == 'AP5':
            xlabel = 'AP-5'

            years = [2016,2017,2018]
        
        for season in seasons:
            print(season)
            db=pd.DataFrame()       #reset empty
            #This section selects only data relevant to the aqs site
 
            # set dataframe maybe
            d=df_com.copy()
            
            d['AQSID'] = d['AQSID'].astype(str)
            if species == 'O3': # only use sites common
                d = pd.merge(d,df_aqsid_o3,on='AQSID')
            else:
                d = pd.merge(d,df_aqsid_pm,on='AQSID')
            
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
                        e = '11/29/2009' 
                    else:
                        e = '11/30/2009'
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
                        e = '5/29/2009' 
                    else:
                        e = '5/31/2009'
                    dates = pd.date_range(start=s,end=e)

                    
            plt.rcParams["figure.figsize"] = (6,3)
            plt.tight_layout() # spaces the plots out a bit

            # Change data to monthly averages
            if species == 'O3':
                ylim = (10,65)
                ylabel = 'Ozone [ppb]'
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
                    
                    dbc = dbc.append(x1.groupby(x1.index.day).mean()) # This bit unnecessary. Averages over the whole timeframe into a single month
                    #dbc = x1
                db = dbc.dropna()
                
                db['datetime'] = dates
                db = db.set_index('datetime')
            else:
                ylim = (0,25)
                ylabel = 'PM$_{2.5}$ [\u03BCg m$^{-3}$]'
                d1 = d1.groupby(d1.index.day).mean()
                d2 = d2.groupby(d2.index.day).mean()
                d3 = d3.groupby(d3.index.day).mean()
                cat = [d1,d2,d3]
                db = pd.concat(cat).reset_index(drop=True)
                db['datetime'] = dates
                db = db.set_index('datetime')
            #db = db.resample('D', convention='start').mean()
            
            if season == 'Spring':
                data.append(list(db[species+'_mod'].dropna()))
                data_obs.append(list(db[species+'_obs'].dropna()))
            if season == 'Summer':
                data1.append(list(db[species+'_mod'].dropna()))
                data_obs1.append(list(db[species+'_obs'].dropna()))
            if season == 'Fall':
                data2.append(list(db[species+'_mod'].dropna()))
                data_obs2.append(list(db[species+'_obs'].dropna()))
            if season == 'Winter':
                data3.append(list(db[species+'_mod'].dropna()))
                data_obs3.append(list(db[species+'_obs'].dropna()))

            #names.append(version)
                
    # Modify the data lists to be by version not by season
    data_ap3 = [data[0],data1[0],data2[0],data3[0]]
    data_ap4 = [data[1],data1[1],data2[1],data3[1]]
    data_ap5 = [data[2],data1[2],data2[2],data3[2]]
    
    data_ap3_obs = [data_obs[0],data_obs1[0],data_obs2[0],data_obs3[0]]
    data_ap4_obs = [data_obs[1],data_obs1[1],data_obs2[1],data_obs3[1]]
    data_ap5_obs = [data_obs[2],data_obs1[2],data_obs2[2],data_obs3[2]]
    
    # Plotting section
    fig = plt.figure(figsize=(6,6),dpi=300)
    label = 10
    
    print(names)
    names = ['Spring','Summer','Fall','Winter']
    sites = len(data_ap3)
    
    def set_box_color(bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color=color)
    
    # Box plot dimensions/spacing
    a = 1.4
    b = 0.2
    width_box = 0.3
    
    ax = fig.add_subplot(3,1,1)
    ax.set_title('(a) AP-3',fontsize = label)
    bpl =ax.boxplot(data_ap3, positions=np.array(range(len(data_ap3)))*a-b, sym='', widths=width_box)
    bpr =ax.boxplot(data_ap3_obs, positions=np.array(range(len(data_ap3_obs)))*a+b, sym='', widths=width_box)
    ax.set_xlim(-1,5)
    plt.xticks([],[])
    ax.yaxis.set_ticks_position('none') 
    plt.grid(True,alpha=0.7,axis='y') 
    ax.set_ylim(ylim)
    set_box_color(bpl, 'red')
    set_box_color(bpr, 'black')
    ax.grid(False)
    plt.plot([], c='Red', label='Forecast')
    plt.plot([], c='Black', label='Observation')
    plt.legend()
    
    
    
    ax = fig.add_subplot(3,1,2)
    ax.set_title('(b) AP-4', fontsize = label)
    bpl = ax.boxplot(data_ap4, positions=np.array(range(len(data_ap4)))*a-b, sym='', widths=width_box)
    bpr = ax.boxplot(data_ap4_obs, positions=np.array(range(len(data_ap4_obs)))*a+b, sym='', widths=width_box)  
    ax.set_xlim(-1,5)
    plt.xticks([],[])
    ax.yaxis.set_ticks_position('none') 
    plt.grid(True,alpha=0.7,axis='y')
    ax.set_ylabel(ylabel)
    ax.set_ylim(ylim)
    set_box_color(bpl, 'red')
    set_box_color(bpr, 'black')
    ax.grid(False)
    
    ax = fig.add_subplot(3,1,3)
    ax.set_title('(c) AP-5', fontsize = label)
    bpl = ax.boxplot(data_ap5, positions=np.array(range(len(data_ap5)))*a-b, sym='', widths=width_box)
    bpr = ax.boxplot(data_ap5_obs, positions=np.array(range(len(data_ap5_obs)))*a+b, sym='', widths=width_box)    
    ax.set_xlim(-1,5)
    ax.yaxis.set_ticks_position('none') 
    plt.grid(True,alpha=0.7,axis='y')
    ax.set_ylim(ylim)
    plt.xticks([0,1.5,2.8,4.2],names)
    set_box_color(bpl, 'red')
    set_box_color(bpr, 'black')
    
    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False)         # ticks along the top edge are off
    #labelbottom=False) # labels along the bottom edge are off
    ax.grid(False)
    
    
    # Removex ticks
    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=True) # labels along the bottom edge are off
    
    #ax.set_ylabel(species+' '+'('+unit_list+')') 
    plt.grid(True,alpha=0.7,axis='y')
    ax.grid(False)
    
# =============================================================================
#     # place letters 
#     ax.text(1.09, 1.72,'A', ha='right', va='center', transform=ax.transAxes,fontsize=20)
#     ax.text(1.09, 0.5,'B', ha='right', va='center', transform=ax.transAxes,fontsize=20)
# =============================================================================
    #fig.tight_layout()
    plt.savefig(inputDir+'/plots/boxplot/'+species+'boxplot_4seasons_common.png',  pad_inches=0.1, bbox_inches='tight')
    plt.show()
    plt.close()

