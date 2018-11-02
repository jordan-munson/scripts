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
inputdir = r'E:/Research/AIRPACT_eval/stats/'
outputdir = r'E:/Research/AIRPACT_eval/plots/bugle'

#Load data
#o3_rural = pd.read_csv(inputdir+'O3_rural.csv').drop(['Unnamed: 0'],axis=1)
#o3_suburban = pd.read_csv(inputdir+'O3_suburban.csv').drop(['Unnamed: 0'],axis=1)
#o3_urban = pd.read_csv(inputdir+'O3_urban.csv').drop(['Unnamed: 0'],axis=1)
#pm_rural = pd.read_csv(inputdir+'PM_rural.csv').drop(['Unnamed: 0'],axis=1)
#pm_suburban = pd.read_csv(inputdir+'PM_suburban.csv').drop(['Unnamed: 0'],axis=1)
#pm_urban = pd.read_csv(inputdir+'PM_urban.csv').drop(['Unnamed: 0'],axis=1)

df_stats = pd.read_csv(inputdir+'aqs_version_stats.csv').drop(['Unnamed: 0'],axis=1)

# Bugle plot for met is not advised, but the code is here incase it ever is
'''
#df_airpact = pd.read_csv(inputdir+'df_airpact.csv').drop(['Unnamed: 0','lat','lon'],axis=1)
#df_obs = pd.read_csv(inputdir+'df_obs.csv').drop(['Unnamed: 0','Local Site Name'],axis=1).rename(columns={'datetime':'DateTime'})
df_stats = pd.read_csv(inputdir + '/AQS_stats/aqs_stats.csv').drop(['Unnamed: 0','model'],axis=1)
ap3_stats = pd.read_csv(inputdir + '/AQS_stats/aqs_stats_ap3.csv').drop(['Unnamed: 0','model'],axis=1)
ap4_stats = pd.read_csv(inputdir + '/AQS_stats/aqs_stats_ap4.csv').drop(['Unnamed: 0','model'],axis=1)
ap5_stats = pd.read_csv(inputdir + '/AQS_stats/aqs_stats_ap5.csv').drop(['Unnamed: 0','model'],axis=1)
ap_total = pd.read_csv(inputdir + '/AQS_stats/aqs_stats_total.csv').drop(['Unnamed: 0','model'],axis=1)
#df_all = pd.merge(df_airpact,df_obs,how ='outer',left_index=True,right_index=True, on = ['DateTime','AQS_ID'])
print('Dataframes read')

# Seperate the measuremnet types
df_temp = df_stats.loc[df_stats['index']=='TEMP2_1']
df_pres = df_stats.loc[df_stats['index']=='PRSFC_1'] # While the pressure data is here, it has large error
df_rh = df_stats.loc[df_stats['index']=='RH_1']
df_ws = df_stats.loc[df_stats['index']=='WS_1']
df_wd = df_stats.loc[df_stats['index']=='WD_1']
'''
# Seperate types
df_o3 = df_stats.loc[df_stats['index']=='O3_mod']
df_pm = df_stats.loc[df_stats['index']=='PM2.5_mod']

#list site types
sites = ['URBAN AND CENTER CITY','SUBURBAN','RURAL']
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
#colors = np.where(df_stats["station ID"]=='URBAN AND CENTER CITY','r','-')
#colors[df_stats["station ID"]=='SUBURBAN'] = 'g'
#colors[df_stats["station ID"]=='RURAL'] = 'b'
colors = ['r','g','b']

#ax.scatter(df_o3['Mean'],df_o3['NMB [%]'],c=colors, marker = 'o',label='Ozone')
#ax.scatter(df_pres['Mean'],df_pres['NMB [%]'],c=colors, marker = '*',label = 'Pressure')
#ax.scatter(df_rh['Mean'],df_rh['NMB [%]'],c=colors, marker = '^', label = 'RH')
ax.scatter(df_pm['Mean'],df_pm['FB'],c=colors, marker = 'D', label = 'PM_2.5')
#ax.scatter(df_wd['Mean'],df_wd['NMB [%]'],c=colors, marker = '+', label = 'WD')

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

#Draw rectangle to encompass the sitetypes
rect = patches.Rectangle((23.9,6),6,5,facecolor='none',linewidth=1,edgecolor='black',linestyle='solid',clip_on=False,alpha=0.3)
#ax.add_patch(rect)

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
#colors = np.where(df_stats["station ID"]=='URBAN AND CENTER CITY','r','-')
#colors[df_stats["station ID"]=='SUBURBAN'] = 'g'
#colors[df_stats["station ID"]=='RURAL'] = 'b'
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

#Draw rectangle to encompass the sitetypes
rect = patches.Rectangle((23.9,6),6,5,facecolor='none',linewidth=1,edgecolor='black',linestyle='solid',clip_on=False,alpha=0.3)
#ax.add_patch(rect)

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






























