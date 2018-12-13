# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 12:05:27 2018

@author: Jordan
"""
import matplotlib.pyplot as plt
import matplotlib as mpl

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


fig = plt.figure(figsize=(10,18))
fig.text(-0.02, 0.5, 'Ozone (ppb)', va='center', rotation='vertical')
fig.suptitle('Seasonal Variations by AIRPACT Version',y=1.02) # title
fig.tight_layout() # spaces the plots out a bit

#Annotate versions in
fig.text(0.5, .99, 'AIRPACT 3', va='center',ha='center')
fig.text(0.5, 0.66, 'AIRPACT 4', va='center',ha='center')
fig.text(0.5, 0.33, 'AIRPACT 5', va='center',ha='center')
for i in [1,2,3,4,5,6,7,8,9,10,11,12]:
    ax = fig.add_subplot(6,2,i)
    plt.rcParams["figure.figsize"] = (8,4)
    plt.tight_layout() # spaces the plots out a bit
    
    ax.set_xlabel('')        # Gets rid of the 'DateTime' x label and replaces with a space
    ax.set_title(str('Winter'),fontsize=12) # sets the titles of individ plots as the season, and makes the font smaller
    plt.legend(prop={'size': 10})#,loc=3) # Places the legend in the lower left corner at a size of 10
    sze = 10 #size of annotation text
    
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    #ax.xaxis.labelpad = 100
    
    
    plt.grid(True)    # Add grid lines to make graph interpretation easier
    