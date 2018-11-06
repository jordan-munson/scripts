# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:58:32 2018

@author: Jordan Munson
"""
# Script to plot basemap PNG files to folium for presentation

#Import libraries
import matplotlib
matplotlib.use('Agg')  # Uncomment this when using in Kamiak/Aeolus
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

# Set file paths
base_dir=r'G:/Research/Urbanova_Jordan/'
output_dir = r'G:/Research/scripts/folium_files/'
git_dir = 'https://github.com/jordan-munson/scripts/raw/master/folium_files/'

# Set times
start_year = 2018
start_month = 1
start_day = 11

end_year = 2018
end_month = 1
#end_day = monthrange(end_year, end_month)[1]
end_day = 31

# set start and end date
start = datetime.datetime(start_year, start_month, start_day, hour=0)
end = datetime.datetime(end_year, end_month, end_day, hour=23)
timezone = pytz.timezone("utc")
start = timezone.localize(start)
end = timezone.localize(end)

# Load data
name =base_dir+ '1p33_'+start.strftime("%Y%m%d")+'_'+end.strftime("%Y%m%d")

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
unit_list = ["ppb", "$ug/m^3$"]

############################################
# Averaged domain basemaps       
############################################
#save maps into the pdf file (two maps in single page)
with PdfPages(base_dir+'maps/urbanova_avg_basemap_' + '_'+ start.strftime("%Y%m%d") + '-' +  end.strftime("%Y%m%d") + '.pdf') as pdf:
    
    for i, sp in enumerate(var_list):
        plt.style.use("dark_background")
        fig = plt.figure(figsize=(14,10))
        #plt.title(sp)
        o3_max = 45
        pm_max = 30
        o3_bins = np.arange(0, o3_max, 5)
        pm_bins = np.arange(0, pm_max, 3)
        # compute auto color-scale using maximum concentrations
        down_scale = np.percentile(airpact[sp], 5)
        up_scale = np.percentile(airpact[sp], 95)
        if sp == "O3":
            clevs = o3_bins
        else:
            clevs = pm_bins
        #clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
        print("debug clevs", clevs, sp)
        

        cs = m.contourf(x,y,airpact[sp].mean(axis=0),clevs,cmap=plt.get_cmap('jet'), extend='both')
        cs.cmap.set_under('cyan')
        cs.cmap.set_over('black')
        
        #m.drawcoastlines()
        #m.drawstates()
        #m.drawcountries()
        #m.drawcounties()
        #m.drawrivers()

        cblabel = unit_list[i]
        cbticks = True
        cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
        cbar.set_label(cblabel)
        
        #if cbticks:
        #    cbar.set_ticks(clevs)
        
        # print the surface-layer mean on the map plot
        #if sp == 'O3':
            #plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" ppb", xy=(0, 1.02), xycoords='axes fraction')
        #else:
            #plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" $ug/m^3$", xy=(0, 1.02), xycoords='axes fraction')
        outpng = base_dir +'maps/urbanova_basemap_' +str(end_month)+'_'+ sp + '.png'
        print(outpng)
        #fig.savefig(fig) 
        plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False)
        plt.show()
#%%
#base map
m = Basemap(projection='merc',
              llcrnrlon = lon[0,0], urcrnrlon = lon[90-1,90 -1], 
              llcrnrlat = lat[0,0], urcrnrlat = lat[90-1,90-1],
              resolution='h',
              area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
x,y = m(lon,lat)
var_list = ["O3", "PMIJ"]
unit_list = ["ppb", "$ug/m^3$"]
############################################
# hourly domain basemaps, this takes lots of time if doing hourly. Switch to daily could be prudent over a long timespan
############################################
#save maps into the pdf file (two maps in single page)

for i, sp in enumerate(var_list):
    
    for t in range(0, len(airpact[sp])): 
        plt.style.use("dark_background")
        outpng = base_dir +'maps/daily_basemap/airpact_hourly_basemap_' + sp + '_%05d.png' % t
        print(outpng)
        
        fig = plt.figure(figsize=(14,10))
        #plt.title('at ' + airpact["DateTime"][t,0,0])
        
        #o3_bins = np.arange(0, 45, 5)
        #pm_bins = np.arange(0, 12, 1.2)
        # compute auto color-scale using maximum concentrations
        down_scale = np.percentile(airpact[sp], 5)
        up_scale = np.percentile(airpact[sp], 95)
        if sp == "O3":
            clevs = o3_bins
        else:
            clevs = pm_bins
        #clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
        print("debug clevs", clevs, sp)
        
        print(unit_list[i], sp, t)

        cs = m.contourf(x,y,airpact[sp][t,:,:],clevs,cmap=plt.get_cmap('jet'), extend='both')
        cs.cmap.set_under('cyan')
        cs.cmap.set_over('black')
        
        #m.drawcoastlines()
        #m.drawstates()
        #m.drawcountries()
        
        cblabel = unit_list[i]
        cbticks = True
        cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
        cbar.set_label(cblabel)
        if cbticks:
            cbar.set_ticks(clevs)
        
        # print the surface-layer mean on the map plot
        plt.annotate("mean: " + str(airpact[sp][t,:,:].mean()) + " "+ unit_list[i] + ' at ' + airpact["DateTime"][t,0,0], xy=(0.02, 0.98), xycoords='axes fraction')
        
        plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False) 
        plt.show()
# This requires ffmpeg program, which is not easy to install in aeolus/kamiak
# To make a video, download all the pngs in your computer and execute the command below
# "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_PMIJ_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_PMIJ_output.webm" 
# "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_O3_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_O3_output.webm" 

# Attempt to run ffmpeg 
os.chdir('G:/Research/Urbanova_Jordan')
check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_hourly_basemap_PMIJ_%05d.png','-b:v','5000k', output_dir+'movie_PMIJ_output.webm'])
check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_hourly_basemap_O3_%05d.png','-b:v','5000k', output_dir+'movie_O3_output.webm'])
print('Videos made')
#%%

#base map
m = Basemap(projection='merc',
              llcrnrlon = lon[0,0], urcrnrlon = lon[90-1,90 -1], 
              llcrnrlat = lat[0,0], urcrnrlat = lat[90-1,90-1],
              resolution='h',
              area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
x,y = m(lon,lat)
var_list = ["O3", "PMIJ"]
unit_list = ["ppb", "$ug/m^3$"]
############################################
# hourly domain basemaps, this takes lots of time if doing hourly. Switch to daily could be prudent over a long timespan
############################################
#save maps into the pdf file (two maps in single page)

for i, sp in enumerate(var_list):
    
    for t in range(0, len(airpact[sp])): 
        plt.style.use("dark_background")
           
        outpng = base_dir +'maps/daily_basemap/airpact_hourly_basemap_tiled_' + sp + '_%05d.png' % t
        print(outpng)
        
        fig = plt.figure(figsize=(14,10))
        #plt.title('at ' + airpact["DateTime"][t,0,0])
        
        #o3_bins = np.arange(0, 45, 5)
        #pm_bins = np.arange(0, 12, 1.2)
        # compute auto color-scale using maximum concentrations
        down_scale = np.percentile(airpact[sp], 5)
        up_scale = np.percentile(airpact[sp], 95)
        vmin = 0
        if sp == "O3":
            clevs = o3_bins
            vmax = o3_max
        else:
            clevs = pm_bins
            vmax = pm_max
        #clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
        print("debug clevs", clevs, sp)
        
        print(unit_list[i], sp, t)

        #cs = m.contourf(x,y,airpact[sp][t,:,:],clevs,cmap=plt.get_cmap('jet'), extend='both')
        #cs.cmap.set_under('cyan')
        #cs.cmap.set_over('black')
        
        #m.drawcoastlines()
        #m.drawstates()
        #m.drawcountries()

        # These two lines below change the map to continuos. However this muddles the image
        cmap = plt.get_cmap('jet')
        colormesh = m.pcolormesh(x, y, airpact[sp][t,:,:], vmin = vmin,vmax=vmax, cmap=cmap)
        
        cblabel = unit_list[i]
        cbticks = True
        cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
        cbar.set_label(cblabel)
        if cbticks:
            cbar.set_ticks(clevs)
        
        # print the surface-layer mean on the map plot
        plt.annotate("mean: " + str(airpact[sp][t,:,:].mean()) + " "+ unit_list[i] + ' at ' + airpact["DateTime"][t,0,0], xy=(0.02, 0.98), xycoords='axes fraction')
        
        plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False) 
        plt.show()
# This requires ffmpeg program, which is not easy to install in aeolus/kamiak
# To make a video, download all the pngs in your computer and execute the command below
# "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_PMIJ_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_PMIJ_output.webm" 
# "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_O3_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_O3_output.webm" 

# Attempt to run ffmpeg 
os.chdir('G:/Research/Urbanova_Jordan')
check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_hourly_basemap_tiled_PMIJ_%05d.png','-b:v','5000k', output_dir+'movie_PMIJ_tiled_output.webm'])
check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_hourly_basemap_tiled_O3_%05d.png','-b:v','5000k', output_dir+'movie_O3_tiled_output.webm'])
print('Videos made')

#%%
######################################
        # Plot folium
######################################
m= folium.Map(location=[47.6588, -117.4260],zoom_start=9.25) # Create the plot
m.add_child(folium.LatLngPopup()) #Add click lat/lon functionality

# mins and max's of the plot
lon_min=np.amin(airpact['lon'])
lat_min=np.amin(airpact['lat'])
lon_max=np.amax(airpact['lon'])
lat_max=np.amax(airpact['lat'])

extents = [[lat_min, lon_min], [lat_max, lon_max]]

# Set paths to monthly average maps
png1 = base_dir+'maps/urbanova_basemap_1_O3.png'
png2 = base_dir+'maps/urbanova_basemap_1_PMIJ.png'

# Set paths to videos
video1 = git_dir+'movie_O3_output.webm'
video2 = git_dir+'movie_PMIJ_output.webm'
video3 = git_dir+'movie_O3_tiled_output.webm'
video4 = git_dir+'movie_PMIJ_tiled_output.webm'
#video1 = output_dir+'movie_O3_output.webm'
#video2 = output_dir+'movie_PMIJ_output.webm'
#video3 = output_dir+'movie_O3_tiled_output.webm'
#video4 = output_dir+'movie_PMIJ_tiled_output.webm'

# Add monthly average maps to Folium
folium.raster_layers.ImageOverlay(png1,bounds = extents,name='Ozone',opacity = 0.5, show = False).add_to(m)
folium.raster_layers.ImageOverlay(png2,bounds = extents,name='PM',opacity = 0.5,show = False).add_to(m) #Unchecks the PM layer so that only ozone is seen

# Add videos to Folium
folium.raster_layers.VideoOverlay(video_url=video1,bounds = extents,name='O3_video',opacity = 0.5,attr = 'O3_video_map',show = True,autoplay=True).add_to(m)
folium.raster_layers.VideoOverlay(video_url=video2,bounds = extents,name='PM_video',opacity = 0.5,attr = 'pm_video_map',show = False,autoplay=True).add_to(m)
folium.raster_layers.VideoOverlay(video_url=video3,bounds = extents,name='O3_tiled_video',opacity = 0.5,attr = 'O3_tiled_video_map',show = False,autoplay=True).add_to(m)
folium.raster_layers.VideoOverlay(video_url=video4,bounds = extents,name='PM_tiled_video',opacity = 0.5,attr = 'pm_tiled_video_map',show = False,autoplay=True).add_to(m)

# Add ability to move between layers
folium.LayerControl().add_to(m)

# Save and show the created map. Use Jupyter to see the map within your console
m.save(output_dir+'folium_ozone_pm_map.html')
m
print('done')


