# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 14:34:44 2019

@author: Jordan Munson
"""

import pandas as pd
import datetime as dt

#import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np



base_dir = r'E:/Research/Benmap/'
plotDir = r'E:\Research\Benmap\plots\speciation/'

# =============================================================================
# # =============================================================================
# # Unfortunately, PM10 speciation, only has 'PM10 Total 0-10um STP' for the PNW....
# # =============================================================================
# df_2010 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_PM10_speciation_2010.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
# df_2010['Year'] = '2010'
# df_2011 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_PM10_speciation_2011.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
# df_2011['Year'] = '2011'
# df_2012 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_PM10_speciation_2012.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
# df_2012['Year'] = '2012'
# df_2013 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_PM10_speciation_2013.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
# df_2013['Year'] = '2013'
# df_2014 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_PM10_speciation_2014.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
# df_2014['Year'] = '2014'
# df_2015 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_PM10_speciation_2015.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
# df_2015['Year'] = '2015'
# df_2016 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_PM10_speciation_2016.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
# df_2016['Year'] = '2016'
# df_2017 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_PM10_speciation_2017.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
# df_2017['Year'] = '2017'
# df_2018 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_PM10_speciation_2018.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
# df_2018['Year'] = '2018'
# 
# df_list = [df_2010,df_2011,df_2012,df_2013,df_2014,df_2015,df_2016,df_2017,df_2018]
# 
# df_pm10 = pd.concat(df_list)
# 
# df_wa = df_pm10.loc[df_pm10['State Code'].astype(str)=='53', df_pm10.columns] # selects only washington
# df_or = df_pm10.loc[df_pm10['State Code'].astype(str)=='41', df_pm10.columns] # selects only washington
# df_id = df_pm10.loc[df_pm10['State Code'].astype(str)=='16', df_pm10.columns] # selects only washington
# 
# df_pm10 = pd.concat([df_wa,df_or,df_id])
# 
# # Formate the date
# df_pm10['Date GMT'] = df_pm10['Date GMT']+' '+df_pm10['Time GMT']
# df_pm10 = df_pm10.drop(['Time GMT'],axis='columns')
# df_pm10['Date GMT'] = pd.to_datetime(df_pm10['Date GMT'])
# df_pm10["Date GMT"] = df_pm10["Date GMT"].apply(lambda x: x - dt.timedelta(hours=8)) #Adjust to PST
# 
# print(df_wa['Parameter Name'].unique())
# print(df_or['Parameter Name'].unique())
# print(df_id['Parameter Name'].unique())
# =============================================================================


#%%
# =============================================================================
# pm2.5 speciation
# =============================================================================
df_2010 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_pm2.5_speciation_2010.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
df_2010['Year'] = '2010'
df_2011 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_pm2.5_speciation_2011.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
df_2011['Year'] = '2011'
df_2012 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_pm2.5_speciation_2012.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
df_2012['Year'] = '2012'
df_2013 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_pm2.5_speciation_2013.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
df_2013['Year'] = '2013'
df_2014 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_pm2.5_speciation_2014.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
df_2014['Year'] = '2014'
df_2015 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_pm2.5_speciation_2015.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
df_2015['Year'] = '2015'
df_2016 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_pm2.5_speciation_2016.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
df_2016['Year'] = '2016'
df_2017 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_pm2.5_speciation_2017.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
df_2017['Year'] = '2017'
df_2018 = pd.read_csv(base_dir+'AQS_data/speciation/aqs_pm2.5_speciation_2018.csv').drop(['Unnamed: 0','Unnamed: 1'],axis=1)
df_2018['Year'] = '2018'

df_list = [df_2010,df_2011,df_2012,df_2013,df_2014,df_2015,df_2016,df_2017,df_2018]

df_pm25 = pd.concat(df_list)

df_wa = df_pm25.loc[df_pm25['State Code'].astype(str)=='53', df_pm25.columns] # selects only washington
df_or = df_pm25.loc[df_pm25['State Code'].astype(str)=='41', df_pm25.columns] # selects only washington
df_id = df_pm25.loc[df_pm25['State Code'].astype(str)=='16', df_pm25.columns] # selects only washington

df_pm25 = pd.concat([df_wa,df_or,df_id])

# Formate the date
df_pm25['Date GMT'] = df_pm25['Date GMT']+' '+df_pm25['Time GMT']
df_pm25 = df_pm25.drop(['Time GMT'],axis='columns')
df_pm25['Date GMT'] = pd.to_datetime(df_pm25['Date GMT'])
df_pm25["Date GMT"] = df_pm25["Date GMT"].apply(lambda x: x - dt.timedelta(hours=8)) #Adjust to PST

print(df_wa['Parameter Name'].unique())
print(df_or['Parameter Name'].unique())
print(df_id['Parameter Name'].unique())

#%%
# =============================================================================
# Plotting
# =============================================================================
# Barplot
functions = ['Black Carbon PM2.5 at 880 nm', 'UV Carbon PM2.5 at 370 nm']
years = ['2010','2011','2012','2013','2014','2015','2016','2017','2018']
fig = plt.figure(figsize=(7.5,6),dpi=100)
ax = fig.add_subplot(1,1,1)
for function in functions:
    da = pd.DataFrame(columns = ['State Code',
 'County Code',
 'Site Num',
 'Latitude',
 'Longitude',
 'Parameter Name',
 'Date GMT',
 'Sample Measurement',
 'Units of Measure',
 'State Name',
 'County Name',
 'Year'])
    
    
    for year in years:
        for counties in ['Grant', 'Klamath', 'Multnomah', 'Jackson', 'Washington', 'Union']:
        # select data
            d = df_pm25.copy()
    
            d['Parameter Name'] = d['Parameter Name'].astype(str)
            d = d.loc[d['Parameter Name'] == function]
            d = d.loc[d['County Name'] == counties]
            d = d.loc[d['Year'] == year]

            
            # Calculate yearly averages
            d = d.set_index('Date GMT').drop(['Latitude','Longitude'],axis=1)
            d = d.resample('Y', how = 'mean')
            
            da = pd.concat([da,d])
            #d = d.sort_values(by='Sample Measurement', ascending=False).reset_index(drop=True) # Sort by DEQ for consistency
            try:
                ymax = max(d['Sample Measurement'])
            except ValueError:
                continue
            
    labels = years
    da = da.resample('Y', how = 'mean')
    x = np.arange(len(da['Sample Measurement']))  # the label locations
    width = 0.35  # the width of the bars
    
    if function == 'Black Carbon PM2.5 at 880 nm':
        
        rects1 = ax.bar(x+ width/2, da['Sample Measurement'], width, label='Black Carbon')

        ax.set_title('AQS Speciation')
    else:      
        print(function)
        rects2 = ax.bar(x- width/2, da['Sample Measurement'], width, label='UV Carbon')
        ax.legend()
        ax.set_ylim(0, 1.7)
        ax.set_ylabel('PM$_{2.5}$ \u03BCg m$^{-3}$')

        plt.xticks(x, labels, rotation='vertical')

    ax.tick_params(axis='x', which='both', length=0)

#fig.tight_layout()
function_save = function.replace(" ", "_")
plt.savefig(plotDir + 'barplots/_'+function_save+'_barplot.png')
plt.show()