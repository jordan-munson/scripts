# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:35:07 2019

@author: riptu
"""
import numpy as np
from   netCDF4 import Dataset

inputDir = r'G:/Research/Ports/combined_ncdf/'


for pollutant in ['PM2.5','O3']:
    outFile   = r'G:/Research/Ports/input_to_benmap/Ports_benmap_' + pollutant + '.csv' # output file name

    for month in ['Jan','Apr','Jul']:#,'Oct']:
    
        # CMAQ output file for the date
        nc_file = inputDir+month+"/base/combined_avg.ncf"
        
        concData   = Dataset(nc_file, 'r')
    
        hourlyConc = concData.variables[pollutant][:, 0, :, :]
        
        concArray = hourlyConc
        
        ntimes      = concArray.shape[0]
        nrows       = concArray.shape[1]
        ncols       = concArray.shape[2]
        annualArray = np.empty((nrows, ncols))
        
        for irow in np.arange(0,nrows):
            for icol in np.arange(0,ncols):
                annualArray[irow,icol] = np.mean(concArray[:,irow,icol])
        if month == 'Jan':
            jan_array = annualArray
        if month == 'Apr':
            apr_array = annualArray
        if month == 'Jul':
            jul_array = annualArray                
        if month == 'Oct':
            oct_array = annualArray                
                
                
    annualArray = (jan_array+apr_array+jul_array)/3 #+oct_array)/4          
                
    inArray = annualArray
    # now write the values stored in the array to a text file
    file2write  = outFile 
    benmap_file = open(file2write, 'w')
    print ('writing to BenMap, output file %s ...'%(file2write))

    outLine = '%s,%s,%s,%s,%s,%s\n'%('Column','Row','Metric','Seasonal Metric','Annual Metric','Values')
    benmap_file.write(outLine)

    nrows = int(inArray.shape[-2])
    ncols = int(inArray.shape[-1])
    to_text = lambda dc : (str('%0.2f'%dc) if dc>0 else '.')

    # now iterate over the numpy array and write values in desired format for input to benmap
    for c in np.arange(0, ncols):
      for r in np.arange(0, nrows):
         daily_list = []
         daily_list.append(inArray[r, c])

         dailyconc_list = [to_text(concentration) for concentration in daily_list]
         delimiter = ','
         yearlyValuesString = delimiter.join(dailyconc_list)

         outLine = '%s,%s,%s,%s,%s,"%s"\n'%(c+1, r+1, 'D24HourMean', 'QuarterlyMean', 'Mean', yearlyValuesString)

         benmap_file.write(outLine)

    benmap_file.close()
    print ('*******************')
    print ('Output written to %s'%(file2write))
    print ('*******************')