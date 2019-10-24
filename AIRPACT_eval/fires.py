# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 16:25:18 2019

@author: Jordan
"""

import matplotlib as mpl
#mpl.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt

#Set directory
inputDir = r'E:/Research/AIRPACT_eval/'
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'

# =============================================================================
# Setup
# =============================================================================
# Set plot parameters
mpl.rcParams['font.family'] = 'sans-serif'  # the font used for all labelling/text
# =============================================================================
# mpl.rcParams['font.size'] = 24.0
# mpl.rcParams['xtick.major.size']  = 10
# mpl.rcParams['xtick.major.width'] = 2
# mpl.rcParams['xtick.minor.size']  = 5
# mpl.rcParams['xtick.minor.width'] = 1
# mpl.rcParams['ytick.major.size']  = 10
# mpl.rcParams['ytick.major.width'] = 2
# mpl.rcParams['ytick.minor.size']  = 5
# mpl.rcParams['ytick.minor.width'] = 1
# mpl.rcParams['ytick.direction']   = 'in'
# mpl.rcParams['xtick.direction']   = 'in'
# =============================================================================

states = ['WA','OR','ID','MT']#,'CA']
#states = ['NATION']

# =============================================================================
# Plot fire data
# =============================================================================
df_fire = pd.read_csv(inputDir+'fire_data.csv')

years = [2010,2011,2012,2013,2014,2015,2016,2017,2018]
df_com = pd.DataFrame(index = years, columns=['Fires', 'Acres', 'State']).fillna(0)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for state in states:
    # Format
    d = df_fire.loc[df_fire['State']==state]
    d = d.set_index('Year') 
    d.loc[:,'Fires'] = pd.to_numeric(d.loc[:,'Fires'], errors='coerce')/1000
    d.loc[:,'Acres'] = pd.to_numeric(d.loc[:,'Acres'], errors='coerce')/1000
    df_com['Fires'] = df_com['Fires']+d['Fires']
    df_com['Acres'] = df_com['Acres']+d['Acres']
    # plot
df_com.ix[:,['Fires','Acres']].plot(kind='line', style='-', ax=ax, color=['black', 'blue']) # if key error, check spaces in column i.e. d(list)

# plot settings
ax.set_ylabel('Acres Burned / 1000')

plt.show()
plt.close()
df_com.to_csv(inputDir+'fires.csv')
#%%
# =============================================================================
# This method is much prettier than above. Plots a time series of total acreas burned and also divides into WA, OR, ID
# =============================================================================
years = [2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
fires = pd.DataFrame(index = years, columns=['Fires']).fillna(0)
for state in states:
    # Format
    d = df_fire.loc[df_fire['State']==state]
    d = d.set_index('Year') 
    d.loc[:,'Fires'] = pd.to_numeric(d.loc[:,'Fires'], errors='coerce')/1000
    d.loc[:,'Acres'] = pd.to_numeric(d.loc[:,'Acres'], errors='coerce')/1000
    d = d.rename(columns={'Acres':state + ' Fire'}).drop(['Fires','State'],axis=1).drop([2006,2007,2008])
    
    fires = pd.merge(fires,d,left_index=True,right_index=True)


#fires = pd.read_csv(r'E:/Research/AIRPACT_eval/fires.csv').set_index('Unnamed: 0').drop('State',axis=1)
#fires = fires.reset_index().rename(columns={'Unnamed: 0':'index'})
#fires1 = fires.set_index('index')
fires.index = fires.index.map(str)  # set as string so that the merge later on works

fires['Fires'] = fires['WA Fire'] + fires['OR Fire'] + fires['ID Fire']
fire_max = 3300
legend_x = 1.1

fig = plt.figure(figsize=(6,4),dpi=300)
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Year')
fires.plot(y=['WA Fire','OR Fire','ID Fire'],ax=ax,label=['WA','OR','ID'])
fires.plot(y=['Fires'],ax=ax,linestyle=':',color = 'black',label=['Total'])
ax.fill_between(fires.index,0,fires.Fires,alpha = 0.05, color='black')
ax.set_ylabel('Acres Burned/1000')
ax.set_ylim(0,fire_max)
ax.set_xticklabels(years)
ax.legend(loc='center left', bbox_to_anchor=(legend_x, 0.1)).remove() # Places legend outside of plot to the right

ax.legend(loc='center left', bbox_to_anchor=(legend_x, 0.9)) # Places legend outside of plot to the right
fig.tight_layout()
plt.savefig(inputDir + 'plots/fire/decadal_acres_burned.png')

