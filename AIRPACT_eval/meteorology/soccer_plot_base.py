# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 07:38:43 2018

@author: riptu
"""
# Load libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set directories
inputdir = r'E:/Research/AIRPACT_eval/meteorology/'
outputdir = r'E:/Research/AIRPACT_eval/meteorology/AQS_plots/soccer_plots'

#Load data
#df_airpact = pd.read_csv(inputdir+'df_airpact.csv').drop(['Unnamed: 0','lat','lon'],axis=1)
#df_obs = pd.read_csv(inputdir+'df_obs.csv').drop(['Unnamed: 0','Local Site Name'],axis=1).rename(columns={'datetime':'DateTime'})
df_stats = pd.read_csv(inputdir + 'aqs_stats.csv').drop(['Unnamed: 0','model'],axis=1)

#df_all = pd.merge(df_airpact,df_obs,how ='outer',left_index=True,right_index=True, on = ['DateTime','AQS_ID'])
print('Dataframes read')

# Seperate the measuremnet types
df_temp = df_stats.loc[df_stats['index']=='TEMP2_1']
df_pres = df_stats.loc[df_stats['index']=='PRSFC_1']
df_rh = df_stats.loc[df_stats['index']=='RH_1']
df_ws = df_stats.loc[df_stats['index']=='WS_1']
df_wd = df_stats.loc[df_stats['index']=='WD_1']

#list site types
sites = ['URBAN AND CENTER CITY','SUBURBAN','RURAL']
#%%
# Plot
fig, ax = plt.subplots(figsize=(8, 4))


# Set axis so that the plot resembles a soccer plot
ymax = max(df_stats['NME [%]']) +2
xmax = max(df_stats['NMB [%]'])
xmin = abs(min(df_stats['NMB [%]'])) 

if xmax > xmin:
    xmin=xmax*(-1)
else:
    xmax =xmin
    xmin=xmin*(-1)
    
xmax = xmax +5
xmin = xmin -5
plt.ylim((0,ymax))
plt.xlim((xmin,xmax))

# Draw the characteristic soccer plot rectangles
rect1 = patches.Rectangle((-10,0),20,10,facecolor='none',linewidth=1,edgecolor='black',linestyle='dashed')
rect2 = patches.Rectangle((-15,0),30,15,facecolor='none',linewidth=1,edgecolor='black',linestyle='dashed')

ax.add_patch(rect1)
ax.add_patch(rect2)

# Label plot
ax.set(title='AIRPACT 2009 - 2018',xlabel='NMB (%)',ylabel='NME (%)')

# Add color to the plot, colors signifying which site type
#colors = np.where(df_stats["station ID"]=='URBAN AND CENTER CITY','r','-')
#colors[df_stats["station ID"]=='SUBURBAN'] = 'g'
#colors[df_stats["station ID"]=='RURAL'] = 'b'
colors = ['r','g','b']

ax.scatter(df_temp['NMB [%]'],df_temp['NME [%]'],c=colors, marker = 'o',label='Temperature')
ax.scatter(df_pres['NMB [%]'],df_pres['NME [%]'],c=colors, marker = '*',label = 'Pressure')
ax.scatter(df_rh['NMB [%]'],df_rh['NME [%]'],c=colors, marker = '^', label = 'RH')
ax.scatter(df_ws['NMB [%]'],df_ws['NME [%]'],c=colors, marker = 'D', label = 'WS')
ax.scatter(df_wd['NMB [%]'],df_wd['NME [%]'],c=colors, marker = '+', label = 'WD')

# Place textbox of color legend
textstr = '\n'.join((
        r'Urban - red',
        r'Suburban - green',
        r'Rural - blue'))
props = dict(boxstyle='square', facecolor='white', alpha=0.0)
props1 = dict(boxstyle='square', facecolor='white', alpha=0.3)

# Draw legends
ax.text(1.03,0.5,'Urban',transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, color='red')
ax.text(1.03,0.43,'Suburban',transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, color='green')
ax.text(1.03,0.36,'Rural',transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props, color='blue')


#ax.legend()
legend = plt.legend(loc=(1.02,0.6))
plt.setp(legend.get_texts(), color='black')

#Draw rectangle to encompass the sitetypes
rect = patches.Rectangle((23.9,6),6,5,facecolor='none',linewidth=1,edgecolor='black',linestyle='solid',clip_on=False,alpha=0.3)
ax.add_patch(rect)

# Save the plot
fig.savefig(outputdir + '/airpact_2009-2018.png' ,bbox_inches='tight')

