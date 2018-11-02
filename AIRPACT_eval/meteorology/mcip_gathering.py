# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 15:09:23 2018

@author: Jordan Munson
"""
#####################################################################
# Setup the script
#####################################################################

# Import libraries
import pandas as pd
import numpy as np
import os
import time
import calendar
from   netCDF4 import Dataset
from datetime import timedelta
from functions_for_benmap import *

# Set directories
inputDir = '/archive/lar/'
outDir = '/data/lar/users/jmunson/longterm_airpact/'
# Specify date range
beginDate  = '2009-01-01'    # begin date of simulations
endDate    = '2018-08-13'    # end date of simulations

#################################################
# based on user inputs, create some date variables
dateRange = pd.date_range(beginDate, endDate, freq='D') # date range of simulations
firstDay  = beginDate.split('-')[0]+'-01-01'            # first day of year
lastDay   = beginDate.split('-')[0]+'-12-31'            # last day of year
yearDates = pd.date_range(firstDay, lastDay, freq='D')  # date range of year
simYear   = beginDate.split('-')[0]                     # for labelling output files

outFile   = outDir + 'list_of_days.txt' # output file name

#####################################################################
# Make a list out of the day's of data available
#####################################################################
concData = []
# Use an if statement maybe. Section of Code below is from Vikrams benmap script
for i, date in enumerate(dateRange):
    stryr = '{:04d}'.format(date.year)
    strmt = '{:02d}'.format(date.month)
    strdy = '{:02d}'.format(date.day)
    YMD   = stryr + strmt + strdy
    doy   = date.strftime('%j')
    YJDay = stryr + doy
    
    # CMAQ output file for the date
   # inputDir == '/data/lar/users/jmunson/Urbanova_regrid4km/'
    nc_file = inputDir+"/{YearJDay}00/.regrid4km.ncf".format(inDir=inputDir, YearJDay=YMD)

    # read in the data
    if (os.path.isfile(nc_file)):
        #concData   = Dataset(nc_file, 'r')
        
        # CMAQ concentrations are in ppm, we need ppb; no change for PM2.5  
#        if pollutant == 'O3':
 #          hourlyConc = concData.variables[pollutant][:, 0, :, :]

        if i==0:
           concArray = hourlyConc
        else:
           concArray = np.concatenate((concArray, hourlyConc), axis=0)
        print ('finished processing for %s .....'%str(date))
        concData.close()
    else:
        print ('File:%s doesnt exist'%(nc_file))
        if i==0:
           concArray = np.empty((24,grd.NROWS, grd.NCOLS))
        else:
           #concArray = np.concatenate((concArray, hourlyConc), axis=0)  # instead of zeros, fill with data from previous day
           pass
        #print(concArray.shape)

        continue

# Print the list
print(day_list)









