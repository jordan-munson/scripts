# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 08:33:10 2018

@author: Jordan Munson
"""
import matplotlib as mpl
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import time
from matplotlib.dates import DateFormatter

starttime = time.time()
begin_time = time.time()

#Set directorys
inputDir = r'E:/Research/AIRPACT_eval/'
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'
aqsid = pd.read_csv(r'E:\Research\AIRPACT_eval/aqs_sites.csv')
        
        
# Open statistics script
exec(open(stat_path).read())

# load data
df_com = pd.read_csv(inputDir+'AQS_data/df_com_aplong.csv').drop('Unnamed: 0', axis=1)
df_com.loc[:,'O3_mod'] = pd.to_numeric(df_com.loc[:,'O3_mod'], errors='coerce')
df_com.loc[:,'PM2.5_mod'] = pd.to_numeric(df_com.loc[:,'PM2.5_mod'], errors='coerce')
df_com.loc[:,'O3_obs'] = pd.to_numeric(df_com.loc[:,'O3_obs'], errors='coerce')
df_com.loc[:,'PM2.5_obs'] = pd.to_numeric(df_com.loc[:,'PM2.5_obs'], errors='coerce')
df_com['datetime'] = pd.to_datetime(df_com['datetime'])

# Load common AQSID
df_com['AQSID'] = df_com['AQSID'].astype(str) # force this column as string to avoid any combining erros.
df_aqsid_o3 = pd.read_csv(inputDir+'/o3_aqsid.csv',dtype=str).drop('Unnamed: 0', axis=1) # load in AQSID that are present for all versions of AIRPACT. This is created later in the script.
df_aqsid_pm = pd.read_csv(inputDir+'/pm_aqsid.csv',dtype=str).drop('Unnamed: 0', axis=1) # load in AQSID that are present for all versions of AIRPACT. This is created later in the script.

print('Data loading section done')

# Set plot parameters
mpl.rcParams['font.family'] = 'calibri'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 10.0
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


# =============================================================================
# stats_com = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
# stats_com.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
# stats_com = stats_com.drop(0,1)
# =============================================================================

#%%
# =============================================================================
#  The section below makes seasonal plots irregardless of site type
# =============================================================================

settings = ['RURAL', 'SUBURBAN', 'URBAN AND CENTER CITY']
seasons = ['Summer','Fall','Winter','Spring'] 
# =============================================================================
# seasons = ['Summer','Winter'] 
# =============================================================================

pollutant = ['PM2.5','O3']

# =============================================================================
# pollutant = ['O3']
# pollutant = ['PM2.5']
# =============================================================================

versions = ['AP3','AP4','AP5']

# Short version to make running on pc faster

for species in pollutant:
    stats_com = pd.DataFrame(['Forecast Mean', 'Observation Mean', 'MB','ME','FB [%]','FE [%]',"NMB [%]", "NME [%]", "RMSE", "R^2 [-]",'Forecast 98th','Observation 98th','version','season','unit','species'])
    stats_com.index = ['Forecast Mean', 'Observation Mean', 'MB','ME','FB [%]','FE [%]',"NMB [%]", "NME [%]", "RMSE", "R^2 [-]",'Forecast 98th','Observation 98th','version','season','unit','species']
    stats_com = stats_com.drop(0,1)
    print(species)
    da = df_com    #.dropna(subset=['Location Setting'])
    # Create the overal plot and its settings
    fig = plt.figure(figsize=(6,3),dpi=300)#8,4)) # seems to do nothing here really
    if species == 'PM2.5':
        #fig.set_ylabel('$PM_{2.5} (ug/m^3)$')
        fig.text(-0.015, 0.5, '$PM_{2.5} [ug/m^3]$', va='center', rotation='vertical')
        da = pd.merge(da,df_aqsid_pm,on='AQSID') # isolate to common aqsid
        var_units = '\u03BCg m$^{-3}$'

    else:
        #fig.set_ylabel('Ozone (ppb)') 
        fig.text(-0.015, 0.5, 'Ozone [ppb]', va='center', rotation='vertical')
        da = pd.merge(da,df_aqsid_o3,on='AQSID') # isolate to common aqsid
        var_units = 'ppb'

    fig.tight_layout() # spaces the plots out a bit

    fig.text(0.185, 1, 'AP-3', va='center',ha='center') # 0.98
    fig.text(0.505, 1, 'AP-4', va='center',ha='center')
    fig.text(0.83, 1, 'AP-5', va='center',ha='center')
    # seasons
    
    for version,i in zip(versions,[0,1,2]):#[0,4,8]):
        print(version)
    # Set date range used based of versions
        if version == 'AP3':

            years = [2009,2010,2011,2012]
        elif version == 'AP4':

            years = [2013,2014,2015]
        elif version == 'AP5':

            years = [2016,2017,2018]
           
        for season in seasons:
            print(season)
            db=pd.DataFrame()       #reset empty
            #This section selects only data relevant to the aqs site
 
            # set dataframe maybe
            #d=df_com.copy()
            d = da.copy()
            d=d.ix[:,[species+'_obs',species+'_mod','datetime']]
            #print('starting datetime conversion')
            d['date'] = pd.to_datetime(d['datetime'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
            #print('datetime conversion finished')
            d = d.set_index('datetime') # Set datetime column as index
            d1=pd.DataFrame()
            d2=pd.DataFrame()
            d3=pd.DataFrame()
            for year in years:
            # Select seasons
                if season == 'Summer':
                    year = str(year)
                    mask = (d.index > year+'-6-1') & (d.index <= year+'-6-30')
                    d11=d.loc[mask]
                    d1 = d1.append(d11)
                    mask = (d.index > year+'-7-1') & (d.index <= year+'-7-31')
                    d22=d.loc[mask]
                    d2 = d2.append(d22)
                    mask = (d.index > year+'-8-1') & (d.index <= year+'-8-31')
                    d33=d.loc[mask]
                    d3 = d3.append(d33)
                    s = '6/1/2009'
                    if species == 'O3':    
                        e = '8/30/2009'
                    else:
                        e = '8/31/2009'
                    dates = pd.date_range(start=s,end=e) 
                    ax = fig.add_subplot(2,3,4+i)#(6,2,3+i)
                    
                if season == 'Fall':
                    year = str(year)
                    mask = (d.index > year+'-9-1') & (d.index <= year+'-9-30')
                    d11=d.loc[mask]
                    d1 = d1.append(d11)
                    mask = (d.index > year+'-10-1') & (d.index <= year+'-10-31')
                    d22=d.loc[mask]
                    d2 = d2.append(d22)
                    mask = (d.index > year+'-11-1') & (d.index <= year+'-11-30')
                    d33=d.loc[mask]
                    d3 = d3.append(d33)
                    s = '9/1/2009'
                    e = '11/30/2009'
                    if species == 'O3':
                        e = '11/29/2009' 
                    else:
                        e = '11/30/2009'
                    dates = pd.date_range(start=s,end=e)
                    #ax = fig.add_subplot(6,2,4+i)
                    
                if season == 'Winter':
                    if year == 2009:   # Don't have 2008 data, so have to skip first iteration
                        continue
                    mask = (d.index > str(year-1)+'-12-1') & (d.index <= str(year-1)+'-12-31')
                    d11=d.loc[mask]
                    d1 = d1.append(d11)
                    year = str(year)
                    mask = (d.index > year+'-1-1') & (d.index <= year+'-1-31')
                    d22=d.loc[mask]
                    d2 = d2.append(d22)
                    mask = (d.index > year+'-2-1') & (d.index <= year+'-2-28')
                    d33=d.loc[mask]
                    d3 = d3.append(d33)
                    s = '12/1/2009'
                    if species == 'O3':
                        e = '2/27/2010' 
                    else:
                        e = '2/28/2010'
                    dates = pd.date_range(start=s,end=e)
                    ax = fig.add_subplot(2,3,1+i)#(6,2,1+i)

                    
                if season == 'Spring':
                    if year == 2009:   # Don't have 2008 data, so have to skip first iteration
                        continue
                    year = str(year)
                    mask = (d.index > year+'-3-1') & (d.index <= year+'-3-31')
                    d11=d.loc[mask]
                    d1 = d1.append(d11)
                    mask = (d.index > year+'-4-1') & (d.index <= year+'-4-30')
                    d22=d.loc[mask]
                    d2 = d2.append(d22)
                    mask = (d.index > year+'-5-1') & (d.index <= year+'-5-31')
                    d33=d.loc[mask]
                    d3 = d3.append(d33)
                    s = '3/1/2009'
                    e = '5/31/2009'
                    if species == 'O3':
                        e = '5/29/2009' 
                    else:
                        e = '5/31/2009'
                    dates = pd.date_range(start=s,end=e)
                    #ax = fig.add_subplot(6,2,2+i)

                    
            #plt.rcParams["figure.figsize"] = (8,4)
            plt.tight_layout() # spaces the plots out a bit

            # Change data to monthly averages
            if species == 'O3':
                # 8-hour ozone script from http://danielrothenberg.com/gcpy/examples/timeseries/calc_mda8_timeseries.html
                cat = [d1,d2,d3]
                db = pd.concat(cat).reset_index(drop=True).set_index('date')

                # find daily max 8 hour average
                dbc = pd.DataFrame()
                for x in cat:
                    x = x.drop('date',axis=1)
                    x = x.resample('H').mean()
                    avg_8hr_o3 = x.rolling(8,min_periods=6).mean()
                    times = avg_8hr_o3.index.values - pd.Timedelta('8h')
                    avg_8hr_o3.index.values[:] = times
                    
                    avg_8hr_o3['date'] = avg_8hr_o3.index.strftime('%H')
                    intervals = ['00','01','02','03','04','05','06','24'] # remove these hours as per EPA regulation
                    for interval in intervals:
                        avg_8hr_o3 = avg_8hr_o3[~avg_8hr_o3.date.str.contains(interval)]
                        
                    x1 = avg_8hr_o3.resample('D').max().drop('date',axis=1)
# =============================================================================
#                     # this way performs the calc like Joe suggested 2/6/19
#                     x = x.drop('date',axis=1)
#                     avg_8hr_o3 = x.rolling(8,min_periods=6).mean()
#                     times = avg_8hr_o3.index.values - pd.Timedelta('8h')
#                     avg_8hr_o3.index.values[:] = times
#                     avg_8hr_o3 = avg_8hr_o3.resample('H').mean()
#                     x1 = avg_8hr_o3.resample('D').max().dropna()
# =============================================================================
                    
                    dbc = dbc.append(x1.groupby(x1.index.day).mean())
                db = dbc.dropna()
                
                db['datetime'] = dates
                db = db.set_index('datetime')
            else:
                d1 = d1.groupby(d1.index.day).mean()
                d2 = d2.groupby(d2.index.day).mean()
                d3 = d3.groupby(d3.index.day).mean()
                cat = [d1,d2,d3]
                db = pd.concat(cat).reset_index(drop=True)
                db['datetime'] = dates
                db = db.set_index('datetime')
            #db = db.resample('D', convention='start').mean()
            if season == 'Summer' or season == 'Winter':
                # Plotting section
                #ax = fig.add_subplot(1,i,1)
                #Plot
                db.ix[:,[species+'_obs', species+'_mod']].plot(kind='line', style='-', ax=ax, color=['black', 'red'])
                ax.set_xlim(s,e) # set limits in the hopes of removing doubled last label
                plt.setp(ax.get_xticklabels())#, horizontalalignment='right') # angle x axis labels
                if species == 'PM2.5':
                    #ax.set_ylabel('$PM_{2.5} (ug/m^3)$')
                    ax.set_ylim(0,30)
                    height = 20 # Height of annotations in graphs
                    spc = 1.2 # Space the annotations are moved up and down
                else:
                    #ax.set_ylabel('Ozone (ppb)')
                    ax.set_ylim(20,75)
                    #ax.set_ylim(0,120) # for use with 8 hour max ave
                    height=10
                    spc = 2
                
                #ax.set_xlim('2009-1-1','2018-7-1')
                myFmt = DateFormatter("%b")
                months = mdates.MonthLocator() 
                days = mdates.DayLocator(bymonthday=(1,1))  
                ax.xaxis.set_major_formatter(myFmt)
                ax.xaxis.set_major_locator(months)
                ax.xaxis.set_minor_locator(days)
                ax.set_xlabel('')        # Gets rid of the 'DateTime' x label and replaces with a space
    
                sze = 10 #size of annotation text            
                
                # Set letter denoting plot
                if i ==0:
                    if season == 'Winter':
                        abc = '(a)'
                        plt.legend(['Observation','Forecast'],prop={'size': 8})
                    else:
                        abc = '(d)'
                        ax.get_legend().remove()
                if i ==1:
                    ax.get_legend().remove()
                    if season == 'Winter':
                        abc = '(b)'
                    else:
                        abc = '(e)'
                if i ==2:
                    ax.get_legend().remove()
                    if season == 'Winter':
                        abc = '(c)'
                    else:
                        abc = '(f)'
                #ax.text(0.5, 1.1,abc, ha='right', va='center', transform=ax.transAxes)
                ax.set_title(abc,fontsize = sze)
        
                plt.grid(True)    # Add grid lines to make graph interpretation easier
            
            #Calculate Statistics
            try:
                #Run stats functions
                aq_stats = stats_version(db, species+'_mod', species+'_obs')
            
                aq_stats.columns = aq_stats.columns.str.replace(species, species+'_'+version+'_'+season)     
       
                # Merge stats into single dataframe
                aq_stats.columns = aq_stats.columns.str.replace('_mod', '')    
                aq_stats = aq_stats.T
                aq_stats['version'] = version
                aq_stats['season'] = season
                aq_stats['unit'] = var_units
                aq_stats['species'] = species
                aq_stats = aq_stats.T
                stats_com = pd.merge(stats_com, aq_stats, how = 'inner', left_index = True, right_index = True)     

            except (ZeroDivisionError):
                print('Zero division error in stats section')
                pass
    stats_com = stats_com.T
    stats_com.to_csv(inputDir + '/stats/seasonal_'+species+'_common.csv')
    try:
        if species == 'O3':
            print('O3')          
            plt.savefig(inputDir+'/plots/seasons/'+'O3_8hr_seasons_common.png',  pad_inches=0.1, bbox_inches='tight')
        else:
            print('PM')
            plt.savefig(inputDir+'/plots/seasons/'+'PM_seasons_common.png',  pad_inches=0.1, bbox_inches='tight')
        plt.show()
        plt.close()
    except(FileNotFoundError):
        pass
end_time = time.time()
print("Run time was %s minutes"%(round((end_time-begin_time)/60)))
print('done')





