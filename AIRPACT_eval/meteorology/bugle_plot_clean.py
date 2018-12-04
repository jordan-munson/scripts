# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 14:42:41 2018

@author: Jordan Munson
"""

# Load libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set directories
inputdir = r'G:/Research/AIRPACT_eval/stats/'
outputdir = r'G:/Research/AIRPACT_eval/plots/bugle'

#Load data
df_stats = pd.read_csv(inputdir+'aqs_version_stats.csv').drop(['Unnamed: 0'],axis=1)

# Seperate types
df_o3 = df_stats.loc[df_stats['index']=='O3_mod']
df_pm = df_stats.loc[df_stats['index']=='PM2.5_mod']

#%%
# Plot

# PM
fig, ax = plt.subplots(figsize=(8, 4))

# Set axis so that the plot resembles a soccer plot
plt.ylim((-100,100))
plt.xlim((0,10))

# Label plot
ax.set(title='PM_2.5 per AIRPACT Version',xlabel='Mean',ylabel='FB [%]')

# Add color to the plot, colors signifying which site type
colors = ['r','g','b']

ax.scatter(df_pm['Mean'],df_pm['FB'],c=colors, marker = 'D', label = 'PM_2.5')

# Define props
props = dict(boxstyle='square', facecolor='white', alpha=0.0)
props1 = dict(boxstyle='square', facecolor='white', alpha=0.3)

# Draw legends
ax.text(1.03,0.5,'AP3',transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, color='red')
ax.text(1.03,0.43,'AP4',transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, color='green')
ax.text(1.03,0.36,'AP5',transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, color='blue')

#ax.legend()
legend = plt.legend(loc=(1.02,0.6))
plt.setp(legend.get_texts(), color='black')

#Draw grid
plt.grid(b=None, which='major', axis='y')

# Draw characteristic bugle curves
def graph(func, x_range,color):
   x = np.arange(*x_range)
   y = func(x)
   plt.plot(x, y,color = color,alpha =0.7)

# Criteria lines
graph(lambda x: 70*(np.power(0.3, x))+60, (0,11),'red') # Top
graph(lambda x: -70*(np.power(0.3, x))-60, (0,11),'red') # Bottom

# Goal lines
graph(lambda x: 70*(np.power(0.3, x))+30, (0,11),'green') # Top
graph(lambda x: -70*(np.power(0.3, x))-30, (0,11),'green') # Bottom

fig.savefig(outputdir + '/airpact_bugle_version_pm.png' ,bbox_inches='tight')

#%%
# 03
fig, ax = plt.subplots(figsize=(8, 4))

# Set axis so that the plot resembles a soccer plot
plt.ylim((-100,100))
plt.xlim((0,40))

# Label plot
ax.set(title='O3 per AIRPACT Version',xlabel='Mean',ylabel='FB (%)')

# Add color to the plot, colors signifying which site type
colors = ['r','g','b']

ax.scatter(df_o3['Mean'],df_o3['FB'],c=colors, marker = 'o',label='Ozone')
#ax.scatter(df_pm['Mean'],df_pm['NMB [%]'],c=colors, marker = 'D', label = 'PM_2.5')

# Define props
props = dict(boxstyle='square', facecolor='white', alpha=0.0)
props1 = dict(boxstyle='square', facecolor='white', alpha=0.3)

# Draw legends
ax.text(1.03,0.5,'AP3',transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, color='red')
ax.text(1.03,0.43,'AP4',transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, color='green')
ax.text(1.03,0.36,'AP5',transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, color='blue')

#ax.legend()
legend = plt.legend(loc=(1.02,0.6))
plt.setp(legend.get_texts(), color='black')

#Draw grid
plt.grid(b=None, which='major', axis='y')

# Draw characteristic bugle curves
def graph(func, x_range,color):
   x = np.arange(*x_range)
   y = func(x)
   plt.plot(x, y,color = color,alpha =0.7)

line_lim = 50
# Criteria lines
criteria = 30
graph(lambda x: 70*(np.power(0.3, x))+criteria, (0,line_lim),'red') # Top
graph(lambda x: -70*(np.power(0.3, x))-criteria, (0,line_lim),'red') # Bottom

# Goal lines
goal = 15
graph(lambda x: 70*(np.power(0.3, x))+goal, (0,line_lim),'green') # Top
graph(lambda x: -70*(np.power(0.3, x))-goal, (0,line_lim),'green') # Bottom

fig.savefig(outputdir + '/airpact_bugle_version_o3.png' ,bbox_inches='tight')
df_stats.to_csv(outputdir+'/aqs_bugle_stats.csv')

