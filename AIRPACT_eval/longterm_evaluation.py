# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 10:18:47 2018

@author: Jordan Munson
"""

import matplotlib as mpl
import pandas as pd
import matplotlib.dates as mdates
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
#Set directory
inputDir = r'E:/Research/AIRPACT_eval/All_Criteria_pollutant_obs_2014-2017_Yunha/'
# Open statistics script
exec(open(r'E:/Research/Urbanova_Jordan/statistical_functions.py').read())

##############################################################################
#Run stats for individual years
##############################################################################

#2014
#Call species csv's
species = ['CO','NO2','O3','PM10','PM2.5','SO2']
g = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
g.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
g = g.drop(0,1)

for pollutant in species:
    d=pd.read_csv(inputDir + pollutant + '.csv', sep=',')
    d['date'] = pd.to_datetime(d['date'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")  
    mask = (d['date'] > '2014-7-1') & (d['date'] <= '2015-6-30')    #Select time span to run for
    d=d.loc[mask]   #Portion of only running for specific dates
    d = d.dropna()  #Remove values that are nan, otherwise messes with the stats
    
    # This section lines up the correct mod and obs columns
    try:
        obs = 'Daily_mean_Conc'
        mod = 'AP4.'+pollutant+'.Daily_mean_Conc'
        aq_stats = stats(d,mod,obs) # stats is a function in the referenced script in the beginning
        
    except(KeyError):
        try:
            obs = 'Daily_8hrmax_Conc'
            mod = 'AP4.'+pollutant+'.Daily_8hrmax_Conc'
            aq_stats = stats(d,mod,obs)
            
        except(KeyError):
                obs = 'Daily_1hrmax_Conc'
                mod = 'AP4.'+pollutant+'.Daily_1hrmax_Conc'
                aq_stats = stats(d,mod,obs)
    # Remove rows that would create 0 when subtracted, without this FB and FE result as infinite due to 0 in their denominator
    d['diff'] = d[obs].abs()-d[mod].abs()
    d = d.drop(d[d['diff'] == 0].index)
    aq_stats=stats(d,mod,obs)
    
    g = pd.merge(g, aq_stats, how = 'inner', left_index = True, right_index = True) #Combines this time section into one dataframe
stats_2014=np.transpose(g)
#stats_2014=g

#2015
#Call species csv's
species = ['CO','NO2','O3','PM10','PM2.5','SO2']
g = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
g.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
g = g.drop(0,1)

for pollutant in species:
    d=pd.read_csv(inputDir + pollutant + '.csv', sep=',')
    d['date'] = pd.to_datetime(d['date'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")  
    mask = (d['date'] > '2015-7-1') & (d['date'] <= '2016-6-30')
    d=d.loc[mask]
    d = d.dropna()    
    
    try:
        obs = 'Daily_8hrmax_Conc'
        mod = 'AP4.'+pollutant+'.Daily_8hrmax_Conc'
        aq_stats = stats(d,mod,obs)
    except(KeyError):
        try:
            obs = 'Daily_1hrmax_Conc'
            mod = 'AP4.'+pollutant+'.Daily_1hrmax_Conc'
            aq_stats = stats(d,mod,obs)
        except(KeyError):
            obs = 'Daily_mean_Conc'
            mod = 'AP4.'+pollutant+'.Daily_mean_Conc'
            aq_stats = stats(d,mod,obs)
    d['diff'] = d[obs].abs()-d[mod].abs()
    d = d.drop(d[d['diff'] == 0].index)
    aq_stats=stats(d,mod,obs)
    
    g = pd.merge(g, aq_stats, how = 'inner', left_index = True, right_index = True)
stats_2015=np.transpose(g)
#stats_2015=g

#2016
#Call species csv's
species = ['CO','NO2','O3','PM10','PM2.5','SO2']
g = pd.DataFrame(['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"])
g.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
g = g.drop(0,1)

for pollutant in species:
    d=pd.read_csv(inputDir + pollutant + '.csv', sep=',')
    d['date'] = pd.to_datetime(d['date'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")  
    mask = (d['date'] > '2016-7-1') & (d['date'] <= '2017-6-30')
    d=d.loc[mask]
    d = d.dropna()    
    
    try:
        obs = 'Daily_8hrmax_Conc'
        mod = 'AP4.'+pollutant+'.Daily_8hrmax_Conc'
        aq_stats = stats(d,mod,obs)
    except(KeyError):
        try:
            obs = 'Daily_1hrmax_Conc'
            mod = 'AP4.'+pollutant+'.Daily_1hrmax_Conc'
            aq_stats = stats(d,mod,obs)
        except(KeyError):
            obs = 'Daily_mean_Conc'
            mod = 'AP4.'+pollutant+'.Daily_mean_Conc'
            aq_stats = stats(d,mod,obs)
    d['diff'] = d[obs].abs()-d[mod].abs()
    d = d.drop(d[d['diff'] == 0].index)
    aq_stats=stats(d,mod,obs)
    
    g = pd.merge(g, aq_stats, how = 'inner', left_index = True, right_index = True)
stats_2016=np.transpose(g)
#stats_2016=g

stats_2014.to_csv(inputDir + '/stats_2014.csv')
stats_2015.to_csv(inputDir + '/stats_2015.csv')
stats_2016.to_csv(inputDir + '/stats_2016.csv')

#%%
# Set plot parameters
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
'''
#Plot
def daily(df):
    for AQS_ID in list(set(df['AQS_ID'])):
        d = df.loc[df['AQS_ID']==AQS_ID]
        print(d)
        site_nameinfo = d.ix[AQS_ID, 'Sitename']
    
        fig,ax=plt.subplots(1,1, figsize=(12,4))
        d.set_index('datetime').ix[:,['obs','AP5_4km']].plot(kind='line', style='-', ax=ax, color=['black', 'blue'], label=['OBS', 'Model'])
        ax.set_title(site_nameinfo)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        #    ax.set_ylabel(abrv+' '+unit)        
        ax.legend(['OBS', 'AP5'], fontsize=12)

        plt.savefig(inputDir + AQS_ID+'.pdf', pad_inches=0.1, bbox_inches='tight')

CO = pd.read_csv(inputDir + 'CO.csv', sep=',')
d['date'] = pd.to_datetime(d['date'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")  
daily(CO)
'''

CO = pd.read_csv(inputDir + 'CO.csv', sep=',')
df = CO.drop_duplicates()
'''
for AQS_ID in list(set(df['AQS_ID'])):
        d = df.loc[df['AQS_ID']==AQS_ID]
        #site_nameinfo = d.ix[AQS_ID, 'Sitename']
        d=d.reset_index()
        site_nameinfo = d.loc[0,'Sitename']
        
        fig,ax=plt.subplots(1,1, figsize=(12,4))
        d['date'] = pd.to_datetime(d['date'], infer_datetime_format=True)
        ax.xaxis_date()
        d=d.set_index('date').ix[:,['Daily_8hrmax_Conc','AP4.CO.Daily_8hrmax_Conc']]
        d.plot(kind='line', style='-', ax=ax, color=['black', 'blue'], label=['OBS', 'Model'])
        ax.set_title(site_nameinfo)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.set_ylabel('CO (ppm)')
        ax.set_xlabel('2014-2017')        
        ax.legend(['Observation', 'Model'], fontsize=12)

        plt.savefig(inputDir + '/plots/hourly/hourly_'+site_nameinfo+'.pdf', pad_inches=0.1, bbox_inches='tight')
             
''' 
#Read ozone and pm dataframes
O3 = pd.read_csv(inputDir + 'O3.csv', sep=',').drop(['Parameter.Name'], axis = 1) #Drops parameter name to avoid conflicts
PM2p5 = pd.read_csv(inputDir + 'PM2.5.csv', sep=',').drop(['Parameter.Name'], axis = 1)
df = pd.merge(O3,PM2p5, on = ['AQS_ID','date','XCell','YCell','Latitude','Longitude','Sitename'], how = 'outer')  #Combines datagrames
   
# Scatter plots
for AQS_ID in list(set(O3['AQS_ID'])):
    #This section selects only data relevant to the aqs site
    d = O3.loc[O3['AQS_ID']==AQS_ID]
    d=d.reset_index()
    site_nameinfo = d.loc[0,'Sitename'] #Gets the longname of the site to title the plot
    d=d.ix[:,['Daily_8hrmax_Conc','AP4.O3.Daily_8hrmax_Conc','date']]
    d['date'] = pd.to_datetime(d['date'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
    fig,ax=plt.subplots(1,1, figsize=(8,8)) #Set figure dimensions
    
    #Find max values to set axis
    #axismax = max(max(d['AP4.PM2.5.Daily_mean_Conc'],numeric_only=True),max(d['AP4.O3.Daily_8hrmax_Conc']))     #This works on some PC's but not others
    try:    #The axis max makes sure the x and y axis are the same
        axismax= max(d.max(numeric_only=True))
        ax.set_ylim(0,axismax)
        ax.set_xlim(0,axismax)
        plt.plot([0,axismax], [0,axismax], color='black')
    except ValueError:
        pass
    
    #Plot first section of year
    mask = (d['date'] > '2014-7-1') & (d['date'] <= '2015-6-30')
    da=d.loc[mask]
    ax.scatter(da['Daily_8hrmax_Conc'], da['AP4.O3.Daily_8hrmax_Conc'], c='b', label = '07/14-07/15',linewidths=None, alpha=0.7) #Plotting the data
    
    #Plot first section of year
    mask = (d['date'] > '2015-7-1') & (d['date'] <= '2016-6-30')
    db=d.loc[mask]
    ax.scatter(db['Daily_8hrmax_Conc'], db['AP4.O3.Daily_8hrmax_Conc'], c='r', label = '07/15-07/16',linewidths=None, alpha=0.7) #Plotting the data
    
    #Plot first section of year
    mask = (d['date'] > '2016-7-1') & (d['date'] <= '2017-6-30')
    dc=d.loc[mask]
    ax.scatter(dc['Daily_8hrmax_Conc'], dc['AP4.O3.Daily_8hrmax_Conc'], c='g', label = '07/16-07/17',linewidths=None, alpha=0.7) #Plotting the data
    
    ax.set_aspect('equal', 'box')
    plt.axis('equal')
    ax.set_ylabel('Ozone Modeled')
    ax.set_xlabel('Ozone Observed')        
    ax.set_title(site_nameinfo) 
    plt.legend()

    #plt.plot()
    if axismax>1:
        plt.savefig(inputDir +'/plots/scatter/Ozone_scatter_' + site_nameinfo+'.png', pad_inches=0.1, bbox_inches='tight')
    else:
        pass
        
# Scatter plots
for AQS_ID in list(set(PM2p5['AQS_ID'])):
    #This section selects only data relevant to the aqs site
    d = PM2p5.loc[PM2p5['AQS_ID']==AQS_ID]
    d=d.reset_index()
    site_nameinfo = d.loc[0,'Sitename'] #Gets the longname of the site to title the plot
    d=d.ix[:,['Daily_mean_Conc','AP4.PM2.5.Daily_mean_Conc','date']]
    d['date'] = pd.to_datetime(d['date'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
    fig,ax=plt.subplots(1,1, figsize=(8,8)) #Set figure dimensions
    
    #Find max values to set axis
    #axismax = max(max(d['AP4.PM2.5.Daily_mean_Conc'],numeric_only=True),max(d['AP4.O3.Daily_8hrmax_Conc']))     #This works on some PC's but not others
    try:    #The axis max makes sure the x and y axis are the same
        axismax= max(d.max(numeric_only=True))
        ax.set_ylim(0,axismax)
        ax.set_xlim(0,axismax)
        plt.plot([0,axismax], [0,axismax], color='black')
    except ValueError:
        pass
    
    #Plot first section of year
    mask = (d['date'] > '2014-7-1') & (d['date'] <= '2015-6-30')
    da=d.loc[mask]
    ax.scatter(da['Daily_mean_Conc'], da['AP4.PM2.5.Daily_mean_Conc'], c='b', label = '07/14-07/15',linewidths=None, alpha=0.7) #Plotting the data
    
    #Plot first section of year
    mask = (d['date'] > '2015-7-1') & (d['date'] <= '2016-6-30')
    db=d.loc[mask]
    ax.scatter(db['Daily_mean_Conc'], db['AP4.PM2.5.Daily_mean_Conc'], c='r', label = '07/15-07/16',linewidths=None, alpha=0.7) #Plotting the data
    
    #Plot first section of year
    mask = (d['date'] > '2016-7-1') & (d['date'] <= '2017-6-30')
    dc=d.loc[mask]
    ax.scatter(dc['Daily_mean_Conc'], dc['AP4.PM2.5.Daily_mean_Conc'], c='g', label = '07/16-07/17',linewidths=None, alpha=0.7) #Plotting the data
    
    ax.set_aspect('equal', 'box')
    plt.axis('equal')
    ax.set_ylabel('$PM_{2.5}$ Modeled')
    ax.set_xlabel('$PM_{2.5}$ Observed')        
    ax.set_title(site_nameinfo) 
    plt.legend()

    #plt.plot()
    if axismax>1:
        plt.savefig(inputDir +'/plots/scatter/PM_scatter_' + site_nameinfo+'.png', pad_inches=0.1, bbox_inches='tight')
    else:
        pass
        
        
        
#test = pd.read_csv(r'E:/Research/AIRPACT_eval/AQS_data/hourly_44201_2014.csv', sep=',')    
#%%
'''
obs_sp = ['Daily_mean_Conc']

for i, sp in enumerate(obs_sp):
    
    cnt = 0
    figs = plt.figure()
    plot_num = 321 # 6 plots in a single page
    fig = plt.figure(figsize=(10, 10)) # inches
    
    out_pdf = inputDir +'/plots/scatter/PM_scatter_' + str(cnt)+'.png'
    print(out_pdf)   
    
    pdf = PdfPages(out_pdf)
    # Scatter plots
    for AQS_ID in list(set(PM2p5['AQS_ID'])):
        #This section selects only data relevant to the aqs site
        d = PM2p5.loc[PM2p5['AQS_ID']==AQS_ID]
        d=d.reset_index()
        site_nameinfo = d.loc[0,'Sitename'] #Gets the longname of the site to title the plot
        d=d.ix[:,['Daily_mean_Conc','AP4.PM2.5.Daily_mean_Conc','date']]
        d['date'] = pd.to_datetime(d['date'], infer_datetime_format=True) #format="%m/%d/%y %H:%M")
        fig,ax=plt.subplots(1,1, figsize=(8,8)) #Set figure dimensions
    
        #Find max values to set axis
        #axismax = max(max(d['AP4.PM2.5.Daily_mean_Conc'],numeric_only=True),max(d['AP4.O3.Daily_8hrmax_Conc']))     #This works on some PC's but not others
        try:    #The axis max makes sure the x and y axis are the same
            axismax= max(d.max(numeric_only=True))
            ax.set_ylim(0,axismax)
            ax.set_xlim(0,axismax)
            plt.plot([0,axismax], [0,axismax], color='black')
        except ValueError:
            pass
    
        #Plot first section of year
        mask = (d['date'] > '2014-7-1') & (d['date'] <= '2015-6-30')
        da=d.loc[mask]
        ax.scatter(da['Daily_mean_Conc'], da['AP4.PM2.5.Daily_mean_Conc'], c='b', label = '07/14-07/15',linewidths=None, alpha=0.7) #Plotting the data
    
        #Plot first section of year
        mask = (d['date'] > '2015-7-1') & (d['date'] <= '2016-6-30')
        db=d.loc[mask]
        ax.scatter(db['Daily_mean_Conc'], db['AP4.PM2.5.Daily_mean_Conc'], c='r', label = '07/15-07/16',linewidths=None, alpha=0.7) #Plotting the data
    
        #Plot first section of year
        mask = (d['date'] > '2016-7-1') & (d['date'] <= '2017-6-30')
        dc=d.loc[mask]
        ax.scatter(dc['Daily_mean_Conc'], dc['AP4.PM2.5.Daily_mean_Conc'], c='g', label = '07/16-07/17',linewidths=None, alpha=0.7) #Plotting the data
    
        ax.set_aspect('equal', 'box')
        plt.axis('equal')
        ax.set_ylabel('$PM_2.5$ Modeled')
        ax.set_xlabel('$PM_2.5$ Observed')        
        ax.set_title(site_nameinfo) 
        plt.legend()

        plot_num += 1

        if(cnt > 0) & (np.remainder(cnt,6) == 5):
            print("saving at cnt :", cnt)
            pdf.savefig(fig)
            plot_num = 321
            fig = plt.figure(figsize=(10, 10)) # inches

        cnt += 1
    pdf.close()
    plt.close('all')

'''






