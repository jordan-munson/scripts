# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 10:16:51 2019

@author: Jordan Munson
"""

import matplotlib as mpl
#mpl.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import time
import matplotlib.ticker as ticker

starttime = time.time()
begin_time = time.time()
#Set directory
inputDir = r'E:/Research/AIRPACT_eval/'
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'


# Set plot parameters
mpl.rcParams['font.family'] = 'calibri'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 10 # 10 for paper. 28 for presentations
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
df_com = pd.read_csv(inputDir+'AQS_data/df_com_aplong.csv').drop('Unnamed: 0', axis=1)
df_com.loc[:,'O3_mod'] = pd.to_numeric(df_com.loc[:,'O3_mod'], errors='coerce')
df_com.loc[:,'PM2.5_mod'] = pd.to_numeric(df_com.loc[:,'PM2.5_mod'], errors='coerce')
df_com.loc[:,'O3_obs'] = pd.to_numeric(df_com.loc[:,'O3_obs'], errors='coerce')
df_com.loc[:,'PM2.5_obs'] = pd.to_numeric(df_com.loc[:,'PM2.5_obs'], errors='coerce')
df_com['datetime'] = pd.to_datetime(df_com['datetime'])
df_com['AQSID'] = df_com['AQSID'].astype(str)
# =============================================================================
# df_aqsid = pd.read_csv(inputDir+'/common_aqsid.csv',dtype=str).drop('Unnamed: 0', axis=1) # load in AQSID that are present for all versions of AIRPACT. This is created later in the script.
# =============================================================================
df_aqsid_o3 = pd.read_csv(inputDir+'/o3_aqsid.csv',dtype=str).drop('Unnamed: 0', axis=1) # load in AQSID that are present for all versions of AIRPACT. This is created later in the script.
df_aqsid_pm = pd.read_csv(inputDir+'/pm_aqsid.csv',dtype=str).drop('Unnamed: 0', axis=1) # load in AQSID that are present for all versions of AIRPACT. This is created later in the script.

def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)
print('Data loading section done')

#%%
# =============================================================================
# # =============================================================================
# #  Boxplot Diurnal
# # =============================================================================
# aq_stats_com = pd.DataFrame(['Forecast Mean', 'Observation Mean', 'MB','ME','FB [%]','FE [%]',"NMB [%]", "NME [%]", "RMSE", "R^2 [-]",'Forecast 98th','Observation 98th','version','unit','species'])
# aq_stats_com.index = ['Forecast Mean', 'Observation Mean', 'MB','ME','FB [%]','FE [%]',"NMB [%]", "NME [%]", "RMSE", "R^2 [-]",'Forecast 98th','Observation 98th','version','unit','species']
# aq_stats_com = aq_stats_com.drop(0,1)      
# stats_pm_rural = aq_stats_com
# stats_pm_urban = aq_stats_com
# stats_pm_suburban = aq_stats_com
# stats_ozone_rural = aq_stats_com
# stats_ozone_urban = aq_stats_com
# stats_ozone_suburban = aq_stats_com
# 
# stats_pm_rural.name = 'PM2.5 Rural'
# stats_pm_urban.name = 'PM2.5 Urban'
# stats_pm_suburban.name = 'PM2.5 Suburban'
# stats_ozone_rural.name = 'Ozone Rural'
# stats_ozone_urban.name = 'Ozone Urban'
# stats_ozone_suburban.name = 'Ozone Suburban'
# 
# # =============================================================================
# # # Diurnal yearly plots
# # =============================================================================
# data = []
# years = [2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]    
# pollutant = ['O3']#,'PM2.5']
# settings = ['RURAL', 'SUBURBAN', 'URBAN AND CENTER CITY']
# versions = ['AP-3','AP-4','AP-5']
# hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
# for species in pollutant:
#     fig = plt.figure(dpi=100,figsize= (6.125,7)) #This is as small as can currently go without having some overlap of labels 14,16 for a presentation size plot
#     
# 
#     for version,i,abc in zip(versions,[1,2,3],['(a)','(b)','(c)']):
#         name = version + ' ' + species
#         print(version)
#         # Set date range used based of versions
#         if version == 'AP-3':
#             start_date ='2009-05-01'
#             end_date = '2012-12-31'
#         elif version == 'AP-4':
#             start_date ='2013-01-01'
#             end_date = '2015-12-31'
#         elif version == 'AP-5':
#             start_date ='2016-01-01'
#             end_date = '2018-12-31'
#         elif version == 'Total':
#             start_date ='2009-05-01'
#             end_date = '2018-12-31'
#             
#                 # Locate correct site model data
#         mask = (df_com['datetime'] > start_date) & (df_com['datetime'] <= end_date) # Create a mask to determine the date range used
#     
#         da = df_com.copy().loc[mask]       
#         da = da.reset_index(drop=True)
# 
#         ax = fig.add_subplot(3,1,i)
#    
#         d = da.copy()
#         d.loc[:,species+'_mod'] = pd.to_numeric(d.loc[:,species+'_mod'], errors='coerce')
#         d=d.reset_index()
#         site_type = d.loc[0,'Location Setting']
#         site_type=site_type.replace(" ", "_")
#         d.drop('AQSID',1)
#         d=d.set_index('datetime')
#         df_stats=d
#         df_time = d.copy().dropna(subset=[species+'_mod',species+'_obs'])
# 
#         # Create lists of each individual hour
#         time_0_mod =  df_time.between_time('0:00', '0:59')[species+'_mod'].tolist()
#         time_1_mod =  df_time.between_time('1:00', '1:59')[species+'_mod'].tolist()
#         time_2_mod =  df_time.between_time('2:00', '2:59')[species+'_mod'].tolist()
#         time_3_mod =  df_time.between_time('3:00', '3:59')[species+'_mod'].tolist()
#         time_4_mod =  df_time.between_time('4:00', '4:59')[species+'_mod'].tolist()
#         time_5_mod =  df_time.between_time('5:00', '5:59')[species+'_mod'].tolist()
#         time_6_mod =  df_time.between_time('6:00', '6:59')[species+'_mod'].tolist()
#         time_7_mod =  df_time.between_time('7:00', '7:59')[species+'_mod'].tolist()
#         time_8_mod =  df_time.between_time('8:00', '8:59')[species+'_mod'].tolist()
#         time_9_mod =  df_time.between_time('9:00', '9:59')[species+'_mod'].tolist()
#         time_10_mod = df_time.between_time('10:00','10:59')[species+'_mod'].tolist()
#         time_11_mod = df_time.between_time('11:00','11:59')[species+'_mod'].tolist()
#         time_12_mod = df_time.between_time('12:00','12:59')[species+'_mod'].tolist()
#         time_13_mod = df_time.between_time('13:00','13:59')[species+'_mod'].tolist()
#         time_14_mod = df_time.between_time('14:00','14:59')[species+'_mod'].tolist()
#         time_15_mod = df_time.between_time('15:00','15:59')[species+'_mod'].tolist()
#         time_16_mod = df_time.between_time('16:00','16:59')[species+'_mod'].tolist()
#         time_17_mod = df_time.between_time('17:00','17:59')[species+'_mod'].tolist()
#         time_18_mod = df_time.between_time('18:00','18:59')[species+'_mod'].tolist()
#         time_19_mod = df_time.between_time('19:00','19:59')[species+'_mod'].tolist()
#         time_20_mod = df_time.between_time('20:00','20:59')[species+'_mod'].tolist()
#         time_21_mod = df_time.between_time('21:00','21:59')[species+'_mod'].tolist()
#         time_22_mod = df_time.between_time('22:00','22:59')[species+'_mod'].tolist()
#         time_23_mod = df_time.between_time('23:00','23:59')[species+'_mod'].tolist()      
#         # determine for obs now
#         time_0_obs =  df_time.between_time('0:00', '0:59')[species+'_obs'].tolist()
#         time_1_obs =  df_time.between_time('1:00', '1:59')[species+'_obs'].tolist()
#         time_2_obs =  df_time.between_time('2:00', '2:59')[species+'_obs'].tolist()
#         time_3_obs =  df_time.between_time('3:00', '3:59')[species+'_obs'].tolist()
#         time_4_obs =  df_time.between_time('4:00', '4:59')[species+'_obs'].tolist()
#         time_5_obs =  df_time.between_time('5:00', '5:59')[species+'_obs'].tolist()
#         time_6_obs =  df_time.between_time('6:00', '6:59')[species+'_obs'].tolist()
#         time_7_obs =  df_time.between_time('7:00', '7:59')[species+'_obs'].tolist()
#         time_8_obs =  df_time.between_time('8:00', '8:59')[species+'_obs'].tolist()
#         time_9_obs =  df_time.between_time('9:00', '9:59')[species+'_obs'].tolist()
#         time_10_obs = df_time.between_time('10:00','10:59')[species+'_obs'].tolist()
#         time_11_obs = df_time.between_time('11:00','11:59')[species+'_obs'].tolist()
#         time_12_obs = df_time.between_time('12:00','12:59')[species+'_obs'].tolist()
#         time_13_obs = df_time.between_time('13:00','13:59')[species+'_obs'].tolist()
#         time_14_obs = df_time.between_time('14:00','14:59')[species+'_obs'].tolist()
#         time_15_obs = df_time.between_time('15:00','15:59')[species+'_obs'].tolist()
#         time_16_obs = df_time.between_time('16:00','16:59')[species+'_obs'].tolist()
#         time_17_obs = df_time.between_time('17:00','17:59')[species+'_obs'].tolist()
#         time_18_obs = df_time.between_time('18:00','18:59')[species+'_obs'].tolist()
#         time_19_obs = df_time.between_time('19:00','19:59')[species+'_obs'].tolist()
#         time_20_obs = df_time.between_time('20:00','20:59')[species+'_obs'].tolist()
#         time_21_obs = df_time.between_time('21:00','21:59')[species+'_obs'].tolist()
#         time_22_obs = df_time.between_time('22:00','22:59')[species+'_obs'].tolist()
#         time_23_obs = df_time.between_time('23:00','23:59')[species+'_obs'].tolist()           
#         
#         b=d.groupby(d.index.hour).std()
#         d.groupby(d.index.hour).mean().ix[:,[species+'_obs', species+'_mod']].plot(kind='line', style='-', ax=ax, color=['black', 'red'], label=['Observation', 'Model'])
#         data_obs = []
#         data_mod = []
#         for time_data in [time_0_obs,time_1_obs,time_2_obs,time_3_obs,time_4_obs,time_5_obs,time_6_obs,time_7_obs,time_8_obs
#                      ,time_9_obs,time_10_obs,time_11_obs,time_12_obs,time_13_obs,time_14_obs,time_15_obs,time_16_obs,time_17_obs
#                      ,time_18_obs,time_19_obs,time_20_obs,time_21_obs,time_22_obs,time_23_obs]:
#             data_obs.append(time_data)
# 
#         for time_data in [time_0_mod,time_1_mod,time_2_mod,time_3_mod,time_4_mod,time_5_mod,time_6_mod,time_7_mod,time_8_mod
#                      ,time_9_mod,time_10_mod,time_11_mod,time_12_mod,time_13_mod,time_14_mod,time_15_mod,time_16_mod,time_17_mod
#                      ,time_18_mod,time_19_mod,time_20_mod,time_21_mod,time_22_mod,time_23_mod]:
#             data_mod.append(time_data)
#             
#         bpl = ax.boxplot(data_obs)
#         bpr = ax.boxplot(data_mod)
#         set_box_color(bpl, 'black')
#         set_box_color(bpr, 'red')
#         
#         ax.set_title(abc + ' ' + version)
#     
#         if species == 'PM2.5':
#             ax.set_ylabel('PM$_{2.5}$ [\u03BCg m$^{-3}$]')
#             ax.set_ylim(0,25)
#         else:
#             ax.set_ylabel('Ozone [ppb]')
#             ax.set_ylim(-20,100)
#             
#         ax.set_xlabel('Mean Diurnal (hours)')
#         d = d.groupby(d.index.hour).mean()
#         e = b
#         c = d-b
#         e = d+b
#         x = hours
#         #ax.text(0.95,1.03,'Site type: '+str(site_type),ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
#         #plt.fill_between(x, c[species+'_mod'], e[species+'_mod'], facecolor='red', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) #Model
#         #plt.fill_between(x, c[species+'_obs'], e[species+'_obs'], facecolor='black', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) #Obs
#         ax.legend(['Observation', 'Model', 'Std. Dev.'], fontsize=10)
#         ax.grid(False)
#         
# 
#          #Calculate Statistics. Organized the way they are so as to make plotting easier
#         df_stats = df_stats.reset_index(drop=True)
#         df_stats = df_stats.ix[:,[species+'_mod',species+'_obs','AQSID']]
#         df_stats = df_stats.dropna()
#         df_stats['diff'] = df_stats[species+'_obs'].abs()-df_stats[species+'_mod'].abs()
#         df_stats = df_stats.drop(df_stats[df_stats['diff'] == 0].index)
# 
#             # Save diurnal plots
# # =============================================================================
# #                 try:
# #                     if species == 'O3':
# #                         plt.savefig(inputDir+'/plots/diurnal/'+'O3_diurnal_'+site_type+'_'+year+'_common.png',  pad_inches=0.1, bbox_inches='tight')
# #                     else:
# #                         plt.savefig(inputDir+'/plots/diurnal/'+'PM_diurnal_'+site_type+'_'+year+'_common.png',  pad_inches=0.1, bbox_inches='tight')
# #                 except(FileNotFoundError):
# #                     print('file not found error')
# #                     pass
# # =============================================================================
# 
#     fig.tight_layout() # spaces the plots out a bit
#     plt.show()
#     plt.close()        
# =============================================================================
 
#%%
exec(open(stat_path).read())
#Plot data
#Function to help move spines
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    
aq_stats_com = pd.DataFrame(['Forecast Mean', 'Observation Mean', 'MB','ME','FB [%]','FE [%]',"NMB [%]", "NME [%]", "RMSE", "R^2 [-]",'Forecast 98th','Observation 98th','version','unit','species'])
aq_stats_com.index = ['Forecast Mean', 'Observation Mean', 'MB','ME','FB [%]','FE [%]',"NMB [%]", "NME [%]", "RMSE", "R^2 [-]",'Forecast 98th','Observation 98th','version','unit','species']
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
    
years = [2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]    
pollutant = ['O3']#,'PM2.5']
settings = ['RURAL', 'SUBURBAN', 'URBAN AND CENTER CITY']
versions = ['AP-3','AP-4','AP-5']

for species in pollutant:
    fig = plt.figure(dpi=100,figsize= (6.125,7)) #This is as small as can currently go without having some overlap of labels 14,16 for a presentation size plot
    

    for version,i,abc in zip(versions,[1,2,3],['(a)','(b)','(c)']):
        print(version)
        # Set date range used based of versions
        if version == 'AP-3':
            start_date ='2009-05-01'
            end_date = '2012-12-31'
        elif version == 'AP-4':
            start_date ='2013-01-01'
            end_date = '2015-12-31'
        elif version == 'AP-5':
            start_date ='2016-01-01'
            end_date = '2018-12-31'
        elif version == 'Total':
            start_date ='2009-05-01'
            end_date = '2018-12-31'
            
                # Locate correct site model data
        mask = (df_com['datetime'] > start_date) & (df_com['datetime'] <= end_date) # Create a mask to determine the date range used
    
        da = df_com.copy().loc[mask]       
        da = da.reset_index(drop=True)

        ax = fig.add_subplot(3,1,i)
   
        d = da.copy()
        d.loc[:,species+'_mod'] = pd.to_numeric(d.loc[:,species+'_mod'], errors='coerce')
        d=d.reset_index()
        site_type = d.loc[0,'Location Setting']
        site_type=site_type.replace(" ", "_")
        d.drop('AQSID',1)
        d=d.set_index('datetime')

        df_stats=d
        
        #
            
        b=d.groupby(d.index.hour).std()
# =============================================================================
#         d.groupby(d.index.hour).mean().ix[:,[species+'_obs', species+'_mod']].plot(kind='line', style='-', ax=ax, color=['black', 'red'], label=['Observation', 'Model'])
# =============================================================================
        ax.set_title(abc + ' ' + version)
        


        if species == 'PM2.5':
            ax.set_ylabel('PM$_{2.5}$ [\u03BCg m$^{-3}$]')
            ax.set_ylim(0,25)
        else:
            ax.set_ylabel('Ozone [ppb]')
            ax.set_ylim(0,65)
            
        d = d.groupby(d.index.hour).mean()
        e = b
        c = d-b
        e = d+b
        x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        #ax.text(0.95,1.03,'Site type: '+str(site_type),ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
        
        # plot a fill line of std. dev
# =============================================================================
#         plt.fill_between(x, c[species+'_mod'], e[species+'_mod'], facecolor='red', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) #Model
#         plt.fill_between(x, c[species+'_obs'], e[species+'_obs'], facecolor='black', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) #Obs
# =============================================================================

        # plot error bars
        linewidth = 10
        transparency = 0.5
        plt.errorbar(x, d[species+'_mod'],b[species+'_mod'],color = 'red', alpha = transparency,elinewidth = 6,ls = '--')    
        plt.errorbar(x, d[species+'_obs'],b[species+'_obs'],color = 'black', alpha = transparency,elinewidth = 10)        
        
        d.ix[:,[species+'_obs']].plot(kind='line', style='-',marker='o', ax=ax, color=['black'], label=['Observation'])
        d.ix[:,[species+'_mod']].plot(kind='line', style='-',marker='v', ax=ax, color=['red'], label=['Forecast'])

        ax.grid(False)
        
        # only have label on bottom plot, and legend in top plot
        if version == 'AP-5':
            ax.set_xlabel('Hours')
            ax.get_legend().remove()
        elif version == 'AP-3':
            ax.legend(['Observation', 'Model'], fontsize=10,loc = 'upper left',framealpha=0.0)
            ax.set_xlabel('')
        else:
            ax.set_xlabel('')
            ax.get_legend().remove()
        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
            
         #Calculate Statistics. Organized the way they are so as to make plotting easier
        df_stats = df_stats.reset_index(drop=True)
        df_stats = df_stats.ix[:,[species+'_mod',species+'_obs','AQSID']]
        df_stats = df_stats.dropna()
        df_stats['diff'] = df_stats[species+'_obs'].abs()-df_stats[species+'_mod'].abs()
        df_stats = df_stats.drop(df_stats[df_stats['diff'] == 0].index)
            # Save diurnal plots
# =============================================================================
#                 try:
#                     if species == 'O3':
#                         plt.savefig(inputDir+'/plots/diurnal/'+'O3_diurnal_'+site_type+'_'+year+'_common.png',  pad_inches=0.1, bbox_inches='tight')
#                     else:
#                         plt.savefig(inputDir+'/plots/diurnal/'+'PM_diurnal_'+site_type+'_'+year+'_common.png',  pad_inches=0.1, bbox_inches='tight')
#                 except(FileNotFoundError):
#                     print('file not found error')
#                     pass
# =============================================================================

    fig.tight_layout() # spaces the plots out a bit
    plt.show()
    plt.close()        
 
# =============================================================================
# # Save stats           
# stats_pm_rural.T.to_csv(inputDir+'/stats/PM_rural_common.csv')   
# stats_pm_urban.T.to_csv(inputDir+'/stats/PM_urban_common.csv')   
# stats_pm_suburban.T.to_csv(inputDir+'/stats/PM_suburban_common.csv')   
# 
# stats_ozone_rural.T.to_csv(inputDir+'/stats/O3_rural_common.csv')   
# stats_ozone_urban.T.to_csv(inputDir+'/stats/O3_urban_common.csv')   
# stats_ozone_suburban.T.to_csv(inputDir+'/stats/O3_suburban_common.csv')     
# =============================================================================

#%%

# =============================================================================
# Seasonal diurnal plots
# =============================================================================

exec(open(stat_path).read())
#Plot data
    
aq_stats_com = pd.DataFrame(['Forecast Mean', 'Observation Mean', 'MB','ME','FB [%]','FE [%]',"NMB [%]", "NME [%]", "RMSE", "R^2 [-]",'Forecast 98th','Observation 98th','version','unit','species'])
aq_stats_com.index = ['Forecast Mean', 'Observation Mean', 'MB','ME','FB [%]','FE [%]',"NMB [%]", "NME [%]", "RMSE", "R^2 [-]",'Forecast 98th','Observation 98th','version','unit','species']
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
    
years = [2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]    
pollutant = ['O3']#,'PM2.5']
settings = ['RURAL', 'SUBURBAN', 'URBAN AND CENTER CITY']
versions = ['AP-3','AP-4','AP-5']
seasons = ['Summer','Winter']
for season in seasons:
    for species in pollutant:
        fig = plt.figure(dpi=100,figsize= (6.125,7)) #This is as small as can currently go without having some overlap of labels 14,16 for a presentation size plot
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
            
        
        for version,i in zip(versions,[1,2,3]):
            if version == 'AP3':
                xlabel = 'AP-3'
    
                years = [2009,2010,2011,2012]
            elif version == 'AP4':
                xlabel = 'AP-4'
    
                years = [2013,2014,2015]
            elif version == 'AP5':
                xlabel = 'AP-5'
    
                years = [2016,2017,2018]
            
            
            print(season)
            db=pd.DataFrame()       #reset empty
            #This section selects only data relevant to the aqs site
     
            # set dataframe maybe
            d=df_com.copy()
            
            d['AQSID'] = d['AQSID'].astype(str)
            
    # =============================================================================
    #             d=d.ix[:,[species+'_obs',species+'_mod','datetime']]
    # =============================================================================
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
                    dates = pd.date_range(start=s,end=e ,freq='H') 
                    
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
                    dates = pd.date_range(start=s,end=e ,freq='H')
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
                    dates = pd.date_range(start=s,end=e ,freq='H')
    
                    
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
                    dates = pd.date_range(start=s,end=e ,freq='H')
                        
                # combine sub dataframes
                da = pd.DataFrame()                      
                cat = [d1,d2,d3]
                da = pd.concat(cat).reset_index(drop=True)
                da = da.rename(columns={'date':'datetime'})
    
                
            #d = da.copy()
            ax = fig.add_subplot(3,1,i)
            if version == 'AP-3':
                start_date ='2009-05-01'
                end_date = '2012-12-31'
            elif version == 'AP-4':
                start_date ='2013-01-01'
                end_date = '2015-12-31'
            elif version == 'AP-5':
                start_date ='2016-01-01'
                end_date = '2018-12-31'
            elif version == 'Total':
                start_date ='2009-05-01'
                end_date = '2018-12-31'
                
            mask = (da['datetime'] > start_date) & (da['datetime'] <= end_date) # Create a mask to determine the date range used
            d = da.copy().loc[mask]   
            
            d.loc[:,species+'_mod'] = pd.to_numeric(d.loc[:,species+'_mod'], errors='coerce')
            d=d.reset_index()
            site_type = d.loc[0,'Location Setting']
            site_type=site_type.replace(" ", "_")
            d.drop('AQSID',1)
            d=d.set_index('datetime')
    
            df_stats=d
            
            #
                
            b=d.groupby(d.index.hour).std()
    
    # =============================================================================
    #         d.groupby(d.index.hour).mean().ix[:,[species+'_obs', species+'_mod']].plot(kind='line', style='-', ax=ax, color=['black', 'red'], label=['Observation', 'Model'])
    # =============================================================================
            ax.set_title(abc + ' ' + version)
            
    
    
            if species == 'PM2.5':
                ax.set_ylabel('PM$_{2.5}$ [\u03BCg m$^{-3}$]')
                ax.set_ylim(0,25)
            else:
                ax.set_ylabel('Ozone [ppb]')
                ax.set_ylim(0,70)
                
            d = d.groupby(d.index.hour).mean()
            e = b
            c = d-b
            e = d+b
            x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
            #ax.text(0.95,1.03,'Site type: '+str(site_type),ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
            
            # plot a fill line of std. dev
    # =============================================================================
    #         plt.fill_between(x, c[species+'_mod'], e[species+'_mod'], facecolor='red', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) #Model
    #         plt.fill_between(x, c[species+'_obs'], e[species+'_obs'], facecolor='black', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) #Obs
    # =============================================================================
    
            # plot error bars
            linewidth = 10
            transparency = 0.5
            plt.errorbar(x, d[species+'_mod'],b[species+'_mod'],color = 'red', alpha = transparency,elinewidth = 6,ls = '--')    
            plt.errorbar(x, d[species+'_obs'],b[species+'_obs'],color = 'black', alpha = transparency,elinewidth = 10)        
            
            d.ix[:,[species+'_obs']].plot(kind='line', style='-',marker='o', ax=ax, color=['black'], label=['Observation'])
            d.ix[:,[species+'_mod']].plot(kind='line', style='-',marker='v', ax=ax, color=['red'], label=['Forecast'])
    
            
            ax.grid(False)
            
            # only have label on bottom plot, and legend in top plot
            if version == 'AP-5':
                ax.set_xlabel('Hours')
                ax.get_legend().remove()
            elif version == 'AP-3':
                ax.legend(['Observation', 'Forecast'], fontsize=10,loc = 'upper left',framealpha=0.0)
                ax.set_xlabel('')
            else:
                ax.set_xlabel('')
                ax.get_legend().remove()
            # format x axis
            #ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    # =============================================================================
    #         func = lambda x, pos: "" if np.isclose(x,-1) else x
    #         plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(func))
    #         plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(func))
    #         #plt.xlim(0,23)
    # =============================================================================
            
            
             #Calculate Statistics. Organized the way they are so as to make plotting easier
            df_stats = df_stats.reset_index(drop=True)
            df_stats = df_stats.ix[:,[species+'_mod',species+'_obs','AQSID']]
            df_stats = df_stats.dropna()
            df_stats['diff'] = df_stats[species+'_obs'].abs()-df_stats[species+'_mod'].abs()
            df_stats = df_stats.drop(df_stats[df_stats['diff'] == 0].index)
                    # Save diurnal plots

        


    fig.tight_layout() # spaces the plots out a bit
    if species == 'O3':
        plt.savefig(inputDir+'/plots/diurnal/'+'O3_diurnal_'+season+'.png',  pad_inches=0.1, bbox_inches='tight')
    else:
        plt.savefig(inputDir+'/plots/diurnal/'+'PM_diurnal_'+season+'.png',  pad_inches=0.1, bbox_inches='tight')
    plt.show()
    plt.close()       
    print('The plot above is ' + season)