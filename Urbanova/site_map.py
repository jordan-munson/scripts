# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 16:15:10 2019

@author: riptu
"""
import rasterio
import contextily as ctx
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt






# Load file containing AQS site lat/lon
aqs_sites = pd.read_csv(r'E:/Research/Benmap/AQS_data/daily_'+''+'aqs_formatted_'+'2017'+'.csv')
aqs_sites['Monitor Name'] = aqs_sites['Monitor Name'].str[:2]
aqs_wa = aqs_sites[aqs_sites['Monitor Name'].str.contains("53")]
aqs_or = aqs_sites[aqs_sites['Monitor Name'].str.contains("41")]
aqs_id = aqs_sites[aqs_sites['Monitor Name'].str.contains("16")]
aqs_sites = pd.concat([aqs_wa,aqs_or,aqs_id])
aqs_sites = gpd.GeoDataFrame(aqs_sites)
geometry = [Point(xy) for xy in zip(aqs_sites.Longitude,aqs_sites.Latitude)]
aqs_sites = gpd.GeoDataFrame(aqs_sites,geometry=geometry)
aqs_sites = aqs_sites.drop(['Metric','Seasonal Metric','Statistic','Values'],axis=1)

# Plot
fig = plt.figure(figsize=(6.5,6.5),dpi=100)
ax = fig.add_subplot(1,1,1)

aqs_sites.plot(ax=ax,markersize=3,color='blue',edgecolor='white',linewidth=.3,marker='o',label='AQS sites')