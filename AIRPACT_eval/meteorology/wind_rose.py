# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 09:23:58 2018

@author: Jordan Munson
"""

import pandas as pd

from windrose import plot_windrose
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import matplotlib.ticker as tkr

# Set directories
inputdir = r'E:/Research/AIRPACT_eval/meteorology/'
outputdir = r'E:/Research/AIRPACT_eval/meteorology/AQS_plots/windrose/'

#Load data
df_airpact = pd.read_csv(inputdir+'df_airpact.csv').drop(['Unnamed: 0','lat','lon'],axis=1)
df_obs = pd.read_csv(inputdir+'df_obs.csv').drop(['Unnamed: 0','Local Site Name'],axis=1).rename(columns={'datetime':'DateTime'})


#%%
# Plot model wind roses
versions = ['AP3','AP4','AP5']

for version in versions:
    
    # Set date range used based of versions
    if version == 'AP3':
        start_date ='2009-05-01'
        end_date = '2014-07-01'
    elif version == 'AP4':
        start_date ='2014-07-01'
        end_date = '2015-12-01'
    elif version == 'AP5':
        start_date ='2015-12-01'
        end_date = '2018-07-01'
        
    # Locate correct site model data
    #Manipulate dataframe
    df=df_airpact
    mask = (df['DateTime'] > start_date) & (df['DateTime'] <= end_date) # Create a mask to determine the date range used
    df = df.loc[mask]  
    df = df.groupby("DateTime").mean()
    df = df.rename(columns={'WSPD10':'speed','WDIR10':'direction'})
    df = df[['speed','direction']]
    
    print(df.dtypes)
    
    bins = np.arange(0.0, 11, 2)
    plot_windrose(df,kind='bar',bins=bins,normed=True) # If want to change colors, cmap=cm.hot. normed sets the lines as percents
    # Look at the link below for how to use and modify the wind rose.
    # https://windrose.readthedocs.io/en/latest/usage.html#a-stacked-histogram-with-normed-displayed-in-percent-results
    plt.title(version + ' Predicted')
    plt.legend(title="m/s")#, loc=(1.2,0))
    
    plt.savefig(outputdir + version+'_predicted_windrose.png' ,bbox_inches='tight')
    plt.show()
    plt.close()
    
    # Now the observed results
    #Manipulate data frame
    df = df_obs
    mask = (df['DateTime'] > start_date) & (df['DateTime'] <= end_date) # Create a mask to determine the date range used
    df = df.loc[mask]  
    df = df.groupby("DateTime").mean()
    df = df.rename(columns={'aqs_wspd':'speed','aqs_wdir':'direction'})
    df = df[['speed','direction']]
    
    print(df.dtypes)
    
    # Actualy plot the wind rose here
    bins = np.arange(0.0, 11, 2)
    plot_windrose(df,kind='bar',bins=bins,normed=True)
    
    plt.title(version + ' Observed')
    plt.legend(title="m/s")#, loc=(1.2,0))
    plt.savefig(outputdir + version+'_observed_windrose.png' ,bbox_inches='tight')

    plt.show()
    plt.close()
    
#    bins = np.arange(0, 30 + 1, 1)
#    bins = bins[1:]
#    
#    ax, params = plot_windrose(df, kind='pdf', bins=bins)
#    print("Weibull params:")
#    print(params)
#    # plt.savefig("screenshots/pdf.png")
#    plt.show()
#    plt.close()

#%%
'''
# Try to plot them all on one page
df1 = df_airpact
df1 = df1.groupby("DateTime").mean()
df1 = df1.rename(columns={'WSPD10':'speed','WDIR10':'direction'})
df1 = df1[['speed','direction']]
wd1  =df1['direction']
ws1 = df1['speed']

df2 = df_obs
df2 = df2.groupby("DateTime").mean()
df2 = df2.rename(columns={'aqs_wspd':'speed','aqs_wdir':'direction'})
df2 = df2[['speed','direction']]
wd2  =df2['direction']
ws2 = df2['speed']

fig, (ax1,ax2) = plt.subplots(1,2)
ax1 = WindroseAxes.from_ax()
ax1.contourf(wd1, ws1, bins=bins)
ax1.set_legend()
   
ax2 = WindroseAxes.from_ax()
ax2.contourf(wd2, ws2, bins=bins)
ax2.set_legend()
 
#f, axarr = plt.subplots(2,2)
#axarr[0,0]=plot_windrose(df1,kind='bar',bins=bins,normed=True)
#axarr[0,1]=plot_windrose(df2,kind='bar',bins=bins,normed=True)
#axarr[1,0]=plot_windrose(df3,kind='bar',bins=bins,normed=True)
# Suppossed example of plotting these on a single page
#https://github.com/python-windrose/windrose/blob/master/samples/example_subplots.py




#First create some toy data:
x = np.linspace(0, 2*np.pi, 400)
y = np.sin(x**2)

#Creates just a figure and only one subplot
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('Simple plot')

#Creates two subplots and unpacks the output array immediately
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.plot(x, y)
ax1.set_title('Sharing Y axis')
ax2.scatter(x, y)

'''




print('Done')









