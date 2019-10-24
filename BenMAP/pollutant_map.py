# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 10:10:51 2019

@author: Jordan Munson
"""

# Import libraries
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from shapely.geometry import Point

# set paths
inputDir = r'E:/Research/Benmap/output/'
plotDir = r'E:/Research/Benmap/plots/'


# load in shapefiles
counties = gpd.read_file(r'E:\Research\Benmap\benmap_shapefile_output/Krewski.shp')
counties = counties.rename(columns={"COL": "Col",'ROW':'Row'})
states = gpd.read_file(r'E:\Research\Benmap\benmap_shapefile_output/state/state.shp')
states = states.rename(columns={"COL": "Col",'ROW':'Row'})
states['zeros'] = 0

# Load in state lines and table with WA, OR, ID data
df_table = pd.read_csv(inputDir+'df_table1.csv')
df_states = pd.read_csv(inputDir+'df_states.csv').drop(['Unnamed: 0'],axis=1)
df_states = gpd.GeoDataFrame(df_states)

#%%

# =============================================================================
# Plot pollutants
# =============================================================================

# format county lines a bit to plot empty
county_lines = counties.copy()
county_lines['zeros'] = 0
county_lines = pd.merge(df_table,county_lines)# Merged so that the only county lines are ones from WA, OR, ID
county_lines = gpd.GeoDataFrame(county_lines)

# Load in spatial data from BenMAP
deq_ozone = gpd.read_file(r'C:\Users\riptu\Documents\My BenMAP-CE Files\Result\APVR\AIRPACT\pollutant_shapefiles/deq_ozone.shp')
model_ozone = gpd.read_file(r'C:\Users\riptu\Documents\My BenMAP-CE Files\Result\APVR\AIRPACT\pollutant_shapefiles/airpact_ozone.shp')
monitor_ozone = gpd.read_file(r'C:\Users\riptu\Documents\My BenMAP-CE Files\Result\APVR\AIRPACT\pollutant_shapefiles/monitor_ozone.shp')

deq_pm = gpd.read_file(r'C:\Users\riptu\Documents\My BenMAP-CE Files\Result\APVR\AIRPACT\pollutant_shapefiles/deq_pm.shp')
model_pm = gpd.read_file(r'C:\Users\riptu\Documents\My BenMAP-CE Files\Result\APVR\AIRPACT\pollutant_shapefiles/model_pm.shp')
monitor_pm = gpd.read_file(r'C:\Users\riptu\Documents\My BenMAP-CE Files\Result\APVR\AIRPACT\pollutant_shapefiles/monitor_pm.shp')


datasets=['AIRPACT','AQS','DEQ']
pollutants = ['Ozone','PM2.5']
year = '2017'
cmap = 'OrRd'

for pollutant in pollutants:
    print(pollutant)
    if pollutant == 'Ozone':
        species = 'o3_'
    else:
        species = ''
    # Load file containing AQS site lat/lon
    aqs_sites = pd.read_csv(r'E:/Research/Benmap/AQS_data/daily_'+species+'aqs_formatted_'+year+'.csv')
    aqs_sites['Monitor Name'] = aqs_sites['Monitor Name'].str[:2]
    aqs_wa = aqs_sites[aqs_sites['Monitor Name'].str.contains("53")] # select only WA
    aqs_or = aqs_sites[aqs_sites['Monitor Name'].str.contains("41")] # Select only OR
    aqs_id = aqs_sites[aqs_sites['Monitor Name'].str.contains("16")] # Select only ID
    aqs_sites = pd.concat([aqs_wa,aqs_or,aqs_id])
    aqs_sites = gpd.GeoDataFrame(aqs_sites) # Convert to geodataframe
    geometry = [Point(xy) for xy in zip(aqs_sites.Longitude,aqs_sites.Latitude)]
    aqs_sites = gpd.GeoDataFrame(aqs_sites,geometry=geometry)
    aqs_sites = aqs_sites.drop(['Metric','Seasonal Metric','Statistic','Values'],axis=1)
    
    fig = plt.figure(figsize=(6.5,6.5),dpi=300)
    for dataset,i in zip(datasets,[1,2,3]):

        alpha = 0.7
        linewidth = .3
        
        if pollutant == 'Ozone':
            name = 'D8HourMax'
            unit = '[ppb]'
            vmax = 75
            vmin = 20
            
            if dataset == 'DEQ':
                d = deq_ozone.copy()               
                label = dataset + ' (c)'
            if dataset == 'AIRPACT':
                d = model_ozone.copy()
                label = dataset + ' (a)' 
            if dataset == 'AQS':
                d = monitor_ozone.copy()
                label = dataset + ' (b)'
                
        else:
            name = 'D24HourMean'
            unit = '\u03BCg m$^{-3}$'
            vmax = 25
            vmin = 0
            
            if dataset == 'DEQ':
                d = deq_pm.copy()
                label = dataset + ' (c)'
            if dataset == 'AIRPACT':
                d = model_pm.copy()
                label = dataset + ' (a)'
            if dataset == 'AQS':
                d = monitor_pm.copy()
                label = dataset + ' (b)'
        d = gpd.GeoDataFrame(d)
        

        # Plotting section
        ax = fig.add_subplot(3,1,i)
        plt.title(label)
        im = d.dropna(subset=[name]).plot(column=name, cmap=cmap, legend=False,ax=ax,vmin=vmin,vmax=vmax,linewidth=1, edgecolor='face') # pollutant plot
        states = df_states.plot(column = 'zeros',cmap='hot', legend=False,linewidth=linewidth+.2,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha) # state lines
        county = county_lines.plot(column = 'zeros',cmap='hot', legend=False,linewidth=linewidth,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha) # County lines
        if dataset == 'AQS':
            aqs_sites.plot(ax=ax,markersize=3,color='blue',edgecolor='white',linewidth=.3,marker='o',label='AQS sites') # plot monitoring sites
        ax.set_axis_off()
        
        
        #set-up colorbar
        norm = colors.Normalize(vmin=vmin, vmax=vmax)
        cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        
        # add colorbar
        ax_cbar = fig.colorbar(cbar, ax=ax)
        # add label for the colorbar
        ax_cbar.set_label(unit)

        
    fig.tight_layout() # spaces the plots out a bit
    plt.savefig(plotDir + 'maps/'+pollutant+'_'+year+'_map.png')
    plt.show()
    plt.close()

