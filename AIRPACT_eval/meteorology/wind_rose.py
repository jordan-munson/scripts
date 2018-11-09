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

# Set directories
inputdir = r'G:/Research/AIRPACT_eval/meteorology/'
outputdir = r'G:/Research/AIRPACT_eval/meteorology/AQS_plots/windrose/'

#Load data
df_airpact = pd.read_csv(inputdir+'df_airpact.csv').drop(['Unnamed: 0','lat','lon'],axis=1)
df_obs = pd.read_csv(inputdir+'df_obs.csv').drop(['Unnamed: 0','Local Site Name'],axis=1).rename(columns={'datetime':'DateTime'})


#%%
types = ['obs','mod']
# Plot model wind roses
versions = ['AP3','AP4','AP5']

for version in versions:
    
    # Set date range used based of versions
    if version == 'AP3':
        start_date ='2009-05-01'
        end_date = '2014-07-01'
    elif version == 'AP4':
        start_date ='2014-07-01'
        end_date = '2015-12-01'
    elif version == 'AP5':
        start_date ='2015-12-01'
        end_date = '2018-07-01'
    for i in types:
        # Locate correct site model data
        #Manipulate dataframe
        
        if i == 'obs':
            df=df_airpact
            title = (version + ' Predicted')
            save = outputdir + version+'_predicted_windrose.png'
            df = df.rename(columns={'WSPD10':'speed','WDIR10':'direction'})
        else:
            df=df_obs
            title = (version + ' Observed')
            save = outputdir + version+'_observed_windrose.png'
            df = df.rename(columns={'aqs_wspd':'speed','aqs_wdir':'direction'})

        mask = (df['DateTime'] > start_date) & (df['DateTime'] <= end_date) # Create a mask to determine the date range used
        df = df.loc[mask]  
        df = df.groupby("DateTime").mean()
        df = df[['speed','direction']]
        
        print(df.dtypes)
        
        bins = np.arange(0.0, 11, 2)
        plot_windrose(df,kind='bar',bins=bins,normed=True) # If want to change colors, cmap=cm.hot. normed sets the lines as percents
        # Look at the link below for how to use and modify the wind rose.
        # https://windrose.readthedocs.io/en/latest/usage.html#a-stacked-histogram-with-normed-displayed-in-percent-results
        plt.title(title)
        plt.legend(title="m/s")#, loc=(1.2,0))
        
        plt.savefig( save,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False)
        plt.show()
        plt.close()
        
    
#    bins = np.arange(0, 30 + 1, 1)
#    bins = bins[1:]
#    
#    ax, params = plot_windrose(df, kind='pdf', bins=bins)
#    print("Weibull params:")
#    print(params)
#    # plt.savefig("screenshots/pdf.png")
#    plt.show()
#    plt.close()
#%%
# =============================================================================
# Plot in Folium
# =============================================================================
m= folium.Map(location=[47.6588, -117.4260],zoom_start=9) # Create the plot
m.add_child(folium.LatLngPopup()) #Add click lat/lon functionality

# mins and max's of the plot
lon_min=np.amin(-118.22552490234375)
lat_min=np.amin(47.08146286010742)
lon_max=np.amax(-116.51278686523438)
lat_max=np.amax(48.234893798828125)

extents = [[lat_min, lon_min], [lat_max, lon_max]]
types = ['observed','predicted']
for sp in version:
    for i in types:
        print('Plotting '+sp+' to Folium map')
        # Name variables
    #    check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_emissions_hourly_basemap_'+sp+'_%05d.png','-b:v','5000k', output_dir+'movie_'+sp+'_output.webm'])
    #    check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_emissions_hourly_basemap_tiled_'+sp+'_%05d.png','-b:v','5000k', output_dir+'movie_'+sp+'_tiled_output.webm'])
        png = outputdir + version+'_'+i+'_windrose.png'
        #video1 = git_dir+'movie_'+sp+'_output.webm'
        #video2 = git_dir+'movie_'+sp+'_tiled_output.webm'
        
        #Plot average map
        folium.raster_layers.ImageOverlay(png,bounds = extents,name=sp,opacity = 0.5, show = False).add_to(m)
        
        #Plot countourf video
        #folium.raster_layers.VideoOverlay(video_url=video1,bounds = extents,name=sp+'_video',opacity = 0.5,attr = sp+'_video_map',show = False,autoplay=True).add_to(m)
        #Plot colormap video
        #folium.raster_layers.VideoOverlay(video_url=video2,bounds = extents,name=sp+'_tiled_video',opacity = 0.5,attr = sp+'_tiled_video_map',show = False,autoplay=True).add_to(m)

# Add ability to move between layers
folium.LayerControl().add_to(m)

# Save and show the created map. Use Jupyter to see the map within your console
m.save(inputdir+'folium_windrose_map.html')

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









