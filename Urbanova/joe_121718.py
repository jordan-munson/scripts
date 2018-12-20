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
base_dir=r'G:/Research/Urbanova_Jordan/'
grid_dir_urb=r'G:\Research\Urbanova_Jordan\Urbanova_ref_site_comparison\Urbanova/2018\2018011100\MCIP37/'
data_dir=r'E:/big_research_files/'
output_dir = r'G:/Research/scripts/folium_files/'
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

exec(open(r"G:/Research/scripts/Urbanova/airpact_functions.py").read())
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

modeloutputs= [data_dir +'/old_CCTM/ACONC_'+now.strftime('%Y%m%d')+'.ncf']

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
modeloutputs= [data_dir +'new_CCTM/ACONC_'+now.strftime('%Y%m%d')+'.ncf']
urbanova_new = get_aconc_DF(start, end, layer)
print('Urb new done')
#base map
m = Basemap(projection='merc',
              llcrnrlon = lon[0,0], urcrnrlon = lon[90-1,90 -1], 
              llcrnrlat = lat[0,0], urcrnrlat = lat[90-1,90-1],
              resolution='h', area_thresh=1000)# setting area_thresh doesn't plot lakes/coastlines smaller than threshold
x,y = m(lon,lat)
var_list = ["O3",'CO','NH3','NO','NO2','SO2','BENZENE','PMIJ']
unit_list = ["ppb",'ppmv','ppmv','ppmv','ppmv','ppmv','ppmv','ug/m3']
rnd = 7 # value to use when rounding

#urbanova = pd.DataFrame()
urbanova = urbanova_old.copy()
# calculate PM2.5
#Create lists to sum
aomij_list = ['AXYL1J','AXYL2J','AXYL3J','ATOL1J','ATOL2J','ATOL3J','ABNZ1J','ABNZ2J','ABNZ3J','AISO1J','AISO2J','AISO3J','ATRP1J','ATRP2J','ASQTJ','AALKJ','AORGCJ','AOLGBJ','AOLGAJ','APOCI','APOCJ','APNCOMI','APNCOMJ']
atoti_list = ['ASO4I','ANO3I','ANH4I','ANAI','ACLI','AECI','APOCI','APNCOMI','AOTHRI']
atotj_list = ['ASO4J','ANO3J','ANH4J','ANAJ','ACLJ','AECJ','AOTHRJ','AFEJ','ASIJ','ATIJ','ACAJ','AMGJ','AMNJ','AALJ','AKJ']
#empty arrays to fill
urbanova_old['AOMIJ'] = np.empty( ( 24, y_dim, x_dim), dtype = float)
urbanova_old['ATOTI'] = np.empty( ( 24, y_dim, x_dim), dtype = float)
urbanova_old['ATOTJ'] = np.empty( ( 24, y_dim, x_dim), dtype = float)

for i in aomij_list:
    urbanova_old['AOMIJ'] = urbanova_old['AOMIJ'] + urbanova_old[i]
for i in atoti_list:
    urbanova_old['ATOTI'] = urbanova_old['ATOTI'] + urbanova_old[i]
for i in atotj_list:
    urbanova_old['ATOTJ'] = urbanova_old['ATOTJ'] + urbanova_old[i]    
urbanova_old['ATOTJ'] = urbanova_old['ATOTJ']-(urbanova_old['APOCI']+urbanova_old['APNCOMI'])

urbanova_old['PMIJ'] = urbanova_old['ATOTI'] + urbanova_old['ATOTJ']

# now do same for new cctm
urbanova_new['AOMIJ'] = np.empty( ( 24, y_dim, x_dim), dtype = float)
urbanova_new['ATOTI'] = np.empty( ( 24, y_dim, x_dim), dtype = float)
urbanova_new['ATOTJ'] = np.empty( ( 24, y_dim, x_dim), dtype = float)

for i in aomij_list:
    urbanova_new['AOMIJ'] = urbanova_new['AOMIJ'] + urbanova_new[i]
for i in atoti_list:
    urbanova_new['ATOTI'] = urbanova_new['ATOTI'] + urbanova_new[i]
for i in atotj_list:
    urbanova_new['ATOTJ'] = urbanova_new['ATOTJ'] + urbanova_new[i]    
urbanova_new['ATOTJ'] = urbanova_new['ATOTJ']-(urbanova_new['APOCI']+urbanova_new['APNCOMI'])

urbanova_new['PMIJ'] = urbanova_new['ATOTI'] + urbanova_new['ATOTJ']
for sp in var_list:
    urbanova[sp] =  -urbanova_old[sp]+urbanova_new[sp]
urbanova['O3']=urbanova['O3'] *1000 # convert from ppm to ppb
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
        
        fig, ax = plt.subplots(figsize=(14,10))
       # plt.title(sp +'_at_' + urbanova["DateTime"][t,0,0])
        
        # compute auto color-scale using maximum concentrations
        down_scale = np.percentile(urbanova[sp], 5)
        up_scale = np.percentile(urbanova[sp], 95)
        clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10),6)
        print("debug clevs", clevs, sp)
        
        cblabel = unit_list[i]
        print(unit_list[i], sp, t)
        cbticks = True
        cs = m.contourf(x,y,urbanova[sp][t,:,:],clevs,cmap=plt.get_cmap('jet'), extend='both')
        cs.cmap.set_under('cyan')
        cs.cmap.set_over('black')
        #m.drawcounties()
        
                # annotate with text box
        textstr = "mean: " + str(round(urbanova[sp][t,:,:].mean(),rnd)) + " "+ unit_list[i] + ' ' + sp +'_at_' + urbanova["DateTime"][t,0,0]
        props = dict(boxstyle='round', facecolor='black', alpha=0.5) # settings for text box
        
        # place a text box in upper left in axes coords
        ax.text(0.05, 0.97, textstr, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)
        
        # attempt to place box around 
        props = dict(boxstyle='round', facecolor='black', alpha=0.6) # settings for text box
        textstr = '                                                                                         '
        ax.text(0.0145, 0.059, textstr, transform=ax.transAxes, fontsize=22,
                verticalalignment='top', bbox=props)
    
        cblabel = unit_list[i]
        cbticks = True
        cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
        cbar.set_label(cblabel)
        
        # print the surface-layer mean on the map plot
        #plt.annotate("mean: " + str(urbanova[sp][t,:,:].mean()) + " "+ unit_list[i] + ' ' + sp +'_at_' + urbanova["DateTime"][t,0,0], xy=(0.04, 0.98), xycoords='axes fraction')
        
        plt.savefig(outpng,transparent=True, bbox_inches='tight', pad_inches=0, frameon = False)
        plt.show()
        plt.close()
    # This requires ffmpeg program, which is not easy to install in aeolus/kamiak
    os.chdir(base_dir)
    check_call(['ffmpeg', '-y', '-framerate','2', '-i',base_dir+'maps/cctm_comp/urbanova_comp_hourly_basemap_' + sp + '_%05d.png','-b:v','5000k', output_dir+'movie_'+sp+'_output.webm'])

#%%
#Delta map
############################################
# Delta averaged domain basemaps          Positive values represent an overestimation from 1p33km. The maps are sp33km-4km
############################################
#save maps into the pdf file (two maps in single page)    
for i, sp in enumerate(var_list):
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14,10))
    #plt.title(sp)
    
    # compute auto color-scale using maximum concentrations
    down_scale = np.percentile(urbanova[sp], 5)
    up_scale = np.percentile(urbanova[sp], 95)

    clevs = np.round(np.arange(down_scale, up_scale, (up_scale-down_scale)/10), 6) # If ValueError: Contour levels must be increasing, simply increase round number
    print("debug clevs", clevs, sp)
    
    cblabel = unit_list[i]
    cbticks = True
    cs = m.contourf(x,y,urbanova[sp].mean(axis=0),clevs,cmap=plt.get_cmap('jet'), extend='both')
    cs.cmap.set_under('cyan')
    cs.cmap.set_over('black')
    
    # Find min and max values
    map_min = np.amin(urbanova[sp])
    map_max = np.amax(urbanova[sp])
    
    
    #m.drawcoastlines()
    #m.drawstates()
   # m.drawcountries()
#        m.drawcounties()

    # annotate with text box
    textstr ='\n'.join(( "mean: " + str(round(urbanova[sp].mean(),rnd)) + " "+ unit_list[i] + ' ' + sp,
                        'max: ' + str(round(map_max,rnd)),
                        'min: ' + str(round(map_min,rnd))))
    props = dict(boxstyle='round', facecolor='black', alpha=0.5) # settings for text box
    
    # place a text box in upper left in axes coords
    ax.text(0.05, 0.97, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    
    # attempt to place box around 
    props = dict(boxstyle='round', facecolor='black', alpha=0.6) # settings for text box
    textstr = '                                                                                         '
    ax.text(0.0145, 0.059, textstr, transform=ax.transAxes, fontsize=22,
            verticalalignment='top', bbox=props)
    cblabel = unit_list[i]
    cbticks = True
    cbar = m.colorbar(location='bottom',pad="-12%")    # Disable this for the moment
    cbar.set_label(cblabel)
    # print the surface-layer mean on the map plot
    
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
m= folium.Map(location=[47.6588, -117.4260],zoom_start=9) # Create the plot
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
#%%
# =============================================================================
# # =============================================================================
# # Time series
# # =============================================================================
# pollutants = ['PM2.5','O3']
# 
# start_date = str(start_year)+'-'+str(start_month)+'-'+str(start_day)
# end_date = str(end_year)+'-'+str(end_month)+'-'+str(end_day)
# 
# airnow_data= data_dir +"AIRNowSites_" +  now.strftime("%Y%m%d") + "_v6.dat"
# col_names_modeled = ['date', 'time', 'site_id', 'pollutant', 'concentration']
# col_names_observed= ['datetime', 'site_id', 'O3_AP5_1p33km', 'PM2.5_AP5_1p33km', 'O3_obs', 'PM2.5_obs']
# df_obs   = pd.read_csv('http://lar.wsu.edu/R_apps/2018ap5/data/hrly2018.csv', sep=',', names=col_names_observed, skiprows=[0],dtype='unicode')
# df_sites = pd.read_csv(data_dir + 'aqsid.csv', skiprows=[1],dtype='unicode') # skip 2nd row which is blank
# df_sites.rename(columns={'AQSID':'site_id'}, inplace=True)
# 
# mask = (df_obs['datetime'] > start_date) & (df_obs['datetime'] <= end_date) # Create a mask to determine the date range used
# df_obs = df_obs.loc[mask]
# 
# for abrv in pollutants:
#     # extract only abrv data
#     df_base = df_base.loc[df_base['pollutant']==pollutant, df_base.columns]
#     # Renames the abrv to concentration
#     df_base.columns = df_base.columns.str.replace('concentration',abrv+ '_AP5_1.33km')
# 
#     # convert datatime colume to time data (This conversion is so slow)
#     print('Executing datetime conversion, this takes a while')
#     df_base['datetime'] = pd.to_datetime(df_base['date'] + ' ' + df_base['time'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
#     df_obs['datetime'] = pd.to_datetime(df_obs['datetime'], infer_datetime_format=True)
#     print('datetime conversion complete')
# 
#     #Convert model data to PST from UTC (PST = UTC-8)
#     df_base["datetime"] = df_base["datetime"].apply(lambda x: x - dt.timedelta(hours=8))
#     df_obs["datetime"] = df_obs["datetime"].apply(lambda x: x - dt.timedelta(hours=8))
#     df_base = df_base.drop('date',axis=1)
#     df_base = df_base.drop('time',axis=1)
#     # sites which are common between base and Observations
#     sites_common = set(df_obs['site_id']).intersection(set(df_base['site_id']))
# 
# 
#     ## take only the data which is for common sites
#     df_obs_new = pd.DataFrame(columns=df_obs.columns)
#     df_base_new = pd.DataFrame(columns=df_base.columns)
#     for sites in sites_common:
#         #    print sites
#         df1 = df_obs.loc[df_obs['site_id']==sites, df_obs.columns]
#         df3 = df_base.loc[df_base['site_id']==sites, df_base.columns]
#         df_obs_new = pd.concat([df_obs_new, df1], join='outer', ignore_index=True)
#         df_base_new = pd.concat([df_base_new, df3], join='outer', ignore_index=True)
# 
#     # merge now
#     df_obs_mod = pd.merge(df_obs_new, df_base_new, on=['datetime', 'site_id'], how='outer')
# 
#     # get rid of rows if abrv base is not available
#     df_obs_mod = df_obs_mod[pd.notnull(df_obs_mod[abrv+'_AP5_1.33km'])]
# 
# 
# 
#     df_tseries = df_obs_mod.copy() 
#     df_siteinfo = df_sites.set_index('site_id')
# 
# # convert object to numeric (This is required to plot these columns)
#     df_tseries.loc[:,abrv+'_AP5_4km'] = pd.to_numeric(df_tseries.loc[:,abrv+'_AP5_4km'])
#     df_tseries.loc[:,abrv+'_AP5_1.33km'] = pd.to_numeric(df_tseries.loc[:,abrv+'_AP5_1.33km'])
#     df_tseries.loc[:,abrv+'_obs'] = pd.to_numeric(df_tseries.loc[:,abrv+'_obs'])
# 
#     df_tseries['datetime'] = df_tseries['datetime'].dt.tz_localize('UTC').dt.tz_convert('US/Pacific')
#     print(set(df_tseries['site_id']))
# =============================================================================
    
print('done')