# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 09:32:04 2019

@author: Jordan Munson
"""


# import some libraries
import pandas as pd
import time
from calendar import monthrange
import datetime as dt

starttime = time.time()
day='01'
month = '01' 
year  = '2019' 

endday = '01'
endmonth='10'
endyear='2019'

end_year=int(endyear)
end_month=int(endmonth) 
endday = str(monthrange(end_year, end_month)[1])

inputDir          = r'E:\Research\Urbanova_Jordan/'
plotDir           =r'E:\Research\Urbanova_Jordan\output/'
stats_dir = r'E:/Research/scripts/Urbanova/'
urb_path = inputDir +  'Urbanova_ref_site_comparison/Urbanova/'
air_path = inputDir + 'Urbanova_ref_site_comparison/AIRPACT/'
file_modelled_base = inputDir +'/airnow/merged_'+str(end_year)+'_Urb_airnow_forecasts.csv'

# Set file paths
file_modelled_base = inputDir +'/airnow/merged_'+str(end_year)+'_Urb_airnow_forecasts.csv'
print(file_modelled_base)
file_airnowsites  = inputDir+ '/aqsid.csv'
#file_airnowsites  = '/data/lar/projects/Urbanova/2018/2018040400/POST/CCTM/aqsid.csv' # Hard coded as some aqsid files do not include all site ID's, this one does.
print(file_airnowsites)

# Open statistics script
exec(open(stats_dir +"statistical_functions.py").read()) 
#%%
# Need to load 2019 data from individual sites
df_obs_orig = pd.DataFrame()
folder = ['160090011', '160550003', '160550004', '530630001',
       '530630021', '530630046', '530630047', '530639995', '530639997',
       '530650002', '530750006', '530639999']
apan_col_names = ['datetime','O3_AP5_4km','PM2.5_AP5_4km','CO_AP5_4km','NO_AP5_4km','NO2_AP5_4km','NOX_AP5_4km','WSPM2.5_AP5_4km','PM10_AP5_4km','SO2_AP5_4km',
                  'O3_obs','PM2.5_obs','CO_obs','NO_obs','NO2_obs','NOX_obs','PM10_obs','SO2_obs']
for file in folder:
    try:
        x = pd.read_csv('http://lar.wsu.edu/R_apps/2019ap5/data/byAQSID/'+file+'.apan',names=apan_col_names,header=None,skiprows=1)
        x['site_id'] = file
        df_obs_orig=df_obs_orig.append(x)
    except:
        print('http://lar.wsu.edu/R_apps/2019ap5/data/byAQSID/'+file+'.apan')
        continue

# remove pollutants not interested in here
df = df_obs_orig.copy()
df = df_obs_orig.drop(['CO_AP5_4km','NO_AP5_4km','NO2_AP5_4km','NOX_AP5_4km','WSPM2.5_AP5_4km','PM10_AP5_4km','SO2_AP5_4km',
                       'CO_obs','NO_obs','NO2_obs','NOX_obs','PM10_obs','SO2_obs'],axis=1)
    





# Load site data
df_sites = pd.read_csv(file_airnowsites, skiprows=[1],dtype='unicode') # skip 2nd row which is blank
df_sites.rename(columns={'AQSID':'site_id'}, inplace=True)
#%%
species = ['PM2.5','OZONE']
pollutants = ['PM2.5','O3']

g = pd.DataFrame(['Forecast Mean', 'Observation Mean', 'MB','ME','FB [%]','FE [%]',"NMB [%]", "NME [%]", "RMSE", "R^2 [-]",'Forecast 98th','Observation 98th','AQSID','Pollutant','Forecast'])
g.index = ['Forecast Mean', 'Observation Mean', 'MB','ME','FB [%]','FE [%]',"NMB [%]", "NME [%]", "RMSE", "R^2 [-]",'Forecast 98th','Observation 98th','AQSID','Pollutant','Forecast']
g = g.drop(0,1)

for abrv,pollutant in zip(pollutants,species):
    print('Now running '+pollutant)
    for site in folder:
        # Format Urbanova data
        df_base  = pd.read_csv(file_modelled_base).drop('Unnamed: 0',axis=1) # new method
        df_base = df_base.loc[df_base['pollutant']==pollutant, df_base.columns]
        #print(df_base['site_id'].unique())
        # Renames the abrv to concentration
        df_base.columns = df_base.columns.str.replace('concentration',abrv+ '_AP5_1.33km')
        df_base = df_base.dropna(subset=[abrv+'_AP5_1.33km'])
        
        # Format AP-5 data
        d = df.loc[df['site_id'] == site]
        d = d.dropna(subset=[abrv+'_AP5_4km', abrv+'_obs'])

        
        # convert datatime colume to time data (This conversion is so slow)
        #print('Executing datetime conversion, this takes a while')
        df_base['datetime'] = pd.to_datetime(df_base['date'] + ' ' + df_base['time'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
        d['datetime'] = pd.to_datetime(d['datetime'], infer_datetime_format=True)
        #print('datetime conversion complete')
        
        #Convert model data to PST from UTC (PST = UTC-8)
        df_base["datetime"] = df_base["datetime"].apply(lambda x: x - dt.timedelta(hours=8))
        d["datetime"] = d["datetime"].apply(lambda x: x - dt.timedelta(hours=8))
        df_base = df_base.drop('date',axis=1)
        df_base = df_base.drop('time',axis=1)
        
        
     # sites which are common between base and Observations
        sites_common = set(d['site_id']).intersection(set(df_base['site_id']))
        
        df_base = pd.merge(df_base,df_sites,how='inner')
        d = pd.merge(d,df_sites,how='inner')
    
        aqsid_spokane = pd.DataFrame()
        aqsid_spokane['long_name'] = df_base['long_name'].unique()
    
        d = pd.merge(d,aqsid_spokane,how='inner')
    
        df_obs_mod = pd.merge(d,df_base, how='outer')
        # get rid of rows if abrv base is not available
        #df_obs_mod = df_obs_mod[pd.notnull(df_obs_mod[abrv+'_AP5_1.33km'])]
        
    
        df_tseries = df_obs_mod.copy() 
    
    # convert object to numeric (This is required to plot these columns)
        df_tseries[abrv+'_AP5_4km'] = pd.to_numeric(df_tseries[abrv+'_AP5_4km'])
        df_tseries[abrv+'_AP5_1.33km'] = pd.to_numeric(df_tseries[abrv+'_AP5_1.33km'])
        df_tseries[abrv+'_obs'] = pd.to_numeric(df_tseries[abrv+'_obs'])
        
        #print(max(df_tseries[abrv+'_AP5_4km']))
        
        try:     
            # Calculate statistics for individual sites
            df_tseries = df_tseries.dropna(subset=[abrv+'_AP5_1.33km',abrv+'_obs',abrv+'_AP5_4km',])
            sap  = stats_version(df_tseries,abrv+'_AP5_4km', abrv+'_obs')
            #df_tseries = df_tseries.dropna(subset=[abrv+'_AP5_1.33km',abrv+'_obs'])
            surb  = stats_version(df_tseries,abrv+'_AP5_1.33km', abrv+'_obs')
            

            print(site)
        except ZeroDivisionError:
            print('No data available for '+site + ' for '+abrv)
            continue
        df_site_ap5 = pd.DataFrame([site,abrv,'AIRPACT'], columns = [abrv+'_AP5_4km',],index=['AQSID','Pollutant','Forecast'])
        df_site_urb = pd.DataFrame([site,abrv,'Urbanova'], columns = [abrv+'_AP5_1.33km'],index=['AQSID','Pollutant','Forecast'])           
        
        # create to give row of aqsid
        sap = sap.append(df_site_ap5)
        surb = surb.append(df_site_urb)
        
        # rename to give aqsid
        sap.rename(columns={abrv+'_AP5_4km' : abrv+'_AP5_4km_'+site},inplace=True)
        surb.rename(columns={abrv+'_AP5_1.33km' : abrv+'_AP5_1.33km_'+site},inplace=True)
        
        aq_stats = pd.merge(sap, surb, how = 'inner', left_index = True, right_index = True)
        g = pd.merge(g, aq_stats, how = 'inner', left_index = True, right_index = True)
g = g.T
df_sites.rename(columns={'site_id' : 'AQSID'},inplace=True)
g = pd.merge(g,df_sites, on =['AQSID'])

g.to_csv(inputDir +'/airnow/site_specific_stats.csv')
#%%
# =============================================================================
# Figure out which sites are which site type
# =============================================================================

# load data
df_com = pd.read_csv(r'E:/Research/AIRPACT_eval/AQS_data/df_com_aplong.csv').drop('Unnamed: 0', axis=1)
df_com.loc[:,'O3_mod'] = pd.to_numeric(df_com.loc[:,'O3_mod'], errors='coerce')
df_com.loc[:,'PM2.5_mod'] = pd.to_numeric(df_com.loc[:,'PM2.5_mod'], errors='coerce')
df_com.loc[:,'O3_obs'] = pd.to_numeric(df_com.loc[:,'O3_obs'], errors='coerce')
df_com.loc[:,'PM2.5_obs'] = pd.to_numeric(df_com.loc[:,'PM2.5_obs'], errors='coerce')
df_com['datetime'] = pd.to_datetime(df_com['datetime'])
df_com['AQSID'] = df_com['AQSID'].astype(str)

sitetypes = df_com.drop_duplicates('AQSID')
sitetypes = sitetypes.drop(['O3_obs','PM2.5_obs','datetime','O3_mod','PM2.5_mod'],axis=1)

urb_sites = pd.DataFrame(folder,columns=['AQSID'])
sitetypes = pd.merge(sitetypes,urb_sites, on =['AQSID'])

