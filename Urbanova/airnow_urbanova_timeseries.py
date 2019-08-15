
# This script is modifed based on Vikram Ravi's python code
# program for evaluation of PM2.5 for airpact 5 using airnow data
# author - vikram ravi
# dated - 2016-02-10

############################################################################################################################
# import some libraries
import matplotlib as mpl
#mpl.use('Agg')
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
day='11'
month = '01' 
year  = '2018' 

endday = '11'#'31'
endmonth='07'#'12'
endyear='2019'

end_year=int(endyear)
end_month=int(endmonth) 
endday = str(monthrange(end_year, end_month)[1])

inputDir          = r'E:\Research\Urbanova_Jordan/'
plotDir           =r'E:\Research\Urbanova_Jordan\output/'
stats_dir = r'E:/Research/scripts/Urbanova/'
urb_path = inputDir +  'Urbanova_ref_site_comparison/Urbanova/'
air_path = inputDir + 'Urbanova_ref_site_comparison/AIRPACT/'

# =============================================================================
# inputDir = '/data/lar/users/jmunson'       #Aeolus
# urb_path = '/data/lar/projects/Urbanova' + '/'   #Aeolus
# air_path = '/data/airpact5/AIRRUN' + '/'    #Aeolus
# stats_dir = inputDir
# =============================================================================

# Set file paths and read Urbanova data
file_modelled_base = inputDir +'/airnow/merged_'+str(year)+'_Urb_airnow_forecasts.csv'
file_modelled_base1 = inputDir +'/airnow/merged_'+str(endyear)+'_Urb_airnow_forecasts.csv'
file_modelled_base = pd.read_csv(file_modelled_base).drop('Unnamed: 0',axis=1)
file_modelled_base1 = pd.read_csv(file_modelled_base1).drop('Unnamed: 0',axis=1)
                                 
file_modelled_base = file_modelled_base.append(file_modelled_base1)

file_airnowsites  = inputDir+ '/aqsid.csv'

begin_time = time.time()

#Setup time to pull AIRPACT data
start = dt.datetime(year=int(year), month=int(month), day=int(day), hour=0)
end = dt.datetime(year=int(endyear), month=int(endmonth), day=int(endday), hour=23)
timezone = pytz.timezone("utc") #("America/Los_Angeles")
start = timezone.localize(start)
end = timezone.localize(end)

start_date = year+'-'+month+'-'+day
end_date = endyear+'-'+endmonth+'-'+endday

df_obs_orig = pd.DataFrame()
# download AP-5 data
df_obs_orig1 = pd.DataFrame()
folder = ['000100060', '000100110', '000100111', '000100118', '000100119', '000100125', '000100127', '000100128', '000100132', '000100134',
          '000100135', '000100140', '000100304', '000100308', '000101003', '000101005', '000101101', '000101202', '000101301', '000101401',
          '000101501', '000101601', '000101801', '000102001', '000102102', '000102602', '000103302', '000103502', '000104101', '000105301',
          '000105604', '000106701', '000107100', '060231004', '060231005', '060631007', '060890004', '060890007', '060890009', '060893003',
          '060932001', '061030004', '061050002', '160010010', '160010017', '160050015', '160050020', '160090010', '160090011', '160130004',
          '160150001', '160150002', '160170003', '160190011', '160210002', '160211007', '160211008', '160230101', '160270002', '160291009',
          '160490002', '160490003', '160491012', '160499991', '160530003', '160550003', '160570005', '160571000', '160571012', '160590004',
          '160650002', '160671011', '160690012', '160690013', '160690014', '160790017', '160830007', '160850002', '160871004', '300130001',
          '300290049', '300298001', '300310017', '300310019', '300490004', '300490026', '300530018', '300630024', '300630037', '300630038',
          '300810007', '300890007', '300930005', '410010004', '410030013', '410050004', '410050102', '410090004', '410111036', '410130100',
          '410170004', '410170120', '410190002', '410230002', '410250003', '410290019', '410290133', '410290201', '410290203', '410292129',
          '410310007', '410330011', '410330036', '410330114', '410350004', '410370001', '410390059', '410390060', '410391007', '410391009',
          '410392013', '410399004', '410430009', '410430104', '410432002', '410432003', '410470007', '410470041', '410470123', '410510080',
          '410512008', '410590121', '410591003', '410610120', '410610123', '410630001', '410650007', '410650008', '410670004', '410670005',
          '410670111', '490030003', '490050007', '490110004', '490353006', '490353010', '490353013', '490450004', '490494001', '490495010',
          '490570002', '490571003', '113490352005', '530010003', '530030004', '530050002', '530050003', '530070007', '530070010', '530070011',
          '530090013', '530090015', '530090017', '530110011', '530110022', '530110024', '530130002', '530150015', '530210002', '530251002',
          '530251003', '530270011', '530272002', '530299999', '530310003', '530330010', '530330017', '530330023', '530330030', '530330031',
          '530330057', '530330080', '530331011', '530332004', '530350007', '530370002', '530410004', '530450007', '530470004', '530470009',
          '530470010', '530470013', '530530012', '530530024', '530530029', '530530031', '530531010', '530531018', '530570011', '530570015',
          '530579999', '530610005', '530610020', '530611007', '530630001', '530630021', '530630046', '530630047', '530639995', '530639997',
          '530639999', '530650002', '530650005', '530670005', '530670013', '530710005', '530730005', '530730019', '530750003', '530750005',
          '530750006', '530770005', '530770009', '530770015', '530770016', '840160410002', '840410352222', '840410390101', '840530230001',
          '840530330069', '840530339990', '840530390006', '840530499991', '840530739992', 'TT1010002', 'TT1010003']
apan_col_names = ['datetime','O3_AP5_4km','PM2.5_AP5_4km','CO_AP5_4km','NO_AP5_4km','NO2_AP5_4km','NOX_AP5_4km','WSPM2.5_AP5_4km','PM10_AP5_4km','SO2_AP5_4km',
                  'O3_obs','PM2.5_obs','CO_obs','NO_obs','NO2_obs','NOX_obs','PM10_obs','SO2_obs']

for file in folder:
    try:
        x = pd.read_csv('http://lar.wsu.edu/R_apps/'+'2019'+'ap5/data/byAQSID/'+file+'.apan',names=apan_col_names,header=None,skiprows=1)
        x['site_id'] = file
        df_obs_orig1=df_obs_orig1.append(x)
        
        x1 = pd.read_csv('http://lar.wsu.edu/R_apps/'+'2018'+'ap5/data/byAQSID/'+file+'.apan',names=apan_col_names,header=None,skiprows=1)
        x1['site_id'] = file
        df_obs_orig=df_obs_orig.append(x1)
    except:
        print('http://lar.wsu.edu/R_apps/'+'2019'+'ap5/data/byAQSID/'+file+'.apan')
        continue
  
# There are a couple cells in the downloaded dataset with this in it. Don;t know why, they shouldn't be there. This line removes them.
#if year == 2018: # For some reason, this breaks when used on other years. 
df_obs_orig = df_obs_orig[df_obs_orig.CO_AP5_4km != '******']

df_obs_orig = df_obs_orig.append(df_obs_orig1)
    
# Open statistics script
exec(open(stats_dir +"statistical_functions.py").read()) 
#%%
g = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
g.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
g = g.drop(0,1)

species = ['PM2.5','OZONE','CO','NO2']
for pollutant in species:
    if pollutant == 'PM2.5':
        abrv = 'PM2.5'
        unit = '($ug/m^3$)'
        y_max = 30
        t_title = str(end_year)+ ' Daily Mean '+pollutant
        s_title = t_title
    if pollutant == 'OZONE':
        abrv = 'O3'
        unit = '(ppb)'
        y_max = 70
        t_title = ' O3 Max Daily 8-Hour Average'
        s_title = t_title
    if pollutant == 'CO':
        abrv = 'CO'
        unit = '(ppb)'
        y_max = 500
        t_title = 'CO Max Daily 8-Hour Average'
        s_title = t_title  
    if pollutant == 'NO2':
        abrv = 'NO2'
        unit = '(ppb)'
        y_max = 100
        t_title = 'NO2 Max Daily Hour Average'
        s_title = t_title
        
    print('Running ' + abrv)
    global df_base
    # Read files
    if abrv == 'O3' or abrv == 'PM2.5':
        col_names_modeled = ['date', 'time', 'site_id', 'pollutant', 'concentration']
        col_names_observed= ['datetime', 'site_id', 'O3_AP5_4km', 'PM2.5_AP5_4km', 'O3_obs', 'PM2.5_obs']
        #df_base  = pd.read_csv(file_modelled_base, header=None, names=col_names_modeled, sep='|',dtype='unicode')   #AIRNOW data is seperated by |, thus it has to be specified here
        df_base  = file_modelled_base.copy() # new method
        df_obs   = pd.read_csv('http://lar.wsu.edu/R_apps/'+str(end_year)+'ap5/data/hrly'+str(end_year)+'.csv', sep=',', names=col_names_observed, skiprows=[0],dtype='unicode')
        df_sites = pd.read_csv(file_airnowsites, skiprows=[1],dtype='unicode') # skip 2nd row which is blank
        df_sites.rename(columns={'AQSID':'site_id'}, inplace=True)
        print('O3/PM2.5 files read')
    elif abrv == 'CO' or abrv == 'NO2':
        col_names_modeled = ['date', 'time', 'site_id', 'pollutant', 'concentration']
        col_names_observed= ['datetime', 'site_id','CO_AP5_4km', 'NOX_AP5_4km','NO_AP5_4km', 'NO2_AP5_4km','CO_obs', 'NOX_obs','NO_obs','NO2_obs']
        #df_base   = pd.read_csv(file_modelled_base, header=None, names=col_names_modeled, sep='|',dtype='unicode')   #AIRNOW data is seperated by |, thus it has to be specified here
        df_base  = file_modelled_base.copy() # new method
        df_obs   = pd.read_csv('http://lar.wsu.edu/R_apps/'+str(end_year)+'ap5/data/hrly'+str(end_year)+'_conoxnono2.csv', sep=',', names=col_names_observed, skiprows=[0],dtype='unicode')
        df_sites = pd.read_csv(file_airnowsites, skiprows=[1],dtype='unicode') # skip 2nd row which is blank
        df_sites.rename(columns={'AQSID':'site_id'}, inplace=True)
        print('CO/NOX files read')  
    else:
        col_names_modeled = ['date', 'time', 'site_id', 'pollutant', 'concentration']
        col_names_observed= ['datetime', 'site_id', 'SO2_AP5_4km', 'SO2_obs']
        df_base   = file_modelled_base.copy()   #AIRNOW data is seperated by |, thus it has to be specified here
        df_obs   = pd.read_csv('http://lar.wsu.edu/R_apps/'+str(end_year)+'ap5/data/hrly'+str(end_year)+'_so2.csv', sep=',', names=col_names_observed, skiprows=[0],dtype='unicode')
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
    
    df_base = pd.merge(df_base,df_sites,how='inner')
    df_obs = pd.merge(df_obs,df_sites,how='inner')

    aqsid_spokane = pd.DataFrame()
    aqsid_spokane['long_name'] = df_base['long_name'].unique()

    df_obs = pd.merge(df_obs,aqsid_spokane,how='inner')

    df_obs_mod = pd.merge(df_obs,df_base, how='outer')
    # get rid of rows if abrv base is not available
    #df_obs_mod = df_obs_mod[pd.notnull(df_obs_mod[abrv+'_AP5_1.33km'])]
    

    df_tseries = df_obs_mod.copy() 

# convert object to numeric (This is required to plot these columns)
    df_tseries[abrv+'_AP5_4km'] = pd.to_numeric(df_tseries[abrv+'_AP5_4km'])
    df_tseries[abrv+'_AP5_1.33km'] = pd.to_numeric(df_tseries[abrv+'_AP5_1.33km'])
    df_tseries[abrv+'_obs'] = pd.to_numeric(df_tseries[abrv+'_obs'])
    print(max(df_tseries[abrv+'_AP5_4km']))
    #df_tseries['datetime'] = df_tseries['datetime'].dt.tz_localize('UTC').dt.tz_convert('US/Pacific')
    #print(set(df_tseries['site_id']))

    #df_tseries = df_tseries.dropna(subset = ['pollutant'])

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

    #print(df_tseries)
    
    # Locate correct site model data
    mask = (df_tseries['datetime'] > start_date) & (df_tseries['datetime'] <= end_date) # Create a mask to determine the date range used
    df_tseries = df_tseries.loc[mask]
    
    if pollutant == 'OZONE' or pollutant == 'CO':
        df_tseries = df_tseries.set_index('datetime')
        df_tseries = df_tseries.resample('H').mean()
        avg_8hr_o3 = df_tseries.rolling(8,min_periods=6).mean()
        times = avg_8hr_o3.index.values - pd.Timedelta('8h')
        avg_8hr_o3.index.values[:] = times
        
        avg_8hr_o3['date'] = avg_8hr_o3.index.strftime('%H')
        intervals = ['00','01','02','03','04','05','06','24'] # remove these hours as per EPA regulation
        for interval in intervals:
            avg_8hr_o3 = avg_8hr_o3[~avg_8hr_o3.date.str.contains(interval)]
            
        d = avg_8hr_o3.resample('D').max().drop('date',axis=1)
        
    if pollutant == 'PM2.5':
        d = df_tseries.copy().set_index('datetime')
        d = d.resample('D').mean()
    
    if pollutant == 'NO2':
        d = df_tseries.copy().set_index('datetime')
        d = d.resample('D').max()
        
    t1 = '2018-05-11'
    t2 = '2018-12-21'
    t1 = pd.to_datetime(t1)
    t2 = pd.to_datetime(t2)
#Plot

    fig,ax=plt.subplots(1,1, figsize=(12,4))
            
    d.ix[:,[abrv+'_obs', abrv+'_AP5_4km', abrv+'_AP5_1.33km']].plot(kind='line', style='-', ax=ax, color=['black', 'blue', 'red'], label=['OBS', 'sens', 'base'])
    plt.axvline(dt.datetime(2018, 5, 11),color = 'green')
    plt.axvline(dt.datetime(2018, 12, 21),color = 'green')
    
    ax.set_title(t_title)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.set_ylabel(abrv+' '+unit)
    ax.set_xlabel('PST')
    ax.legend(['OBS', 'AP5_4km', 'AP5_1.33km'], fontsize=12)
    ax.set_ylim(0,y_max)
    ax.yaxis.grid(True) # horizontal lines
    fig.autofmt_xdate()
    
#Calculate Statistics
    try:
        #Run stats functions
# =============================================================================
#         # Use this to calc stats for befor the BCON issue
#         mask = (d.index > start_date) & (d.index <= t1) # Create a mask to determine the date range used
#         d1 = d.loc[mask]
# =============================================================================
        d1 = d
        aq_stats_4km = stats(d1, abrv+'_AP5_4km', abrv+'_obs')
        aq_stats_1p33km = stats(d1, abrv+'_AP5_1.33km', abrv+'_obs')
        aq_stats = pd.merge(aq_stats_1p33km, aq_stats_4km, how = 'inner', left_index = True, right_index = True)
        g = pd.merge(g, aq_stats, how = 'inner', left_index = True, right_index = True)
        
     
    #Drop some stats to put on plots
#        aq_stats = aq_stats.drop('MB',0)        
#        aq_stats = aq_stats.drop('ME',0)
#        aq_stats = aq_stats.drop('RMSE',0)
#        aq_stats = aq_stats.drop('NMB',0)
#        aq_stats = aq_stats.drop('NME',0)

#            ax.text(0,-0.25, aq_stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
    
    except (ZeroDivisionError):
        print('No observed data, statistics cannot be calculated')
    
    plt.show()
    plt.savefig(inputDir +'/airnow/timeseries_plot/daily_'+abrv+'_'+ year +month +day+ '-' + endyear + endmonth + endday+'.pdf', pad_inches=0.1, bbox_inches='tight')
    #g.to_csv(inputDir +'/airnow/airnow_'+abrv+'_stats.csv')
    plt.close()
    #print(df_tseries)
    
# Scatter plots
    fig,ax=plt.subplots(1,1, figsize=(8,8))
    #d = df_tseries.copy()
    #d=d.set_index('datetime')
    #d = d.resample('D').mean()
    #d=d.groupby(d.index.hour).rolling('24H').mean().ix[:,[abrv+'_obs', abrv+'_AP5_4km', abrv+'_AP5_1.33km']]
    ax.scatter(d[abrv+'_obs'], d[abrv+'_AP5_4km'], c='b', label = '4km',linewidths=None, alpha=0.7)
    ax.scatter(d[abrv+'_obs'], d[abrv+'_AP5_1.33km'], c='r', marker='s', label = '1.33km',linewidths=None,alpha=0.7)        
    axismax = max(max(d[abrv+'_AP5_4km']),max(d[abrv+'_AP5_1.33km']))
    plt.plot([0,axismax], [0,axismax], color='black')
    ax.set_aspect('equal', 'box')
    plt.axis('equal')
    ax.set_ylabel('Modeled '+abrv+' '+unit)
    ax.set_xlabel('Observed '+abrv+' '+unit)        
    ax.set_title(s_title) 
    plt.legend()
    ax.set_ylim(0,axismax) #axismax
    ax.set_xlim(0,axismax)
    fig.autofmt_xdate()
   # print(d)

#Calculate Statistics
# =============================================================================
#     try:
#         #Run stats functions
#         aq_stats_4km = stats(d, abrv+'_AP5_4km', abrv+'_obs')
#         aq_stats_1p33km = stats(d, abrv+'_AP5_1.33km', abrv+'_obs')
#         aq_stats = pd.merge(aq_stats_1p33km, aq_stats_4km, how = 'inner', left_index = True, right_index = True)
#     
#         aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_1.33km', '1.33km ' + site_nameinfo)    
#         aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
#    
#     #Clean up column names
#         aq_stats.columns = aq_stats.columns.str.replace('1.33km ' + site_nameinfo, '1.33km')    
#         aq_stats.columns = aq_stats.columns.str.replace('4km ' + site_nameinfo, '4km')     
#     
#     #Drop some stats to put on plots
#         aq_stats = aq_stats.drop('MB',0)        
#         aq_stats = aq_stats.drop('ME',0)
#         aq_stats = aq_stats.drop('RMSE',0)
#         aq_stats = aq_stats.drop('NMB',0)
#         aq_stats = aq_stats.drop('NME',0)
# 
# #            ax.text(0,-0.12, aq_stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
#         plt.savefig(inputDir +'/airnow/'+month+'/scatter_plots/scatter_'+abrv+'_'+ year +month +day+ '-' + endyear + endmonth + endday+'.pdf', pad_inches=0.1, bbox_inches='tight') #Placed this here so that if there is no oberved data, it won't save an empty plot
# 
#     except (ZeroDivisionError):
#         pass
# =============================================================================
    plt.show()
    plt.savefig(inputDir +'/airnow/scatter_plots/scatter_'+abrv+'_'+ year +month +day+ '-' + endyear + endmonth + endday+'.pdf', pad_inches=0.1, bbox_inches='tight')
    plt.close()
# =============================================================================
# # Diurnal plots
#     for sid in list(set(df_tseries['site_id'])):
#         d = df_tseries.loc[df_tseries['site_id']==sid]
#         site_nameinfo = df_siteinfo.ix[sid, 'long_name']
#         d.drop('site_id',1)
#         fig,ax=plt.subplots(1,1, figsize=(12,4))
#         d=d.set_index('datetime')
#         b=d.groupby(d.index.hour).std()
#         d.groupby(d.index.hour).mean().ix[:,[abrv+'_obs', abrv+'_AP5_4km', abrv+'_AP5_1.33km']].plot(kind='line', style='-', ax=ax, color=['black', 'blue', 'red'], label=['OBS', 'sens', 'base'])
#         ax.set_title(site_nameinfo)
#         ax.set_ylabel(abrv+' '+unit)
#         ax.set_xlabel('Mean Diurnal (hours)')
#         d = d.groupby(d.index.hour).mean()
#         e = b
#         c = d-b
#         e = d+b
#         x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
#         ax.set_ylim(bottom=0)
#         plt.fill_between(x, c[abrv+'_AP5_4km'], e[abrv+'_AP5_4km'], facecolor='blue', edgecolor='black',alpha = 0.1, label=['Std. Dev.']) 
#         plt.fill_between(x, c[abrv+'_AP5_1.33km'], e[abrv+'_AP5_1.33km'],facecolor='red', edgecolor='black',alpha = 0.1, label=['Std. Dev.'])     
#         ax.legend(['OBS', 'AP5_4km', 'AP5_1.33km', 'Std. Dev.'], fontsize=12)
#         print('Plotted ' + site_nameinfo)
#         
# #Calculate Statistics
#         try:
#             #Run stats functions
#             aq_stats_4km = stats(d, abrv+'_AP5_4km', abrv+'_obs')
#             aq_stats_1p33km = stats(d, abrv+'_AP5_1.33km', abrv+'_obs')
#             aq_stats = pd.merge(aq_stats_1p33km, aq_stats_4km, how = 'inner', left_index = True, right_index = True)
#         
#             aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_1.33km', '1.33km ' + site_nameinfo)    
#             aq_stats.columns = aq_stats.columns.str.replace(abrv+'_AP5_4km', '4km ' + site_nameinfo)     
#    
#         #Clean up column names
#             aq_stats.columns = aq_stats.columns.str.replace('1.33km ' + site_nameinfo, '1.33km')    
#             aq_stats.columns = aq_stats.columns.str.replace('4km ' + site_nameinfo, '4km')     
#         
#         #Drop some stats to put on plots
#             aq_stats = aq_stats.drop('MB',0)        
#             aq_stats = aq_stats.drop('ME',0)
#             aq_stats = aq_stats.drop('RMSE',0)
#             aq_stats = aq_stats.drop('NMB',0)
#             aq_stats = aq_stats.drop('NME',0)
# 
# #            ax.text(0,-0.25, aq_stats, ha='center', va='center', transform=ax.transAxes, fontsize = 10, bbox=dict(facecolor='beige', edgecolor='black', boxstyle='round'))
#         
#         except (ZeroDivisionError):
#             pass
#         plt.savefig(inputDir+'/airnow/'+month+'/diurnal_plot/'+abrv+'_'+site_nameinfo+'_'+ year +month +day+ '-' + endyear + endmonth + endday+'.pdf',  pad_inches=0.1, bbox_inches='tight')
# 
# =============================================================================
#%%
# Run the function
#airnow('OZONE','O3','($ppb$)')
#airnow('PM2.5','PM2.5','($ug/m^3$)')
#airnow('CO','CO','($ppb$)')
#airnow('NOX','NOX','($ppb$)')
#airnow('SO2','SO2','($ppb$)')     No SO2 data in airnow v5
g = g.T
print(g)
g.to_csv(inputDir +'/airnow/airnow_'+str(end_year)+'_stats.csv')
end_time = time.time()
print("Run time was %s seconds"%(end_time-begin_time))
print("End of airnow Analysis")











