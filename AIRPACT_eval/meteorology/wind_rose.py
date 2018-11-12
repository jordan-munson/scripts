# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 09:23:58 2018

@author: Jordan Munson
"""

import pandas as pd

from windrose import plot_windrose
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import matplotlib.ticker as tkr
import folium
from folium import FeatureGroup
# Set directories
inputdir = r'G:/Research/AIRPACT_eval/meteorology/'
outputdir = r'G:/Research/AIRPACT_eval/meteorology/AQS_plots/windrose/'
#Load data
df_airpact = pd.read_csv(inputdir+'df_airpact.csv').drop(['Unnamed: 0'],axis=1)
df_obs = pd.read_csv(inputdir+'df_obs.csv').drop(['Unnamed: 0'],axis=1).rename(columns={'datetime':'DateTime','Latitude':'lat','Longitude':'lon'})

types = ['predicted','observed']# Plot model wind roses
versions = ['AP3','AP4','AP5']

# =============================================================================
# #Create AQSID Column form state code, county code, and site num
# aqsid = pd.read_csv(r'G:\Research\AIRPACT_eval/aqs_sites.csv')
# aqsid = aqsid.ix[:,['State Code','County Code','Site Number','Local Site Name','Location Setting']]
# 
# aqsid['County Code'] = ["%03d" % n for n in aqsid['County Code'] ]
# aqsid['Site Number'] = ["%04d" % n for n in aqsid['Site Number'] ]
# 
# aqsid['AQS_ID'] = (aqsid['State Code']).astype(str) + (aqsid['County Code']).astype(str)+(aqsid['Site Number']).astype(str)
# 
# # Must force every cell in AQSID to be a string, otherwise lose most of data
# aqsid['AQS_ID'] = aqsid['AQS_ID'].astype(str)
# df_obs['AQS_ID'] = df_obs['AQS_ID'].astype(str)
# 
# df_obs = pd.merge(df_obs,aqsid) # Merge df_mod and aqsid so as to add names and such to the datafram
# df_obs = df_obs.drop(['State Code','County Code','Site Number'], axis=1)
# 
# =============================================================================
#%%

# =============================================================================
# for version in versions:
#     
#     # Set date range used based of versions
#     if version == 'AP3':
#         start_date ='2009-05-01'
#         end_date = '2014-07-01'
#     elif version == 'AP4':
#         start_date ='2014-07-01'
#         end_date = '2015-12-01'
#     elif version == 'AP5':
#         start_date ='2015-12-01'
#         end_date = '2018-07-01'
#     for i in types:
#         print('Working on ' +i)
#         # Locate correct site model data
#         #Manipulate dataframe
#         if i == 'predicted':
#             df1=df_airpact
#             title = (version + ' Predicted')
#             name = 'site_name'
#         else:
#             df1=df_obs
#             title = (version + ' Observed')
#             name = 'Local Site Name'
#             
#         df2 = df1.copy()
#         for sid in list(set(df2['AQS_ID'])):
#             # Reset df, need to use df1 for this.
#             df = df2
#                 
#             # Locate values correlating to site ID
#             df = df.loc[df['AQS_ID']==sid]
#             
#             # Reset the index so that the name can be found in the first row
#             df = df.reset_index(drop=True)
#             
#             # Find the site name, if not available use site id
#             site_nameinfo = str(df[name][0])
#             if site_nameinfo == 'nan':
#                 site_nameinfo = str(sid)
#             # If blank space in name exists, replace with _
#             site_nameinfo = site_nameinfo.replace(" ", "_")
#             site_nameinfo = site_nameinfo.replace("/", "-")
#             
#             # Just grab time period desired (airpact version)
#             mask = (df['DateTime'] > start_date) & (df['DateTime'] <= end_date) # Create a mask to determine the date range used
#             df = df.loc[mask]  
#             df = df.groupby("DateTime").mean()   
#             
#             # Set save name and rename columns for plot
#             if i == 'predicted':
#                 save = outputdir +site_nameinfo+'_'+ version+'_predicted_windrose.png'
#                 df = df.rename(columns={'WSPD10':'speed','WDIR10':'direction'})
#             else:
#                 save = outputdir +site_nameinfo+'_'+ version+'_observed_windrose.png'
#                 df = df.rename(columns={'aqs_wspd':'speed','aqs_wdir':'direction'})
#             df = df[['speed','direction']]
#             df = df.dropna()
#             # Plot windrose
#             bins = np.arange(0.0, 11, 2)
#             plot_windrose(df,kind='bar',bins=bins,normed=True) # If want to change colors, cmap=cm.hot. normed sets the lines as percents
#             # Look at the link below for how to use and modify the wind rose.
#             # https://windrose.readthedocs.io/en/latest/usage.html#a-stacked-histogram-with-normed-displayed-in-percent-results
#             
#             plt.title(site_nameinfo+' '+version+ ' '+i)
#             plt.legend(title="m/s")#, loc=(1.2,0))
#             try:
#                 plt.savefig( save,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False)
#             except ValueError:
#                 continue
#             plt.show()
#             plt.close()
# =============================================================================
        
#%%
# Folium setup
m= folium.Map(location=[47.6588, -117.4260],zoom_start=9) # Create the plot
m.add_child(folium.LatLngPopup()) #Add click lat/lon functionality

# mins and max's of the plot
lon_min=np.amin(-118.22552490234375)
lat_min=np.amin(47.08146286010742)
lon_max=np.amax(-116.51278686523438)
lat_max=np.amax(48.234893798828125)

plotted_sites = []
missing_sites = []
extents = [[lat_min, lon_min], [lat_max, lon_max]]
# Plot to Folium
for version in versions:
    feature_group = FeatureGroup(name=version)
    for i in types:
        if i == 'predicted':
            df1=df_airpact
            title = (version + ' Predicted')
            name = 'site_name'
        else:
            df1=df_obs
            title = (version + ' Observed')
            name = 'Local Site Name'
            
        df2 = df1.copy()
        
        for sid in list(set(df2['AQS_ID'])):
            df = df2
                
            # Locate values correlating to site ID
            df = df.loc[df['AQS_ID']==sid]            
            # Reset the index so that the name can be found in the first row
            df = df.reset_index(drop=True)
            
            # Find the site name, if not available use site id
            site_nameinfo = str(df[name][0])
            if site_nameinfo == 'nan':
                site_nameinfo = str(sid)
            # If blank space in name exists, replace with _
            site_nameinfo = site_nameinfo.replace(" ", "_")
            site_nameinfo = site_nameinfo.replace("/", "-")
            
            # Set the location of the wind roses on the map
            df = df.dropna()
            try:
                site_lat = df['lat'][0]
                site_lon = df['lon'][0]
            except IndexError:
                print('Missing ' + site_nameinfo+' '+version+ ' '+i)
                missing_sites.append(site_nameinfo+'_'+version+ '_'+i)
                continue
            
            width = 0.15
            height = 0.15
            
            lon_min=np.amin(site_lon - width)
            lat_min=np.amin(site_lat - height)
            lon_max=np.amax(site_lon + width)
            lat_max=np.amax(site_lat + height)
            extents = [[lat_min, lon_min], [lat_max, lon_max]]
            
            # Plot windrose on folium
            print('Plotting '+site_nameinfo+' '+version+ ' '+i+' to Folium map')
            # Name variables
            png = outputdir + site_nameinfo+'_'+ version+'_'+i+'_windrose.png'
            
            #Plot average map
            try:
                folium.raster_layers.ImageOverlay(png,bounds = extents,name=site_nameinfo+' '+version+ ' '+i,opacity = 0.7, show = True).add_to(feature_group)
                plotted_sites.append(site_nameinfo+'_'+version+ '_'+i)
            except FileNotFoundError:
                print('Missing ' + site_nameinfo+' '+version+ ' '+i)
                missing_sites.append(site_nameinfo+'_'+version+ '_'+i)
                continue
    feature_group.add_to(m)
        
# Add ability to move between layers
folium.LayerControl().add_to(m)

# Save and show the created map. Use Jupyter to see the map within your console
m.save(inputdir+'folium_windrose_map.html')
m
# Print how many sites have been plotted
print('Number of plotted sites is ' + str(len(plotted_sites)))
print('Number of missing sites is ' + str(len(missing_sites)))
    
#%%
'''
# Try to plot them all on one page
df1 = df_airpact
df1 = df1.groupby("DateTime").mean()
df1 = df1.rename(columns={'WSPD10':'speed','WDIR10':'direction'})
df1 = df1[['speed','direction']]
wd1  =df1['direction']
ws1 = df1['speed']

df2 = df_obs
df2 = df2.groupby("DateTime").mean()
df2 = df2.rename(columns={'aqs_wspd':'speed','aqs_wdir':'direction'})
df2 = df2[['speed','direction']]
wd2  =df2['direction']
ws2 = df2['speed']

fig, (ax1,ax2) = plt.subplots(1,2)
ax1 = WindroseAxes.from_ax()
ax1.contourf(wd1, ws1, bins=bins)
ax1.set_legend()
   
ax2 = WindroseAxes.from_ax()
ax2.contourf(wd2, ws2, bins=bins)
ax2.set_legend()
 
#f, axarr = plt.subplots(2,2)
#axarr[0,0]=plot_windrose(df1,kind='bar',bins=bins,normed=True)
#axarr[0,1]=plot_windrose(df2,kind='bar',bins=bins,normed=True)
#axarr[1,0]=plot_windrose(df3,kind='bar',bins=bins,normed=True)
# Suppossed example of plotting these on a single page
#https://github.com/python-windrose/windrose/blob/master/samples/example_subplots.py




#First create some toy data:
x = np.linspace(0, 2*np.pi, 400)
y = np.sin(x**2)

#Creates just a figure and only one subplot
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('Simple plot')

#Creates two subplots and unpacks the output array immediately
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.plot(x, y)
ax1.set_title('Sharing Y axis')
ax2.scatter(x, y)

'''




print('Done')









