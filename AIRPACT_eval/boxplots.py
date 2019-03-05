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

# =============================================================================
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


df_mod.loc[:,'O3_mod'] = pd.to_numeric(df_mod.loc[:,'O3_mod'], errors='coerce')
df_mod.loc[:,'PM2.5_mod'] = pd.to_numeric(df_mod.loc[:,'PM2.5_mod'], errors='coerce')


#%%
pollutant = ['O3','PM2.5']
versions = ['AP3','AP4','AP5']
seasons = ['Summer']#,'Winter'] 

for species in pollutant:
    data=[]
    data1=[]
    names=[]
    sites=[]
    if species == 'O3':
        unit_list = 'ppb'
    else:
        unit_list = '$ug/m^3$'
        
    da = df_com.dropna(subset=['Location Setting'])
    
    for version in versions:
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
        d = da.loc[mask]
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
                    dates = pd.date_range(start='3/1/2009',end='5/31/2009')

                    
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
    
            data.append(list(db[species+'_mod'].dropna()))
            data1.append(list(db[species+'_obs'].dropna()))
            names.append(version)
            
    # Plotting section
    fig = plt.figure(figsize=(8,8))
    fig.tight_layout()
    label = 20
    if species == 'O3':
        fig.suptitle('Summer 8-Hour Max Average Ozone ',ha='center') # title
        fig.text(0.03, 0.5, 'Ozone (ppb)', va='center', rotation='vertical')
    else:
        fig.suptitle('Summer Daily Average PM2.5',ha='center') # title        
        fig.text(0, 0.5, '$PM_{2.5} (ug/m^3)$', va='center', rotation='vertical')
    sites = len(data)
    
    ax = fig.add_subplot(2,1,1)
    ax.set_title('Modeled',fontsize = label)

    ax.boxplot(data)
    plt.xticks([],[])
    plt.grid(True,alpha=0.7,axis='y')
    #ax.set_ylabel(species+' '+'('+unit_list+')') 
    
    ax = fig.add_subplot(2,1,2)
    ax.set_title('Observed', fontsize = label)

    ax.boxplot(data1)
    plt.xticks([1,2,3],names)
    #ax.set_ylabel(species+' '+'('+unit_list+')') 
    plt.grid(True,alpha=0.7,axis='y')
    
    plt.show()
    plt.savefig(inputDir+'/plots/boxplot/'+species+'boxplot.png',  pad_inches=0.1, bbox_inches='tight')
    plt.close()
















