# Script modified off of Kai Fans script
import matplotlib
matplotlib.use('Agg')  # Uncomment this when using in Kamiak/Aeolus
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
import pytz
import os
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pickle
#pd.show_versions()

#import folium
#import simplekml

# Set file paths
# =============================================================================
# base_dir=r'E:/Research/Urbanova_Jordan/'
# data_dir= base_dir + '/Urbanova_ref_site_comparison/Urbanova/'
# grid_dir_4km=base_dir + '/Urbanova_ref_site_comparison/AIRPACT/2018/2018011100/MCIP37/'
# grid_dir_urb=base_dir + '/Urbanova_ref_site_comparison/Urbanova/2018/2018011100/MCIP37/'
# urb_path = data_dir
# airpact_path = base_dir + '/Urbanova_ref_site_comparison/AIRPACT/'
# =============================================================================


base_dir = '/data/lar/users/jmunson/'
data_dir = '/data/lar/projects/Urbanova/'
grid_dir_urb = '/data/lar/projects/Urbanova/2018/2018011100/MCIP37/'
grid_dir_4km='/data/airpact5/AIRRUN/2018/2018011100/MCIP37/'
urb_path = '/data/lar/projects/Urbanova/'
airpact_path = '/data/airpact5/saved/'

start_year = 2018
start_month = 1
start_day = 11

end_year = 2018
end_month = 1
#end_day = monthrange(end_year, end_month)[1]
end_day = 31

exec(open(base_dir + "/airpact_functions.py").read())
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
print("start date is "+ start.strftime("%Y%m%d") + ' combining 1.33km files' )
now = start

# Start time loop
modeloutputs = []
modeloutputs.append(data_dir + now.strftime('%Y')+'/'+ now.strftime('%Y%m%d')+'00'+'/POST/CCTM/'+'combined_' + now.strftime('%Y%m%d')+'.ncf')
print(modeloutputs)
now += timedelta(hours=24)
# For loop to find the combined3D files for specified time period
for t in range(0, date_diff):
    
    # Handles missing days
    if os.path.isfile(data_dir + now.strftime('%Y')+'/'+ now.strftime('%Y%m%d')+'00'+'/POST/CCTM/'+'combined_' + now.strftime('%Y%m%d')+'.ncf'):
        # set a directory containing Urbanova data
        modeloutputs.append(data_dir + now.strftime('%Y')+'/'+ now.strftime('%Y%m%d')+'00'+'/POST/CCTM/'+'combined_' + now.strftime('%Y%m%d')+'.ncf')
        #Changes day to next
        now += timedelta(hours=24)            
    else:
        print('adding 24 hours')
        now += timedelta(hours=24)

# =============================================================================
#     if os.path.isfile(regrid_path + 'combined_' + now.strftime('%Y%m%d')+'.regrid4km.ncf'):
#         # set a directory containing Urbanova data
#         modeloutputs.append(airpact_path + now.strftime('%Y')+'/'+now.strftime('%m')+'/aconc/combined_' + now.strftime('%Y%m%d')+'.ncf')
#         #Changes day to next
#         now += timedelta(hours=24)            
#     else:
#         print('adding 24 hours')
#         now += timedelta(hours=24)
# =============================================================================

print('1.33km file paths arrayed')

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

airpact = get_airpact_DF(start, end, layer)

# Save the dictionary to be used in Folium mapping script
def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    
name = '1p33_'+start.strftime("%Y%m%d")+'_'+end.strftime("%Y%m%d")
save_obj(airpact,name)    
