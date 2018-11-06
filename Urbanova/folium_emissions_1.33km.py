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
name =base_dir+ '1p33_emissions_'+start.strftime("%Y%m%d")+'_'+end.strftime("%Y%m%d")

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
airpact = load_obj(name)

# Create NOX from NO and NO2
airpact['NOX'] = airpact['NO2']+airpact['NO']

# obtain model lat and lon - needed for AQS eval and basemap
lat = airpact['lat'][0]
lon = airpact['lon'][0]

# Create list of species to iterate over in the for loops
var_list = ["CO", "PM10", 'BENZENE','PMFINE','NOX']
unit_list = ["moles/h", "$g/h$","moles/h","$g/h$","moles/h"]

#Convert from units/second to units/hour to make visualization easier
for sp in var_list:
    airpact[sp] = airpact[sp]*3600
#%%
#base map
m = Basemap(projection='merc',
              llcrnrlon = lon[0,0], urcrnrlon = lon[90-1,90 -1], 
              llcrnrlat = lat[0,0], urcrnrlat = lat[90-1,90-1],
              resolution='h',
              area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
x,y = m(lon,lat)

############################################
# Averaged domain basemaps       
############################################

# Set the colorbar values
CO_max = np.amax(airpact['CO']) # find max conc value
pm_max = np.amax(airpact['PM10'])
benz_max = np.amax(airpact['BENZENE'])
pmf_max = np.amax(airpact['PMFINE'])
nox_max = np.amax(airpact['NOX'])

intervals = 12 # set desired interval number

CO_steps = CO_max/intervals # Calculate necessary step amount to get correct interval
pm_steps = pm_max/intervals
benz_steps = benz_max/intervals
pmf_steps = pmf_max/intervals
nox_steps = nox_max/intervals

CO_bins = np.arange(0, CO_max, CO_steps) # create the bins the colorbars are made from using previous calculated variables
pm_bins = np.arange(0, pm_max, pm_steps)
benz_bins = np.arange(0, benz_max, benz_steps)
pmf_bins = np.arange(0, pmf_max, pmf_steps)
nox_bins = np.arange(0, nox_max, nox_steps)

#save maps into the pdf file (two maps in single page)
with PdfPages(base_dir+'maps/urbanova_emissions_avg_basemap_' + '_'+ start.strftime("%Y%m%d") + '-' +  end.strftime("%Y%m%d") + '.pdf') as pdf:
    
    for i, sp in enumerate(var_list):
        plt.style.use("dark_background")
        
        fig = plt.figure(figsize=(14,10))
        #plt.title(sp)

        # compute auto color-scale using maximum concentrations
        down_scale = np.percentile(airpact[sp], 5)
        up_scale = np.percentile(airpact[sp], 95)
        vmin = 0
        if sp == "CO":
            clevs = CO_bins
            vmax = CO_max
        elif sp == 'BENZENE':
            clevs = benz_bins
            vmax = benz_max
        elif sp == 'PMFINE':
            clevs = pmf_bins
            vmax = pmf_max
        elif sp == 'NOX':
            clevs = nox_bins
            vmax = nox_max
        else:
            clevs = pm_bins
            vmax = pm_max
        #clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
        print("debug clevs", clevs, sp)
        
        cmap = plt.get_cmap('jet')
        colormesh = m.pcolormesh(x, y, airpact[sp][:,:,:].mean(axis=0), vmin = vmin,vmax=vmax, cmap=cmap)
        #cs = m.contourf(x,y,airpact[sp].mean(axis=0),clevs,cmap=plt.get_cmap('jet'), extend='both')
        #cs.cmap.set_under('cyan')
        #cs.cmap.set_over('black')
        
        #m.drawcoastlines()
        #m.drawstates()
        #m.drawcountries()
        #m.drawcounties()
        #m.drawrivers()

        cblabel = sp + ' (' + unit_list[i] +')'
        cbticks = True
        cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
        cbar.set_label(cblabel)
        #cbar.outline.set_edgecolor('white')
        #cbar.outline.set_linewidth(2)
        
        #cbaxes=fig.add_axes([0.8,0.1,0.03,0.8])
        #cbaxes.tick_params(axis='both', colors='white')
     
        
        # print the surface-layer mean on the map plot
        #if sp == 'CO':
            #plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" moles/s", xy=(0, 1.02), xycoords='axes fraction')
        #else:
            #plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" $g/s$", xy=(0, 1.02), xycoords='axes fraction')
        outpng = base_dir +'maps/urbanova_emissions_basemap_' +str(end_month)+'_'+ sp + '.png'
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
os.chdir('G:/Research/Urbanova_Jordan') # needed for ffmpeg
############################################
# hourly domain basemaps, this takes lots of time if doing hourly. Switch to daily could be prudent over a long timespan
############################################
#save maps into the pdf file (two maps in single page)

for i, sp in enumerate(var_list):
    
    for t in range(0, len(airpact[sp])): 
            
        outpng = base_dir +'maps/daily_basemap/airpact_emissions_hourly_basemap_' + sp + '_%05d.png' % t
        print(outpng)
        plt.style.use("dark_background")        
        fig = plt.figure(figsize=(14,10))

        #plt.title('at ' + airpact["DateTime"][t,0,0])
        
        #CO_bins = np.arange(0, 45, 5)
        #pm_bins = np.arange(0, 12, 1.2)
        # compute auto color-scale using maximum concentrations
        down_scale = np.percentile(airpact[sp], 5)
        up_scale = np.percentile(airpact[sp], 95)
        if sp == "CO":
            clevs = CO_bins
        elif sp == 'BENZENE':
            clevs = benz_bins
        elif sp == 'PMFINE':
            clevs = pmf_bins
        elif sp == 'NOX':
            clevs = nox_bins
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
        
        cblabel = sp + ' (' + unit_list[i] +')'
        cbticks = True
        cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
        cbar.set_label(cblabel)
        if cbticks:
            cbar.set_ticks(clevs)
        
        # print the surface-layer mean on the map plot
        plt.annotate("mean: " + str(airpact[sp][t,:,:].mean()) + " "+ unit_list[i] + ' at ' + airpact["DateTime"][t,0,0], xy=(0, 0.98), xycoords='axes fraction')
        
        plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False) 
        plt.show()
    check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_emissions_hourly_basemap_'+sp+'_%05d.png','-b:v','5000k', output_dir+'movie_'+sp+'_output.webm'])

# This requires ffmpeg program, which is not easy to install in aeolus/kamiak
# To make a video, download all the pngs in your computer and execute the command below
# "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_PM10_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_PM10_output.webm" 
# "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_CO_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_CO_output.webm" 

# Attempt to run ffmpeg 

#check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_emissions_hourly_basemap_PM10_%05d.png','-b:v','5000k', output_dir+'movie_PM10_output.webm'])
#check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_emissions_hourly_basemap_CO_%05d.png','-b:v','5000k', output_dir+'movie_CO_output.webm'])
print('Contourf done')
#%%

#base map
m = Basemap(projection='merc',
              llcrnrlon = lon[0,0], urcrnrlon = lon[90-1,90 -1], 
              llcrnrlat = lat[0,0], urcrnrlat = lat[90-1,90-1],
              resolution='h',
              area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
x,y = m(lon,lat)
############################################
# hourly domain basemaps, this takes lots of time if doing hourly. Switch to daily could be prudent over a long timespan
############################################
#save maps into the pdf file (two maps in single page)

for i, sp in enumerate(var_list):
    
    for t in range(0, len(airpact[sp])): 
        plt.style.use("dark_background")            
        outpng = base_dir +'maps/daily_basemap/airpact_emissions_hourly_basemap_tiled_' + sp + '_%05d.png' % t
        print(outpng)
        
        fig = plt.figure(figsize=(14,10))
        #plt.title('at ' + airpact["DateTime"][t,0,0])
        
        #CO_bins = np.arange(0, 45, 5)
        #pm_bins = np.arange(0, 12, 1.2)
        # compute auto color-scale using maximum concentrations
        down_scale = np.percentile(airpact[sp], 5)
        up_scale = np.percentile(airpact[sp], 95)
        vmin = 0
        if sp == "CO":
            clevs = CO_bins
            vmax = CO_max
        elif sp == 'BENZENE':
            clevs = benz_bins
            vmax = benz_max
        elif sp == 'PMFINE':
            clevs = pmf_bins
            vmax = pmf_max
        elif sp == 'NOX':
            clevs = nox_bins
            vmax = nox_max
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

        # These two lines below change the map colormesh, which shows the grid
        cmap = plt.get_cmap('jet')
        colormesh = m.pcolormesh(x, y, airpact[sp][t,:,:], vmin = vmin,vmax=vmax, cmap=cmap)
        
        cblabel = sp + ' (' + unit_list[i] +')'
        cbticks = True
        cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
        cbar.set_label(cblabel)
        #if cbticks:
        #    cbar.set_ticks(clevs)
        
        # print the surface-layer mean on the map plot
        plt.annotate("mean: " + str(airpact[sp][t,:,:].mean()) + " "+ unit_list[i] + ' at ' + airpact["DateTime"][t,0,0], xy=(0, 0.98), xycoords='axes fraction')
        
        plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False) 
        plt.show()
    check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_emissions_hourly_basemap_tiled_'+sp+'_%05d.png','-b:v','5000k', output_dir+'movie_'+sp+'_tiled_output.webm'])

# This requires ffmpeg program, which is not easy to install in aeolus/kamiak
# To make a video, download all the pngs in your computer and execute the command below
# "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_PM10_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_PM10_output.webm" 
# "ffmpeg -y -framerate 10 -i G:\Research\Urbanova_Jordan\maps\daily_basemap\airpact_hourly_basemap_CO_%05d.png -b:v 5000k G:\Research\Urbanova_Jordan\maps\daily_basemap\movie_CO_output.webm" 

# Attempt to run ffmpeg 
#os.chdir('G:/Research/Urbanova_Jordan')
#check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_emissions_hourly_basemap_tiled_PM10_%05d.png','-b:v','5000k', output_dir+'movie_PM10_tiled_output.webm'])
#check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_emissions_hourly_basemap_tiled_CO_%05d.png','-b:v','5000k', output_dir+'movie_CO_tiled_output.webm'])
print('Colormesh done')

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

for sp in var_list:
    print('Plotting '+sp+' to Folium map')
    # Name variables
#    check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_emissions_hourly_basemap_'+sp+'_%05d.png','-b:v','5000k', output_dir+'movie_'+sp+'_output.webm'])
#    check_call(['ffmpeg', '-y', '-framerate','10', '-i',base_dir+'maps/daily_basemap/airpact_emissions_hourly_basemap_tiled_'+sp+'_%05d.png','-b:v','5000k', output_dir+'movie_'+sp+'_tiled_output.webm'])
    png = base_dir+'maps/urbanova_emissions_basemap_1_'+sp+'.png'
    video1 = git_dir+'movie_'+sp+'_output.webm'
    video2 = git_dir+'movie_'+sp+'_tiled_output.webm'
    
    #Plot average map
    folium.raster_layers.ImageOverlay(png,bounds = extents,name=sp,opacity = 0.5, show = False).add_to(m)
    
    #Plot countourf video
    folium.raster_layers.VideoOverlay(video_url=video1,bounds = extents,name=sp+'_video',opacity = 0.5,attr = sp+'_video_map',show = False,autoplay=True).add_to(m)
    #Plot colormap video
    folium.raster_layers.VideoOverlay(video_url=video2,bounds = extents,name=sp+'_tiled_video',opacity = 0.5,attr = sp+'_tiled_video_map',show = False,autoplay=True).add_to(m)

# Add ability to move between layers
folium.LayerControl().add_to(m)

# Save and show the created map. Use Jupyter to see the map within your console
m.save(output_dir+'folium_emissions_map.html')
m
print('done')


