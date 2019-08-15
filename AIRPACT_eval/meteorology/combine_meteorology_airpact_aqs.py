# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 10:50:43 2019

@author: Jordan
"""


############################################
##########     IMPORT MODULES     ##########
############################################
import pandas as pd

 # Set a directory containing python scripts
base_dir = "/data/lar/users/jmunson/longterm_airpact/"
aqs_dir = base_dir + '/AQS_data'
aqsid_path = aqs_dir + '/aqs_sites.csv'

#%%
# Read the met data
df1 = pd.read_csv(aqs_dir + '/airpact_aqs_met_200951_2010818.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df2 = pd.read_csv(aqs_dir + '/airpact_aqs_met_201091_20121020.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df3 = pd.read_csv(aqs_dir + '/airpact_aqs_met_20121021_2013326.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df4 = pd.read_csv(aqs_dir + '/airpact_aqs_met_2013326_201471.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df5 = pd.read_csv(aqs_dir + '/airpact_aqs_met_201511_2016112.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df6 = pd.read_csv(aqs_dir + '/airpact_aqs_met_2016113_201711.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df7 = pd.read_csv(aqs_dir + '/airpact_aqs_met_201712_2017531.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df8 = pd.read_csv(aqs_dir + '/airpact_aqs_met_201761_201811.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df9 = pd.read_csv(aqs_dir + '/airpact_aqs_met_201812_2018814.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
df10 = pd.read_csv(aqs_dir + '/airpact_aqs_met_2018815_20181231.csv').drop(['Unnamed: 0','ix','iy'],axis=1)
print('Met data read')

# Combine the met data
df_airpact = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10])

df_airpact['DateTime'] = pd.to_datetime(df_airpact['DateTime'])
df_airpact['AQS_ID'] = df_airpact['AQS_ID'].astype(str)

print('df_airpact data concatenated')

#exec(open(base_dir + "/airpact_functions.py").read())


del([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10])

##############################################################################
# Read AQS data. csv's created from 'AQS_grabbing.py' script, and the model data from the previous lines of code
##############################################################################
# Read AQS data
df_wa = pd.read_csv(aqs_dir + '/Washington_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_or = pd.read_csv(aqs_dir + '/Oregon_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_id = pd.read_csv(aqs_dir + '/Idaho_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
#df_cc = pd.read_csv(aqs_dir + 'Canada_aqs.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_mt = pd.read_csv(aqs_dir + '/Montana_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_ca = pd.read_csv(aqs_dir + '/California_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_nv = pd.read_csv(aqs_dir + '/Nevada_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )
df_ut = pd.read_csv(aqs_dir + '/Utah_aqs_met.csv', sep = ',',parse_dates=[['Date Local', 'Time Local']] )

#  Combine AQS data
df_list = [df_wa,df_or,df_id,df_mt,df_ca,df_nv,df_ut]
df_obs = pd.concat(df_list)
del([df_wa,df_or,df_id,df_mt,df_ca,df_nv,df_ut])

#Create AQSID Column form state code, county code, and site num
df_obs['County Code'] = ["%03d" % n for n in df_obs['County Code'] ]
df_obs['Site Num'] = ["%04d" % n for n in df_obs['Site Num'] ]

df_obs['AQS_ID'] = (df_obs['State Code']).astype(str) + (df_obs['County Code']).astype(str)+(df_obs['Site Num']).astype(str)

# Drop columns of data we are not looking at so as to increase the speed of the script
df_obs = df_obs.drop(['Unnamed: 0','Unnamed: 1','State Name','County Name','State Code','County Code','Site Num','Units of Measure','Latitude','Longitude'],axis=1)
df_obs = df_obs.rename(columns={'Date Local_Time Local': 'datetime','Parameter Name':'Parameter_Name'})

#Create AQSID Column form state code, county code, and site num
aqsid = pd.read_csv(aqsid_path)
aqsid = aqsid.ix[:,['State Code','County Code','Site Number','Local Site Name','Location Setting']]

aqsid['County Code'] = ["%03d" % n for n in aqsid['County Code'] ]
aqsid['Site Number'] = ["%04d" % n for n in aqsid['Site Number'] ]

aqsid['AQS_ID'] = (aqsid['State Code']).astype(str) + (aqsid['County Code']).astype(str)+(aqsid['Site Number']).astype(str)

# Must force every cell in AQSID to be a string, otherwise lose most of data
aqsid['AQS_ID'] = aqsid['AQS_ID'].astype(str)
df_obs['AQS_ID'] = df_obs['AQS_ID'].astype(str)

df_obs = pd.merge(df_obs,aqsid) # Merge df_mod and aqsid so as to add names and such to the datafram
df_obs = df_obs.drop(['State Code','County Code','Site Number'], axis=1)
print('Observed data read and combined')

# The obs data must be formatted so that the species are columns
df_obs_pres = df_obs.loc[(df_obs['Parameter_Name'] == 'Barometric pressure')].rename(columns={'Sample Measurement':'aqs_pressure'}).drop(['Parameter_Name'],axis=1)
df_obs_temp = df_obs.loc[(df_obs['Parameter_Name'] == 'Outdoor Temperature')].rename(columns={'Sample Measurement':'aqs_temp'}).drop(['Parameter_Name'],axis=1)
df_obs_rh = df_obs.loc[(df_obs['Parameter_Name'] == 'Relative Humidity ')].rename(columns={'Sample Measurement':'aqs_rh'}).drop(['Parameter_Name'],axis=1)
df_obs_wspd = df_obs.loc[(df_obs['Parameter_Name'] == 'Wind Speed - Resultant')].rename(columns={'Sample Measurement':'aqs_wspd'}).drop(['Parameter_Name'],axis=1)
df_obs_wdir = df_obs.loc[(df_obs['Parameter_Name'] == 'Wind Direction - Resultant')].rename(columns={'Sample Measurement':'aqs_wdir'}).drop(['Parameter_Name'],axis=1)

df_obs1 = pd.merge(df_obs_pres,df_obs_temp,how='outer')
df_obs = pd.merge(df_obs_wspd,df_obs_wdir,how='outer')
df_obs = pd.merge(df_obs,df_obs_rh,how='outer')
df_obs = pd.merge(df_obs,df_obs1,how='outer')

# Add site types to df_airpact. They used to be there but something must have changed...
df_airpact = pd.merge(df_airpact,aqsid).drop(['State Code','County Code','Site Number'], axis=1)
#df_obs2 = pd.concat([df_obs_pres,df_obs_temp,df_obs_rh,df_obs_wspd,df_obs_wdir],axis=1)
#df_com = pd.merge(df_obs, df_airpact, how='outer')

# Save the data so that this process does not have to be done over and over again
df_airpact.to_csv(base_dir+'/outputs/df_airpact_met.csv')
df_obs.to_csv(base_dir+'/outputs/df_obs_met.csv')


