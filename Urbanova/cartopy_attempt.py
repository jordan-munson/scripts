# -*- coding: utf-8 -*-
"""
Spyder Editor

Author: Jordan Munson
"""
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
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
#%matplotlib inline

base_dir=r'G:/Research/Urbanova_Jordan/'

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

# obtain model lat and lon
lat = airpact['lat'][0]
lon = airpact['lon'][0]
#%%
# mins and max's of the plot
lon_min=np.amin(airpact['lon'])
lat_min=np.amin(airpact['lat'])
lon_max=np.amax(airpact['lon'])
lat_max=np.amax(airpact['lat'])

extents = [lon_min, lon_max, lat_min, lat_max ]

sp = 'O3'

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
#fig = plt.figure(figsize=(14,10))
ax = plt.axes(projection=ccrs.Mercator())
#plt.contourf(lon,lat,airpact[sp].mean(axis=0),clevs,cmap=plt.get_cmap('jet'), extend='both',
#             transform=ccrs.Mercator(latitude_true_scale=47.6588))
ax.coastlines()
ax.stock_img()
ax.set_extent(extents)

ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.RIVERS)

# mark a known place to help us geo-locate ourselves
#ax.plot(-117.4260, 47.6588, 'bo', markersize=7, transform=ccrs.Mercator())
#ax.text(-117.4, 47.6, 'Spokane', transform=ccrs.Mercator())

# Save the plot by calling plt.savefig() BEFORE plt.show()
#plt.savefig('coastlines.pdf')
plt.savefig(r'C:\Users\Jordan\Desktop/coastlines.png')

plt.show()

#%%

m= folium.Map(location=[47.6588, -117.4260],zoom_start=9.25) # Create the plot
m.add_child(folium.LatLngPopup()) #Add click lat/lon functionality

# mins and max's of the plot
lon_min=np.amin(airpact['lon'])
lat_min=np.amin(airpact['lat'])
lon_max=np.amax(airpact['lon'])
lat_max=np.amax(airpact['lat'])

extents = [[lat_min, lon_min], [lat_max, lon_max]]

# Set paths to monthly average maps
png1 = r'C:\Users\Jordan\Desktop/coastlines.png'

# Add monthly average maps to Folium
folium.raster_layers.ImageOverlay(png1,bounds = extents,name='Ozone',opacity = 0.5, show = True).add_to(m)


# Add ability to move between layers
folium.LayerControl().add_to(m)
m.save(r'C:\Users\Jordan\Desktop/cartopy_test.html')
m
