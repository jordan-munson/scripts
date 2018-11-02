'''
Author - Vikram Ravi
Functions for use with create_benmap_stitched_input_for_o3_PM25.py
'''
# import required modules
from math import ceil
import numpy as np
#%%
# domain information & simulation time steps
#nrows = 258
#ncols = 285
#ntime = 360

# some dummy data
#ozone  = np.random.randint(15,75,size=(ntime,nrows,ncols))

#%%

##############################################################
# FUNCTIONS FOR O3

# function to calculate daily 1-hr maximum at each grid cell
def get1hrDailyMax(hourlyO3):
    maxTimes = int(ceil(hourlyO3.shape[0]/24.))
    nrows    = hourlyO3.shape[1]
    ncols    = hourlyO3.shape[2]
    maxArray = np.empty((maxTimes, nrows, ncols))

    # iterate to calculate daily 1 hr maximum conc
    for iday, itime in enumerate(np.arange(0,24*maxTimes,24)):
        print ('Calculating Daily Max 1-Hr O3 for day = %s'%(iday))
        for irow in np.arange(0,nrows):
            for icol in np.arange(0,ncols):
                maxArray[iday,irow,icol] = np.max(hourlyO3[itime:itime+24,irow,icol])
    return maxArray

# function to calculate 8-hr rolling mean
def get8hrRollingMean(hourlyO3):
   nrows  = hourlyO3.shape[1]
   ncols  = hourlyO3.shape[2]
   o38hr  = np.empty((1,nrows,ncols))
   tmp    = np.empty((1,nrows,ncols))
   
   # iterate over a window of eight
   for i in np.arange(int(hourlyO3.shape[0])-8):
       print ('Calculating 8-Hr Rolling Mean O3 for hour = %s'%(i))
       tmp[0,:,:] = np.mean(hourlyO3[i:i+8, :, :], axis=0)
       if i==0:
           o38hr[0,:,:] = tmp
       else:
           o38hr = np.concatenate((o38hr, tmp), axis=0)
   return o38hr

#%%
# function to calculate daily 8-hr maximum at each grid cell
def get8hrDailyMax(o3_8hrMean):
    maxTimes = int(ceil(o3_8hrMean.shape[0]/24.))
    nrows    = o3_8hrMean.shape[1]
    ncols    = o3_8hrMean.shape[2]
    maxArray = np.empty((maxTimes, nrows, ncols))
    
    # iterate to calculate daily 8 hr maximum conc
    for iday, itime in enumerate(np.arange(0,24*maxTimes,24)):
        print ('Calculating Daily Max 8-Hr O3 for day = %s'%(iday))
        for irow in np.arange(0,o3_8hrMean.shape[1]):
            for icol in np.arange(0,o3_8hrMean.shape[2]):
                maxArray[iday,irow,icol] = np.max(o3_8hrMean[itime:itime+24,irow,icol])
    return maxArray

##############################################################
#%%
# FUNCTIONS FOR PM2.5

# function to calculate daily 24-hr mean at each grid cell
def get24hrDailyMean(hourlyPM):
    maxTimes  = int(ceil(hourlyPM.shape[0]/24.))
    nrows     = hourlyPM.shape[1]
    ncols     = hourlyPM.shape[2]
    meanArray = np.empty((maxTimes, nrows, ncols))

    # iterate to calculate daily 24 hr mean conc
    for iday, itime in enumerate(np.arange(0,24*maxTimes,24)):
        print ('Calculating Daily 24-Hr Mean PM2.5 for day = %s'%(iday))
        for irow in np.arange(0,hourlyPM.shape[1]):
            for icol in np.arange(0,hourlyPM.shape[2]):
                meanArray[iday,irow,icol] = np.mean(hourlyPM[itime:itime+24,irow,icol])
    return meanArray

def getQuarterlyMean(pm25_24hrMean, specialCase=False):
    maxTimes  = 4 # 4 quarters in a year
    ntimes    = pm25_24hrMean.shape[0]
    nrows     = pm25_24hrMean.shape[1]
    ncols     = pm25_24hrMean.shape[2]
    qtrArray  = np.empty((maxTimes, nrows, ncols))

    # if the quarterly mean is calculated from a full year of CMAQ simulations, assumes that the input array time dimension corresponds to 365/366 daily mean values
    itimes    = lambda daysInYear: ([91, 91, 92, 92] if daysInYear == 366 else [90, 91, 92, 91]) # number of days in each quarter

    # special case: quarterly mean is calculated from an episode simulation
    if specialCase:
        episodeMeanPM = np.empty((nrows, ncols))
        for irow in np.arange(0,nrows):
            for icol in np.arange(0,ncols):
                episodeMeanPM[irow,icol] = np.mean(pm25_24hrMean[:,irow,icol])
                qtrArray[:,irow,icol]    = episodeMeanPM[irow,icol]

    # if calculating based on a full year CTM simulation
    else:
        # iterate to calculate quarterly mean conc
        for iqtr in np.arange(0,4):
            print ('Calculating Quarterly Mean PM2.5 for Quarter = %s'%(iqtr))

            if iqtr == 0:
               qtrBeginIndex = 0
               qtrEndIndex   = itimes(ntimes)[iqtr]
            else:
               qtrBeginIndex = np.sum(itimes(ntimes)[0:iqtr])
               qtrEndIndex   = np.sum(itimes(ntimes)[0:iqtr+1])

            for irow in np.arange(0,nrows):
                for icol in np.arange(0,ncols):
                    qtrArray[iqtr,irow,icol] = np.mean(pm25_24hrMean[qtrBeginIndex:qtrEndIndex,irow,icol])
    return qtrArray

def getAnnualMean(pm25_24hrMean, specialCase=False):
    ntimes      = pm25_24hrMean.shape[0]
    nrows       = pm25_24hrMean.shape[1]
    ncols       = pm25_24hrMean.shape[2]
    annualArray = np.empty((nrows, ncols))

    # special case: annual mean is calculated from an episode simulation
    if specialCase:
        episodeMeanPM = np.empty((nrows, ncols))
        print ('Calculating Annual Mean PM2.5 from 24-Hr Mean PM2.5')
        for irow in np.arange(0,nrows):
            for icol in np.arange(0,ncols):
                episodeMeanPM[irow,icol] = np.mean(pm25_24hrMean[:,irow,icol])
                annualArray[irow,icol] = episodeMeanPM[irow,icol]
    else: # NOTE: yet to be modificd for calculating anual from quarterly mean
        print ('Calculating Annual Mean PM2.5 from Quarterly Mean PM2.5')
        for irow in np.arange(0,nrows):
            for icol in np.arange(0,ncols):
                annualArray[irow,icol] = np.mean(pm25_24hrMean[:,irow,icol])
    return annualArray

##############################################################
# FUNCTION TO WRITE TO OUTPUT FILE
def writeBenMapFile(inArray, inCase, inMetric, inPollutant, inFile):

   # now write the values stored in the array to a text file
   file2write  = inFile 
   benmap_file = open(file2write, 'w')
   print ('writing to BenMap, output file %s ...'%(file2write))

   outLine = '%s,%s,%s,%s,%s,%s\n'%('Column','Row','Metric','Seasonal Metric','Annual Metric','Values')
   benmap_file.write(outLine)

   if not inMetric == 'AnnualMean': timeLength = int(inArray.shape[0])
   nrows = int(inArray.shape[-2])
   ncols = int(inArray.shape[-1])
   to_text = lambda dc : (str('%0.2f'%dc) if dc>0 else '.')

   # now iterate over the numpy array and write values in desired format for input to benmap
   for c in np.arange(0, ncols):
     for r in np.arange(0, nrows):
        daily_list = []
        if inMetric == 'AnnualMean':
           daily_list.append(inArray[r, c])
        else:
           for t in np.arange(0, timeLength):
              daily_list.append(inArray[t, r, c])

        dailyconc_list = [to_text(concentration) for concentration in daily_list]
        delimiter = ','
        yearlyValuesString = delimiter.join(dailyconc_list)
        if inMetric == 'QuarterlyMean':
           outLine = '%s,%s,%s,%s,%s,"%s"\n'%(c+1, r+1, 'D24HourMean', inMetric, '', yearlyValuesString)
        elif inMetric == 'AnnualMean':
           outLine = '%s,%s,%s,%s,%s,"%s"\n'%(c+1, r+1, 'D24HourMean', 'QuarterlyMean', 'Mean', yearlyValuesString)
        else:
           outLine = '%s,%s,%s,%s,%s,"%s"\n'%(c+1, r+1, inMetric, '', '', yearlyValuesString)
        benmap_file.write(outLine)

   benmap_file.close()
   print ('*******************')
   print ('Output written to %s'%(file2write))
   print ('*******************')

