# Script modified off of Kai Fans script
import matplotlib
matplotlib.use('Agg')  # Uncomment this when using in Kamiak/Aeolus
import pandas as pd
import numpy as np
import time
import datetime
from datetime import timedelta
import pytz
import os
from netCDF4 import Dataset
import copy
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
from matplotlib import dates
from matplotlib.dates import date2num, DayLocator, DateFormatter
from calendar import monthrange
import pickle
#import simplekml

# Set file paths
base_dir=r'E:\Research\Urbanova_Jordan/'
data_dir=r'E:\Research\Urbanova_Jordan\Urbanova_ref_site_comparison\Urbanova/'
grid_dir_4km=r'E:\Research\Urbanova_Jordan\Urbanova_ref_site_comparison\AIRPACT\2018\2018011100\MCIP37/'
grid_dir_urb=r'E:\Research\Urbanova_Jordan\Urbanova_ref_site_comparison\Urbanova/2018\2018011100\MCIP37/'
urb_path = data_dir
airpact_path = r'E:\Research\Urbanova_Jordan\Urbanova_ref_site_comparison\AIRPACT/'
regrid_path = r'E:\Research\Urbanova_Jordan\Urbanova_regrid4km/'
exec(open(r"E:/Research/scripts/Urbanova/airpact_functions.py").read())

filetype = 'not_aconc' # needed for airpact_functions script. use 'aconc' for lots of species

#base_dir = '/data/lar/users/jmunson/'
#data_dir = '/data/lar/projects/Urbanova/'
#grid_dir_urb = '/data/lar/projects/Urbanova/2018/2018011100/MCIP37/'
#grid_dir_4km='/data/airpact5/AIRRUN/2018/2018011100/MCIP37/'
#urb_path = '/data/lar/projects/Urbanova/'
#airpact_path = '/data/airpact5/saved/'
#regrid_path = '/data/lar/projects/Urbanova_output/Urbanova_regrid4km/'

start_year = 2018
start_month = 2
start_day = 14

end_year = 2018
end_month = 2
#end_day = monthrange(end_year, end_month)[1]
end_day = 14

# set start and end date
start = datetime.datetime(start_year, start_month, start_day, hour=0)
end = datetime.datetime(end_year, end_month, end_day, hour=23)
timezone = pytz.timezone("utc")
start = timezone.localize(start)
end = timezone.localize(end)
# set layer
layer=0

#Set up date diff for time loop
date_diff =end -start
date_diff =  int(round( date_diff.total_seconds()/60/60/24)) # total hour duration
print("start date is "+ start.strftime("%Y%m%d") + ' combining 4km files' )
now = start

modeloutputs = []
#modeloutputs.append(r'E:\Research\Urbanova_Jordan\Urbanova_regrid4km/combined_' + now.strftime('%Y%m%d')+'.regrid4km.ncf')
modeloutputs.append(airpact_path + now.strftime('%Y')+'/'+now.strftime('%m')+'/aconc/combined_' + now.strftime('%Y%m%d')+'.ncf')
print(modeloutputs)
now += timedelta(hours=24)
# For loop to find the combined3D files for specified time period
for t in range(0, date_diff):
    
    # Handles missing days
    if os.path.isfile(regrid_path + 'combined_' + now.strftime('%Y%m%d')+'.regrid4km.ncf'):
        # set a directory containing Urbanova data
        modeloutputs.append(airpact_path + now.strftime('%Y')+'/'+now.strftime('%m')+'/aconc/combined_' + now.strftime('%Y%m%d')+'.ncf')
        #Changes day to next
        now += timedelta(hours=24)            
    else:
        print('adding 24 hours')
        now += timedelta(hours=24)
'''
    if os.path.isfile(regrid_path + 'combined_' + now.strftime('%Y%m%d')+'.regrid4km.ncf'):
        # set a directory containing Urbanova data
        modeloutputs.append(airpact_path + now.strftime('%Y')+'/'+now.strftime('%m')+'/aconc/combined_' + now.strftime('%Y%m%d')+'.ncf')
        #Changes day to next
        now += timedelta(hours=24)            
    else:
        print('adding 24 hours')
        now += timedelta(hours=24)
'''
print('4km file paths arrayed')

print(modeloutputs)

# open and read wrfout using netCDF function (Dataset)
if os.path.isfile(modeloutputs[0]):
    nc  = Dataset(modeloutputs[0], 'r')
    print('reading ', modeloutputs[0])
else:
    print("no file")
    exit()
    
# x_dim and y_dim are the x (lon) and y (lat) dimensions of the model
x_dim = len(nc.dimensions['COL'])
y_dim = len(nc.dimensions['ROW'])
nc.close()

# obtain model lat and lon - needed for AQS eval and basemap
latlon = grid_dir_4km+"/GRIDCRO2D"
fin0 = Dataset(latlon, 'r')
lat = fin0.variables['LAT'][0,0]
lon = fin0.variables['LON'][0,0]
w = (fin0.NCOLS)*(fin0.XCELL)
h = (fin0.NROWS)*(fin0.YCELL)
lat_0 = fin0.YCENT
lon_0 = fin0.XCENT
fin0.close()

airpact_3d = get_airpact_DF(start, end, layer)
print(airpact_3d.keys())
print(airpact_3d['PMIJ'].shape)
print(airpact_3d['DateTime'].shape)
print(airpact_3d['lat'].shape)

airpact_3d['lat'] = airpact_3d['lat'][:,186:216,136:166]
airpact_3d['lon'] = airpact_3d['lon'][:,186:216,136:166]
airpact_3d['PMIJ'] = airpact_3d['PMIJ'][:,186:216,136:166]
airpact_3d['O3'] = airpact_3d['O3'][:,186:216,136:166]
airpact_3d['DateTime'] = airpact_3d['DateTime'][:,186:216,136:166]
airpact_2d = airpact_3d

#%%

date_diff =end -start
date_diff =  int(round( date_diff.total_seconds()/60/60/24)) # total hour duration
print("start date is "+ start.strftime("%Y%m%d") + ' catting regrid files' )
now = start

modeloutputs = []
modeloutputs.append(regrid_path + 'combined_' + now.strftime('%Y%m%d')+'.regrid4km.ncf')
print(modeloutputs)
now += timedelta(hours=24)
# For loop to find the combined3D files for specified time period

for t in range(0, date_diff):
    
    # Handles missing days
    if os.path.isfile(regrid_path + 'combined_' + now.strftime('%Y%m%d')+'.regrid4km.ncf'):
        # set a directory containing Urbanova data
        modeloutputs.append(regrid_path + 'combined_' + now.strftime('%Y%m%d')+'.regrid4km.ncf')
        #Changes day to next
        now += timedelta(hours=24)            
    else:
        print('adding 24 hours')
        now += timedelta(hours=24) 
        
print(modeloutputs)

print('Regrid finished')

#print(modeloutputs)

# open and read wrfout using netCDF function (Dataset)
if os.path.isfile(modeloutputs[0]):
    nc  = Dataset(modeloutputs[0], 'r')
    print('reading ', modeloutputs[0])
else:
    print("no file")
    exit()
    
# x_dim and y_dim are the x (lon) and y (lat) dimensions of the model
x_dim = len(nc.dimensions['COL'])
y_dim = len(nc.dimensions['ROW'])
nc.close()

# obtain model lat and lon - needed for AQS eval and basemap
latlon = grid_dir_urb+"/GRIDCRO2D"
fin0 = Dataset(latlon, 'r')
lat = fin0.variables['LAT'][0,0]
lon = fin0.variables['LON'][0,0]
w = (fin0.NCOLS)*(fin0.XCELL)
h = (fin0.NROWS)*(fin0.YCELL)
lat_0 = fin0.YCENT
lon_0 = fin0.XCENT
fin0.close()

#Drop rows and columns to make lat/lon coordinates match
lat = lat[1::3, 1::3]
lon = lon[1::3, 1::3]

airpact_3d = get_airpact_DF(start, end, layer)
print(airpact_3d.keys())
print(airpact_3d['PMIJ'].shape)
print(airpact_3d['DateTime'].shape)
print(airpact_3d['lat'].shape)

name = base_dir+'1p33_regrid4km_'+start.strftime("%Y%m%d")+'_'+end.strftime("%Y%m%d")+'_PST'
def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
airpact = load_obj(name)
#base map
m = Basemap(projection='lcc', width=w, height=h, lat_0=lat_0, lon_0=lon_0,
              llcrnrlon = lon[0,0], urcrnrlon = lon[30-1,30 -1], 
              llcrnrlat = lat[0,0], urcrnrlat = lat[30-1,30-1],
              resolution='h', area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
x,y = m(lon,lat)
var_list = ["O3", "PMIJ"]
unit_list = ["ppb", "$ug/m^3$"]
airpact = airpact_3d
airpact['O3'] =  airpact_3d['O3']-airpact_2d['O3']
airpact['PMIJ'] =  airpact_3d['PMIJ'] - airpact_2d['PMIJ']

#%%
############################################
# hourly domain basemaps
############################################

# =============================================================================
# #save maps into the pdf file (two maps in single page)
# from subprocess import check_call
# for i, sp in enumerate(var_list):
#     
#     for t in range(0, len(airpact_3d[sp])): 
#             
#         outpng = base_dir +'outputs/airpact_hourly_basemap_' + sp + '_%05d.png' % t
#         print(outpng)
#         
#         fig = plt.figure(figsize=(14,10))
#         plt.title(sp +'_at_' + airpact_3d["DateTime"][t,0,0])
#         
#         # compute auto color-scale using maximum concentrations
#         down_scale = np.percentile(airpact_3d[sp], 5)
#         up_scale = np.percentile(airpact_3d[sp], 95)
#         clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
#         print("debug clevs", clevs, sp)
#         
#         cblabel = unit_list[i]
#         print(unit_list[i], sp, t)
#         cbticks = True
#         cs = m.contourf(x,y,airpact_3d[sp][t,:,:],clevs,cmap=plt.get_cmap('jet'), extend='both')
#         cs.cmap.set_under('cyan')
#         cs.cmap.set_over('black')
#         
#         m.drawcoastlines()
#         m.drawstates()
#         m.drawcountries()
#         
#         cbar = m.colorbar(location='bottom',pad="5%")
#         cbar.set_label(cblabel)
#         if cbticks:
#             cbar.set_ticks(clevs)
#         
#         # print the surface-layer mean on the map plot
#         plt.annotate("mean: " + str(airpact_3d[sp][t,:,:].mean()) + " "+ unit_list[i], xy=(0, 1.02), xycoords='axes fraction')
#         
#         plt.savefig(outpng) 
#         plt.show()
# # This requires ffmpeg program, which is not easy to install in aeolus/kamiak
# # To make a video, download all the pngs in your computer and execute the command below
# # "ffmpeg -framerate 3 -i WRFChem_hourly_basemap_T2_%05d.png T2_output.mp4" 
# #        
# #    check_call(["ffmpeg", "-framerate", "3", "-i", "outputs/WRFChem_hourly_basemap_"+sp+ "_%05d.png",  "outputs/"+sp + "_output.mp4"])
# =============================================================================

#Delta map
############################################
# Delta averaged domain basemaps          Positive values represent an overestimation from 1p33km. The maps are sp33km-4km
############################################
#save maps into the pdf file (two maps in single page)
with PdfPages(base_dir+'maps/delta_avg_basemap_' + '_'+ start.strftime("%Y%m%d") + '-' +  end.strftime("%Y%m%d") + '.pdf') as pdf:
    
    for i, sp in enumerate(var_list):
        
        fig = plt.figure(figsize=(14,10))
        plt.title(sp)
        
        # compute auto color-scale using maximum concentrations
        down_scale = np.percentile(airpact[sp], 5)
        up_scale = np.percentile(airpact[sp], 95)
        if sp == "O3":
            clevs = [-4,-3,-2,-1,0,1,2,3,4,5]
            vmin = -4
            vmax = 5
        else:
            clevs = [-1.2,-.8,-.4,0,.4,.8,1.2]
            vmin = -1.2
            vmax = 1.2
        #clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
        print("debug clevs", clevs, sp)
        
        cblabel = unit_list[i]
        cbticks = True
# =============================================================================
#         #Contour way
#         cs = m.contourf(x,y,airpact[sp].mean(axis=0),clevs,cmap=plt.get_cmap('jet'), extend='both')
#         cs.cmap.set_under('cyan')
#         cs.cmap.set_over('black')
# =============================================================================
        
        # Colormesh way
        cmap = plt.get_cmap('jet')
        colormesh = m.pcolormesh(x, y, airpact[sp].mean(axis=0), vmin = vmin,vmax=vmax, cmap=cmap)
        colormesh.cmap.set_over('black')
        
        #m.drawcoastlines()
        #m.drawstates()
       # m.drawcountries()
        m.drawcounties()
        cbar = m.colorbar(location='bottom',pad="5%")
        cbar.set_label(cblabel)
        if cbticks:
            cbar.set_ticks(clevs)
        
        # print the surface-layer mean on the map plot
        #if sp == 'O3':
            #plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" ppb", xy=(0, 1.02), xycoords='axes fraction')
        #else:
            #plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" $ug/m^3$", xy=(0, 1.02), xycoords='axes fraction')
        outpng = base_dir +'maps/delta_basemap_' +str(end_month)+'_'+ sp + '.png'
        print(outpng)
        #fig.savefig(fig) 
        plt.savefig(outpng)
        plt.show()
''' 
# Ratio map       
airpact['O3'] =  airpact_3d['O3']/airpact_2d['O3']
airpact['PMIJ'] =  airpact_3d['PMIJ']/airpact_2d['PMIJ']
############################################
# averaged domain basemaps          Positive values represent an overestimation from 1p33km. The maps are 1p33km/4km
############################################
#save maps into the pdf file (two maps in single page)
with PdfPages(base_dir+'maps/ratio_avg_basemap_' + '_'+ start.strftime("%Y%m%d") + '-' +  end.strftime("%Y%m%d") + '.pdf') as pdf:
    
    for i, sp in enumerate(var_list):
        
        fig = plt.figure(figsize=(14,10))
        plt.title(sp)
        
        # compute auto color-scale using maximum concentrations
        down_scale = np.percentile(airpact[sp], 5)
        up_scale = np.percentile(airpact[sp], 95)
        clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
        print("debug clevs", clevs, sp)
        
        cblabel = unit_list[i]
        cbticks = True
        cs = m.contourf(x,y,airpact[sp].mean(axis=0),clevs,cmap=plt.get_cmap('jet'), extend='both')
        cs.cmap.set_under('cyan')
        cs.cmap.set_over('black')
        
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()
#        m.drawcounties()
        cbar = m.colorbar(location='bottom',pad="5%")
        cbar.set_label(cblabel)
        if cbticks:
            cbar.set_ticks(clevs)
        
        # print the surface-layer mean on the map plot
        if sp == 'O3':
            plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" ppb", xy=(0, 1.02), xycoords='axes fraction')
        else:
            plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" $ug/m^3$", xy=(0, 1.02), xycoords='axes fraction')
        
        pdf.savefig(fig) 
        plt.show()
'''        


# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 10:55:17 2018

Script from Kai Fan to turn PNG into google maps
"""


from simplekml import (Kml, OverlayXY, ScreenXY, Units, RotationXY,AltitudeMode, Camera)


def make_kml(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat,
             figs, colorbar=None, **kw):
    """TODO: LatLon bbox, list of figs, optional colorbar figure,
    and several simplekml kw..."""

    kml = Kml()
    altitude = kw.pop('altitude', 2e7)
    roll = kw.pop('roll', 0)
    tilt = kw.pop('tilt', 0)
    altitudemode = kw.pop('altitudemode', AltitudeMode.relativetoground)
    camera = Camera(latitude=np.mean([urcrnrlat, llcrnrlat]),
                    longitude=np.mean([urcrnrlon, llcrnrlon]),
                    altitude=altitude, roll=roll, tilt=tilt,
                    altitudemode=altitudemode)

    kml.document.camera = camera
    draworder = 0
    for fig in figs:  # NOTE: Overlays are limited to the same bbox.
        draworder += 1
        ground = kml.newgroundoverlay(name='GroundOverlay')
        ground.draworder = draworder
        ground.visibility = kw.pop('visibility', 1)
        ground.name = kw.pop('name', fig[-6:-4])
        ground.color = kw.pop('color', '9effffff')
        ground.atomauthor = kw.pop('author', 'ocefpaf')
        ground.latlonbox.rotation = kw.pop('rotation', 0)
        ground.description = kw.pop('description', 'Matplotlib figure')
        ground.gxaltitudemode = kw.pop('gxaltitudemode',
                                       'clampToSeaFloor')
        ground.icon.href = fig
        ground.latlonbox.east = llcrnrlon
        ground.latlonbox.south = llcrnrlat
        ground.latlonbox.north = urcrnrlat
        ground.latlonbox.west = urcrnrlon

    if colorbar:  # Options for colorbar are hard-coded (to avoid a big mess).
        screen = kml.newscreenoverlay(name='ScreenOverlay')
        screen.icon.href = colorbar
        screen.overlayxy = OverlayXY(x=0, y=0,
                                     xunits=Units.fraction,
                                     yunits=Units.fraction)
        screen.screenxy = ScreenXY(x=0.015, y=0.075,
                                   xunits=Units.fraction,
                                   yunits=Units.fraction)
        screen.rotationXY = RotationXY(x=0.5, y=0.5,
                                       xunits=Units.fraction,
                                       yunits=Units.fraction)
        screen.size.x = 0
        screen.size.y = 0
        screen.size.xunits = Units.fraction
        screen.size.yunits = Units.fraction
        screen.visibility = 1

    kmzfile = kw.pop('kmzfile', 'overlay.kmz')
    kml.savekmz(kmzfile)

import numpy as np
import matplotlib.pyplot as plt

def gearth_fig(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, pixels=1024):
    """Return a Matplotlib `fig` and `ax` handles for a Google-Earth Image."""
    aspect = np.cos(np.mean([llcrnrlat, urcrnrlat]) * np.pi/180.0)
    xsize = np.ptp([urcrnrlon, llcrnrlon]) * aspect
    ysize = np.ptp([urcrnrlat, llcrnrlat])
    aspect = ysize / xsize

    if aspect > 1.0:
        figsize = (10.0 / aspect, 10.0)
    else:
        figsize = (10.0, 10.0 * aspect)

    if False:
        plt.ioff()  # Make `True` to prevent the KML components from poping-up.
    fig = plt.figure(figsize=figsize,
                     frameon=False,
                     dpi=pixels//10)
    # KML friendly image.  If using basemap try: `fix_aspect=False`.
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(llcrnrlon, urcrnrlon)
    ax.set_ylim(llcrnrlat, urcrnrlat)
    return fig, ax

#base_dir='/Users/fankai/'

#lat=lat.flatten()
#lon=lon.flatten()
#lat, lon = np.meshgrid(lat, lon)

import numpy.ma as ma
#from palettable import colorbrewer


import glob
figures=glob.glob(r'E:\Research\Urbanova_Jordan\maps/'+'*.png')
    
make_kml(llcrnrlon=lon.min(),
         llcrnrlat=lat.min(),
         urcrnrlon=lon.max(),
         urcrnrlat=lat.max(),
         figs=figures,# colorbar=base_dir+'legend.png',
         kmzfile=base_dir+'6.kmz') 
print('End of script')


