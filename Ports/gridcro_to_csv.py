# Script modified off of Kai Fans script

from netCDF4 import Dataset
import pandas as pd

# Set file paths
grid_dir=r'E:/Research/Ports/'

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

# Create list from the array
df_lat = pd.DataFrame(lat)
df_lon = pd.DataFrame(lon)

# Make empty dataframes to fill in the for loop
df_lat1 = pd.DataFrame(columns=[0])
df_lon1 = pd.DataFrame(columns=[0])

# run for loop to fill dataframes with lat/lon information
for x in list(range(0,219)):
    # create empty dataframes
    temp_lat = pd.DataFrame(columns=[0])
    temp_lon = pd.DataFrame(columns=[0])
    
    # fill empty dataframes with one row
    temp_lat[0] = df_lat[x]
    temp_lon[0] = df_lon[x]
    
    # add dataframes
    df_lat1 = df_lat1.append(temp_lat,ignore_index=True)
    df_lon1 = df_lon1.append(temp_lon,ignore_index=True)
    
# rename to lat/lon respectively
df_lat1 = df_lat1.rename(columns={0:'ROW'})
df_lon1 = df_lon1.rename(columns={0:'COL'})

# Merge lat and lon
df_latlon = pd.merge(df_lat1,df_lon1,right_index=True,left_index=True)

# save to csv to use in a gis softwtware to create a grid
df_latlon.to_csv(grid_dir + 'latlon.csv',index=False)
