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


fig = plt.figure(figsize=(26,10))
fig.text(-0.02, 0.5, 'Ozone (ppb)', va='center', rotation='vertical')
fig.suptitle('Seasonal Variations by AIRPACT Version',y=1.025) # title
fig.tight_layout() # spaces the plots out a bit

#Annotate versions in
fig.text(0.184, .98, 'AIRPACT 3', va='center',ha='center')
fig.text(0.51, 0.98, 'AIRPACT 4', va='center',ha='center')
fig.text(0.835, 0.98, 'AIRPACT 5', va='center',ha='center')
for i in [1,2,3,4,5,6]:
    ax = fig.add_subplot(2,3,i)
    plt.rcParams["figure.figsize"] = (8,4)
    plt.tight_layout() # spaces the plots out a bit
    
    ax.set_xlabel('')        # Gets rid of the 'DateTime' x label and replaces with a space
    ax.set_title(str('Winter'),fontsize=12) # sets the titles of individ plots as the season, and makes the font smaller
    plt.legend(prop={'size': 10})#,loc=3) # Places the legend in the lower left corner at a size of 10
    sze = 10 #size of annotation text
    
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    #ax.xaxis.labelpad = 100
    
    
    plt.grid(True)    # Add grid lines to make graph interpretation easier
#%%
# =============================================================================
# from datetime import datetime
# import matplotlib.pyplot as plt
# from matplotlib.dates import DateFormatter
# 
# myDates = [datetime(2012,1,i+3) for i in range(10)]
# myValues = [5,6,4,3,7,8,1,2,5,4]
# fig, ax = plt.subplots()
# ax.plot(myDates,myValues)
# 
# myFmt = DateFormatter("%b")
# ax.xaxis.set_major_formatter(myFmt)
# 
# ## Rotate date labels automatically
# fig.autofmt_xdate()
# plt.show()
# =============================================================================
