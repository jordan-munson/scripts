# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:58:32 2018

@author: Jordan Munson
"""
# Script to plot basemap PNG files to folium for presentation

#Import libraries
import matplotlib
#matplotlib.use('Agg')  # Uncomment this when using in Kamiak/Aeolus
import numpy as np
import datetime
import pytz
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pickle
import folium
import os
from subprocess import check_call 
from mpl_toolkits.basemap import Basemap
from pytz import timezone
from datetime import timedelta
import copy

# Set file paths
base_dir=r'E:/Research/Urbanova_Jordan/'
output_dir = r'E:/Research/scripts/folium_files/'
# =============================================================================
# git_dir = 'https://github.com/jordan-munson/scripts/raw/master/folium_files/'
# =============================================================================
git_dir = r'E:/Research/scripts/folium_files/'

month = 2

# Set times
start_year = 2019
start_month = month
start_day = 1

end_year = 2019
end_month = month
#end_day = monthrange(end_year, end_month)[1]
end_day = 1

# set start and end date
start = datetime.datetime(start_year, start_month, start_day, hour=0)
end = datetime.datetime(end_year, end_month, end_day, hour=23)
timezone = pytz.timezone("utc")
start = timezone.localize(start)
end = timezone.localize(end)

# Load data
# Data from "urbanova_mapping_1.33km.py"
name =base_dir+ '1p33_'+start.strftime("%Y%m%d")+'_'+end.strftime("%Y%m%d")#+'_PST'

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
airpact = load_obj(name)

# obtain model lat and lon - needed for AQS eval and basemap
lat = airpact['lat'][0]
lon = airpact['lon'][0]

#%%
#base map
m = Basemap(projection='merc',
              llcrnrlon = lon[0,0], urcrnrlon = lon[90-1,90 -1], 
              llcrnrlat = lat[0,0], urcrnrlat = lat[90-1,90-1],
              resolution='h',
              area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
x,y = m(lon,lat)
var_list = ["O3", "PMIJ"]
unit_list = ["ppb", "\u03BCg m$^{-3}$"]

############################################
# Averaged domain basemaps       
############################################
#save maps into the pdf file (two maps in single page)
with PdfPages(base_dir+'maps/urbanova_avg_basemap_' + '_'+ start.strftime("%Y%m%d") + '-' +  end.strftime("%Y%m%d") + '.pdf') as pdf:
    
    for i, sp in enumerate(var_list):
        plt.style.use("dark_background")
        fig = plt.figure(figsize=(14,10),dpi=300)
        #plt.title(sp)
        o3_max = 45
        pm_max = 13
        o3_bins = np.arange(0, o3_max, 5)
        pm_bins = np.arange(0, pm_max, 5)
        vmin = 0
        # compute auto color-scale using maximum concentrations
        down_scale = np.percentile(airpact[sp], 5)
        up_scale = np.percentile(airpact[sp], 95)
        if sp == "O3":
            clevs = o3_bins
            vmax = o3_max
            vmin = 20
        else:
            clevs = pm_bins
            vmax = pm_max
        #clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
        print("debug clevs", clevs, sp)
        

# =============================================================================
#           # countour method
#         cs = m.contourf(x,y,airpact[sp].mean(axis=0),clevs,cmap=plt.get_cmap('jet'), extend='both')
#         cs.cmap.set_under('cyan')
#         cs.cmap.set_over('black')
# =============================================================================
        # colormesh method
        cmap = plt.get_cmap('jet')
        colormesh = m.pcolormesh(x, y, airpact[sp].mean(axis=0), vmin = vmin,vmax=vmax, cmap=cmap)
        colormesh.cmap.set_over('black')

        
        #m.drawcoastlines()
        #m.drawstates()
        #m.drawcountries()
        #m.drawcounties()
        #m.drawrivers()

        cblabel = unit_list[i]
        cbticks = True
        cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
        cbar.set_label(cblabel)
        
        
# =============================================================================
#         plt.annotate("mean: " + str(round(airpact[sp].mean(),2)) + " "+ unit_list[i], xy=(0.04, 0.98), xycoords='axes fraction')
# =============================================================================
        
        #if cbticks:
        #    cbar.set_ticks(clevs)
        
        # print the surface-layer mean on the map plot
        #if sp == 'O3':
            #plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" ppb", xy=(0, 1.02), xycoords='axes fraction')
        #else:
            #plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" $ug/m^3$", xy=(0, 1.02), xycoords='axes fraction')
        outpng = output_dir +'urbanova_basemap_' +str(end_month)+'_'+ sp + '.png'
        print(outpng)
        #fig.savefig(fig) 
        plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False)
        plt.show()
        plt.close()
# =============================================================================
# #%%
# #base map
# m = Basemap(projection='merc',
#               llcrnrlon = lon[0,0], urcrnrlon = lon[90-1,90 -1], 
#               llcrnrlat = lat[0,0], urcrnrlat = lat[90-1,90-1],
#               resolution='h',
#               area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
# x,y = m(lon,lat)
# var_list = ["O3", "PMIJ"]
# unit_list = ["ppb", "$ug/m^3$"]
# ############################################
# # hourly domain basemaps, this takes lots of time if doing hourly. Switch to daily could be prudent over a long timespan
# ############################################
# 
# for i, sp in enumerate(var_list):
#     
#     for t in range(0, len(airpact[sp])): 
#         plt.style.use("dark_background")
#         outpng = base_dir +'maps/daily_basemap/airpact_hourly_basemap_' + sp + '_%05d.png' % t
#         print(outpng)
#         
#         fig = plt.figure(figsize=(14,10))
#         #plt.title('at ' + airpact["DateTime"][t,0,0])
#         
#         #o3_bins = np.arange(0, 45, 5)
#         #pm_bins = np.arange(0, 12, 1.2)
#         # compute auto color-scale using maximum concentrations
#         down_scale = np.percentile(airpact[sp], 5)
#         up_scale = np.percentile(airpact[sp], 95)
#         if sp == "O3":
#             clevs = o3_bins
#         else:
#             clevs = pm_bins
#         #clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
#         print("debug clevs", clevs, sp)
#         
#         print(unit_list[i], sp, t)
# 
#         cs = m.contourf(x,y,airpact[sp][t,:,:],clevs,cmap=plt.get_cmap('jet'), extend='both')
#         cs.cmap.set_under('cyan')
#         cs.cmap.set_over('black')
#         
#         #m.drawcoastlines()
#         #m.drawstates()
#         #m.drawcountries()
#         
#         cblabel = unit_list[i]
#         cbticks = True
#         cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
#         cbar.set_label(cblabel)
#         if cbticks:
#             cbar.set_ticks(clevs)
#         
#         # Convert to PST
# # =============================================================================
# #         try:
# #             datetime_object = str(datetime.datetime.strptime(airpact["DateTime"][t,0,0], '%Y%m%d %H:%M %Z'))
# #         except ValueError:
# #             pass
# # =============================================================================
#         # print the surface-layer mean on the map plot
#         plt.annotate("mean: " + str(round(airpact[sp][t,:,:].mean(),2)) + " "+ unit_list[i] + ' at ' + str(airpact["DateTime"][t,0,0]) + ' PST', xy=(0.04, 0.98), xycoords='axes fraction')
#         
#         plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False) 
#         plt.show()
#         plt.close()
# # This requires ffmpeg program, which is not easy to install in aeolus/kamiak
# # To make a video, download all the pngs in your computer and execute the command below
# # "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_PMIJ_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_PMIJ_output.webm" 
# # "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_O3_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_O3_output.webm" 
# 
# # Attempt to run ffmpeg 
# os.chdir(base_dir) # framerate of 5 for small time spans
# check_call(['ffmpeg', '-y', '-framerate','24', '-i',base_dir+'maps/daily_basemap/airpact_hourly_basemap_PMIJ_%05d.png','-b:v','5000k', output_dir+'movie_PMIJ_output.webm'])
# check_call(['ffmpeg', '-y', '-framerate','24', '-i',base_dir+'maps/daily_basemap/airpact_hourly_basemap_O3_%05d.png','-b:v','5000k', output_dir+'movie_O3_output.webm'])
# print('Videos made')
# #%%
# 
# #base map
# m = Basemap(projection='merc',
#               llcrnrlon = lon[0,0], urcrnrlon = lon[90-1,90 -1], 
#               llcrnrlat = lat[0,0], urcrnrlat = lat[90-1,90-1],
#               resolution='h',
#               area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
# x,y = m(lon,lat)
# var_list = ["O3", "PMIJ"]
# unit_list = ["ppb", "$ug/m^3$"]
# ############################################
# # hourly domain basemaps, this takes lots of time if doing hourly. Switch to daily could be prudent over a long timespan
# ############################################
# #save maps into the pdf file (two maps in single page)
# 
# for i, sp in enumerate(var_list):
#     
#     for t in range(0, len(airpact[sp])): 
#         plt.style.use("dark_background")
#            
#         outpng = base_dir +'maps/daily_basemap/airpact_hourly_basemap_tiled_' + sp + '_%05d.png' % t
#         print(outpng)
#         pm_max = 35
#         fig = plt.figure(figsize=(14,10))
#         #plt.title('at ' + airpact["DateTime"][t,0,0])
#         
#         #o3_bins = np.arange(0, 45, 5)
#         #pm_bins = np.arange(0, 12, 1.2)
#         # compute auto color-scale using maximum concentrations
#         down_scale = np.percentile(airpact[sp], 5)
#         up_scale = np.percentile(airpact[sp], 95)
#         vmin = 0
#         if sp == "O3":
#             clevs = o3_bins
#             vmax = o3_max
#         else:
#             clevs = pm_bins
#             vmax = pm_max
#         #clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
#         print("debug clevs", clevs, sp)
#         
#         print(unit_list[i], sp, t)
# 
#         #cs = m.contourf(x,y,airpact[sp][t,:,:],clevs,cmap=plt.get_cmap('jet'), extend='both')
#         #cs.cmap.set_under('cyan')
# 
#         
#         #m.drawcoastlines()
#         #m.drawstates()
#         #m.drawcountries()
# 
#         # These two lines below change the map to continuos. However this muddles the image
#         cmap = plt.get_cmap('jet')
#         colormesh = m.pcolormesh(x, y, airpact[sp][t,:,:], vmin = vmin,vmax=vmax, cmap=cmap)
#         colormesh.cmap.set_over('black')
#         cblabel = unit_list[i]
#         cbticks = True
#         cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
#         cbar.set_label(cblabel)
#         if cbticks:
#             cbar.set_ticks(clevs)
#             
#         # Convert to PST
# # =============================================================================
# #         try:
# #             datetime_object = str(datetime.datetime.strptime(airpact["DateTime"][t,0,0], '%Y%m%d %H:%M %Z') - timedelta(hours=8))
# #         except ValueError:
# #             pass
# # =============================================================================
#         # print the surface-layer mean on the map plot
#         plt.annotate("mean: " + str(round(airpact[sp][t,:,:].mean(),2)) + " "+ unit_list[i] + ' at ' + str(airpact["DateTime"][t,0,0]) + ' PST', xy=(0.04, 0.98), xycoords='axes fraction')
#         
#         plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False) 
#         plt.show()
#         plt.close()
# # This requires ffmpeg program, which is not easy to install in aeolus/kamiak
# # To make a video, download all the pngs in your computer and execute the command below
# # "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_PMIJ_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_PMIJ_output.webm" 
# # "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_O3_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_O3_output.webm" 
# 
# # Attempt to run ffmpeg 
# os.chdir(base_dir) # framerate of 5 for small time spans
# check_call(['ffmpeg', '-y', '-framerate','24', '-i',base_dir+'maps/daily_basemap/airpact_hourly_basemap_tiled_PMIJ_%05d.png','-b:v','5000k', output_dir+'movie_PMIJ_tiled_output.webm'])
# check_call(['ffmpeg', '-y', '-framerate','24', '-i',base_dir+'maps/daily_basemap/airpact_hourly_basemap_tiled_O3_%05d.png','-b:v','5000k', output_dir+'movie_O3_tiled_output.webm'])
# print('Videos made')
# =============================================================================

#%%

# =============================================================================
# #base map
# m = Basemap(projection='merc',
#               llcrnrlon = lon[0,0], urcrnrlon = lon[90-1,90 -1], 
#               llcrnrlat = lat[0,0], urcrnrlat = lat[90-1,90-1],
#               resolution='h',
#               area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
# x,y = m(lon,lat)
# var_list = ["PMIJ",'O3']
# unit_list = ["$ug/m^3$","ppb" ]
# datetime = []
# ############################################
# # hourly domain basemaps, this takes lots of time if doing hourly. Switch to daily could be prudent over a long timespan
# ############################################
# #save maps into the pdf file (two maps in single page)
# for i, sp in enumerate(var_list):
#     t_days = int(len(airpact[sp])/24)
#     temp = np.empty( ( t_days, 90, 90), '|U18')
#     df_daily = {}
#     for t in range(0,t_days):
#         
#         # Do daily average and MD8HA
#         if sp == 'PMIJ':
#             days=t
#             t = t*24
#             temp[days] = (airpact[sp][t,:,:]+airpact[sp][t+1,:,:]+airpact[sp][t+2,:,:]+airpact[sp][t+3,:,:]+airpact[sp][t+4,:,:]+airpact[sp][t+5,:,:]+airpact[sp][t+6,:,:]+airpact[sp][t+7,:,:]+airpact[sp][t+8,:,:]+airpact[sp][t+9,:,:]+airpact[sp][t+10,:,:]+airpact[sp][t+11,:,:]+airpact[sp][t+12,:,:]+airpact[sp][t+13,:,:]+airpact[sp][t+14,:,:]+airpact[sp][t+15,:,:]+airpact[sp][t+16,:,:]+airpact[sp][t+17,:,:]+airpact[sp][t+18,:,:]+airpact[sp][t+19,:,:]+airpact[sp][t+20,:,:]+airpact[sp][t+21,:,:]+airpact[sp][t+22,:,:]+airpact[sp][t+23,:,:])/24  
#             df_daily[sp] = temp
#             datetime.append(airpact['DateTime'][t,0,0])
#             
#         else:
#             days=t
#             t = t*24
#             temp[days] = (airpact[sp][t,:,:]+airpact[sp][t+1,:,:]+airpact[sp][t+2,:,:]+airpact[sp][t+3,:,:]+airpact[sp][t+4,:,:]+airpact[sp][t+5,:,:]+airpact[sp][t+6,:,:]+airpact[sp][t+7,:,:]+airpact[sp][t+8,:,:]+airpact[sp][t+9,:,:]+airpact[sp][t+10,:,:]+airpact[sp][t+11,:,:]+airpact[sp][t+12,:,:]+airpact[sp][t+13,:,:]+airpact[sp][t+14,:,:]+airpact[sp][t+15,:,:]+airpact[sp][t+16,:,:]+airpact[sp][t+17,:,:]+airpact[sp][t+18,:,:]+airpact[sp][t+19,:,:]+airpact[sp][t+20,:,:]+airpact[sp][t+21,:,:]+airpact[sp][t+22,:,:]+airpact[sp][t+23,:,:])/24  
#             df_daily[sp] = temp
#             datetime.append(airpact['DateTime'][t,0,0])
#             
#     df_daily[sp] = df_daily[sp].astype(np.float)
#     for t in range(0, len(df_daily[sp])): 
#         plt.style.use("dark_background")
#            
#         outpng = base_dir +'maps/daily_basemap/airpact_daily_basemap_tiled_' + sp + '_%05d.png' % t
#         print(outpng)
#         pm_max = 35
#         fig = plt.figure(figsize=(14,10))
#         #plt.title('at ' + airpact["DateTime"][t,0,0])
#         
# 
#         
#         o3_bins = np.arange(0, 45, 5)
#         pm_bins = np.arange(0, pm_max, 5)
#         # compute auto color-scale using maximum concentrations
#         #down_scale = np.percentile(df_daily[sp], 5)
#         #up_scale = np.percentile(df_daily[sp], 95)
#         vmin = 0
#         if sp == "O3":
#             clevs = o3_bins
#             vmax = o3_max
#         else:
#             clevs = pm_bins
#             vmax = pm_max
#         #clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
#         print("debug clevs", clevs, sp)
#         
#         print(unit_list[i], sp, t)
# 
#         #cs = m.contourf(x,y,df_daily[sp][t,:,:],clevs,cmap=plt.get_cmap('jet'), extend='both')
#         #cs.cmap.set_under('cyan')
# 
#         
#         #m.drawcoastlines()
#         #m.drawstates()
#         #m.drawcountries()
# 
#         # These two lines below change the map to continuos. However this muddles the image
#         cmap = plt.get_cmap('jet')
#         colormesh = m.pcolormesh(x, y, df_daily[sp][t,:,:], vmin = vmin,vmax=vmax, cmap=cmap)
#         colormesh.cmap.set_over('black')
#         cblabel = unit_list[i]
#         cbticks = True
#         cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
#         cbar.set_label(cblabel)
#         if cbticks:
#             cbar.set_ticks(clevs)
#             
#         # print the surface-layer mean on the map plot
#         plt.annotate("mean: " + str(round(df_daily[sp][t,:,:].mean(),2)) + " "+ unit_list[i] + ' at ' + str(datetime[t])[0:8], xy=(0.04, 0.98), xycoords='axes fraction')
#         
#         plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False) 
#         plt.show()
#         plt.close()
# # This requires ffmpeg program, which is not easy to install in aeolus/kamiak
# # To make a video, download all the pngs in your computer and execute the command below
# # "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_PMIJ_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_PMIJ_output.webm" 
# # "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_O3_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_O3_output.webm" 
# 
# # Attempt to run ffmpeg 
# os.chdir(base_dir) # framerate of 5 for small time spans
# check_call(['ffmpeg', '-y', '-framerate','3', '-i',base_dir+'maps/daily_basemap/airpact_daily_basemap_tiled_PMIJ_%05d.png','-b:v','5000k', output_dir+'movie_PMIJ_daily_tiled_output.webm'])
# check_call(['ffmpeg', '-y', '-framerate','3', '-i',base_dir+'maps/daily_basemap/airpact_daily_basemap_tiled_O3_%05d.png','-b:v','5000k', output_dir+'movie_O3_daily_tiled_output.webm'])
# print('Videos made')
# =============================================================================

#%%
# =============================================================================
# #base map
# m = Basemap(projection='merc',
#               llcrnrlon = lon[0,0], urcrnrlon = lon[90-1,90 -1], 
#               llcrnrlat = lat[0,0], urcrnrlat = lat[90-1,90-1],
#               resolution='h',
#               area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
# x,y = m(lon,lat)
# var_list = ["O3", "PMIJ"]
# unit_list = ["ppb", "$ug/m^3$"]
# datetime = []
# ############################################
# # Contour maps
# ############################################
# 
# for i, sp in enumerate(var_list):
#     t_days = int(len(airpact[sp])/24)
#     temp = np.empty( ( t_days, 90, 90), '|U18')
#     df_daily = {}
#     for t in range(0,t_days):
#     
#         # Do daily average and MD8HA
#         if sp == 'PMIJ':
#             days=t
#             t = t*24
#             temp[days] = (airpact[sp][t,:,:]+airpact[sp][t+1,:,:]+airpact[sp][t+2,:,:]+airpact[sp][t+3,:,:]+airpact[sp][t+4,:,:]+airpact[sp][t+5,:,:]+airpact[sp][t+6,:,:]+airpact[sp][t+7,:,:]+airpact[sp][t+8,:,:]+airpact[sp][t+9,:,:]+airpact[sp][t+10,:,:]+airpact[sp][t+11,:,:]+airpact[sp][t+12,:,:]+airpact[sp][t+13,:,:]+airpact[sp][t+14,:,:]+airpact[sp][t+15,:,:]+airpact[sp][t+16,:,:]+airpact[sp][t+17,:,:]+airpact[sp][t+18,:,:]+airpact[sp][t+19,:,:]+airpact[sp][t+20,:,:]+airpact[sp][t+21,:,:]+airpact[sp][t+22,:,:]+airpact[sp][t+23,:,:])/24  
#             df_daily[sp] = temp
#             datetime.append(airpact['DateTime'][t,0,0])
#             
#         else:
#             days=t
#             t = t*24
#             temp[days] = (airpact[sp][t,:,:]+airpact[sp][t+1,:,:]+airpact[sp][t+2,:,:]+airpact[sp][t+3,:,:]+airpact[sp][t+4,:,:]+airpact[sp][t+5,:,:]+airpact[sp][t+6,:,:]+airpact[sp][t+7,:,:]+airpact[sp][t+8,:,:]+airpact[sp][t+9,:,:]+airpact[sp][t+10,:,:]+airpact[sp][t+11,:,:]+airpact[sp][t+12,:,:]+airpact[sp][t+13,:,:]+airpact[sp][t+14,:,:]+airpact[sp][t+15,:,:]+airpact[sp][t+16,:,:]+airpact[sp][t+17,:,:]+airpact[sp][t+18,:,:]+airpact[sp][t+19,:,:]+airpact[sp][t+20,:,:]+airpact[sp][t+21,:,:]+airpact[sp][t+22,:,:]+airpact[sp][t+23,:,:])/24  
#             df_daily[sp] = temp
#             datetime.append(airpact['DateTime'][t,0,0])
#             
#     df_daily[sp] = df_daily[sp].astype(np.float)
#     
#     for t in range(0, len(df_daily[sp])): 
#         plt.style.use("dark_background")
#         outpng = base_dir +'maps/daily_basemap/airpact_daily_basemap_' + sp + '_%05d.png' % t
#         print(outpng)
# 
#         fig = plt.figure(figsize=(14,10))
#         #plt.title('at ' + airpact["DateTime"][t,0,0])
#         
#         #o3_bins = np.arange(0, 45, 5)
#         #pm_bins = np.arange(0, 12, 1.2)
#         # compute auto color-scale using maximum concentrations
#         down_scale = np.percentile(df_daily[sp], 5)
#         up_scale = np.percentile(df_daily[sp], 95)
#         if sp == "O3":
#             clevs = o3_bins
#         else:
#             clevs = pm_bins
#         #clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
#         print("debug clevs", clevs, sp)
#         
#         print(unit_list[i], sp, t)
# 
#         cs = m.contourf(x,y,df_daily[sp][t,:,:],clevs,cmap=plt.get_cmap('jet'), extend='both')
#         cs.cmap.set_under('cyan')
#         cs.cmap.set_over('black')
#         
#         #m.drawcoastlines()
#         #m.drawstates()
#         #m.drawcountries()
#         
#         cblabel = unit_list[i]
#         cbticks = True
#         cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
#         cbar.set_label(cblabel)
#         if cbticks:
#             cbar.set_ticks(clevs)
# 
#         # print the surface-layer mean on the map plot
#         plt.annotate("mean: " + str(round(df_daily[sp][t,:,:].mean(),2)) + " "+ unit_list[i] + ' at ' + str(datetime[t])[0:8], xy=(0.04, 0.98), xycoords='axes fraction')
#         
#         plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False) 
#         plt.show()
#         plt.close()
# # This requires ffmpeg program, which is not easy to install in aeolus/kamiak
# # To make a video, download all the pngs in your computer and execute the command below
# # "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_PMIJ_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_PMIJ_output.webm" 
# # "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_O3_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_O3_output.webm" 
# 
# # Attempt to run ffmpeg 
# os.chdir(base_dir) # framerate of 5 for small time spans
# check_call(['ffmpeg', '-y', '-framerate','3', '-i',base_dir+'maps/daily_basemap/airpact_daily_basemap_PMIJ_%05d.png','-b:v','5000k', output_dir+'movie_PMIJ_daily_output.webm'])
# check_call(['ffmpeg', '-y', '-framerate','3', '-i',base_dir+'maps/daily_basemap/airpact_daily_basemap_O3_%05d.png','-b:v','5000k', output_dir+'movie_O3_daily_output.webm'])
# print('Videos made')
# =============================================================================

#%%
######################################
        # Plot folium
######################################
# =============================================================================
# m= folium.Map(location=[47.6588, -117.4260],zoom_start=9.25) # Create the plot
# =============================================================================
# =============================================================================
# m= folium.Map(location=[47.8313, -116.8732],zoom_start=13) # for PM
# =============================================================================
m= folium.Map(location=[47.6589, -117.4263],zoom_start=13) # for o3
m.add_child(folium.LatLngPopup()) #Add click lat/lon functionality

# mins and max's of the plot
lon_min=np.amin(airpact['lon'])
lat_min=np.amin(airpact['lat'])
lon_max=np.amax(airpact['lon'])
lat_max=np.amax(airpact['lat'])

extents = [[lat_min, lon_min], [lat_max, lon_max]]

# Set paths to monthly average maps
png1 = git_dir+'urbanova_basemap_'+str(end_month)+'_O3.png'
png2 = git_dir+'urbanova_basemap_'+str(end_month)+'_PMIJ.png'

# Set paths to videos
#video1 = git_dir+'movie_O3_daily_output.webm'
#video2 = git_dir+'movie_PMIJ_daily_output.webm'
# =============================================================================
# video3 = git_dir+'movie_O3_daily_tiled_output.webm'
# video4 = git_dir+'movie_PMIJ_daily_tiled_output.webm'
# =============================================================================

# Add monthly average maps to Folium
folium.raster_layers.ImageOverlay(png1,bounds = extents,name='Ozone',opacity = 0.5, show = True).add_to(m)
folium.raster_layers.ImageOverlay(png2,bounds = extents,name='PM',opacity = 0.5,show = False).add_to(m) #Unchecks the PM layer so that only ozone is seen

# Add videos to Folium
#folium.raster_layers.VideoOverlay(video_url=video1,bounds = extents,name='O3_video',opacity = 0.5,attr = 'O3_video_map',show = True,autoplay=True).add_to(m)
#folium.raster_layers.VideoOverlay(video_url=video2,bounds = extents,name='PM_video',opacity = 0.5,attr = 'pm_video_map',show = False,autoplay=True).add_to(m)
# =============================================================================
# folium.raster_layers.VideoOverlay(video_url=video3,bounds = extents,name='O3_timelapse_video',opacity = 0.5,attr = 'O3_tiled_video_map',show = True,autoplay=True).add_to(m)
# folium.raster_layers.VideoOverlay(video_url=video4,bounds = extents,name='PM_timelapse_video',opacity = 0.5,attr = 'pm_tiled_video_map',show = False,autoplay=True).add_to(m)
# =============================================================================

# Add ability to move between layers
folium.LayerControl().add_to(m)

# Save and show the created map. Use Jupyter to see the map within your console
m.save(output_dir+'urbanova_20190'+str(end_month)+'01.html')
m
print('done')


