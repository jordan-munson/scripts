# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 13:49:56 2019

@author: Jordan Munson
"""


import matplotlib as mpl
#mpl.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import time
#from mpl_toolkits.basemap import Basemap
#import geopandas as gpd
import numpy as np

import cartopy.crs as ccrs
import cartopy
import cartopy.io.shapereader as shpreader
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1 import AxesGrid
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from netCDF4 import Dataset as netcdf_dataset
from matplotlib.colors import LogNorm
# =============================================================================
# #Set directory and load data
# =============================================================================
inputDir = r'E:\Research\Benmap/'
plotDir = inputDir+'plots/'
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'
shp_name = r'E:\Research\Benmap\benmap_shapefile_output/Krewski.shp'

# Set plot parameters
dpi = 300
mpl.rcParams['font.family'] = 'calibri'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 28 # 10 for paper. 28 for presentations
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

# =============================================================================
# df_table = pd.read_csv(inputDir+'output/df_table.csv').drop('Unnamed: 0',axis=1)
# df_table = gpd.GeoDataFrame(df_table)
# =============================================================================
                            
#counties = gpd.read_file(r'E:\Research\Benmap\benmap_shapefile_output/Krewski.shp')        
counties = shpreader.Reader(shp_name)               
counties = counties.records() 
country = next(counties)                           

# =============================================================================
# df_table = pd.read_csv(r'E:\Research\Benmap\output/df_table.csv').drop('Unnamed: 0',axis=1)
# =============================================================================
df_table = pd.read_csv(r'E:\Research\Benmap\output/df_table_inclusive.csv').drop('Unnamed: 0',axis=1)
# =============================================================================
# plot
# =============================================================================

      
data_crs = ccrs.AlbersEqualArea()  
useproj = ccrs.UTM(10)

# =============================================================================
# projections = [ccrs.PlateCarree(), # PlateCarree somehow works now..........................
# ccrs.AlbersEqualArea()
# ,ccrs.AzimuthalEquidistant()
# ,ccrs.EquidistantConic()
# ,ccrs.LambertConformal()
# ,ccrs.LambertCylindrical()
# ,ccrs.Mercator()
# ,ccrs.Miller()
# ,ccrs.Mollweide()
# ,ccrs.Orthographic()
# ,ccrs.Robinson()
# ,ccrs.Sinusoidal()
# ,ccrs.Stereographic()
# ,ccrs.TransverseMercator()
# ,ccrs.UTM(10)
# ,ccrs.InterruptedGoodeHomolosine()
# ,ccrs.RotatedPole()
# #,ccrs.OSGB()
# #,ccrs.EuroPP()
# ,ccrs.Geostationary()
# ,ccrs.NearsidePerspective()
# ,ccrs.EckertI()
# ,ccrs.EckertII()
# ,ccrs.EckertIII()
# ,ccrs.EckertIV()
# ,ccrs.EckertV()
# ,ccrs.EckertVI()
# #,ccrs.EqualEarth()
# ,ccrs.Gnomonic()
# ,ccrs.LambertAzimuthalEqualArea()
# ,ccrs.NorthPolarStereo()
# ,ccrs.OSNI()
# ,ccrs.SouthPolarStereo()]
# =============================================================================

# =============================================================================
# Percent incidence maps
# =============================================================================
projection = ccrs.PlateCarree()
endpoints = ['Mortality'] # sets the endpoints we are looking at
pollutants = ['PM2.5','Ozone']
#year = 2016
useproj = projection
#%%
for pollutant in pollutants:
    for endpoint in endpoints:
        fig = plt.figure(figsize=(10,10),dpi=dpi)
        for source,i in zip(['Model','Monitor','DEQ'],[1,2,3]):
            
            #fig, ax = plt.subplots(3, 1, subplot_kw=dict(projection=projection))
            #ax = fig.add_subplot(3,1,i)
            ax = plt.subplot(3,1,i,projection=useproj)
            
            print('Projection below is ' + str(projection))


            lon1 = -125
            lon2 = -110.5
            lat1 = 41
            lat2 = 50
            ax.set_extent([lon1, lon2, lat1, lat2],useproj)
            
            # Create a Stamen terrain background instance.
            stamen_terrain = cimgt.Stamen(style='terrain')
            ax.add_image(stamen_terrain, 8)
                                         
                
            # Matplotlib portion
            cmap = mpl.cm.Blues
            max_users=250
            for country in shpreader.Reader(shp_name).records():
                d = df_table.copy()
                name = country.attributes['Pooled Inc']
                column = country.attributes['COL']
                row = country.attributes['ROW']
                
                #Locate correct value from df_table
                d = d.loc[d['Pollutant'] == pollutant].loc[d['Endpoint Group'] == endpoint].loc[d['Col'] == column].loc[d['Row'] == row].reset_index(drop=True)  # .loc[d['Year'] == year]
                try:
                    d_mon = (d['mon_2016'][0] + d['mon_2017'][1] + d['mon_2018'][2])/3
                    d_mod = (d['mod_2016'][0] + d['mod_2017'][1] + d['mod_2018'][2])/3
                    d_deq = (d['DEQ'][0] + d['DEQ'][1] + d['DEQ'][2])/3
                    
# =============================================================================
#                     d_mon = d['mon_'+str(year)][0]
#                     d_mod = d['mod_'+str(year)][0]
#                     d_deq = d['DEQ'][0]
# =============================================================================
                    d_pop = d['Population'][0]
                except IndexError:
                    d_mon = 0.00000000000001
                    d_mod = 0.00000000000001
                    d_deq = 0.00000000000001 # Need to do this as some counties arent there for some reason.... this at leasts plots a white area
                    d_pop = 1
                    pass

                if column == 53:
                    alpha = 1
                elif column == 41:
                    alpha=1
                elif column ==16:
                    alpha=1
                else:
                    alpha = 0
                if pollutant == 'PM2.5':
                    multiplier = 1000 # 1000
                else:
                    multiplier = 2000 # 1000
                    
                num_users = name #countries[name]
                if source == 'Model':
                    im = ax.add_geometries(country.geometry, projection,
                                facecolor=cmap(d_mod/d_pop*multiplier),alpha=alpha)
                    title = 'AIRPACT (a)'
                if source == 'Monitor':
                    im = ax.add_geometries(country.geometry, projection,
                                facecolor=cmap(d_mon/d_pop*multiplier),alpha=alpha)
                    title = 'AQS (b)'
                if source == 'DEQ':
                    im = ax.add_geometries(country.geometry, projection,
                                facecolor=cmap(d_deq/d_pop*multiplier),alpha=alpha)
                    title = 'DEQ (c)'
                    
            sm = ax.imshow(np.arange(100).reshape((10, 10))/multiplier,cmap=cmap)
            #sm = plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(1))
            #sm = plt.plot(0,0.001)
            #sm._A = []
            cbar=plt.colorbar(sm,ax=ax,fraction=0.12, pad=0.04) # fraction=0.03, pad=0.04 # for when used on each subplot
            cbar.set_label('% '+endpoint, rotation=90)
            
            plt.title(title)

            
            
# =============================================================================
#             vmax = 250
#             vmin = 0        
#             im = d.loc[d['Endpoint Group'] == endpoint].loc[d['Pollutant'] == pollutant].dropna(subset=['DEQ']).plot('DEQ', cmap='Greys', markeredgecolor='black', legend=False,ax=ax)
# =============================================================================
            
            # add state lines and other lines
            states_provinces = cfeature.NaturalEarthFeature(
                category='cultural',
                name='admin_1_states_provinces_lines',
                scale='50m',
                facecolor='none')
            ax.add_feature(states_provinces, edgecolor='gray')
            ax.add_feature(cartopy.feature.COASTLINE, edgecolor='gray')
            ax.add_feature(cartopy.feature.BORDERS, edgecolor='gray')
            
        plt.savefig(plotDir + 'maps/averaged_'+pollutant+'_'+endpoint+'_map.png',bbox_inches = 'tight',pad_inches = 0)
        plt.show()
        plt.close()

#%%
# =============================================================================
# 2017
# =============================================================================
for pollutant in pollutants:
    for endpoint in endpoints:
        fig = plt.figure(figsize=(10,10),dpi=dpi)
        for source,i in zip(['Model','Monitor','DEQ'],[1,2,3]):
            
            #fig, ax = plt.subplots(3, 1, subplot_kw=dict(projection=projection))
            #ax = fig.add_subplot(3,1,i)
            ax = plt.subplot(3,1,i,projection=useproj)
            
            print('Projection below is ' + str(projection))


            lon1 = -125
            lon2 = -110.5
            lat1 = 41
            lat2 = 50
            ax.set_extent([lon1, lon2, lat1, lat2],useproj)
            
            # Create a Stamen terrain background instance.
            stamen_terrain = cimgt.Stamen(style='terrain')
            ax.add_image(stamen_terrain, 8)
                                         
                
            # Matplotlib portion
            cmap = mpl.cm.Blues
            max_users=250
            for country in shpreader.Reader(shp_name).records():
                d = df_table.copy()
                name = country.attributes['Pooled Inc']
                column = country.attributes['COL']
                row = country.attributes['ROW']
                
                #Locate correct value from df_table
                d = d.loc[d['Pollutant'] == pollutant].loc[d['Endpoint Group'] == endpoint].loc[d['Col'] == column].loc[d['Row'] == row].reset_index(drop=True)  # .loc[d['Year'] == year]
                try:
                    d_mon = d['mon_2017'][1]
                    d_mod = d['mod_2017'][1]*0.42
                    d_deq = d['DEQ'][1]
                    
# =============================================================================
#                     d_mon = d['mon_'+str(year)][0]
#                     d_mod = d['mod_'+str(year)][0]
#                     d_deq = d['DEQ'][0]
# =============================================================================
                    d_pop = d['Population'][0]
                except IndexError:
                    d_mon = 0.00000000000001
                    d_mod = 0.00000000000001
                    d_deq = 0.00000000000001 # Need to do this as some counties arent there for some reason.... this at leasts plots a white area
                    d_pop = 1
                    pass

                if column == 53:
                    alpha = 1
                elif column == 41:
                    alpha=1
                elif column ==16:
                    alpha=1
                else:
                    alpha = 0
                if pollutant == 'PM2.5':
                    multiplier = 1000 # 1000
                else:
                    multiplier = 3000 # 2000
                    
                num_users = name #countries[name]
                if source == 'Model':
                    im = ax.add_geometries(country.geometry, projection,
                                facecolor=cmap(d_mod/d_pop*multiplier),alpha=alpha)
                    title = 'AIRPACT'
                if source == 'Monitor':
                    im = ax.add_geometries(country.geometry, projection,
                                facecolor=cmap(d_mon/d_pop*multiplier),alpha=alpha)
                    title = 'AQS'
                if source == 'DEQ':
                    im = ax.add_geometries(country.geometry, projection,
                                facecolor=cmap(d_deq/d_pop*multiplier),alpha=alpha)
                    title = source
                   
            #ax.set_ylim(0,0.025)
            sm = ax.imshow(np.arange(100).reshape((10, 10))/multiplier,cmap=cmap)
            #sm = plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(1))
            #sm = plt.plot(0,0.001)
            #sm._A = []
            cbar=plt.colorbar(sm,ax=ax,fraction=0.12, pad=0.04) # fraction=0.03, pad=0.04 # for when used on each subplot
            cbar.set_label('% '+endpoint, rotation=90)
            
            plt.title(title)

            
            
# =============================================================================
#             vmax = 250
#             vmin = 0        
#             im = d.loc[d['Endpoint Group'] == endpoint].loc[d['Pollutant'] == pollutant].dropna(subset=['DEQ']).plot('DEQ', cmap='Greys', markeredgecolor='black', legend=False,ax=ax)
# =============================================================================
            
            # add state lines and other lines
            states_provinces = cfeature.NaturalEarthFeature(
                category='cultural',
                name='admin_1_states_provinces_lines',
                scale='50m',
                facecolor='none')
            ax.add_feature(states_provinces, edgecolor='gray')
            ax.add_feature(cartopy.feature.COASTLINE, edgecolor='gray')
            ax.add_feature(cartopy.feature.BORDERS, edgecolor='gray')
        fig.tight_layout() 
        plt.savefig(plotDir + 'maps/2017_'+pollutant+'_'+endpoint+'_map.png',bbox_inches = 'tight',pad_inches = 0)
        plt.show()
        plt.close()
#%%
# =============================================================================
# # =============================================================================
# # Log normalized maps        
# # =============================================================================
#         
# for pollutant in pollutants:
#     for endpoint in endpoints:
#         fig = plt.figure(figsize=(7.5,7),dpi=150)
#         for source,i in zip(['Model','Monitor','DEQ'],[1,2,3]):
#             
#             #fig, ax = plt.subplots(3, 1, subplot_kw=dict(projection=projection))
#             #ax = fig.add_subplot(3,1,i)
#             ax = plt.subplot(3,1,i,projection=useproj)
#             
#             print('Projection below is ' + str(projection))
# 
# 
#             lon1 = -125
#             lon2 = -110.5
#             lat1 = 41
#             lat2 = 50
#             ax.set_extent([lon1, lon2, lat1, lat2],useproj)
#             
#             # Create a Stamen terrain background instance.
#             stamen_terrain = cimgt.Stamen(style='terrain')
#             ax.add_image(stamen_terrain, 8)
#                                          
#                 
#             # Matplotlib portion
#             cmap = mpl.cm.Blues
#             max_users=250
#             for country in shpreader.Reader(shp_name).records():
#                 # load data into for loop
#                 d = df_table.copy()
#                 
#                 d['mon_2016_log'] = np.log10(d['mon_2016']) # transform data to log
#                 d['mon_2017_log'] = np.log10(d['mon_2017']) # transform data to log
#                 d['mon_2018_log'] = np.log10(d['mon_2018']) # transform data to log
#                 d['mod_2016_log'] = np.log10(d['mod_2016']) # transform data to log
#                 d['mod_2017_log'] = np.log10(d['mod_2017']) # transform data to log
#                 d['mod_2018_log'] = np.log10(d['mod_2018']) # transform data to log
#                 d['DEQ_log'] = np.log10(d['DEQ']) # transform data to log
#                 deq = d.copy()
#                 
#                 name = country.attributes['Pooled Inc']
#                 column = country.attributes['COL']
#                 row = country.attributes['ROW']
#                 
#                 #Locate correct value from df_table
#                 d = d.loc[d['Pollutant'] == pollutant].loc[d['Endpoint Group'] == endpoint].loc[d['Col'] == column].loc[d['Row'] == row].reset_index(drop=True)  # .loc[d['Year'] == year]
#                 try:
#                     d_mon = (d['mon_2016_log'][0] + d['mon_2017_log'][1] + d['mon_2018_log'][2])/3
#                     d_mod = (d['mod_2016_log'][0] + d['mod_2017_log'][1] + d['mod_2018_log'][2])/3
#                     d_deq = (d['DEQ_log'][0] + d['DEQ_log'][1] + d['DEQ_log'][2])/3
#                     
# # =============================================================================
# #                     d_mon = d['mon_'+str(year)][0]
# #                     d_mod = d['mod_'+str(year)][0]
# #                     d_deq = d['DEQ'][0]
# # =============================================================================
#                     d_pop = d['Population'][0]
#                 except IndexError:
#                     d_mon = 0.00000000000001
#                     d_mod = 0.00000000000001
#                     d_deq = 0.00000000000001 # Need to do this as some counties arent there for some reason.... this at leasts plots a white area
#                     d_pop = 1
#                     pass
# 
#                 if column == 53:
#                     alpha = 1
#                 elif column == 41:
#                     alpha=1
#                 elif column ==16:
#                     alpha=1
#                 else:
#                     alpha = 0
#                 multiplier = 1000
#                 num_users = name #countries[name]
#                 if source == 'Model':
#                     im = ax.add_geometries(country.geometry, projection,
#                                 facecolor=cmap(d_mon),alpha=alpha)
#                 if source == 'Monitor':
#                     im = ax.add_geometries(country.geometry, projection,
#                                 facecolor=cmap(d_mod),alpha=alpha)
#                 if source == 'DEQ':
#                     im = ax.add_geometries(country.geometry, projection,
#                                 facecolor=cmap(d_deq),alpha=alpha)
#                     
#             sm = ax.imshow(np.arange(100).reshape((10, 10))/multiplier,cmap=cmap,norm=LogNorm(),vmin=0.1, vmax=10)
#             #ax.set_ylim(0.1,10)
#             #sm = plt.cm.ScalarMappable(cmap=cmap,norm=plt.Normalize(1))
#             #sm = plt.plot(0,0.001)
#             #sm._A = []
#             cbar=plt.colorbar(sm,ax=ax,fraction=0.12, pad=0.04) # fraction=0.03, pad=0.04 # for when used on each subplot
#             cbar.set_label(endpoint, rotation=90)
#             
#             plt.title(source)
# 
#             
#             
# # =============================================================================
# #             vmax = 250
# #             vmin = 0        
# #             im = d.loc[d['Endpoint Group'] == endpoint].loc[d['Pollutant'] == pollutant].dropna(subset=['DEQ']).plot('DEQ', cmap='Greys', markeredgecolor='black', legend=False,ax=ax)
# # =============================================================================
#             
#             # add state lines and other lines
#             states_provinces = cfeature.NaturalEarthFeature(
#                 category='cultural',
#                 name='admin_1_states_provinces_lines',
#                 scale='50m',
#                 facecolor='none')
#             ax.add_feature(states_provinces, edgecolor='gray')
#             ax.add_feature(cartopy.feature.COASTLINE, edgecolor='gray')
#             ax.add_feature(cartopy.feature.BORDERS, edgecolor='gray')
#         fig.tight_layout()    
#         plt.savefig(plotDir + 'maps/averaged_'+pollutant+'_'+endpoint+'_map.png',bbox_inches = 'tight',pad_inches = 0)
#         plt.show()
#         plt.close()        
# =============================================================================
