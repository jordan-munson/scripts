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

# Set file paths
base_dir=r'E:\Research\Urbanova_Jordan/'
data_dir=r'E:\Research\Urbanova_Jordan\Urbanova_ref_site_comparison\Urbanova/'
#grid_dir=r'E:\Research\Urbanova_Jordan\Urbanova_ref_site_comparison\AIRPACT\2018\2018011100\MCIP37/'
grid_dir=r'E:\Research\Urbanova_Jordan\Urbanova_ref_site_comparison\Urbanova/2018\2018011100\MCIP37/'

#base_dir = '/data/lar/users/jmunson/'
#ata_dir = '/data/lar/projects/Urbanova/'
#grid_dir = '/data/lar/projects/Urbanova/2018/2018011100/MCIP37/'

exec(open(r"E:/Research/scripts/Urbanova/airpact_functions.py").read())
# set start and end date
start = datetime.datetime(year=2018, month=2, day=13, hour=0)
end = datetime.datetime(year=2018, month=2, day=14, hour=23)
timezone = pytz.timezone("utc")
start = timezone.localize(start)
end = timezone.localize(end)
# set layer
layer=0
filetype = 'not_aconc'
#Set up date diff for time loop
date_diff =end -start
date_diff =  int(round( date_diff.total_seconds()/60/60/24)) # total hour duration
print("start date is "+ start.strftime("%Y%m%d") )
now = start

modeloutputs = []
#modeloutputs.append(data_dir + str(start.year) + "/" + now.strftime('%Y%m%d') + "00/POST/CCTM"+"/combined3d_" + now.strftime('%Y%m%d') + '.ncf')
modeloutputs.append(r'E:\Research\Urbanova_Jordan\Urbanova_regrid4km/combined_' + now.strftime('%Y%m%d')+'.regrid4km.ncf')

now += timedelta(hours=24)
# For loop to find the combined3D files for specified time period
for t in range(0, date_diff):
    
    # Handles missing days
    if os.path.isfile(r'E:\Research\Urbanova_Jordan\Urbanova_regrid4km/combined_' + now.strftime('%Y%m%d')+'.regrid4km.ncf'):
        # set a directory containing Urbanova data
        modeloutputs.append(r'E:\Research\Urbanova_Jordan\Urbanova_regrid4km/combined_' + now.strftime('%Y%m%d')+'.regrid4km.ncf')
        #Changes day to next
        now += timedelta(hours=24)            
    else:
        print('adding 24 hours')
        now += timedelta(hours=24)
#    try:
#        os.path.isfile(data_dir + str(start.year) + "/" + now.strftime('%Y%m%d') + "00/POST/CCTM"+"/combined3d_" + now.strftime('%Y%m%d') + '.ncf')
#    except:
#        print('adding another 24 hours')
#        now += timedelta(hours=24)

print('AIRNOW data concatenated')

print(modeloutputs)
#%%
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
latlon = grid_dir+"/GRIDCRO2D"
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
#base map
m = Basemap(projection='lcc', width=w, height=h, lat_0=lat_0, lon_0=lon_0,
              llcrnrlon = lon[0,0], urcrnrlon = lon[30-1,30 -1], 
              llcrnrlat = lat[0,0], urcrnrlat = lat[30-1,30-1], resolution='h', area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
x,y = m(lon,lat)
var_list = ["O3", "PMIJ"]
unit_list = ["ppb", "ug m-3"]
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

############################################
# averaged domain basemaps
############################################
#save maps into the pdf file (two maps in single page)
with PdfPages(base_dir+'maps/airpactRegrid_avg_basemap_' + '_'+ start.strftime("%Y%m%d") + '-' +  end.strftime("%Y%m%d") + '.pdf') as pdf:
    
    for i, sp in enumerate(var_list):
        
        fig = plt.figure(figsize=(14,10))
        plt.title(sp)
        
        # compute auto color-scale using maximum concentrations
        #down_scale = np.percentile(airpact_3d[sp], 5)
        #up_scale = np.percentile(airpact_3d[sp], 95)
        down_scale = 28
        up_scale = 46
        clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
        print("debug clevs", clevs, sp)
        
        cblabel = unit_list[i]
        cbticks = True
        cs = m.contourf(x,y,airpact_3d[sp].mean(axis=0),clevs,cmap=plt.get_cmap('jet'), extend='both')
        cs.cmap.set_under('cyan')
        cs.cmap.set_over('black')
        
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()
        m.drawcounties()
        
        cbar = m.colorbar(location='bottom',pad="5%")
        cbar.set_label(cblabel)
        if cbticks:
            cbar.set_ticks(clevs)
        
        # print the surface-layer mean on the map plot
        plt.annotate("mean: " + str(airpact_3d[sp].mean(axis=0).mean()) +" ppb", xy=(0, 1.02), xycoords='axes fraction')
        
        #pdf.savefig(fig) 
        plt.show()
print('End of script')