# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 08:11:31 2019

@author: Jordan Munson
"""

import matplotlib as mpl
#mpl.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import time

starttime = time.time()
begin_time = time.time()

# =============================================================================
# inputDir = '/data/lar/users/jmunson/longterm_airpact/'
# stat_path = '/data/lar/users/jmunson/statistical_functions.py'
# ben_path = '/data/lar/users/jmunson/Met_functions_for_Ben.py'
# =============================================================================

#Set directory
inputDir = r'E:/Research/AIRPACT_eval/'
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'

df_aqsid_o3 = pd.read_csv(inputDir+'/o3_aqsid.csv',dtype=str).drop('Unnamed: 0', axis=1) # load in AQSID that are present for all versions of AIRPACT. This is created later in the script.
df_aqsid_pm = pd.read_csv(inputDir+'/pm_aqsid.csv',dtype=str).drop('Unnamed: 0', axis=1) # load in AQSID that are present for all versions of AIRPACT. This is created later in the script.

exec(open(stat_path).read())


# Set plot parameters
mpl.rcParams['font.family'] = 'calibri'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 10.0
mpl.rcParams['xtick.major.size']  = 5
mpl.rcParams['xtick.major.width'] = 1.5
mpl.rcParams['xtick.minor.size']  = 5
mpl.rcParams['xtick.minor.width'] = 1
mpl.rcParams['ytick.major.size']  = 10
mpl.rcParams['ytick.major.width'] = 2
mpl.rcParams['ytick.minor.size']  = 5
mpl.rcParams['ytick.minor.width'] = 1
mpl.rcParams['ytick.direction']   = 'in'
mpl.rcParams['xtick.direction']   = 'in'


#df_com = pd.read_csv(inputDir+'AQS_data/df_com_aplong.csv').drop('Unnamed: 0', axis=1)
df_com = pd.read_csv(inputDir+'AQS_data/df_com.csv').drop('Unnamed: 0', axis=1)

df_com.loc[:,'O3_mod'] = pd.to_numeric(df_com.loc[:,'O3_mod'], errors='coerce')
df_com.loc[:,'PM2.5_mod'] = pd.to_numeric(df_com.loc[:,'PM2.5_mod'], errors='coerce')
df_com.loc[:,'O3_obs'] = pd.to_numeric(df_com.loc[:,'O3_obs'], errors='coerce')
df_com.loc[:,'PM2.5_obs'] = pd.to_numeric(df_com.loc[:,'PM2.5_obs'], errors='coerce')
df_com['datetime'] = pd.to_datetime(df_com['datetime'])
#df_com = df_com.drop(['Location Setting', 'Local Site Name'], axis=1)
df_com['AQSID'] = df_com['AQSID'].astype(str)

df_pm = pd.merge(df_com,df_aqsid_pm,on='AQSID').drop(['O3_obs','O3_mod'],axis=1).dropna(subset=['PM2.5_obs','PM2.5_mod']) #combine with common sites, drop unecessary column, delete all relevant nans
df_o3 = pd.merge(df_com,df_aqsid_o3,on='AQSID').drop(['PM2.5_obs','PM2.5_mod'],axis=1).dropna(subset=['O3_obs','O3_mod'])
print('Data loading section done')
#%%

versions = ['AP-3','AP-4','AP-5']#,'Total']
pollutant = ['O3','PM2.5']

for species in pollutant:
    fig = plt.figure(dpi=100,figsize=(6,8))
    

    for version in versions:
        print(version)
        if species == 'O3':
            d = df_o3.copy()
            xlim = (0,85)
            xlabel = 'Measured Ozone [ppb]'
        else:
            d = df_pm.copy()    
            xlim = (1,100)
            xlabel = 'Measured PM$_{2.5}$ [\u03BCg m$^{-3}$]'
        # Set date range used based of versions
        if version == 'AP-3':
            start_date ='2009-05-01'
            end_date = '2012-12-31'
            i = 1
            abc = '(a)'
        elif version == 'AP-4':
            start_date ='2013-01-01'
            end_date = '2015-12-31'
            i = 2
            abc = '(b)'
        elif version == 'AP-5':
            start_date ='2016-01-01'
            end_date = '2018-12-31'
            i = 3
            abc = '(c)'
        elif version == 'Total':
            start_date ='2009-05-01'
            end_date = '2018-12-31'
            i = 4
            abc = '(d)'


        # Locate correct site model data
        mask = (d['datetime'] > start_date) & (d['datetime'] <= end_date) # Create a mask to determine the date range used
    
        d = d.copy().loc[mask]       
        d = d.reset_index(drop=True)
        d['version'] = version

        if species=='O3':
            var_name_mod1 = 'O3_mod'
            var_units = 'ppb'
            d = d.set_index('datetime')
            x = d.resample('H').mean()
            avg_8hr_o3 = x.rolling(8,min_periods=6).mean()
            times = avg_8hr_o3.index.values - pd.Timedelta('8h')
            avg_8hr_o3.index.values[:] = times
            d = avg_8hr_o3.resample('D').max().dropna()
            print(max(d['O3_obs']))
            
            
        if species=='PM2.5':
            var_name_mod1 = 'PM2.5_mod'            
            var_units = 'ug/m3'
            d = d.set_index('datetime')
            d = d.resample('D').mean() # resample to 24 hour average
            sze_scale = 0.5 # 0.7
            print(max(d['PM2.5_obs']))
            
            
        # plot section
        ax = fig.add_subplot(3, 1, i)
        plt.scatter(d[species+'_obs'], d[species+'_mod']/d[species+'_obs'],s=.5,color = 'black')
        
        #plt.yscale('log')
        ax.set_yscale('log')
        if species == 'PM2.5':
            ax.set_xscale('log')
        plt.xlim(xlim)
        plt.ylim(0.1,10)
        plt.hlines(1,0,85,colors = 'black',linewidth=1)
        
        if i == 3:
            ax.set_xlabel(xlabel)
        if i == 2:
            ax.set_ylabel('Forecasted / Measured Ratio')



        plt.title(abc)
    fig.tight_layout() # spaces the plots out a bit
    plt.savefig(inputDir + 'plots/scatter/ratio_scatter_'+species+'.png')
    plt.show()
