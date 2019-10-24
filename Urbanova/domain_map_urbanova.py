# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 16:45:25 2019

@author: Jordan Munson
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import cartopy.io.img_tiles as cimgt
import matplotlib as mpl

# Set plot parameters
mpl.rcParams['font.family'] = 'calibri'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 10 # 10 for paper. 28 for presentations

fname = r'C:\Users\riptu\Documents\My BenMAP-CE Files\Result\APVR\AIRPACT\pollutant_shapefiles/urbanova.shp'
fname_airpact = r'C:\Users\riptu\Documents\My BenMAP-CE Files\Result\APVR\AIRPACT\pollutant_shapefiles/airpact_ozone.shp'
useproj = ccrs.PlateCarree()

fig = plt.figure(figsize=(6,6),dpi=300)
ax = plt.subplot(1,1,1,projection=useproj)

# Create a Stamen terrain background instance.
stamen_terrain = cimgt.Stamen(style='terrain')
ax.add_image(stamen_terrain, 8)

# =============================================================================
# # Urbanova extents
# lon1 = -118.4
# lon2 = -116.5
# lat1 = 47
# lat2 = 48.4
# =============================================================================

# AIRPACT extents
lon1 = -127
lon2 = -109
lat1 = 50.5
lat2 = 39

#AIRPACT
shape_feature = ShapelyFeature(Reader(fname_airpact).geometries(),
                   useproj, edgecolor='black',alpha=0.1,facecolor='none')
              
ax.add_feature(shape_feature)

# Urbanova
shape_feature = ShapelyFeature(Reader(fname).geometries(),
                   useproj, edgecolor='red',alpha=0.1,facecolor='none')
              
ax.add_feature(shape_feature)

# Annotate
transform = useproj._as_mpl_transform(ax)
bbox={'facecolor': 'white', 'alpha': 0.7, 'pad': 2}
ax.annotate('Urbanova', xy=(-117.4, 49), xycoords=transform,
            ha='center', va='top',color='red',fontweight='bold',bbox=bbox)
ax.annotate('AIRPACT', xy=(-123, 48.5), xycoords=transform,
            ha='center', va='top',color = 'black',fontweight='bold',bbox=bbox)
            
ax.set_extent([lon1, lon2, lat1, lat2],useproj)
fig.tight_layout()
plt.savefig(r'E:/Research/Urbanova_Jordan/plots/maps/domain_map.png')
plt.show()
