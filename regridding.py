# -*- coding: utf-8 -*-
"""
Created on Thu May 31 12:58:16 2018

@author: riptu
"""
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

base_dir = '/data/lar/users/jmunson/'
data_dir = '/data/lar/projects/Urbanova/'
grid_dir_urb = '/data/lar/projects/Urbanova/2018/2018011100/MCIP37/'
grid_dir_4km='/data/airpact5/AIRRUN/2018/2018011100/MCIP37/'
urb_path = '/data/lar/projects/Urbanova/'
airpact_path = '/data/airpact5/saved/'

exec(open(base_dir + "/airpact_functions.py").read())
# set start and end date
start = datetime.datetime(year=2018, month=1, day=11, hour=0)
end = datetime.datetime(year=2018, month=4, day=30, hour=23)
timezone = pytz.timezone("utc")
start = timezone.localize(start)
end = timezone.localize(end)

#Set up date diff for time loop
date_diff =end -start
date_diff =  int(round( date_diff.total_seconds()/60/60/24)) # total hour duration
print("start date is "+ start.strftime("%Y%m%d") )
now = start

for t in range(0, date_diff):
    
    try:
        os.path.isfile(urb_path + now.strftime('%Y')+'/'+now.strftime('%Y%m%d')+'00/POST/CCTM'+'/combined_' + now.strftime('%Y%m%d'))
        # run regrid program
        os.system('/data/lar/projects/Urbanova_output/qsub_fine2coarse4conc.csh ' + now.strftime('%Y%m%d'))
        # set a directory containing Urbanova data
        #Changes day to next
        now += timedelta(hours=24)  
    except:
        print('adding another 24 hours')
        now += timedelta(hours=24)
    try:
        os.path.isfile(urb_path + now.strftime('%Y')+'/'+now.strftime('%Y%m%d')+'00/POST/CCTM'+'/combined_' + now.strftime('%Y%m%d'))
        # run regrid program
        os.system('/data/lar/projects/Urbanova_output/qsub_fine2coarse4conc.csh ' + now.strftime('%Y%m%d'))
        # set a directory containing Urbanova data
        #Changes day to next
        now += timedelta(hours=24)  
    except:
        print('adding another 24 hours')
        now += timedelta(hours=24)
        
print('Regrid finished')
