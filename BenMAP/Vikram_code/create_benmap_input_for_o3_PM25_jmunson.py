'''
Author - Vikram Ravi, LAR/CEE Washington State University
Initial Version - 12/16/2015 written for PM25
Revised Version - 12/28/2017 modified foto include O3 and PM25, various function for benmap metric moved to 
                             functions_for_benmap.py
Modified -7/31/2018 by Jordan Munson for use in Urbanova research

Purpose - reads in the netCDF file and calculates the daily metric (max, average) and writes
          the output to a text file for use in BenMap software

'''
#%%
#################################################
# IMPORT REQUIRED LIBRARIES / MODULES

import pandas as pd
import numpy as np
import os
import time
import calendar
from   netCDF4 import Dataset
from datetime import timedelta
from functions_for_benmap import *

# for timing
time_begin = time.time()

#%%
#################################################
# USER INPUTS ETC.
# PC
# =============================================================================
# inputDir   = r'E:/Research/Urbanova_Jordan/Urbanova_ref_site_comparison/Urbanova/2018/'
# outDir     = r'E:/Research/Benmap/output/pc/'
# grd_file   = r'E:/Research/Urbanova_Jordan/Urbanova_POST/GRIDCRO2D'    
# =============================================================================

# Aeolus
inputDir   = '/data/lar/projects/Urbanova/2018/' #for Urbanova files
outDir     = '/data/lar/users/jmunson/benmap/script_output/'
grd_file   = '/data/lar/projects/Urbanova/2018/2018011100/MCIP37/GRIDCRO2D'    # This file still exists so the path is valid for this


pollutant  = 'O3'          # PM25 or O3
case       = 'BASE'         # 2EMIS or NARA or BASE
epi_to_qtr = True           # if getting quarterly mean / annual mean from an episode (we assume that quarterly/annual mean equals episodic mean in worst case, NOTE: not valid for fire silumations)
metric     = 'D8HourMax'   # for Ozone - D8HourMax or D1HourMax; for PM2.5 - D24HourMean, QuarterlyMean, AnnualMean
beginDate  = '2018-01-11'    # begin date of simulations
endDate    = '2018-12-31'    # end date of simulations

#################################################
# based on user inputs, create some date variables
dateRange = pd.date_range(beginDate, endDate, freq='D') # date range of simulations
firstDay  = beginDate.split('-')[0]+'-01-01'            # first day of year
lastDay   = beginDate.split('-')[0]+'-12-31'            # last day of year
yearDates = pd.date_range(firstDay, lastDay, freq='D')  # date range of year
simYear   = beginDate.split('-')[0]                     # for labelling output files

outFile   = outDir + simYear + "_" + case + '_NARA_benmap_' + pollutant + '_' + metric  + '.csv' # output file name
################################################
# READ THE INPUT FILES IN NUMPY ARRAYS
grd    = Dataset(grd_file,'r')
nrows  = grd.NROWS
ncols  = grd.NCOLS
grd.close()

for i, date in enumerate(dateRange):
    stryr = '{:04d}'.format(date.year)
    strmt = '{:02d}'.format(date.month)
    strdy = '{:02d}'.format(date.day)
    YMD   = stryr + strmt + strdy
    doy   = date.strftime('%j')
    YJDay = stryr + doy
    
    # CMAQ output file for the date
    if inputDir == '/data/lar/users/jmunson/Urbanova_regrid4km/':
        nc_file = inputDir+"/combined_{YearJDay}.regrid4km.ncf".format(inDir=inputDir, YearJDay=YMD)
    else:
        nc_file = inputDir+YMD+'00'+"/POST/CCTM/combined_{YearJDay}.ncf".format(inDir=inputDir, YearJDay=YMD)
    
    # read in the data
    if (os.path.isfile(nc_file)):
        concData   = Dataset(nc_file, 'r')

        # CMAQ concentrations are in ppm, we need ppb; no change for PM2.5  
        if pollutant == 'O3':
           #hourlyConc = 1000*concData.variables[pollutant][:, 0, :, :] # The units are currently in ppbv, need to check to see if older files are ppm
           hourlyConc = concData.variables[pollutant][:, 0, :, :]
        elif pollutant == 'PMIJ':
           hourlyConc = concData.variables[pollutant][:, 0, :, :]

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
           concArray = np.concatenate((concArray, hourlyConc), axis=0)  # instead of zeros, fill with data from previous day
        #print(concArray.shape)

        continue
#%%

###################################################
# CALL VARIOUS FUNCTION FOR ROLLING MEAN ETC AND WRITE TO OUTPUT FILE

# create array of zeros to create a full year of data at the grid cells
daysBefore  = int(( dateRange[0]  - yearDates[0]  ).days) # days in year before simulation starts
daysAfter   = int(( yearDates[-1] - dateRange[-1] ).days) # days in year after simulation ends
beforeArray = np.zeros((daysBefore, nrows, ncols))        # array of zeros before simulation starts
afterArray  = np.zeros((daysAfter , nrows, ncols))        # array of zeros after simulation ends

# call functions based on metric
if metric == 'D1HourMax': # O3
   conc_1hrMax = get1hrDailyMax(concArray)
   conc_1hrMax = np.concatenate((beforeArray, conc_1hrMax, afterArray), axis=0)
   writeBenMapFile(conc_1hrMax, case, metric, pollutant, outFile)
elif metric == 'D8HourMax': # O3
   conc_8hrAvg = get8hrRollingMean(concArray)
   conc_8hrMax = get8hrDailyMax(conc_8hrAvg)
   conc_8hrMax = np.concatenate((beforeArray, conc_8hrMax, afterArray), axis=0)
   writeBenMapFile(conc_8hrMax, case, metric, pollutant, outFile)
elif metric == 'D24HourMean': # PM25
   conc_24hrAvg = get24hrDailyMean(concArray)
   conc_24hrAvg = np.concatenate((beforeArray, conc_24hrAvg, afterArray), axis=0)
   writeBenMapFile(conc_24hrAvg, case, metric, pollutant, outFile)
elif metric == 'QuarterlyMean': # PM25
   conc_24hrAvg  = get24hrDailyMean(concArray)
   quarterlyMean = getQuarterlyMean(conc_24hrAvg, specialCase=epi_to_qtr)
   writeBenMapFile(quarterlyMean, case, metric, pollutant, outFile)
elif metric == 'AnnualMean': # PM25
   conc_24hrAvg  = get24hrDailyMean(concArray)
   annualMean    = getAnnualMean(conc_24hrAvg, specialCase=epi_to_qtr)
   writeBenMapFile(annualMean, case, metric, pollutant, outFile)

#####################################################

time_end = time.time()
print ('Finishing now...')
print ('Time taken =%s'%(time_end - time_begin))
