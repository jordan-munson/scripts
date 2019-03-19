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
inputDir = r'G:/Research/AIRPACT_eval/'
stat_path = r'G:/Research/scripts/Urbanova/statistical_functions.py'

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

states = ['WA','OR','ID','MT']
# =============================================================================
# Plot fire data
# =============================================================================
df_fire = pd.read_csv(inputDir+'fire_data.csv')

years = [2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
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

#%%


import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)


plt.subplot(211)
plt.imshow(np.random.random((100, 100)), cmap=plt.cm.BuPu_r)
plt.subplot(212)
plt.imshow(np.random.random((100, 100)), cmap=plt.cm.BuPu_r)

plt.subplots_adjust(bottom=0.1, right=.5, top=0.9)
cax = plt.axes([0.85, 0.1, 0.075, 0.8])
plt.colorbar(cax=cax)
plt.show()
































