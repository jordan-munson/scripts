# -*- coding: utf-8 -*-
"""
Created on Tue May 14 14:52:58 2019

@author: Jordan Munson
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

inputDir = r'C:/Users/riptu/Documents/My BenMAP-CE Files/Result/APVR/AIRPACT/'
thesisDir = r'C:/Users/riptu/Documents/My BenMAP-CE Files/Result/APVR/thesis/'
plotDir = r'E:\Research\Benmap\plots/'
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'
exec(open(stat_path).read())


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


# Read in data
mon_2010 = pd.read_csv(inputDir + '2010_mon_csv.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
mon_2011 = pd.read_csv(inputDir + '2011_mon_csv.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
mon_2012 = pd.read_csv(inputDir + '2012_mon_csv.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
mon_2013 = pd.read_csv(inputDir + '2013_mon_csv.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
mon_2014 = pd.read_csv(inputDir + '2014_mon_csv.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
mon_2015 = pd.read_csv(inputDir + '2015_mon_csv.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
mon_2016 = pd.read_csv(inputDir + '2016_mon_csv.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
mon_2017 = pd.read_csv(inputDir + '2017_mon_csv.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
mon_2018 = pd.read_csv(inputDir + '2018_mon_csv.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)

dfs = [mon_2010,mon_2011,mon_2012,mon_2013,mon_2014,mon_2015,mon_2016,mon_2017,mon_2018]

# =============================================================================
# Fires
# =============================================================================
states = ['WA','OR','ID','MT']#,'CA']

df_fire = pd.read_csv(r'E:/Research/AIRPACT_eval/fire_data.csv')

years = [2010,2011,2012,2013,2014,2015,2016,2017,2018]
fires = pd.DataFrame(index = years, columns=['Fires']).fillna(0)
for state in states:
    # Format
    d = df_fire.loc[df_fire['State']==state]
    d = d.set_index('Year') 
    d.loc[:,'Fires'] = pd.to_numeric(d.loc[:,'Fires'], errors='coerce')/1000
    d.loc[:,'Acres'] = pd.to_numeric(d.loc[:,'Acres'], errors='coerce')/1000
    d = d.rename(columns={'Acres':state + ' Fire'}).drop(['Fires','State'],axis=1).drop([2006,2007,2008,2009])
    
    fires = pd.merge(fires,d,left_index=True,right_index=True)


#fires = pd.read_csv(r'E:/Research/AIRPACT_eval/fires.csv').set_index('Unnamed: 0').drop('State',axis=1)
#fires = fires.reset_index().rename(columns={'Unnamed: 0':'index'})
#fires1 = fires.set_index('index')
fires.index = fires.index.map(str)  # set as string so that the merge later on works

fires['Fires'] = fires['WA Fire'] + fires['OR Fire'] + fires['ID Fire']
# =============================================================================
# CA = 6
# ID = 16
# MT = 30
# NV = 32
# OR = 41
# UT = 49
# WA = 53
# WY = 56
# =============================================================================
#percent_mortality['Col'] = mon_2010['Col']
# =============================================================================
# Percent mortality longterm
# =============================================================================
# Set up combined df
percent_mortality = pd.DataFrame()
percent_mortality['state'] = ['WY','WA','UT','OR','NV','MT','ID','CA'] # Data only contains state number, this labels them

# Calculate percent mortality
percent_mortality['2010'] = mon_2010['Point Estimate']/mon_2010['Population']*100*-1
percent_mortality['2011'] = mon_2011['Point Estimate']/mon_2011['Population']*100*-1
percent_mortality['2012'] = mon_2012['Point Estimate']/mon_2012['Population']*100*-1
percent_mortality['2013'] = mon_2013['Point Estimate']/mon_2013['Population']*100*-1
percent_mortality['2014'] = mon_2014['Point Estimate']/mon_2014['Population']*100*-1
percent_mortality['2015'] = mon_2015['Point Estimate']/mon_2015['Population']*100*-1
percent_mortality['2016'] = mon_2016['Point Estimate']/mon_2016['Population']*100*-1
percent_mortality['2017'] = mon_2017['Point Estimate']/mon_2017['Population']*100*-1
percent_mortality['2018'] = mon_2018['Point Estimate']/mon_2018['Population']*100*-1
percent_mortality=percent_mortality.set_index('state',drop=True).T.drop(['WY','UT','MT','NV','CA'],axis=1)

percent_mortality['Total'] = percent_mortality['WA'] + percent_mortality['OR'] + percent_mortality['ID']

#fires = pd.merge(percent_mortality,fires, left_index=True, right_index=True) # merge fires and mortality
legend_x = 1.1
# Begin plotting
# Plotting section
fig = plt.figure(figsize=(7.5,7),dpi=100)
fig.suptitle('Longterm PM$_{2.5}$ Mortality',y=0.95,fontsize=18,ha='center') # title
fig.tight_layout() # spaces the plots out a bit

ax = fig.add_subplot(2,1,1)
percent_mortality.plot(y=['WA','OR','ID'],ax=ax)
#ax.set_ylim(.1,.2)
#ax.set_xlabel('Year')
ax.set_ylabel('% Mortality')
#ax.set_title('Percent Mortality')
ax.legend(loc='center left', bbox_to_anchor=(legend_x, 0.9)).remove() # Places legend outside of plot to the right
fire_max = 3000
# =============================================================================
# # second axis for fire
# 
# ax2 = ax.twinx()
# fires.plot(y=['WA Fire','OR Fire','ID Fire'],ax=ax2,linestyle=':')
# # =============================================================================
# # fires.plot(y=['Fires'],ax=ax2,linestyle=':',color = 'black')
# # =============================================================================
# ax2.fill_between(fires.index,0,fires.Fires,alpha = 0.05, color='black')
# ax2.set_ylabel('Acres Burned/1000')
# ax2.set_ylim(0,fire_max)
# ax2.legend(loc='center left', bbox_to_anchor=(legend_x, 0.1)) # Places legend outside of plot to the right
# =============================================================================


# Verticle lines at significatn wildfire years
ax.axvline(x=2,color='black',linewidth=0.5)
ax.axvline(x=5,color='black',linewidth=0.5)
ax.axvline(x=7,color='black',linewidth=0.5)

# =============================================================================
# straight mortality longterm
# =============================================================================
mortality = pd.DataFrame()
mortality['state'] = ['WY','WA','UT','OR','NV','MT','ID','CA'] # Data only contains state number, this labels them
# Make point estimate positive for an easier to understand plot
mortality['2010'] = mon_2010['Point Estimate']*-1
mortality['2011'] = mon_2011['Point Estimate']*-1
mortality['2012'] = mon_2012['Point Estimate']*-1
mortality['2013'] = mon_2013['Point Estimate']*-1
mortality['2014'] = mon_2014['Point Estimate']*-1
mortality['2015'] = mon_2015['Point Estimate']*-1
mortality['2016'] = mon_2016['Point Estimate']*-1
mortality['2017'] = mon_2017['Point Estimate']*-1
mortality['2018'] = mon_2018['Point Estimate']*-1
mortality=mortality.set_index('state',drop=True).T.drop(['WY','UT','MT','NV','CA'],axis=1)

# =============================================================================
# # add fires
# mortality = mortality.reset_index()
# #fires['index'] = fires['index'].astype(str)
# #mortality = pd.merge(mortality,fires).set_index('index').drop('Fires',axis=1)
# 
# ax = fig.add_subplot(2,1,2)
# mortality.plot(y=['WA','OR','ID'],ax=ax)
# ax.set_xlabel('Year')
# ax.set_ylabel('# of Deaths')
# #ax.set_title('Mortality')
# 
# # second axis for fire
# ax2 = ax.twinx()
# =============================================================================
ax = fig.add_subplot(2,1,2)
ax.set_xlabel('Year')
fires.plot(y=['WA Fire','OR Fire','ID Fire'],ax=ax,label=['WA','OR','ID'])
fires.plot(y=['Fires'],ax=ax,linestyle=':',color = 'black',label=['Total'])
ax.fill_between(fires.index,0,fires.Fires,alpha = 0.05, color='black')
ax.set_ylabel('Acres Burned/1000')
ax.set_ylim(0,fire_max)
ax.legend(loc='center left', bbox_to_anchor=(legend_x, 0.1)).remove() # Places legend outside of plot to the right

ax.legend(loc='center left', bbox_to_anchor=(legend_x, 0.9)) # Places legend outside of plot to the right


# Verticle lines at significatn wildfire years
ax.axvline(x=2,color='black',linewidth=0.5)
ax.axvline(x=5,color='black',linewidth=0.5)
ax.axvline(x=7,color='black',linewidth=0.5)
plt.show()
plt.close()
#%%

years = [2010,2011,2012,2013,2014,2015,2016,2017,2018]
pop = pd.DataFrame()
for df,year in zip(dfs,years):
    
    pop[str(year)] = df['Population']

#%%
# =============================================================================
#  AQI section for plotting good, moderate, etc...
# =============================================================================
    # Load in BenMAP projections
pm_good = pd.read_csv(inputDir + 'aqi_good_pm.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
pm_moderate = pd.read_csv(inputDir + 'aqi_moderate_pm.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
pm_usg = pd.read_csv(inputDir + 'aqi_usg_pm.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
pm_unhealthy = pd.read_csv(inputDir + 'aqi_unhealthy_pm.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
pm_very_unhealthy = pd.read_csv(inputDir + 'aqi_very_unhealthy_pm.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)
pm_hazardous = pd.read_csv(inputDir + 'aqi_haz_pm.CSV').sort_values(by='Col', ascending=False).reset_index(drop=True)

# Create dataframe to combine to
df_aqi = pd.DataFrame()
df_aqi['state'] = ['WY','WA','UT','OR','NV','MT','ID','CA'] # Data only contains state number, this labels them

# Load point data into dataframe
df_aqi['Good'] = pm_good['Point Estimate']/pm_good['Population']*100*-1
df_aqi['Moderate'] = pm_moderate['Point Estimate']/pm_good['Population']*100*-1
df_aqi['USG'] = pm_usg['Point Estimate']/pm_good['Population']*100*-1
df_aqi['Unhealthy'] = pm_unhealthy['Point Estimate']/pm_good['Population']*100*-1
df_aqi['VU'] = pm_very_unhealthy['Point Estimate']/pm_good['Population']*100*-1
df_aqi['Hazardous'] = pm_hazardous['Point Estimate']/pm_good['Population']*100*-1
df_aqi['Population'] = pm_hazardous['Population']/pm_good['Population']*100*-1

df_aqi = df_aqi.drop([0,2,4,5,7]).drop(['Population'],axis=1).reset_index(drop=True).set_index('state').T


ax=df_aqi.plot()
ax.set_xlabel('AQI')
ax.set_ylabel('Percent of Population (%)')
ax.set_title('Mortality due to PM$_{2.5}$')
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5)) # Places legend outside of plot to the right
ax.set_ylim(0,3)

#%%

# =============================================================================
# Model - these are done at a county level
# =============================================================================

siteid = pd.read_csv(r'E:\Research\AIRPACT_eval\aqs_sites/aqs_sites.csv').drop(['Site Number', 'Land Use','Location Setting', 'Latitude','Longitude',
 'Datum',
 'Elevation',
 'Site Established Date',
 'Site Closed Date',
 'Met Site State Code',
 'Met Site County Code',
 'Met Site Site Number',
 'Met Site Type',
 'Met Site Distance',
 'Met Site Direction',
 'GMT Offset',
 'Owning Agency',
 'Local Site Name',
 'Address',
 'Zip Code',
 'City Name',
 'CBSA Name',
 'Tribe Name',
 'Extraction Date'],axis=1)

drop_list = [ #'Delta',
 'Mean',
 'Baseline',
 'Percent Of Baseline',
 'Standard Deviation',
 'Variance',
 'Percentile 2.5',
 'Percentile 7.5',
 'Percentile 12.5',
 'Percentile 17.5',
 'Percentile 22.5',
 'Percentile 27.5',
 'Percentile 32.5',
 'Percentile 37.5',
 'Percentile 42.5',
 'Percentile 47.5',
 'Percentile 52.5',
 'Percentile 57.5',
 'Percentile 62.5',
 'Percentile 67.5',
 'Percentile 72.5',
 'Percentile 77.5',
 'Percentile 82.5',
 'Percentile 87.5',
 'Percentile 92.5',
 'Percentile 97.5', 'Start Age','Author','Endpoint Group','End Age','Version','Endpoint']
    
# Create a dataframe of state/county codes
siteid_1 = siteid[siteid['State Code'] == '53'].drop_duplicates(['County Code'])
siteid_2 = siteid[siteid['State Code'] == '41'].drop_duplicates(['County Code'])
siteid_3 = siteid[siteid['State Code'] == '16'].drop_duplicates(['County Code'])

siteid = pd.concat((siteid_1,siteid_2))
siteid = pd.concat((siteid,siteid_3))
siteid = siteid.rename(columns={"State Code": "Col", "County Code": "Row"})
siteid['Col'] = pd.to_numeric(siteid['Col'])



# =============================================================================
# # Load BenMAP data
# mon_2016 = pd.merge(pd.read_csv(inputDir + '2016_mon_csv_county.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Monitor",'Delta':'Delta_Monitor'})
# mon_2016['Year'] = 2016
# mon_2017 = pd.merge(pd.read_csv(inputDir + '2017_mon_csv_county.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Monitor",'Delta':'Delta_Monitor'})
# mon_2017['Year'] = 2017
# mon_2018 = pd.merge(pd.read_csv(inputDir + '2018_mon_csv_county.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Monitor",'Delta':'Delta_Monitor'})
# mon_2018['Year'] = 2018
# 
# model_2016 = pd.merge(pd.read_csv(inputDir + '2016_model_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})
# model_2016['Year'] = 2016
# model_2017 = pd.merge(pd.read_csv(inputDir + '2017_model_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})
# model_2017['Year'] = 2017
# model_2018 = pd.merge(pd.read_csv(inputDir + '2018_model_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})
# model_2018['Year'] = 2018
# 
# # Load Zanobetti health results
# # Load BenMAP data
# zanobetti_2016 = pd.merge(pd.read_csv(inputDir + '2016_zanobetti_CSV.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Monitor",'Delta':'Delta_Model'})
# zanobetti_2016['Year'] = 2016
# zanobetti_2017 = pd.merge(pd.read_csv(inputDir + '2017_zanobetti_CSV.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Monitor",'Delta':'Delta_Model'})
# zanobetti_2017['Year'] = 2017
# zanobetti_2018 = pd.merge(pd.read_csv(inputDir + '2018_zanobetti_CSV.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Monitor",'Delta':'Delta_Model'})
# zanobetti_2018['Year'] = 2018
# 
# =============================================================================
# =============================================================================
# The section below loads data in a manner that does not leave out certain counties. The above method would be needed to identify counties for a table
# =============================================================================
# Load BenMAP data
mon_2016 = pd.merge(pd.read_csv(inputDir + '2016_mon_csv_county.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col'],how='outer').rename(columns={"Point Estimate": "Monitor",'Delta':'Delta_Monitor'})
mon_2016['Year'] = 2016
mon_2017 = pd.merge(pd.read_csv(inputDir + '2017_mon_csv_county.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col'],how='outer').rename(columns={"Point Estimate": "Monitor",'Delta':'Delta_Monitor'})
mon_2017['Year'] = 2017
mon_2018 = pd.merge(pd.read_csv(inputDir + '2018_mon_csv_county.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col'],how='outer').rename(columns={"Point Estimate": "Monitor",'Delta':'Delta_Monitor'})
mon_2018['Year'] = 2018

model_2016 = pd.merge(pd.read_csv(inputDir + '2016_model_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col'],how='outer').rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})
model_2016['Year'] = 2016
model_2017 = pd.merge(pd.read_csv(inputDir + '2017_model_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col'],how='outer').rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})
model_2017['Year'] = 2017
model_2018 = pd.merge(pd.read_csv(inputDir + '2018_model_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col'],how='outer').rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})
model_2018['Year'] = 2018

# Load Zanobetti health results
# Load BenMAP data
zanobetti_2016 = pd.merge(pd.read_csv(inputDir + '2016_zanobetti_CSV.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col'],how='outer').rename(columns={"Point Estimate": "Monitor",'Delta':'Delta_Model'})
zanobetti_2016['Year'] = 2016
zanobetti_2017 = pd.merge(pd.read_csv(inputDir + '2017_zanobetti_CSV.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col'],how='outer').rename(columns={"Point Estimate": "Monitor",'Delta':'Delta_Model'})
zanobetti_2017['Year'] = 2017
zanobetti_2018 = pd.merge(pd.read_csv(inputDir + '2018_zanobetti_CSV.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col'],how='outer').rename(columns={"Point Estimate": "Monitor",'Delta':'Delta_Model'})
zanobetti_2018['Year'] = 2018






# Combine information
df_com = pd.concat([mon_2016,mon_2017,mon_2018])#.drop(['Row','Col'],axis=1)
df_com1 = pd.concat([model_2016,model_2017,model_2018]).drop(['Row','Col'],axis=1)
df_com = pd.merge(df_com,df_com1,on=['State Name','County Name','Year','Population'])

df_z = pd.concat([zanobetti_2016,zanobetti_2017,zanobetti_2018])#.drop(['Row','Col'],axis=1)
# =============================================================================
# df_com = pd.merge(df_com,mon_2018)
# df_com1 = pd.merge(model_2017,model_2018)
# df_com = pd.merge(df_com,df_com1)
# 
# 
# 
# 
# df_com = pd.DataFrame()
# 
# df_com['County'] = mon_2016['County Name']
# 
# 
# df_com['2016_mon'] = mon_2016['2016_mon']
# df_com['2017_mon'] = mon_2017['2017_mon']
# df_com['2018_mon'] = mon_2018['2018_mon']
# #df_com['2016_mod'] = model_2016['2016_mod']
# df_com['2017_mod'] = model_2017['2017_mod']
# df_com['2018_mod'] = model_2018['2018_mod']
# 
# =============================================================================
df_com['Year'] = df_com['Year'].astype(str)

df_table = df_com.copy()
df_com = df_com.set_index('County Name')#.T

df_z['Year'] = df_z['Year'].astype(str)
df_z = df_z.set_index('County Name')#.T
# =============================================================================
# ax=df_com.plot(y = ['Model','Monitor'])
# ax=df_com.plot(y = ['Monitor'])
# ax=df_com.plot(y = ['Model'])
# =============================================================================
# =============================================================================
# ax.set_xlabel('AQI')
# ax.set_ylabel('Percent of Population (%)')
# ax.set_title('Mortality due to $PM_{2.5}$')
# ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5)) # Places legend outside of plot to the right
# ax.set_ylim(0,3)
# =============================================================================




# =============================================================================
# Plot county map use geopandas
# =============================================================================

# load in shapefiles
counties = gpd.read_file(r'E:\Research\Benmap\benmap_shapefile_output/Krewski.shp')
counties = counties.rename(columns={"COL": "Col",'ROW':'Row'})
states = gpd.read_file(r'E:\Research\Benmap\benmap_shapefile_output/state/state.shp')
states = states.rename(columns={"COL": "Col",'ROW':'Row'})
states['zeros'] = 0

df_counties = pd.merge(df_com,counties) # Merging eliminates the rest of the country
df_z = pd.merge(df_z,counties) # Merging eliminates the rest of the country

df_states = pd.merge(df_com,states)
#df_counties = df_counties.loc[df_counties['Year'] == '2016']
df_counties = gpd.GeoDataFrame(df_counties) # needs to be a GeoDataframe
df_z = gpd.GeoDataFrame(df_z)

df_states = gpd.GeoDataFrame(df_states)
df_states['Col'] = df_states['Col'].drop_duplicates()
df_states = df_states.dropna()

# Plotting section
fig = plt.figure(dpi=100,figsize=(7.5,7))
fig.suptitle('PNW PM$_{2.5}$ Mortality',y=0.94,fontsize=12,ha='center') # title
fig.tight_layout() # spaces the plots out a bit
fig.text(0.06, 0.5, 'Latitude', va='center', rotation='vertical')
fig.text(0.5, 0.09, 'Longitude', va='center',ha = 'center')

# Plot settings
cmap = 'OrRd'
edgecolor = 'k'
vmax = 250
vmin = 0

# =============================================================================
# # Colorbar setup - geopandas doesnt support colorbar changing stuff really. Am just adding colorbar in the presentation instead, not through python
# =============================================================================
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.2) # depends on the user needs
alpha = 0.5

# Add subplots
ax = fig.add_subplot(3,3,7)
plt.title('2018 Monitor')
im = df_counties.loc[df_counties['Year'] == '2018'].plot(column='Monitor', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

ax = fig.add_subplot(3,3,4)
plt.title('2017 Monitor')
im = df_counties.loc[df_counties['Year'] == '2017'].plot(column='Monitor', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
im.axes.get_xaxis().set_visible(False)
states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

ax = fig.add_subplot(3,3,1)
plt.title('2016 Monitor')
im = df_counties.loc[df_counties['Year'] == '2016'].plot(column='Monitor', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
im.axes.get_xaxis().set_visible(False)
states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

ax = fig.add_subplot(3,3,8)
plt.title('2018 Model')
im = df_counties.loc[df_counties['Year'] == '2018'].plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
im.axes.get_yaxis().set_visible(False)
states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

ax = fig.add_subplot(3,3,5)
plt.title('2017 Model')
im = df_counties.loc[df_counties['Year'] == '2017'].plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
im.axes.get_yaxis().set_visible(False)
im.axes.get_xaxis().set_visible(False)
states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

ax = fig.add_subplot(3,3,2)
plt.title('2016 Model')
im = df_counties.loc[df_counties['Year'] == '2016'].plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
im.axes.get_yaxis().set_visible(False)
im.axes.get_xaxis().set_visible(False)
states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
# =============================================================================
# Zanobetti portion
# =============================================================================
ax = fig.add_subplot(3,3,9)
plt.title('2018 Zanobetti')
im = df_z.loc[df_z['Year'] == '2018'].plot(column='Monitor', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
im.axes.get_yaxis().set_visible(False)
states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

ax = fig.add_subplot(3,3,6)
plt.title('2017 Zanobetti')
im = df_z.loc[df_z['Year'] == '2017'].plot(column='Monitor', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
im.axes.get_yaxis().set_visible(False)
im.axes.get_xaxis().set_visible(False)
states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

ax = fig.add_subplot(3,3,3)
plt.title('2016 Zanobetti')
im = df_z.loc[df_z['Year'] == '2016'].plot(column='Monitor', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
im.axes.get_yaxis().set_visible(False)
im.axes.get_xaxis().set_visible(False)
states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
plt.show()
plt.close()



highest_county_mort = pd.merge(df_counties.loc[df_counties['Year']=='2017'].sort_values(by='Monitor', ascending=False).head(),siteid)
highest_county_mort_z = pd.merge(df_z.loc[df_z['Year']=='2017'].sort_values(by='Monitor', ascending=False).head(),siteid)

#%%
# =============================================================================
# # Plotting section for model vs monitor
# =============================================================================
fig = plt.figure(figsize=(7.5,7),dpi=100)
fig.suptitle('Mortality in the PNW due to PM$_{2.5}$',y=0.97,fontsize=20,ha='center') # title
fig.tight_layout() # spaces the plots out a bit
fig.text(0.06, 0.5, 'Latitude', va='center', rotation='vertical')
fig.text(0.5, 0.09, 'Longitude', va='center', ha = 'center')
fig.text(0.30, 0.92, 'Monitor', va='center', ha = 'center',fontsize=18)
fig.text(0.72, 0.92, 'Model', va='center', ha = 'center',fontsize=18)

# Colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.2) # depends on the user needs
alpha = 0.7

endpoints = ['2016','2017','2018'] # sets the endpoints we are looking at

vmax = 250
vmin = 0
# Add subplots
for endpoint, i, j in zip(endpoints,[1,3,5],[2,4,6]):
         
    ax = fig.add_subplot(3,2,i)
    plt.title(endpoint)
    im = df_counties.loc[df_counties['Year'] == endpoint].plot(column='Monitor', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
    states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

    ax = fig.add_subplot(3,2,j)
    plt.title(endpoint)
    im = df_counties.loc[df_counties['Year'] == endpoint].plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
    states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

plt.show()
plt.close()
#%%
# =============================================================================
# # Plotting section for model vs monitor
# =============================================================================
fig = plt.figure(figsize=(7.5,7),dpi=100)
fig.suptitle('PM$_{2.5}$ in the PNW',y=0.97,fontsize=20,ha='center') # title
fig.tight_layout() # spaces the plots out a bit
fig.text(0.06, 0.5, 'Latitude', va='center', rotation='vertical')
fig.text(0.5, 0.09, 'Longitude', va='center', ha = 'center')
fig.text(0.30, 0.92, 'Monitor', va='center', ha = 'center',fontsize=18)
fig.text(0.72, 0.92, 'AP-5', va='center', ha = 'center',fontsize=18)

# Colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.2) # depends on the user needs
alpha = 0.7

endpoints = ['2016','2017','2018'] # sets the endpoints we are looking at

vmax = 12
vmin = 0
# Add subplots
for endpoint, i, j in zip(endpoints,[1,3,5],[2,4,6]):
         
    ax = fig.add_subplot(3,2,i)
    plt.title(endpoint)
    im = df_counties.loc[df_counties['Year'] == endpoint].plot(column='Delta_Monitor', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
    states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

    ax = fig.add_subplot(3,2,j)
    plt.title(endpoint)
    im = df_counties.loc[df_counties['Year'] == endpoint].plot(column='Delta_Model', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
    states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

plt.show()
plt.close()
#%%
# =============================================================================
# 
# # =============================================================================
# # Testing to put monitor plots in the same figure
# # =============================================================================
# 
# fig = plt.figure(figsize=(10,9),dpi=50)
# fig.suptitle('Mortality in the PNW due to PM$_{2.5}$',y=0.97,fontsize=20,ha='center') # title
# fig.tight_layout() # spaces the plots out a bit
# fig.text(0.06, 0.5, 'Latitude', va='center', rotation='vertical')
# fig.text(0.5, 0.09, 'Longitude', va='center', ha = 'center')
# fig.text(0.30, 0.92, 'Monitor', va='center', ha = 'center',fontsize=18)
# fig.text(0.72, 0.92, 'Model', va='center', ha = 'center',fontsize=18)
# 
# for endpoint, i, j, k, z in zip(endpoints,[1,5,9],[2,6,10],[3,7,11],[4,8,12]):
#          
#     ax = fig.add_subplot(3,4,i)
#     plt.title(endpoint)
#     im = df_counties.loc[df_counties['Year'] == endpoint].plot(column='Monitor', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
#     states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
# 
#     ax = fig.add_subplot(3,4,j)
#     plt.title(endpoint)
#     im = df_counties.loc[df_counties['Year'] == endpoint].plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
#     states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
#     
#     vmax = 10
#     ax = fig.add_subplot(3,4,k)
#     plt.title('endpoint')
#     im = df_counties.loc[df_counties['Year'] == endpoint].plot(column='Delta_Monitor', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
#     states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
#     
#     ax = fig.add_subplot(3,4,z)
#     plt.title('endpoint')
#     im = df_counties.loc[df_counties['Year'] == endpoint].plot(column='Delta_Model', cmap=cmap, edgecolor=edgecolor, legend=False,ax=ax,vmin=vmin,vmax=vmax)
#     states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
# 
# plt.show()
# plt.close()
# =============================================================================
#%%
# =============================================================================
# Plot combined results (PM, Ozone, variety of health functions)
# =============================================================================

# set list of columns to drop
drop_list = [ #'Delta',
 'Mean',
 'Baseline',
 'Percent of Baseline',
 'Standard Deviation',
 'Variance',
 'Percentile 2.5',
 'Percentile 7.5',
 'Percentile 12.5',
 'Percentile 17.5',
 'Percentile 22.5',
 'Percentile 27.5',
 'Percentile 32.5',
 'Percentile 37.5',
 'Percentile 42.5',
 'Percentile 47.5',
 'Percentile 52.5',
 'Percentile 57.5',
 'Percentile 62.5',
 'Percentile 67.5',
 'Percentile 72.5',
 'Percentile 77.5',
 'Percentile 82.5',
 'Percentile 87.5',
 'Percentile 92.5',
 'Percentile 97.5', 'Start Age','Author','Endpoint','End Age','Version']#,'Endpoint Group']

# Load model data

# =============================================================================
# model_2018 = pd.merge(pd.read_csv(inputDir + '2018_model_PM_O3_output.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})
# monitor_2018 = pd.merge(pd.read_csv(inputDir + '2018_monitor_PM_O3_output.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})
# =============================================================================

#model_2018 = pd.merge(pd.read_csv(inputDir + '2018_model_PM_O3_output.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})
model_2018 = pd.read_csv(inputDir + '2018_model_PM_O3_output.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index().rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})

monitor_2018 = pd.merge(pd.read_csv(inputDir + '2018_monitor_PM_O3_output.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})
value_2018 = pd.merge(pd.read_csv(inputDir + '2018_model_PM_O3_output_valuation.CSV').rename(columns = {'Column':'Col'}).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})
top_valuation = pd.merge(value_2018.loc[value_2018['Pollutant'] == 'PM2.5'].loc[value_2018['Endpoint'] == 'Mortality, All Cause'].sort_values(by='Model', ascending=False).head(),siteid)


df_mod = pd.merge(model_2018,counties) # Merging eliminates the rest of the country
df_mod = gpd.GeoDataFrame(df_mod) # needs to be a GeoDataframe
df_mod['Pollutant'] = df_mod['Pollutant'].replace('PM2.5 ','PM2.5') # Asthma Exacerbation for some reason had a tailing space at the end... this removes that
df_mod['Endpoint Group'] = df_mod['Endpoint Group'].replace('Emergency Room Visits  Respiratory','Emergency Room Visits') # Asthma Exacerbation for some reason had a tailing space at the end... this removes that


df_mon = pd.merge(monitor_2018,counties) # Merging eliminates the rest of the country
df_mon = gpd.GeoDataFrame(df_mon) # needs to be a GeoDataframe

# Plotting section
fig = plt.figure(figsize=(10,12))#dpi=100)
fig.suptitle('2018 PNW AQ Health Impacts',y=0.93,fontsize=20,ha='center') # title
fig.tight_layout() # spaces the plots out a bit
fig.text(0.06, 0.75, 'Latitude', va='center', rotation='vertical')
fig.text(0.5, 0.09, 'Longitude', va='center', ha = 'center')
fig.text(0.265, 0.9, 'PM$_{2.5}$', va='center', ha = 'center',fontsize=18)
fig.text(0.685, 0.9, 'Ozone', va='center', ha = 'center',fontsize=18)

# Colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.2) # depends on the user needs
alpha = 0.7

endpoints = ['Mortality', 'Asthma Exacerbation', 'Work Loss Days', 'Emergency Room Visits'] # sets the endpoints we are looking at


# Add subplots
for endpoint, i, j in zip(endpoints,[1,3,5,7],[2,4,6,8]):
    
    # Set colorbar max/mins
    if i == 1: # mortality
        vmax = 250
        vmin = 0
    if i == 3: # Asthma
        vmax = 10000
        vmin = 0
    if i == 5: # Work Loss Days
        vmax = 3000
        vmin = 0
    if i ==7: # Emergency room visits
        vmax = 50
        vmin = 0
         
    ax = fig.add_subplot(4,2,i)
    plt.title(endpoint)
    im = df_mod.loc[df_mod['Endpoint Group'] == endpoint].loc[df_mod['Pollutant'] == 'PM2.5'].plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
    states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

    # Set colorbar max/mins
    if i == 1: # mortality
        vmax = 60
        vmin = 0
    if i == 3: # Asthma
        vmax = 10000
        vmin = 0
    if i == 5: # School Loss Days
        endpoint = 'School Loss Days'
        vmax = 50000
        vmin = 0
    if i ==7: # Emergency room visits
        vmax = 50
        vmin = 0

    ax = fig.add_subplot(4,2,j)
    plt.title(endpoint)
    im = df_mod.loc[df_mod['Endpoint Group'] == endpoint].loc[df_mod['Pollutant'] == 'Ozone'].plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
    states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

plt.show()
plt.close()


#%%
# =============================================================================
# Percent incidence map
# =============================================================================

# Plotting section
fig = plt.figure(figsize=(7.5,10))#dpi=100)
fig.suptitle('2018 PNW PM$_{2.5}$ Health Impacts',y=1.02,fontsize=20,ha='center') # title
fig.tight_layout() # spaces the plots out a bit
fig.text(0.06, 0.75, 'Latitude', va='center', rotation='vertical')
fig.text(0.5, 0.09, 'Longitude', va='center', ha = 'center')
fig.text(0.225, 0.98, 'Incidence', va='center', ha = 'center',fontsize=18)
fig.text(0.715, 0.98, '% Incidence', va='center', ha = 'center',fontsize=18)

# Colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.2) # depends on the user needs
alpha = 0.7

endpoints = ['Mortality', 'Asthma Exacerbation', 'Work Loss Days', 'Emergency Room Visits'] # sets the endpoints we are looking at


# Add subplots
for endpoint, i, j in zip(endpoints,[1,3,5,7],[2,4,6,8]):
    
    # Set colorbar max/mins
    if i == 1: # mortality
        vmax = 250
        vmin = 0
    if i == 3: # Asthma
        vmax = 6000
        vmin = 0
    if i == 5: # Work Loss Days
        vmax = 3000
        vmin = 0
    if i ==7: # Emergency room visits
        vmax = 50
        vmin = 0
         
    ax = fig.add_subplot(4,2,i)
    plt.title(endpoint)
    im = df_mod.loc[df_mod['Endpoint Group'] == endpoint].loc[df_mod['Pollutant'] == 'PM2.5'].plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
    states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

    # Set colorbar max/mins
    if i == 1: # mortality
        vmax = 0.1
        vmin = 0
    if i == 3: # Asthma
        vmax = 100
        vmin = 0
    if i == 5: # School Loss Days
        vmax = 10
        vmin = 0
    if i ==7: # Emergency room visits
        vmax = 0.01
        vmin = 0
    
    ax = fig.add_subplot(4,2,j)
    plt.title(endpoint)
    d = df_mod.loc[df_mod['Endpoint Group'] == endpoint].loc[df_mod['Pollutant'] == 'PM2.5']
    d['Model'] = d['Model']/d['Population']*100
    im = d.plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
    states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
fig.tight_layout() # spaces the plots out a bit
plt.show()
plt.close()
#%%
# =============================================================================
# Percent mortality map
# =============================================================================

# Plotting section
fig = plt.figure(figsize=(6,4),dpi=150)
#fig.suptitle('2018 PNW PM$_{2.5}$ Health Impacts',y=0.93,fontsize=20,ha='center') # title
#fig.text(0.06, 0.5, 'Latitude', va='center', rotation='vertical')
#fig.text(0.5, 0.09, 'Longitude', va='center', ha = 'center')
#fig.text(0.265, 0.82, 'Incidence', va='center', ha = 'center',fontsize=18)
#fig.text(0.685, 0.82, '% Incidence', va='center', ha = 'center',fontsize=18)

# Colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.2) # depends on the user needs
alpha = 0.7

endpoints = ['Mortality'] # sets the endpoints we are looking at


# Add subplots
for endpoint in endpoints:

    vmax = 250
    vmin = 0
         
    ax = fig.add_subplot(2,2,1)
    plt.title('Incidence')
    im = df_mod.loc[df_mod['Endpoint Group'] == endpoint].loc[df_mod['Pollutant'] == 'PM2.5'].plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
    states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

    vmax = .1
    
    ax = fig.add_subplot(2,2,2)
    plt.title('% Incidence')
    d = df_mod.loc[df_mod['Endpoint Group'] == endpoint].loc[df_mod['Pollutant'] == 'PM2.5']
    d['Model'] = d['Model']/d['Population']*100
    im = d.plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
    states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
plt.show()
plt.close()
#%%
# =============================================================================
# DEQ analysis section
# =============================================================================


df_deq = pd.read_csv(inputDir + 'deq_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index().rename(columns={"Point Estimate": "Model",'Delta':'Delta_Model'})

counties = counties
df_mod = pd.merge(df_deq,counties) # Merging eliminates the rest of the country
df_mod = gpd.GeoDataFrame(df_mod) # needs to be a GeoDataframe
df_mod['Pollutant'] = df_mod['Pollutant'].replace('PM2.5 ','PM2.5') # Asthma Exacerbation for some reason had a tailing space at the end... this removes that
df_mod['Endpoint Group'] = df_mod['Endpoint Group'].replace('Emergency Room Visits  Respiratory','Emergency Room Visits') # Asthma Exacerbation for some reason had a tailing space at the end... this removes that

# Plotting section
fig = plt.figure(figsize=(6,4),dpi=150)
#fig.suptitle('2018 PNW PM$_{2.5}$ Health Impacts',y=0.93,fontsize=20,ha='center') # title
fig.tight_layout() # spaces the plots out a bit
#fig.text(0.06, 0.5, 'Latitude', va='center', rotation='vertical')
#fig.text(0.5, 0.09, 'Longitude', va='center', ha = 'center')
#fig.text(0.265, 0.82, 'Incidence', va='center', ha = 'center',fontsize=18)
#fig.text(0.685, 0.82, '% Incidence', va='center', ha = 'center',fontsize=18)

# Colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.2) # depends on the user needs
alpha = 0.7
linewidth = 1
endpoints = ['Mortality'] # sets the endpoints we are looking at


# Add subplots
for endpoint in endpoints:

    vmax = 250
    vmin = 0
         
    ax = fig.add_subplot(2,2,1)
    plt.title('Mortality')
    im = df_mod.loc[df_mod['Endpoint Group'] == endpoint].loc[df_mod['Pollutant'] == 'PM2.5'].plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
    states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,linewidth=linewidth,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)

    vmax = .1
    
    ax = fig.add_subplot(2,2,2)
    plt.title('% Mortality')
    d = df_mod.loc[df_mod['Endpoint Group'] == endpoint].loc[df_mod['Pollutant'] == 'PM2.5']
    d['Model'] = d['Model']/d['Population']*100
    im = d.plot(column='Model', cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
    states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,linewidth=linewidth,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
plt.show()
plt.close()
#%%
# =============================================================================
# Create comprehensive table
# =============================================================================

# Find highest impact counties
df_deq = pd.merge(pd.read_csv(inputDir + 'deq_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "DEQ",'Delta':'pollutant_DEQ'}).drop(['Row','Col'],axis=1)
#df_deq['Year'] = '2014-2017'
# =============================================================================
# a = df_deq.drop(['Endpoint Group','State Name'],axis=1).loc[df_deq['Pollutant'] == 'Ozone'].loc[df_deq['Endpoint Group'] == endpoint].sort_values(by=['Model'], ascending=False).head()
# print(a)
# =============================================================================

# load in data
df_model_2016 = pd.merge(pd.read_csv(thesisDir + '2016_model_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "mod_2016",'Delta':'pollutant_model'})
df_model_2017 = pd.merge(pd.read_csv(thesisDir + '2017_model_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "mod_2017",'Delta':'pollutant_model'})
df_model_2018 = pd.merge(pd.read_csv(thesisDir + '2018_model_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "mod_2018",'Delta':'pollutant_model'})

df_monitor_2016 = pd.merge(pd.read_csv(thesisDir + '2016_monitor_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "mon_2016",'Delta':'pollutant_monitor'})
df_monitor_2017 = pd.merge(pd.read_csv(thesisDir + '2017_monitor_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "mon_2017",'Delta':'pollutant_monitor'})
df_monitor_2018 = pd.merge(pd.read_csv(thesisDir + '2018_monitor_csv.CSV').drop(drop_list,axis=1).sort_values(by=['Col','Row'], ascending=False).reset_index(drop=True).set_index('Col').drop([56,6,32,49,30]).reset_index(),siteid, on = ['Row','Col']).rename(columns={"Point Estimate": "mon_2018",'Delta':'pollutant_monitor'})

# Add column with year
df_model_2016['Year'] = '2016'
df_model_2017['Year'] = '2017'
df_model_2018['Year'] = '2018'
df_monitor_2016['Year'] = '2016'
df_monitor_2017['Year'] = '2017'
df_monitor_2018['Year'] = '2018'

#combine data
df_table = pd.concat([df_monitor_2016,df_monitor_2017,df_monitor_2018])#.drop(['Row','Col'],axis=1)
df_table1 = pd.concat([df_model_2016,df_model_2017,df_model_2018]).drop(['Row','Col'],axis=1)
df_table = pd.merge(df_table,df_table1,on=['State Name','County Name','Year','Population','Endpoint Group','Pollutant'],how='outer')
df_table = pd.merge(df_table,df_deq,on=['State Name','County Name','Population','Endpoint Group','Pollutant'],how='outer')
df_table['Pollutant'] = df_table['Pollutant'].replace('PM2.5 ','PM2.5') # Some have an extra space at the end for some reason..


#%%
# =============================================================================
# Plot df_table
# =============================================================================
# Barplot
functions = ['Mortality','Asthma Exacerbation','Emergency Room Visits  Respiratory','filler']
pollutants = ['PM2.5', 'Ozone']
years = ['2016','2017','2018']
inc_or_per = ['incidence']#,'percent']
for iop in inc_or_per:
    for species in pollutants:   
        for function in functions:
            
            if function == 'filler': 
                if species == 'PM2.5':
                    function = 'Work Loss Days'
                else:
                    function = 'School Loss Days'
            fig = plt.figure(figsize=(7.5,6),dpi=100)
            
            for year,i in zip(years,[1,2,3]):
                # select data
                d = df_table.copy()
                d['Endpoint Group'] = d['Endpoint Group'].astype(str)
                d = d.loc[d['Pollutant'] == species].loc[d['Endpoint Group'] == function]
                d = d.sort_values(by='DEQ', ascending=False).reset_index(drop=True) # Sort by DEQ for consistency
                ymax = max(max(d['mod_2016'].dropna()),max(d['mod_2017'].dropna()),max(d['mod_2018'].dropna()))
                if iop == 'incidence':
                    
                    d1 = d.loc[d['Year'] == year].head(20)
                    top_counties = d1['County Name'].to_list()
                    d2 = d.loc[d['Year'] == year]
                    #print(d2.sum())
                    for name in top_counties:
                        #print(name)
                        d2 = d2[d2['County Name'] != name] # this for loop eliminates the top 20
                        
                    d2 = pd.DataFrame(d2.sum()).T
                    d2['County Name'] = 'Residual' # rename, otherwise a massive combined name is here and messes up the plot
                    
                    d = d.loc[d['Year'] == year].head(20)
                    d = pd.concat([d,d2])
                    #print(d.sum())
                    
                    ymax = max(max(d['mon_2016'].dropna()),max(d['mon_2017'].dropna()),max(d['mon_2018'].dropna()),
                               max(d['mod_2016'].dropna()),max(d['mod_2017'].dropna()),max(d['mod_2018'].dropna()),
                               max(d['DEQ'].dropna()),max(d['DEQ'].dropna()),max(d['DEQ'].dropna())) # Base this on DEQ as it is high
                else:
                    d = d.loc[d['Year'] == year].head(20)
                
                labels = d['County Name']
                x = np.arange(len(d['County Name']))  # the label locations
                width = 0.35  # the width of the bars
                
                ax = fig.add_subplot(3,1,i)
                
                if iop == 'incidence':
                    rects1 = ax.bar(x - width/1.5, d['mod_'+year], width, label='Model')
                    rects2 = ax.bar(x, d['mon_'+year], width, label='Monitor')
                    rects3 = ax.bar(x + width/1.5, d['DEQ'], width, label='DEQ')
                    ax.set_ylim(0, ymax+10)
                else:
                    rects1 = ax.bar(x - width/1.5, d['mod_'+year]/d['Population']*100, width, label='Model')
                    rects2 = ax.bar(x, d['mon_'+year]/d['Population']*100, width, label='Monitor')
                    rects3 = ax.bar(x + width/1.5, d['DEQ']/d['Population']*100, width, label='DEQ')
                    ax.set_ylim(0, .07) # .13 for PM mortality, 0.07 for Ozone
                    
                
                
                #Label plot
                if i ==1:
                    ax.legend()
                    ax.set_title('2016 (a)')
                if i ==2:
                    ax.set_ylabel(species +' '+function)
                    ax.set_title('2017 (b)')
                if i ==3:
                    plt.xticks(x, labels, rotation='vertical')
                    ax.set_title('2018 (c)')
                else:
                    plt.xticks(x, '', rotation='vertical')
                ax.tick_params(axis='x', which='both', length=0)
    
            #fig.tight_layout()
            function_save = function.replace(" ", "_")
            plt.savefig(plotDir + 'barplots/'+species+'_'+function_save+'_'+iop+'_barplot.png')
            plt.show()
#%%
# =============================================================================
#         Other type of barplot
# =============================================================================
# Barplot
columns = ['County Name',
 'Endpoint Group',
 'Pollutant',
 'Population',
 'State Name',
 'Year',
 'mon_2016',
 'mon_2017',
 'mon_2018',
 'pollutant_monitor',
 'mod_2016',
 'mod_2017',
 'mod_2018',
 'pollutant_model',
 'DEQ',
 'pollutant_DEQ']
functions = ['Mortality','Asthma Exacerbation','Emergency Room Visits  Respiratory','filler']
pollutants = ['PM2.5', 'Ozone']
years = ['2016','2017','2018']
inc_or_per = ['percent']
for iop in inc_or_per:
    for species in pollutants:  
        fig = plt.figure(figsize=(7.5,6),dpi=100)
        for year,i in zip(years,[1,2,3]):
            ax = fig.add_subplot(3,1,i)
            
                    
            # select data
            d = df_table.copy()
            d['Endpoint Group'] = d['Endpoint Group'].astype(str)
            d = d.loc[d['Pollutant'] == species]
            d = d.sort_values(by='DEQ', ascending=False).reset_index(drop=True) # Sort by DEQ for consistency
            d = d.loc[d['Year'] == year]
            d = d.loc[d['County Name'] == 'King']
            labels = d['Endpoint Group'].replace('Emergency Room Visits  Respiratory', 'ER Visits, Respiratory')
            x = np.arange(len(d['County Name']))  # the label locations
            width = 0.35  # the width of the bars

            ymax = .1
                

            rects1 = ax.bar(x - width/1.5, d['mod_'+year]/d['Population']*100, width, label='Model')
            rects2 = ax.bar(x, d['mon_'+year]/d['Population']*100, width, label='Monitor')
            rects3 = ax.bar(x + width/1.5, d['DEQ']/d['Population']*100, width, label='DEQ')
            #ax.set_ylim(0, ymax) # .13 for PM mortality, 0.07 for Ozone
            
            plt.yscale('log')
            ax.set_ylim(0.001, 1000)
                
                
            #Label plot
            if i ==1:
                ax.legend()
                ax.set_title('2016 (a)')
            if i ==2:
                ax.set_ylabel('Incidence' +' [%]')
                ax.set_title('2017 (b)')
            if i ==3:
                plt.xticks(x, labels)
                ax.set_title('2018 (c)')
            else:
                plt.xticks(x, '', rotation='vertical')
            ax.tick_params(axis='x', which='both', length=0)
    
        #fig.tight_layout()
        #function_save = function.replace(" ", "_")
        plt.savefig(plotDir + 'barplots/'+species+'_'+iop+'_king_barplot.png')
        plt.show()

#%%

# Scatter plot
health_stats = pd.DataFrame(['Forecast Mean','Observatio Mean','MB','ME','FB [%]','FE [%]','NMB [%]','NME [%]','RMSE','R^2 [-]','Forecast 98th','Observation 98th'])
health_stats = health_stats.set_index(0)
for species in pollutants:  
    fig = plt.figure(figsize=(7.5,10),dpi=100)
    for function,k in zip(functions,[0,3,6,9]):
        
        if function == 'filler': 
            if species == 'PM2.5':
                function = 'Work Loss Days'
            else:
                function = 'School Loss Days'
                
        for year,i in zip(years,[1,2,3]):
            # select data
            d = df_table.copy()
            d['Endpoint Group'] = d['Endpoint Group'].astype(str)
            d = d.loc[d['Pollutant'] == species].loc[d['Endpoint Group'] == function]
            d = d.sort_values(by='DEQ', ascending=False).reset_index(drop=True) # Sort by DEQ for consistency
            d = d.loc[d['Year'] == year]#.head(20)
            
            labels = d['County Name']
            x = np.arange(len(d['County Name']))  # the label locations
            width = 0.35  # the width of the bars
            size= 25
            j = i+k
            ax = fig.add_subplot(4,3,j)
            
            d = d.dropna(subset=['DEQ','mod_'+year,'mon_'+year])
            rects1 = ax.scatter(d['DEQ'],d['mod_'+year], label='Model',s=size,alpha = 0.7)
            rects2 = ax.scatter(d['DEQ'],d['mon_'+year], label='Monitor',s=size, alpha = 0.7)
            
            # find best fit line and run stats
            z1 = np.polyfit(d['DEQ'],d['mod_'+year], 1)
            z2 = np.polyfit(d['DEQ'],d['mon_'+year], 1)
            mod_stats = stats_version(d, 'mod_'+year, 'DEQ')
            mod_stats = mod_stats.rename(columns={'mod_'+year:'Model_'+year+'_'+species+ '_'+function})
            mon_stats = stats_version(d, 'mon_'+year, 'DEQ')
            mon_stats = mon_stats.rename(columns={'mon_'+year:'Monitor_'+year+'_'+species + '_'+function})
            health_stats = pd.merge(health_stats,mon_stats, left_index=True,right_index=True)
            health_stats = pd.merge(health_stats,mod_stats, left_index=True,right_index=True)
            
            r2_mod = mod_stats['Model_'+year+'_'+species+ '_'+function][9]
            r2_mon = mon_stats['Monitor_'+year+'_'+species+ '_'+function][9]
            text_string = '\n'.join((
                r'Mod $%.2f$' % (r2_mod, ),
                r'Mon $%.2f$' % (r2_mon, )))


            # place a text box in upper right in axes coords
            ax.text(0.6, 0.25, text_string, transform=ax.transAxes,
            verticalalignment='top')#, bbox=props)

            plt.plot([-200, 20000000], [-200, 20000000], 'k-',linewidth=0.7)

            ax.set_xlim(0, max(d['mod_'+year]))
            ax.set_ylim(0, max(d['mod_'+year]))
            ax.set_aspect('equal')
            #Label plot
            if j ==1:
                ax.legend()
                ax.set_title('2016')
            if j ==2:
                ax.set_title('2017')
            if j==3:
                ax.set_title('2018')
            if j == 11:
                ax.set_xlabel('DEQ')
                
            if i ==1:                
                ax.set_ylabel(function)

            #else:
                #plt.xticks(x, '', rotation='vertical')
            #ax.tick_params(axis='x', which='both', length=0)

    fig.tight_layout()
    function_save = function.replace(" ", "_")
    plt.savefig(plotDir + 'scatter/'+species+'_scatter.png')
    plt.show()
health_stats = health_stats.T
health_stats = health_stats.drop(['Observation 98th','Forecast 98th','NMB [%]','NME [%]'],axis=1)
#%%
# Print total values
years = ['2016','2017','2018']
metrics= ['mod_2016','mod_2017','mod_2018','mon_2016','mon_2017','mon_2018','DEQ']
for species in pollutants:
    print(species)
    for year in years:
        print(year)
        for metric in metrics:
            try:
                print(sum(df_table.loc[df_table['Pollutant'] == species].loc[df_table['Endpoint Group'] == 'Mortality'].loc[df_table['Year'] == year].dropna(subset=[metric])[metric]))
            except:
                continue
#%%



# Print total values
years = ['2016','2017','2018']
metrics= ['pollutant_model','pollutant_monitor','pollutant_DEQ']
for species in pollutants:
    print(species)
    for year in years:
        print(year)
        for metric in metrics:
            try:
                print(np.mean(df_table.loc[df_table['Pollutant'] == species].loc[df_table['Endpoint Group'] == 'Mortality'].loc[df_table['Year'] == year].dropna(subset=[metric])[metric]))
            except:
                continue


#%%
# =============================================================================
# Plot all things - DEQ, Model, Monitor
# =============================================================================




# Plotting section
#fig.suptitle('2018 PNW PM$_{2.5}$ Health Impacts',y=0.93,fontsize=20,ha='center') # title
#
#fig.text(0.06, 0.5, 'Latitude', va='center', rotation='vertical')
#fig.text(0.5, 0.09, 'Longitude', va='center', ha = 'center')
#fig.text(0.265, 0.82, 'Incidence', va='center', ha = 'center',fontsize=18)
#fig.text(0.685, 0.82, '% Incidence', va='center', ha = 'center',fontsize=18)



endpoints = ['Mortality'] # sets the endpoints we are looking at
pollutants = ['PM2.5']
# Add subplots
for pollutant in pollutants:
    for endpoint in endpoints:
        fig = plt.figure(figsize=(6,4),dpi=150)
        for year,i,j,k in zip(years,[1,2,3],[4,5,6],[7,8,9]):  
            
            # Colorbar
            #divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.2) # depends on the user needs
            alpha = 0.7
            linewidth = 1
            
        
            d = df_table.copy()
            d = pd.merge(d,counties)
            d = gpd.GeoDataFrame(d)
            
            
            vmax = 250
            vmin = 0
                 
            ax = fig.add_subplot(3,3,i)
            plt.title(year)
            im = d.loc[d['Endpoint Group'] == endpoint].loc[d['Pollutant'] == pollutant].dropna(subset=['mon_'+year]).plot(column='mon_'+year, cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
            states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,linewidth=linewidth,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
            
            ax = fig.add_subplot(3,3,j)
            #plt.title(year)
            im = d.loc[d['Endpoint Group'] == endpoint].loc[d['Pollutant'] == pollutant].dropna(subset=['mod_'+year]).plot(column='mod_'+year, cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
            states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,linewidth=linewidth,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
            
            ax = fig.add_subplot(3,3,k)
            #plt.title(year)
            im = d.loc[d['Endpoint Group'] == endpoint].loc[d['Pollutant'] == pollutant].dropna(subset=['DEQ']).plot(column='DEQ', cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
            states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,linewidth=linewidth,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
            
    
        #fig.tight_layout() # spaces the plots out a bit
        plt.show()
        plt.close()
d = pd.merge(df_table,counties)
d.to_csv(r'E:\Research\Benmap\output/df_table.csv')
