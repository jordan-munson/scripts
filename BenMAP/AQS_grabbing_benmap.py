# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 09:09:58 2018

This process is not fast and should only be done while connected to ethernet

"""

import pandas as pd
import time
import datetime as dt

base_dir = r'E:/Research/Benmap/'

species =  ['pm_FRM/FEM','pm_non_FRM/FEM']#['o3']# when changing bacl, don't forget to rename the save file line
species_code =  ['88101','88502'] # ['44201']

start_year = 2016 
end_year = start_year+1

# =============================================================================
# species = ['Winds','Temperature','Pressure','RH']
# species_code = ['WIND','TEMP','PRESS','RH_DP']
# =============================================================================

#%%
# =============================================================================
# Hourly - takes long time
# =============================================================================
def aqs(begining,ending):
    AQS={}
    for i in range(0,len(species_code)):
        print(species[i])
        for j in range(begining,ending):
            dataframename = species[i]+str(j)
            start = time.time()
            print(j)
            temp = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/hourly_'+species_code[i]+'_'+str(j)+'.zip',header=0,sep=',')
            temp['Date GMT'] = pd.to_datetime(temp['Date GMT'])
            #temp = temp[(temp['State Name']==state)]  
            AQS[dataframename] = temp
            end = time.time()
            print(round(end-start))       
            dict_AQS = AQS       
 
    AQS_df = pd.concat(dict_AQS)
    AQS_df = AQS_df.drop(['Parameter Code','POC','Datum','Time Local','Date Local','MDL','Uncertainty',
                          'Qualifier','Method Type','Method Code','Method Name','Date of Last Change'], axis=1)
   
    AQS_df.to_csv(base_dir+'AQS_data/aqs_pm_benmap'+'_'+str(begining)+'.csv')

aqs(start_year,end_year)
print('AQS Download done')
#%%
# =============================================================================
# # =============================================================================
# # Daily - takes short time
# # =============================================================================
# def aqs(begining,ending):
#     AQS={}
#     for i in range(0,2):
#         print(species[i])
#         for j in range(begining,ending):
#             dataframename = species[i]+str(j)
#             start = time.time()
#             print(j)
#             temp = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/daily_'+species_code[i]+'_'+str(j)+'.zip',header=0,sep=',')
#             #temp['Date GMT'] = pd.to_datetime(temp['Date GMT'])
#             #temp = temp[(temp['State Name']==state)]  
#             AQS[dataframename] = temp
#             end = time.time()
#             print(round(end-start))       
#             dict_AQS = AQS       
#  
#     AQS_df = pd.concat(dict_AQS)
#     AQS_df = AQS_df.drop(['Parameter Code','POC','Datum',
#                           'Method Code','Method Name','Date of Last Change'], axis=1)
#    
#     AQS_df.to_csv(base_dir+'aqs_daily_pm25_benmap.csv',encoding='utf-8',index = False)
# 
# aqs(2018,2019)
# =============================================================================

#%%
# =============================================================================
# Hourly
# =============================================================================
df = pd.read_csv(base_dir+'AQS_data/aqs_pm_benmap_'+str(start_year)+'.csv',parse_dates=[['Date GMT', 'Time GMT']]).drop(['Parameter Name','Units of Measure','State Name','County Name','Unnamed: 0','Unnamed: 1'],axis=1)
df = df.rename(columns={'Date GMT_Time GMT': 'Date GMT'})
df['Date GMT'] = pd.to_datetime(df['Date GMT'])
df["Date GMT"] = df["Date GMT"].apply(lambda x: x - dt.timedelta(hours=8)) #Adjust to PST


#df = pd.read_csv(base_dir+'aqs_daily_pm25_benmap.csv',low_memory=False).drop(['Parameter Name','Pollutant Standard','Units of Measure','Event Type','Observation Count','Observation Percent','1st Max Value','1st Max Hour','AQI','State Name','County Name','City Name','CBSA Name','Address'],axis=1)
#df = df.loc[df['Sample Duration']=='24-HR BLK AVG', df.columns]
#print(df['Sample Duration'].unique())
#Create AQSID Column form state code, county code, and site num
df['State Code'] = ["%02d" % n for n in df['State Code'] ]
df['County Code'] = ["%03d" % n for n in df['County Code'] ]
df['Site Num'] = ["%04d" % n for n in df['Site Num'] ]

# =============================================================================
# # test just Washington sites
# df = df.loc[df['State Code']=='53', df.columns]
# =============================================================================

df['AQSID'] = (df['State Code']).astype(str) +'-'+ (df['County Code']).astype(str)+'-'+(df['Site Num']).astype(str)+'-' + species_code[0]+'-1'
mysites = df['AQSID'].unique().astype(str)
df = df.drop(['State Code','County Code','Site Num'],axis = 1)

# Change format to that BenMAP wants
df = df.rename(columns={"AQSID": "Monitor Name",'Sample Measurement':'Values'})
df['Metric'] = ''
df['Seasonal Metric'] = ''
df['Statistic'] = ''
df['Monitor Description'] = "'MethodCode=.','LandUse=.','LocationSetting=.','ProbeLocation=.','MonitorObjective=.','POC=1','PollutantID=44201'"

# reorginize df
df = df[['Monitor Name', 'Monitor Description','Latitude', 'Longitude','Metric','Seasonal Metric','Statistic', 'Date GMT', 'Values']]
df['Values'] = df['Values']*1000

# Create date range
date1 = str(start_year)+'-01-01'
date2 = str(start_year)+'-12-31'
mydates = pd.date_range(date1, date2, freq='D').tolist()

# Remove dates other than the specified year
df['Date GMT'] = df['Date GMT'].astype(str)
df = df[~df['Date GMT'].str.contains(str(start_year-1))] # remove data not of the year specified
df = df[~df['Date GMT'].str.contains(str(start_year+1))] # remove data not of the year specified

# Convert date in df to datetime
df['Date GMT'] = pd.to_datetime(df['Date GMT'])

df_b = pd.DataFrame(data=mydates,columns=['Date GMT'])
df_c = pd.DataFrame(columns=['Monitor Name','Monitor Description','Latitude','Longitude','Metric','Seasonal Metric','Statistic','Date GMT','Values'])
for sites in mysites:
    df_a = df.loc[df['Monitor Name']==sites, df.columns] # Locate a single site
    
    
    df_a = pd.merge(df_a,df_b, how = 'outer') # merge to create dataframe with all days of the year
    df_d = df_a.set_index('Date GMT').drop(['Latitude','Longitude'],axis=1)
    df_d = round(df_d.resample('D').mean(),2)
    df_d = df_d.reset_index()
    
    # Rename columns to replace the nans generated in the merge
    df_a['Monitor Name'] = sites
    df_a['Monitor Description'] = df_a['Monitor Description'][0]
    df_a['Latitude'] = df_a['Latitude'][0]
    df_a['Longitude'] = df_a['Longitude'][0]
    df_a['Metric'] = df_a['Metric'][0]
    df_a['Seasonal Metric'] = df_a['Seasonal Metric'][0]
    df_a['Statistic'] = df_a['Statistic'][0]
    
    # Replaces the nans with blank cells
    df_d = df_d.fillna('.')
    
    # Sorts by datetime so that everything is in order
    df_d = df_d.sort_values('Date GMT')
    
    # create list of all conc values
    values = df_d['Values'].astype(str).tolist()

    print(len(values))
    values = ','.join(values)
    
    df_a = pd.DataFrame(df_a.iloc[0])
    df_a = df_a.T
    df_a['Values'] = values[:] 
    
    df_a  = df_a.reset_index(drop =True)
# =============================================================================
#     if df_a['Monitor Description'][0]=='':
#         df_a['Monitor Description'] = 'No description'
#     else:
#         pass
# =============================================================================
    
    df_c = df_c.append(df_a)

df_c = df_c.drop(['Date GMT'],axis=1)
df_c.to_csv(base_dir + 'AQS_data/daily_pm_aqs_formatted'+'_'+str(start_year)+'.csv',index=False, encoding='utf-8-sig')


#%%
# =============================================================================
# # =============================================================================
# # Use this with the benmap tool to convert mon data
# # =============================================================================
# # =============================================================================
# # df = pd.read_csv(base_dir+'aqs_pm25_benmap.csv',low_memory=False,parse_dates=[['Date GMT', 'Time GMT']]).drop(['Parameter Name','Units of Measure','State Name','County Name','Unnamed: 0','Unnamed: 1'],axis=1)
# # df = df.rename(columns={'Date GMT_Time GMT': 'Date GMT'})
# # df['Date GMT'] = pd.to_datetime(df['Date GMT'])
# # =============================================================================
# 
# 
# df = pd.read_csv(base_dir+'aqs_daily_pm25_benmap.csv',low_memory=False).drop(['Parameter Name','Pollutant Standard','Units of Measure','Event Type','Observation Count','Observation Percent','1st Max Value','1st Max Hour','AQI','State Name','County Name','City Name','CBSA Name','Address'],axis=1)
# df = df.loc[df['Sample Duration']=='24-HR BLK AVG', df.columns]
# print(df['Sample Duration'].unique())
# #Create AQSID Column form state code, county code, and site num
# df['County Code'] = ["%03d" % n for n in df['County Code'] ]
# df['Site Num'] = ["%04d" % n for n in df['Site Num'] ]
# 
# df = df.loc[df['State Code']==53, df.columns] # selects only washington
# 
# df['AQSID'] = (df['State Code']).astype(str) + (df['County Code']).astype(str)+(df['Site Num']).astype(str)
# mysites = df['AQSID'].unique().astype(str)
# df = df.drop(['State Code','County Code','Site Num'],axis = 1)
# 
# # Change format to that BenMAP wants
# df = df.rename(columns={"AQSID": "Monitor Name",'Arithmetic Mean':'Value','Date GMT':'Date'})
# df['Metric'] = ''
# df['Seasonal Metric'] = ''
# df['Statistic'] = ''
# df['Monitor Description'] = "'MethodCode=.','LandUse=.','LocationSetting=.','ProbeLocation=.','MonitorObjective=.','POC=1','PollutantID=88101'"
# 
# # reorginize df
# df = df[['Monitor Name', 'Monitor Description','Latitude', 'Longitude','Metric','Seasonal Metric','Statistic', 'Date', 'Value']]
# 
# # Create date range
# date1 = '2018-01-01'
# date2 = '2018-12-31'
# mydates = pd.date_range(date1, date2, freq='D').tolist()
# 
# # Convert date in df to datetime
# df['Date'] = pd.to_datetime(df['Date'])
# 
# df_b = pd.DataFrame(data=mydates,columns=['Date'])
# df_c = pd.DataFrame(columns=['Monitor Name','Monitor Description','Latitude','Longitude','Metric','Seasonal Metric','Statistic','Date','Value'])
# for sites in mysites:
#     df_a = df.loc[df['Monitor Name']==sites, df.columns] # Locate a single site
#     
#     df_a = pd.merge(df_a,df_b, how = 'outer') # merge to create dataframe with all days of the year
#     
#     # Rename columns to replace the nans generated in the merge
#     df_a['Monitor Name'] = sites
#     df_a['Monitor Description'] = df_a['Monitor Description'][0]
#     df_a['Latitude'] = df_a['Latitude'][0]
#     df_a['Longitude'] = df_a['Longitude'][0]
#     df_a['Metric'] = df_a['Metric'][0]
#     df_a['Seasonal Metric'] = df_a['Seasonal Metric'][0]
#     df_a['Statistic'] = df_a['Statistic'][0]
#     
#     # Drops nans
#     df_a = df_a.dropna()
#     
#     # Sorts by datetime so that everything is in order
#     df_a = df_a.sort_values('Date')
#     
#     
#     df_a  = df_a.reset_index(drop =True)
#     df_a['Value'] = round(df_a['Value'],4)
#     
#     # Convert to correct datetime format for benmap
#     df_a['Date'] = df_a['Date'].dt.strftime('%m/%d/%Y')
#     
#     # add montior to total list
#     df_c = df_c.append(df_a)
# #df_c = df_c.drop(['Date GMT'],axis=1)
# 
# df_c.to_csv(base_dir + 'aqs_for_ben_funct.csv',index=False)
# =============================================================================

#%%


# =============================================================================
# #df_ben = pd.read_csv(r'C:\Users\riptu\Documents\My BenMAP-CE Files\Exports/EPA Standard Monitors PM2.5_PM2.5_2013.csv')
# a = '.,.,.,16.4,.,.,.,.,.,3.2,.,.,.,.,.,22.2,.,.,.,.,.,22.2,.,.,.,.,.,5.2,.,.,.,.,.,12.9,.,.,.,.,.,14.1,.,.,.,.,.,17,.,.,.,.,.,5.8,.,.,.,.,.,6.7,.,.,.,.,.,6.4,.,.,.,.,.,5.1,.,.,.,.,.,2.1,.,.,.,.,.,7.7,.,.,.,.,.,7.7,.,.,.,.,.,7.5,.,.,.,.,.,3.1,.,.,.,.,.,5.8,.,.,.,.,.,4.6,.,.,.,.,.,2.5,.,.,.,.,.,9.3,.,.,.,.,.,10.8,.,.,.,.,.,4.3,.,.,.,.,.,2,.,.,.,.,.,2.5,.,.,.,.,.,4,.,.,.,.,.,3.1,.,.,.,.,.,.,.,.,.,.,.,1.9,.,.,.,.,.,3.5,.,.,.,.,.,7.6,.,.,.,.,.,6.7,.,.,.,.,.,.,.,.,.,.,.,5.9,.,.,.,.,.,5,.,.,.,.,.,5.9,.,.,.,.,.,9.8,.,.,.,.,.,11,.,.,.,.,.,4.9,.,.,.,.,.,5.2,.,.,.,.,.,6,.,.,.,.,.,.,.,.,.,.,.,10.5,.,.,.,.,.,4.2,.,.,.,.,.,3,.,.,.,.,.,2.1,.,.,.,.,.,7.5,.,.,.,.,.,14.2,.,.,.,.,.,16.2,.,.,.,.,.,19,.,.,.,.,18.1,11,.,.,.,.,20.5,15.9,.,.,.,.,.,13.9,.,.,.,.,.,2.5,.,.,.,.,.,33.2,.,.,.,.,.,30.6,.,.,.,.,.,9.2,.,.,.,.,.,29.9,.,.,.,.,.,11.6,.,.,.,.,.,7.5,.,.,.,.,.,14,.'
# a = a.split(',')
# 
# =============================================================================








    