# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 07:38:43 2018

@author: Jordan Munson
"""
# Load libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl

import numpy as np

# Set directories
inputdir = r'E:/Research/AIRPACT_eval/meteorology/'
outputdir = r'E:/Research/AIRPACT_eval/meteorology/AQS_plots/soccer_plots'

#Load data
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

#list site types
sites = ['URBAN AND CENTER CITY','SUBURBAN','RURAL']

# Set plot parameters
mpl.rcParams['font.family'] = 'arial'  # the font used for all labelling/text
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

legend_loc = 'upper right'
#%%
# Plot MB and ME
fig, ax = plt.subplots(figsize=(8, 4))


# Set axis so that the plot resembles a soccer plot
ymax = max(df_stats['ME']) +2
xmax = max(df_stats['MB'])
xmin = abs(min(df_stats['MB'])) 

if xmax > xmin:
    xmin=xmax*(-1)
else:
    xmax =xmin
    xmin=xmin*(-1)
    
xmax = xmax +5
xmin = xmin -5
# Hard code these for this plot
plt.ylim((0,12))
plt.xlim((-12,12))

# Draw the characteristic soccer plot rectangles
rect1 = patches.Rectangle((-.5,0),1,.5,facecolor='none',linewidth=1,edgecolor='black',linestyle='dashed') # Wind speed m/s
rect2 = patches.Rectangle((-10,0),20,10,facecolor='none',linewidth=1,edgecolor='black',linestyle='dashed') # Wind direction degrees
rect3 = rect1 = patches.Rectangle((-.5,0),1,.5,facecolor='none',linewidth=1,edgecolor='black',linestyle='dashed') # Temperature celsius
#rect4 = rect1 = patches.Rectangle((-1,0),2,1,facecolor='none',linewidth=1,edgecolor='black',linestyle='dashed') # Humidity g/kg

ax.add_patch(rect1)
ax.add_patch(rect2)
ax.add_patch(rect3)
#ax.add_patch(rect4)

# Label plot
ax.set(title='AIRPACT 2009 - 2018',xlabel='MB',ylabel=' ME')

# Add color to the plot, colors signifying which site type
#colors = np.where(df_stats["station ID"]=='URBAN AND CENTER CITY','r','-')
#colors[df_stats["station ID"]=='SUBURBAN'] = 'g'
#colors[df_stats["station ID"]=='RURAL'] = 'b'
colors = ['r','g','b']

ax.scatter(df_temp['MB'],df_temp['ME'],c=colors, marker = 'o',label='Temp')
#ax.scatter(df_pres['MB'],df_pres['ME'],c=colors, marker = '*',label = 'Pressure')
#ax.scatter(df_rh['MB'],df_rh['ME'],c=colors, marker = '^', label = 'RH')
ax.scatter(df_ws['MB'],df_ws['ME'],c=colors, marker = 'D', label = 'WS')
ax.scatter(df_wd['MB'],df_wd['ME'],c=colors, marker = '+', label = 'WD')

# Place textbox of color legend
textstr = '\n'.join((
        r'Urban - red',
        r'Suburban - green',
        r'Rural - blue'))
props = dict(boxstyle='square', facecolor='white', alpha=0.0)
props1 = dict(boxstyle='square', facecolor='white', alpha=0.3)

# Draw legends
ax.text(1.03,0.5,'Urban',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='red')
ax.text(1.03,0.41,'Suburban',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='green')
ax.text(1.03,0.32,'Rural',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='blue')


#ax.legend()
legend = plt.legend(loc=legend_loc)
plt.setp(legend.get_texts(), color='black')

#Draw rectangle to encompass the sitetypes
#rect = patches.Rectangle((23.9,6),6,5,facecolor='none',linewidth=1,edgecolor='black',linestyle='solid',clip_on=False,alpha=0.3)
#ax.add_patch(rect)

# Save the plot
fig.savefig(outputdir + '/airpact_2009-2018_mbme.png' ,bbox_inches='tight')

#%%
# Plot NMB and NME
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

ax.scatter(df_temp['NMB [%]'],df_temp['NME [%]'],c=colors, marker = 'o',label='Temp')
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
ax.text(1.03,0.5,'Urban',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='red')
ax.text(1.03,0.41,'Suburban',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='green')
ax.text(1.03,0.32,'Rural',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='blue')


#ax.legend()
legend = plt.legend(loc=legend_loc)
plt.setp(legend.get_texts(), color='black')

#Draw rectangle to encompass the sitetypes
rect = patches.Rectangle((23.9,6),6,5,facecolor='none',linewidth=1,edgecolor='black',linestyle='solid',clip_on=False,alpha=0.3)
ax.add_patch(rect)

# Save the plot
fig.savefig(outputdir + '/airpact_2009-2018_nmbnme.png' ,bbox_inches='tight')
#%%
#average stats from site types to get single value
ap3 = pd.DataFrame(ap3_stats.mean(axis=0)).rename(index=str,columns={0:'ap3'}).T
ap4 = pd.DataFrame(ap4_stats.mean(axis=0)).rename(index=str,columns={0:'ap4'}).T
ap5 = pd.DataFrame(ap5_stats.mean(axis=0)).rename(index=str,columns={0:'ap5'}).T

ap3_temp = ap3_stats.loc[ap3_stats['index']=='TEMP2_1']

#df_all = pd.concat([ap3,ap4,ap5])
# Seperate the measuremnet types
df_temp = ap_total.loc[ap_total['index']=='TEMP2_1']
df_pres = ap_total.loc[ap_total['index']=='PRSFC_1'] # While the pressure data is here, it has large error
df_rh = ap_total.loc[ap_total['index']=='RH_1']
df_ws = ap_total.loc[ap_total['index']=='WS_1']
df_wd = ap_total.loc[ap_total['index']=='WD_1']

temp = ap3_stats.mean(axis=0,numeric_only=True)
# Plot NMB and NME
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
ax.set(title='AIRPACT Versions',xlabel='NMB (%)',ylabel='NME (%)')

# Add color to the plot, colors signifying which site type
#colors = np.where(df_stats["station ID"]=='URBAN AND CENTER CITY','r','-')
#colors[df_stats["station ID"]=='SUBURBAN'] = 'g'
#colors[df_stats["station ID"]=='RURAL'] = 'b'
colors = ['r','g','b']

ax.scatter(df_temp['NMB [%]'],df_temp['NME [%]'],c=colors, marker = 'o',label='Temp')
ax.scatter(df_pres['NMB [%]'],df_pres['NME [%]'],c=colors, marker = '*',label = 'Pressure')
ax.scatter(df_rh['NMB [%]'],df_rh['NME [%]'],c=colors, marker = '^', label = 'RH')
ax.scatter(df_ws['NMB [%]'],df_ws['NME [%]'],c=colors, marker = 'D', label = 'WS')
ax.scatter(df_wd['NMB [%]'],df_wd['NME [%]'],c=colors, marker = '+', label = 'WD')

# Place textbox of color legend
textstr = '\n'.join((
        r'AP3 - red',
        r'AP4 - green',
        r'AP5 - blue'))
props = dict(boxstyle='square', facecolor='white', alpha=0.0)
props1 = dict(boxstyle='square', facecolor='white', alpha=0.3)

# Draw legends
ax.text(1.03,0.5,'AP3',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='red')
ax.text(1.03,0.41,'AP4',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='green')
ax.text(1.03,0.32,'AP5',transform=ax.transAxes,
        verticalalignment='top', bbox=props, color='blue')


#ax.legend()
legend = plt.legend(loc=legend_loc)
plt.setp(legend.get_texts(), color='black')

#Draw rectangle to encompass the sitetypes
rect = patches.Rectangle((23.9,6),6,5,facecolor='none',linewidth=1,edgecolor='black',linestyle='solid',clip_on=False,alpha=0.3)
ax.add_patch(rect)

# Save the plot
fig.savefig(outputdir + '/airpact_versions_nmbnme.png' ,bbox_inches='tight')

#%%
# Seperate the measuremnet types
df_temp = ap_total.loc[ap_total['index']=='TEMP2_1']
df_pres = ap_total.loc[ap_total['index']=='PRSFC_1'] # While the pressure data is here, it has large error
df_rh = ap_total.loc[ap_total['index']=='RH_1']
df_ws = ap_total.loc[ap_total['index']=='WS_1']
df_wd = ap_total.loc[ap_total['index']=='WD_1']

# Create a soccer plot function to make them easier
def soccer(x,y,axismax,size1,size2,temp,press,rh,ws,wd):    # x and y are stats looked at, then set plot axis, then squares, then determine which species
    fig, ax = plt.subplots(figsize=(5, 3),dpi=200)
    
    # set axis limits
    plt.ylim((0,axismax))
    plt.xlim((-1*axismax,axismax))
    
    # Set width of rectangles
    width1 = 2*size1
    width2 = 2*size2
    
    # Draw the characteristic soccer plot rectangles
    rect1 = patches.Rectangle((-1*size1,0),width1,size1,facecolor='none',linewidth=1,edgecolor='black',linestyle='dashed')
    rect2 = patches.Rectangle((-1*size2,0),width2,size2,facecolor='none',linewidth=1,edgecolor='black',linestyle='dashed')
    
    ax.add_patch(rect1)
    ax.add_patch(rect2)
    

    
    # Add color to the plot, colors signifying which site type
    #colors = np.where(df_stats["station ID"]=='URBAN AND CENTER CITY','r','-')
    #colors[df_stats["station ID"]=='SUBURBAN'] = 'g'
    #colors[df_stats["station ID"]=='RURAL'] = 'b'
    colors = ['r','g','b']

    if temp == 'yes':
        ax.scatter(df_temp[x],df_temp[y],edgecolors=colors, marker = 'o',label='Temp',facecolors='none')
        name='Temp'
    if press == 'yes':
        ax.scatter(df_pres[x],df_pres[y],edgecolors=colors, marker = '*',label = 'Pressure',facecolors='none')
        name='Pressure'
    if rh == 'yes':
        ax.scatter(df_rh[x],df_rh[y],edgecolors=colors, marker = '^', label = 'RH',facecolors='none')
        name = 'Relative_Humidity'
    if ws == 'yes':
        ax.scatter(df_ws[x],df_ws[y],edgecolors=colors, marker = 'D', label = 'WS',facecolors='none')
        name='Wind_Speed'
    if wd == 'yes':
        ax.scatter(df_wd[x],df_wd[y],edgecolors=colors, marker = '+', label = 'WD',facecolors='none')
        name='Wind_Direction'
    if temp and ws and rh == 'yes':
        name = 'combined'
    # Label plot
    ax.set(xlabel=x,ylabel=y)#,title='Hourly Meteorology')
    
    # Place textbox of color legend
    props = dict(boxstyle='square', facecolor='white', alpha=0.0)
    
    # Draw legends
    vers_anno_x = 1.07 # orig 0.89
    ax.text(vers_anno_x,0.57,'AP-3',transform=ax.transAxes,
            verticalalignment='top', bbox=props, color='red')
    ax.text(vers_anno_x,0.51,'AP-4',transform=ax.transAxes,
            verticalalignment='top', bbox=props, color='green')
    ax.text(vers_anno_x,0.45,'AP-5',transform=ax.transAxes,
            verticalalignment='top', bbox=props, color='blue')
    
    #Draw rectangle to encompass versions
    rect = patches.Rectangle((1.55,.57),.535,.3,facecolor='none',linewidth=1,edgecolor='black',linestyle='solid',clip_on=False,alpha=0.2) # orig size posit values (1.05,.57),.4,.3,
    ax.add_patch(rect)

    #ax.legend()
    legend = plt.legend(loc='lower right',fontsize=8,bbox_to_anchor=(1.21, 0.6))
    plt.setp(legend.get_texts(), color='black')
    
    
    #Draw rectangle and write noe about AP-5
    rect = patches.Rectangle((1.55,.2),.535,.3,facecolor='none',linewidth=1,edgecolor='black',linestyle='solid',clip_on=False,alpha=0.2) # orig size posit values (1.05,.57),.4,.3,
    ax.add_patch(rect)
    
    ax.text(1.02,0.32,'Note: AP-5 \n RH MB \n is 2.4%',transform=ax.transAxes,
    verticalalignment='top', bbox=props, color='black')
    
    # Save the plot
    fig.savefig(outputdir+'/' +name+ '_'+x+'_airpact_versions_for_paper.png' ,bbox_inches='tight')
    
#soccer('NMB [%]','NME [%]',10,15)
#soccer('MB','ME',1.5,0.5,0.5,'yes','no','no','no','no') # Temp
#soccer('MB','ME',1.5,0.5,1,'no','yes','no','no','no') # press
#soccer('MB','ME',1.5,1,1,'no','no','yes','no','no') # rh
#soccer('MB','ME',1.5,0.5,.5,'no','no','no','yes','no') # ws
#soccer('MB','ME',12,10,10,'no','no','no','no','yes') # wd

soccer('MB','ME',1.5,1,0.5,'yes','no','yes','yes','no') # temp,ws,rh
#soccer('NMB [%]','NME [%]',15,1,0.5,'yes','no','yes','yes','no') # temp,ws,rh
    
    
    
    
    
    
    
    
    