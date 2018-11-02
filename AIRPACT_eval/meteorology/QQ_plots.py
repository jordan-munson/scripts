# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 07:43:27 2018

@author: Jordan Munson
"""
# Load libraries
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statsmodels.api as sm
import pylab
import matplotlib.patches as patches


# Set directories
inputdir = r'E:/Research/AIRPACT_eval/meteorology/'
outputdir = r'E:/Research/AIRPACT_eval/meteorology/AQS_plots/QQ_plots/'

#Load data
df_airpact = pd.read_csv(inputdir+'df_airpact.csv').drop(['Unnamed: 0','lat','lon'],axis=1)
df_obs = pd.read_csv(inputdir+'df_obs.csv').drop(['Unnamed: 0','Local Site Name'],axis=1).rename(columns={'datetime':'DateTime'})

# Determine RH
pq0 = 379.90516
a2 = 17.2693882
a3 = 273.16
a4 = 35.86
df_airpact['RH'] = (df_airpact['Q2'] / ( (pq0 / df_airpact['PRSFC']) * np.exp(a2 * 
                   (df_airpact['TEMP2'] - a3) / (df_airpact['TEMP2'] - a4)) ))*100
    
# Convert temp
#df_obs['aqs_temp'] = (df_obs['aqs_temp']+459.67)*(5/9)
df_airpact['TEMP2'] = df_airpact['TEMP2']*9/5 -459.67 #Fahrenheit

# combine data
df_all = pd.merge(df_airpact,df_obs, how ='outer',left_index=True,right_index=True, on = ['AQS_ID','DateTime'])

# Set different versions to run for
versions = ['AIRPACT3','AIRPACT4','AIRPACT5'] #List versions

for version in versions:
    
    # Set date range used based of versions
    if version == 'AIRPACT3':
        start_date ='2009-05-01'
        end_date = '2014-07-01'
    elif version == 'AIRPACT4':
        start_date ='2014-07-01'
        end_date = '2015-12-01'
    elif version == 'AIRPACT5':
        start_date ='2015-12-01'
        end_date = '2018-07-01'
        
    # Locate correct site model data
    mask = (df_all['DateTime'] > start_date) & (df_all['DateTime'] <= end_date) # Create a mask to determine the date range used
    df_mod1 = df_all.loc[mask]        
        
    # Calculate quantiles
    q = np.arange(0.01,1,0.01)
    df_qq = df_mod1.quantile(q)
    
    

    # Plot Temperature
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # Plot them
    ax.scatter(df_qq['aqs_temp'],df_qq['TEMP2'], marker = 'o',label='Temperature')
    
    
    # Label plot
    ax.set(title=version+' Temperature',xlabel='Observed (F)',ylabel='Model (F)')
    
    # Set plot limits
    plot_lim = 100
    plt.ylim((0,plot_lim))
    plt.xlim((0,plot_lim))
    
    # Draw rectangle to point out a value
    rect1 = patches.Rectangle((0,0),50,50,facecolor='none',linewidth=1,edgecolor='black',linestyle='dashed')
    #ax.add_patch(rect1)
    
    # Draw a 1:1 line
    plt.plot([0,100],[0,100], linestyle='--',color='black',alpha=0.5)
    
    fig.savefig(outputdir + version+'_QQ_temp_total.png' ,bbox_inches='tight')
    
    #%%
    # Plot Wind speed
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # Plot them
    ax.scatter(df_qq['aqs_wspd'],df_qq['WSPD10'], marker = 'o',label='Wind Speed')
    
    
    # Label plot
    ax.set(title=version+' Wind Speed',xlabel='Observed (m/s)',ylabel='Model (m/s)')
    
    # Set plot limits
    plot_lim = 16
    plt.ylim((0,plot_lim))
    plt.xlim((0,plot_lim))
    
    # Draw rectangle to point out a value
    rect1 = patches.Rectangle((0,0),50,50,facecolor='none',linewidth=1,edgecolor='black',linestyle='dashed')
    #ax.add_patch(rect1)
    
    # Draw a 1:1 line
    plt.plot([0,100],[0,100], linestyle='--',color='black',alpha=0.5)
    
    fig.savefig(outputdir + version+'_QQ_wspd_total.png' ,bbox_inches='tight')
    
    #%%
    # Plot Wind direction
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # Plot them
    ax.scatter(df_qq['aqs_wdir'],df_qq['WDIR10'], marker = 'o',label='Wind Direction')
    
    
    # Label plot
    ax.set(title=version+' Wind Direction',xlabel='Observed (degrees)',ylabel='Model (degrees)')
    
    # Set plot limits
    plot_lim = 400
    plt.ylim((0,plot_lim))
    plt.xlim((0,plot_lim))
    
    # Draw rectangle to point out a value
    rect1 = patches.Rectangle((0,0),50,50,facecolor='none',linewidth=1,edgecolor='black',linestyle='dashed')
    #ax.add_patch(rect1)
    
    # Draw a 1:1 line
    plt.plot([0,plot_lim],[0,plot_lim], linestyle='--',color='black',alpha=0.5)
    
    fig.savefig(outputdir + version+'_QQ_wdir_total.png' ,bbox_inches='tight')
    
    #%%
    # RH
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # Plot them
    ax.scatter(df_qq['aqs_rh'],df_qq['RH'], marker = 'o',label='Relative Humidity')
    
    
    # Label plot
    ax.set(title=version+' Relative Humidity',xlabel='Observed (%)',ylabel='Model (%)')
    
    # Set plot limits
    plot_lim = 100
    plt.ylim((0,plot_lim))
    plt.xlim((0,plot_lim))
    
    # Draw rectangle to point out a value
    rect1 = patches.Rectangle((0,0),50,50,facecolor='none',linewidth=1,edgecolor='black',linestyle='dashed')
    #ax.add_patch(rect1)
    
    # Draw a 1:1 line
    plt.plot([0,plot_lim],[0,plot_lim], linestyle='--',color='black',alpha=0.5)
    
    fig.savefig(outputdir + version+'_QQ_rh_total.png' ,bbox_inches='tight')














