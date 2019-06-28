# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 09:09:58 2018

This process is not fast and should only be done while connected to ethernet

Script based off of Kai Fan
"""

import pandas as pd
import time
#Set state

species = ['o3','pm_FRM/FEM','pm_non_FRM/FEM'] # when changing bacl, don't forget to rename the save file line
species_code = ['44201','88101','88502']
name = ''
num = 3

# =============================================================================
# species = ['Winds','Temperature','Pressure','RH']
# species_code = ['WIND','TEMP','PRESS','RH_DP']
# name = '_met'
# num = 4
# =============================================================================

def aqs(state,ac):
    AQS={}
    for i in range(0,num):
        print(species[i])
        for j in range(2009,2019):
            dataframename = species[i]+ac+str(j)
            start = time.time()
            print(j)
            temp = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/hourly_'+species_code[i]+'_'+str(j)+'.zip',header=0,sep=',')
            temp['Date GMT'] = pd.to_datetime(temp['Date GMT'])
            temp = temp[(temp['State Name']==state)]  
            AQS[dataframename] = temp
            end = time.time()
            print(round(end-start))       
            dict_AQS = AQS       
 
    AQS_df = pd.concat(dict_AQS)
    AQS_df = AQS_df.drop(['Parameter Code','POC','Datum','Date GMT','Time GMT','MDL','Uncertainty',
                          'Qualifier','Method Type','Method Code','Method Name','Date of Last Change'], axis=1)
   
    AQS_df.to_csv(r'E:/Research/AIRPACT_eval/AQS_data/'+state+'_aqs'+name+'.csv')
    print(state + ' Done')

aqs('Washington','_WA')
aqs('Oregon','_OR')
aqs('Idaho','_ID')
aqs('Montana','_MT')
aqs('California','_CA')
aqs('Utah','_UT')
aqs('Nevada','_NV')
aqs('Canada','_CC')

# =============================================================================
# Take AQS data and merge with observation data
# =============================================================================

inputDir = r'E:/Research/AIRPACT_eval/'

# ##############################################################################
# # Combine hrly model data
# ##############################################################################
# 
# df_1 = pd.read_csv('http://lar.wsu.edu/R_apps/2009ap3/data/2009hrly.csv', sep=',')
# df_2 = pd.read_csv('http://lar.wsu.edu/R_apps/2010ap3/data/2010hrly.csv', sep=',')
# df_3 = pd.read_csv('http://lar.wsu.edu/R_apps/2011ap3/data/hrly2011ap3.csv', sep=',')
# df_4 = pd.read_csv('http://lar.wsu.edu/R_apps/2012ap3/data/hrly2012ap3.csv', sep=',') #Whole years data
# #df_5 = pd.read_csv('http://lar.wsu.edu/R_apps/2012ap4/data/hrly2012.csv', sep=',') #Second half of years data
# df_5 = pd.read_csv('http://lar.wsu.edu/R_apps/2013ap4/data/hrly2013.csv', sep=',')
# df_6 = pd.read_csv('http://lar.wsu.edu/R_apps/2014ap4/data/hrly2014.csv', sep=',')
# df_7 = pd.read_csv('http://lar.wsu.edu/R_apps/2015ap4/data/hrly2015.csv', sep=',') #Full year data
# #df_8 = pd.read_csv('http://lar.wsu.edu/R_apps/2015ap5/data/hrly2015.csv', sep=',')
# df_8 = pd.read_csv('http://lar.wsu.edu/R_apps/2016ap5/data/hrly2016.csv', sep=',')
# df_9 = pd.read_csv('http://lar.wsu.edu/R_apps/2017ap5/data/hrly2017.csv', sep=',')
# df_10 = pd.read_csv('http://lar.wsu.edu/R_apps/2018ap5/data/hrly2018.csv', sep=',')
# 
# #Combine data
# df_list = [df_1,df_2,df_3,df_4,df_5,df_6,df_7,df_8,df_9,df_10]
# df_mod = pd.concat(df_list)
# 
# #Drop uneccesary columns
# df_mod = df_mod.drop(['O3_obs','PM2.5_obs'], axis=1)
# 
# #df_mod = pd.merge(df_mod,aqsid, on='AQSID', how='outer')   
# 
# # Convert to datetime and adjust to PST
# print('Converting datetime, this may take a while')
# df_mod['datetime'] = pd.to_datetime(df_mod['DateTime'], infer_datetime_format=True)
# df_mod["datetime"] = df_mod["datetime"].apply(lambda x: x - dt.timedelta(hours=8)) #Adjust to PST
# df_mod = df_mod.drop(['DateTime'], axis=1)
# 
# df_mod.to_csv(inputDir + '/model_aqs.csv')
# print('Model data combined')
# =============================================================================

##############################################################################
# Read AQS data. csv's created from 'AQS_grabbing.py' script, and the model data from the previous lines of code
##############################################################################
# Read model data
df_mod = pd.read_csv(inputDir + '/model_aqs.csv',sep=',')
df_mod['datetime'] = pd.to_datetime(df_mod['datetime']) #Must convert to date time to merge later
df_mod = df_mod.drop('Unnamed: 0',axis=1)

#Create AQSID Column form state code, county code, and site num
aqsid = pd.read_csv(inputDir+'aqs_sites.csv')
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
df_com['O3_obs'] = df_com['O3_obs']*1000 #convert to ppb
df_obs['O3_obs'] = df_obs['O3_obs']*1000
df_com.loc[:,'PM2.5_obs'] = pd.to_numeric(df_com.loc[:,'PM2.5_obs'], errors='coerce')
df_com = df_com.drop(['State Code','County Code','Site Number'],axis=1) # drop unecessary columns
print('Combined dataframe finished')

df_com.to_csv(inputDir+'AQS_data/df_com_aplong.csv')


    