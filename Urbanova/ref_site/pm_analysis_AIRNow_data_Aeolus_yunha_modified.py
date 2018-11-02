# This script is modifed based on Vikram Ravi's python code
# program for evaluation of PM2.5 for airpact 5 using airnow data
# author - vikram ravi
# dated - 2016-02-10

# Important note:
# It requires concatenate multi-day AIRNOW (modeled and observed) data.
# cat AIRNOW1.dat AIRNOW2.dat AIRNOW3.dat > AIRNOW1-3.dat
# dated - 2017-11-30
# import some libraries
import matplotlib as mpl
mpl.use('Agg')
import pandas as pd
import numpy as np
import math
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MultipleLocator
from matplotlib import dates

from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
import time
import calendar

print('Start of PM Analysis')


mpl.rcParams['font.family'] = 'sans-serif'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 20.0
mpl.rcParams['xtick.major.size']  = 10
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['xtick.minor.size']  = 5
mpl.rcParams['xtick.minor.width'] = 1
mpl.rcParams['ytick.major.size']  = 10
mpl.rcParams['ytick.major.width'] = 2
mpl.rcParams['ytick.minor.size']  = 5
mpl.rcParams['ytick.minor.width'] = 1
mpl.rcParams['ytick.direction']   = 'in'
mpl.rcParams['xtick.direction']   = 'in'

starttime = time.time()
day='11'
month = '01' # options are August or July
year  = '2018' # or 2015

endyear='2018'
endmonth='01'
endday='22' # end day - start day

str_mt = lambda x:(x if len(x) == 2 else '0' + x)

inputDir          = r"G:\Research\Urbanova_Jordan\Urbanova\Urbanova_ref_site_comparison"
#plotDir           =r'/data/lar/projects/Urbanova_output/'

file_modelled_base = inputDir+r'/Urbanova_AIRNowSites_' + year + month + day + '-' + endyear + endmonth + endday+ '_v5.dat'  #Urbanova
print(file_modelled_base)
#file_modelled_base = inputDir+ 'catted_airpact5_O3_and_PM_conc_' + month + year + '_only1-9.dat'
file_modelled_sens = inputDir+ r'/AIRPACT_AIRNowSites_' + year + month + day + '-' + endyear + endmonth + endday + '_v5.dat'   #Airpact
print(file_modelled_sens)
file_observed_aqs = inputDir+r'/AIRNOW_hrly2018.csv'
print(file_observed_aqs)
file_airnowsites  = inputDir+ r'/aqsid.csv'
print(file_airnowsites)
#now read the files
col_names_modeled = ['date', 'time', 'site_id', 'pollutant', 'concentration']
col_names_observed= ['datetime', 'site_id', 'O3_AP5_4km', 'PM2.5_AP5_4km', 'O3_obs', 'PM2.5_obs']
df_base   = pd.read_csv(file_modelled_base, header=None, names=col_names_modeled, sep='|',dtype='unicode')
df_sens   = pd.read_csv(file_modelled_sens, header=None, names=col_names_modeled, sep='|',dtype='unicode')
df_obs   = pd.read_csv(file_observed_aqs, sep=',', names=col_names_observed, skiprows=[0],dtype='unicode')
df_sites = pd.read_csv(file_airnowsites, skiprows=[1],dtype='unicode') # skip 2nd row which is blank
df_sites.rename(columns={'AQSID':'site_id'}, inplace=True)

# select only November observation
#df_obs = df_obs[df_obs['datetime'].str.contains("\A11[/]*")]

 
 # get rid of rows if PM2.5 obs is not available
#df_obs = df_obs[pd.notnull(df_obs['PM2.5_obs'])]

# remove unnecessary column
df_obs = df_obs.drop('PM2.5_AP5_4km',1)
df_obs = df_obs.drop('O3_AP5_4km',1)




# extract only PM2.5 data
df_sens  = df_sens.loc[df_sens['pollutant']=='PM2.5', df_sens.columns]
df_base = df_base.loc[df_base['pollutant']=='PM2.5', df_base.columns]
# RENAME the PM2.5_obs to concentration (which requires for pm_24h_avg function)
df_sens.columns = df_sens.columns.str.replace('concentration', 'PM2.5_AP5_4km')
df_base.columns = df_base.columns.str.replace('concentration', 'PM2.5_AP5_1.33km')

# convert datatime colume to time data (This conversion is so slow)
df_sens['datetime'] = pd.to_datetime(df_sens['date'] + ' ' + df_sens['time'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
df_base['datetime'] = pd.to_datetime(df_base['date'] + ' ' + df_base['time'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
df_obs['datetime'] = pd.to_datetime(df_obs['datetime'], infer_datetime_format=True)

#merge all dataframe into one
#Note that df_obs already has df_sense
result = pd.merge(df_base, df_obs, on=['datetime', 'site_id'], how='inner')

# sites which are common between sens, base and Observations
sites_modeled = set(df_sens['site_id']).intersection(set(df_base['site_id']))
sites_common = set(df_obs['site_id']).intersection(sites_modeled)

## take only the data which is for common sites
df_obs_new = pd.DataFrame(columns=df_obs.columns)
df_sens_new = pd.DataFrame(columns=df_sens.columns)
df_base_new = pd.DataFrame(columns=df_base.columns)
for sites in sites_common:
#    print sites
    df1 = df_obs.loc[df_obs['site_id']==sites, df_obs.columns]
    df2 = df_sens.loc[df_sens['site_id']==sites, df_sens.columns]
    df3 = df_base.loc[df_base['site_id']==sites, df_base.columns]
    df_obs_new = pd.concat([df_obs_new, df1], join='outer', ignore_index=True)
    df_sens_new = pd.concat([df_sens_new, df2], join='outer', ignore_index=True)
    df_base_new = pd.concat([df_base_new, df3], join='outer', ignore_index=True)

# merge now
print(df_obs_new)
df_modeled = pd.merge(df_sens_new, df_base_new, on=['datetime', 'site_id'], how='outer', suffixes=('_sens', '_base'))
df_obs_mod = pd.merge(df_obs_new, df_modeled, on=['datetime', 'site_id'], how='outer')
#print(df_obs_mod)
# get rid of rows if PM2.5 base is not available
df_obs_mod = df_obs_mod[pd.notnull(df_obs_mod['PM2.5_AP5_1.33km'])]

# remove unnecessary column
df_obs_mod = df_obs_mod.drop('date_sens',1)
df_obs_mod = df_obs_mod.drop('date_base',1)
df_obs_mod = df_obs_mod.drop('pollutant_sens',1)
df_obs_mod = df_obs_mod.drop('pollutant_base',1)
df_obs_mod = df_obs_mod.drop('time_base',1)
df_obs_mod = df_obs_mod.drop('time_sens',1)

## Yunha - Dec 02 2017 - PM2.5 24h average caused so many issues (turned off)
## call the 24 hr averaging function
#df_obs_mod.set_index('datetime', inplace=True)
#df_24h = pm_24h_avg(df_obs_mod)
#df_24h['sens/obs'] = df_24h['avg_24hr_sens'] / df_24h['avg_24hr_obs']
#df_24h['base/obs'] = df_24h['avg_24hr_base'] / df_24h['avg_24hr_obs']
#
#df_siteinfo = df_sites.set_index('site_id')

# time series plots - hourly

df_tseries = df_obs_mod.copy() #[['datetime','site_id','concentration', 'concentration_sens', 'concentration_base']]
#df_tseries = df_obs_mod[['site_id','concentration', 'concentration_sens', 'concentration_base']]
#df_tseries = pd.Series(df_tseries, index=df_obs_mod['datetime'])
df_siteinfo = df_sites.set_index('site_id')
#df_tseries['site_id'] = df_tseries['site_id'].astype(int)
##df_tseries.set_index('datetime', inplace=True)
#df_tseries=df_tseries['2015-08-01':'2015-09-01']

# convert object to numeric (This is required to plot these columns)
df_tseries.loc[:,'PM2.5_AP5_4km'] = pd.to_numeric(df_tseries.loc[:,'PM2.5_AP5_4km'])
df_tseries.loc[:,'PM2.5_AP5_1.33km'] = pd.to_numeric(df_tseries.loc[:,'PM2.5_AP5_1.33km'])
df_tseries.loc[:,'PM2.5_obs'] = pd.to_numeric(df_tseries.loc[:,'PM2.5_obs'])

#print(df_tseries.loc[:,'PM2.5_obs'] )
for sid in list(set(df_tseries['site_id'])):
    d = df_tseries.loc[df_tseries['site_id']==sid]
    site_nameinfo = df_siteinfo.ix[sid, 'long_name']
    #print(d.set_index('datetime').ix[:,['PM2.5_obs', 'PM2.5_AP5_4km','PM2.5_AP5_1.33km']])
    d.drop('site_id',1)
    fig,ax=plt.subplots(1,1, figsize=(12,4))
##    d.ix[:,['avg_24hr_sens', 'avg_24hr_base', 'avg_24hr_obs']].plot(kind='line', style='-o', ax=ax)
    d.set_index('datetime').ix[:,['PM2.5_obs', 'PM2.5_AP5_4km','PM2.5_AP5_1.33km']].plot(kind='line', style='-', ax=ax, color=['black', 'blue', 'red'])
    #    d.set_index('datetime').ix[:,['concentration', 'concentration_sens', 'concentration_base']].plot(kind='line', style='-', ax=ax, color=['black', 'blue', 'red'], label=['OBS', 'sens', 'base'])
    ax.set_title(site_nameinfo)
    ax.set_ylabel('PM2.5, ug/m3')
    ax.legend(['OBS', 'AP5_4km', 'AP5_1.33km'], fontsize=12)
    plt.savefig(inputDir+r'/timeseries_plot/PM_'+site_nameinfo+'_'+ year +month +day+ '-' + endyear + endmonth + endday+'.pdf', pad_inches=0.1, bbox_inches='tight')

