# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 13:20:06 2019

@author: Jordan Munson
"""
#Import libraries
import datetime
import pytz
import pickle
from pytz import timezone

# Set file paths
base_dir=r'E:/Research/Urbanova_Jordan/'
output_dir = r'E:/Research/scripts/folium_files/'
git_dir = 'https://github.com/jordan-munson/scripts/raw/master/folium_files/'

# Set times
start_year = 2018
start_month = 1
start_day = 11

end_year = 2018
end_month = 12
#end_day = monthrange(end_year, end_month)[1]
end_day = 31

# set start and end date
start = datetime.datetime(start_year, start_month, start_day, hour=0)
end = datetime.datetime(end_year, end_month, end_day, hour=23)
timezone = pytz.timezone("utc")
start = timezone.localize(start)
end = timezone.localize(end)


# Load data
# Data from "urbanova_mapping_1.33km.py"
name =base_dir+ '1p33_'+start.strftime("%Y%m%d")+'_'+end.strftime("%Y%m%d")+'_PST'

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
airpact = load_obj(name)


#%%
# set species and time
sp = 'O3'


# Calculate mean
print("mean: " + str(round(airpact[sp][5:67,:,:].mean(),2)))
