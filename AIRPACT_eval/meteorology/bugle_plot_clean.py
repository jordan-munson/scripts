# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 14:42:41 2018

@author: Jordan Munson
"""

# Load libraries
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set directories
inputdir = r'E:/Research/AIRPACT_eval/stats/'
outputdir = r'E:/Research/AIRPACT_eval/plots/bugle'

#Load data
#df_stats = pd.read_csv(inputdir+'aqs_version_stats_20190206.csv')#.drop(['Unnamed: 0'],axis=1)
df_stats = pd.read_csv(inputdir+'aqs_version_stats.csv')#.drop(['Unnamed: 0'],axis=1)

# Seperate types
df_o3 = df_stats.loc[df_stats['index']=='O3_mod_hourly']
df_o3_dm8a = df_stats.loc[df_stats['index']=='O3_mod']
df_o3_tot = df_o3.append(df_o3_dm8a)
df_pm = df_stats.loc[df_stats['index']=='PM2.5_mod_hourly']
df_pm_daily = df_stats.loc[df_stats['index']=='PM2.5_mod']
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

figsize = (6,4)
legend_loc = 'upper right'
#%%
# Plot

# PM
fig, ax = plt.subplots(figsize=figsize,dpi = 150)

# Set axis so that the plot resembles a soccer plot
plt.ylim((-100,100))
plt.xlim((0,10))

# Label plot
ax.set(title='PM$_{2.5}$',xlabel='Mean',ylabel='FB (%)')

# Add color to the plot, colors signifying which site type
colors = ['r','g','b']

ax.scatter(df_pm['Mean'],df_pm['FB'],c=colors, marker = 'o', label = 'Hourly')
ax.scatter(df_pm_daily['Mean'],df_pm_daily['FB'],c=colors, marker = 'D',label='Daily')


# Define props
props = dict(boxstyle='square', facecolor='white', alpha=0.0)
props1 = dict(boxstyle='square', facecolor='white', alpha=0.3)

# Draw legends
adj = 0.125
ax.text(1.03,0.5+adj,'AP3',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='red')
ax.text(1.03,0.41+adj,'AP4',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='green')
ax.text(1.03,0.32+adj,'AP5',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='blue')

#ax.legend()
#legend = plt.legend(loc=legend_loc)
#plt.setp(legend.get_texts(), color='black')

#Draw grid
plt.grid(b=None, which='major', axis='y')

# Draw characteristic bugle curves
def graph(func, x_range,color,ls,label):
   x = np.arange(*x_range)
   y = func(x)
   plt.plot(x, y,color = color,alpha =0.7,ls=ls,label=label)
   

# Criteria lines
graph(lambda x: 70*(np.power(0.3, x))+60, (0,11),'black','-.','Criteria') # Top
graph(lambda x: -70*(np.power(0.3, x))-60, (0,11),'black','-.','') # Bottom

# Goal lines
graph(lambda x: 70*(np.power(0.3, x))+30, (0,11),'black','--','Goal') # Top
graph(lambda x: -70*(np.power(0.3, x))-30, (0,11),'black','--','') # Bottom
ax.text(-0.13, 1.08,'A',fontsize = 20, ha='right', va='center', transform=ax.transAxes)

plt.legend(prop={'size': 14},loc = 'upper left')
fig.savefig(outputdir + '/airpact_bugle_version_pm.png' ,bbox_inches='tight')

#%%
# 03
fig, ax = plt.subplots(figsize=figsize, dpi=150)

# Set axis so that the plot resembles a soccer plot
plt.ylim((-100,100))
plt.xlim((0,60))

# Label plot
ax.set(title='Ozone',xlabel='Mean',ylabel='FB (%)')

# Add color to the plot, colors signifying which site type
colors = ['r','g','b']

ax.scatter(df_o3['Mean'],df_o3['FB'],c=colors, marker = 'o',label='Hourly')
ax.scatter(df_o3_dm8a['Mean'],df_o3_dm8a['FB'],c=colors, marker = 'D',label='DM8HA')
ax.legend()
#ax.scatter(df_o3_tot['Mean'],df_o3_tot['FB'],c=colors, marker = 'o',label='')

#ax.scatter(df_pm['Mean'],df_pm['NMB [%]'],c=colors, marker = 'D', label = 'PM_2.5')

# Define props
props = dict(boxstyle='square', facecolor='white', alpha=0.0)
props1 = dict(boxstyle='square', facecolor='white', alpha=0.3)

# Draw legends
ax.text(1.03,0.5+adj,'AP3',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='red')
ax.text(1.03,0.41+adj,'AP4',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='green')
ax.text(1.03,0.32+adj,'AP5',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='blue')

#ax.legend()
#legend = plt.legend(loc=legend_loc)
#plt.setp(legend.get_texts(), color='black')

#Draw grid
plt.grid(b=None, which='major', axis='y')

line_lim = 70
# Criteria lines
criteria = 30
graph(lambda x: 70*(np.power(0.3, x))+criteria, (0,line_lim),'black','-.','Criteria') # Top
graph(lambda x: -70*(np.power(0.3, x))-criteria, (0,line_lim),'black','-.','') # Bottom

# Goal lines
goal = 15
graph(lambda x: 70*(np.power(0.3, x))+goal, (0,line_lim),'black','--','Goal') # Top
graph(lambda x: -70*(np.power(0.3, x))-goal, (0,line_lim),'black','--','') # Bottom

ax.text(-0.13, 1.08,'A',fontsize = 20, ha='right', va='center', transform=ax.transAxes)

legend  = plt.legend(prop={'size': 14},loc = 'upper left')
fig.savefig(outputdir + '/airpact_bugle_version_o3.png' ,bbox_inches='tight')
df_stats.to_csv(outputdir+'/aqs_bugle_stats.csv')

