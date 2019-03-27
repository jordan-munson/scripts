# -*- coding: utf-8 -*-
"""
Created on Thu May 31 12:58:16 2018

@author: riptu
"""
import matplotlib
matplotlib.use('Agg')  # Uncomment this when using in Kamiak/Aeolus
import time as clock
import datetime
from datetime import timedelta
import os
import pandas as pd


base_dir = '/data/lar/users/jmunson/'
urb_path = '/data/lar/projects/Urbanova/'

# Set dates
date1 = '2018-06-20'
date2 = '2018-12-31'
mydates = pd.date_range(date1, date2, freq='D').tolist()


for date in mydates:
    clock.sleep(3) # wait 3 seconds so that hundreds of jobs are not submitted at once...
    time = date.strftime('%Y%m%d')
    try:
        os.path.isfile(urb_path + '2018/'+time+'00/POST/CCTM'+'/combined_' + time)
        # run regrid program
        os.system('/data/lar/users/jmunson/Urbanova_regrid4km/qsub_fine2coarse4conc.csh ' + time)
        # set a directory containing Urbanova data
        #Changes day to next
 
    except:
        print('Missing '+time)

        
print('Regrid finished')
