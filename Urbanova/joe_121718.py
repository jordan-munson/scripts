# 
import matplotlib
#matplotlib.use('Agg')  # Uncomment this when using in Kamiak/Aeolus
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
import folium
from mpl_toolkits.basemap import Basemap
import matplotlib.patches as patches

# Set file paths
base_dir=r'E:/Research/Urbanova_Jordan/'
grid_dir_urb=r'E:\Research\Urbanova_Jordan\Urbanova_ref_site_comparison\Urbanova/2018\2018011100\MCIP37/'
data_dir=r'D:/big_research_files/'
output_dir = r'E:/Research/scripts/folium_files/'
git_dir = 'https://github.com/jordan-munson/scripts/raw/master/folium_files/'

#base_dir = '/data/lar/users/jmunson/'
#data_dir = '/data/lar/projects/Urbanova/'
#grid_dir_urb = '/data/lar/projects/Urbanova/2018/2018011100/MCIP37/'
#grid_dir_4km='/data/airpact5/AIRRUN/2018/2018011100/MCIP37/'
#urb_path = '/data/lar/projects/Urbanova/'
#airpact_path = '/data/airpact5/saved/'
#regrid_path = '/data/lar/projects/Urbanova_output/Urbanova_regrid4km/'

start_year = 2018
start_month = 12
start_day = 15

end_year = 2018
end_month = 12
#end_day = monthrange(end_year, end_month)[1]
end_day = 15

exec(open(r"E:/Research/scripts/Urbanova/airpact_functions.py").read())
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

modeloutputs= [data_dir +'old_ACONC_'+now.strftime('%Y%m%d')+'.ncf']

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
latlon = grid_dir_urb+"/GRIDCRO2D"
fin0 = Dataset(latlon, 'r')
lat = fin0.variables['LAT'][0,0]
lon = fin0.variables['LON'][0,0]
w = (fin0.NCOLS)*(fin0.XCELL)
h = (fin0.NROWS)*(fin0.YCELL)
lat_0 = fin0.YCENT
lon_0 = fin0.XCENT
fin0.close()
filetype = 'aconc'
urbanova_old = get_aconc_DF(start, end, layer)
print('Urb old done')
modeloutputs= [data_dir +'ACONC_'+now.strftime('%Y%m%d')+'.ncf']
urbanova_new = get_aconc_DF(start, end, layer)
print('Urb new done')
#base map
m = Basemap(projection='merc',
              llcrnrlon = lon[0,0], urcrnrlon = lon[90-1,90 -1], 
              llcrnrlat = lat[0,0], urcrnrlat = lat[90-1,90-1],
              resolution='h', area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
x,y = m(lon,lat)
var_list = ["O3",'CO','NH3','NO','NO2','SO2','BENZENE']#, "PMIJ"]
unit_list = ["ppb",'ppmv','ppmv','ppmv','ppmv','ppmv','ppmv']#, "$ug/m^3$"]
#urbanova = pd.DataFrame()
urbanova = urbanova_old.copy()
for sp in var_list:
    urbanova[sp] =  -urbanova_old[sp]+urbanova_new[sp]


#%%
############################################
# hourly domain basemaps
############################################

#save maps into the pdf file (two maps in single page)
from subprocess import check_call
for i, sp in enumerate(var_list):
    
    for t in range(0, len(urbanova[sp])): 
        plt.style.use('dark_background')
        outpng = base_dir +'maps/cctm_comp/urbanova_comp_hourly_basemap_' + sp + '_%05d.png' % t
        print(outpng)
        
        fig = plt.figure(figsize=(14,10))
       # plt.title(sp +'_at_' + urbanova["DateTime"][t,0,0])
        
        # compute auto color-scale using maximum concentrations
        down_scale = np.percentile(urbanova[sp], 5)
        up_scale = np.percentile(urbanova[sp], 95)
        clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),5)
        print("debug clevs", clevs, sp)
        
        cblabel = unit_list[i]
        print(unit_list[i], sp, t)
        cbticks = True
        cs = m.contourf(x,y,urbanova[sp][t,:,:],clevs,cmap=plt.get_cmap('jet'), extend='both')
        cs.cmap.set_under('cyan')
        cs.cmap.set_over('black')

        
        cblabel = unit_list[i]
        cbticks = True
        cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
        cbar.set_label(cblabel)
        
        # print the surface-layer mean on the map plot
        plt.annotate("mean: " + str(urbanova[sp][t,:,:].mean()) + " "+ unit_list[i] + ' ' + sp +'_at_' + urbanova["DateTime"][t,0,0], xy=(0.04, 0.98), xycoords='axes fraction')
        
        plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False)
        plt.show()
        plt.close()
    # This requires ffmpeg program, which is not easy to install in aeolus/kamiak
    os.chdir('E:/Research/Urbanova_Jordan')
    check_call(['ffmpeg', '-y', '-framerate','2', '-i',base_dir+'maps/cctm_comp/urbanova_comp_hourly_basemap_' + sp + '_%05d.png','-b:v','5000k', output_dir+'movie_'+sp+'_output.webm'])

#%%
#Delta map
############################################
# Delta averaged domain basemaps          Positive values represent an overestimation from 1p33km. The maps are sp33km-4km
############################################
#save maps into the pdf file (two maps in single page)    
for i, sp in enumerate(var_list):
    
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(14,10))
    #plt.title(sp)
    
    # compute auto color-scale using maximum concentrations
    down_scale = np.percentile(urbanova[sp], 5)
    up_scale = np.percentile(urbanova[sp], 95)

    clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10), 5) # If ValueError: Contour levels must be increasing, simply increase round number
    print("debug clevs", clevs, sp)
    
    cblabel = unit_list[i]
    cbticks = True
    cs = m.contourf(x,y,urbanova[sp].mean(axis=0),clevs,cmap=plt.get_cmap('jet'), extend='both')
    cs.cmap.set_under('cyan')
    cs.cmap.set_over('black')
    
    #m.drawcoastlines()
    #m.drawstates()
   # m.drawcountries()
#        m.drawcounties()

    cblabel = unit_list[i]
    cbticks = True
    cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
    cbar.set_label(cblabel)
    plt.annotate("mean: " + str(round(urbanova[sp].mean(),5)) + " "+ unit_list[i], xy=(0.04, 0.98), xycoords='axes fraction')
    # print the surface-layer mean on the map plot
    
    plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()), xy=(0, 1.02), xycoords='axes fraction')
    #else:
        #plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" $ug/m^3$", xy=(0, 1.02), xycoords='axes fraction')
    outpng = base_dir +'maps/cctm_comp/delta_basemap_' +str(end_month)+'_'+ sp + '.png'
    print(outpng)
    #fig.savefig(fig) 
    plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False)
    plt.show()
    plt.close()

# =============================================================================
# # Ratio map       
# airpact['O3'] =  airpact_3d['O3']/airpact_2d['O3']
# airpact['PMIJ'] =  airpact_3d['PMIJ']/airpact_2d['PMIJ']
# ############################################
# # averaged domain basemaps          Positive values represent an overestimation from 1p33km. The maps are 1p33km/4km
# ############################################
# #save maps into the pdf file (two maps in single page)
# with PdfPages(base_dir+'maps/ratio_avg_basemap_' + '_'+ start.strftime("%Y%m%d") + '-' +  end.strftime("%Y%m%d") + '.pdf') as pdf:
#     
#     for i, sp in enumerate(var_list):
#         
#         fig = plt.figure(figsize=(14,10))
#         plt.title(sp)
#         
#         # compute auto color-scale using maximum concentrations
#         down_scale = np.percentile(airpact[sp], 5)
#         up_scale = np.percentile(airpact[sp], 95)
#         clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),3)
#         print("debug clevs", clevs, sp)
#         
#         cblabel = unit_list[i]
#         cbticks = True
#         cs = m.contourf(x,y,airpact[sp].mean(axis=0),clevs,cmap=plt.get_cmap('jet'), extend='both')
#         cs.cmap.set_under('cyan')
#         cs.cmap.set_over('black')
#         
#         m.drawcoastlines()
#         m.drawstates()
#         m.drawcountries()
# #        m.drawcounties()
#         cbar = m.colorbar(location='bottom',pad="5%")
#         cbar.set_label(cblabel)
#         if cbticks:
#             cbar.set_ticks(clevs)
#         
#         # print the surface-layer mean on the map plot
#         if sp == 'O3':
#             plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" ppb", xy=(0, 1.02), xycoords='axes fraction')
#         else:
#             plt.annotate("mean: " + str(airpact[sp].mean(axis=0).mean()) +" $ug/m^3$", xy=(0, 1.02), xycoords='axes fraction')
#         
#         pdf.savefig(fig) 
#         plt.show()
# =============================================================================
      

#%%
######################################
        # Plot folium
######################################
m= folium.Map(location=[47.6588, -117.4260],zoom_start=9.25) # Create the plot
m.add_child(folium.LatLngPopup()) #Add click lat/lon functionality

# mins and max's of the plot
lon_min=np.amin(urbanova['lon'])
lat_min=np.amin(urbanova['lat'])
lon_max=np.amax(urbanova['lon'])
lat_max=np.amax(urbanova['lat'])

extents = [[lat_min, lon_min], [lat_max, lon_max]]

# Add monthly average maps to Folium
for sp in var_list:
    folium.raster_layers.ImageOverlay(base_dir +'maps/cctm_comp/delta_basemap_' +str(end_month)+'_'+ sp + '.png',bounds = extents,name=sp,opacity = 0.5, show = False).add_to(m)
    folium.raster_layers.VideoOverlay(video_url=git_dir+'movie_'+sp+'_output.webm',bounds = extents,name=sp+'video',opacity = 0.5,attr = sp+'video',show = False,autoplay=True).add_to(m)


# Add videos to Folium
#folium.raster_layers.VideoOverlay(video_url=video1,bounds = extents,name='O3_video',opacity = 0.5,attr = 'O3_video_map',show = True,autoplay=True).add_to(m)


# Add ability to move between layers
folium.LayerControl().add_to(m)

# Save and show the created map. Use Jupyter to see the map within your console
m.save(output_dir+'folium_cctm_change.html')
m
print('done')