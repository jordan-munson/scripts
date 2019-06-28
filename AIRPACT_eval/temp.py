# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 12:05:27 2018

@author: Jordan
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

# Set plot parameters
mpl.rcParams['font.family'] = 'time new roman'  # the font used for all labelling/text
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


fig = plt.figure(figsize=(6,3))
fig.text(-0.02, 0.5, 'Ozone (ppb)', va='center', rotation='vertical')
#fig.suptitle('Seasonal Variations by AIRPACT Version',y=1.025) # title
fig.tight_layout() # spaces the plots out a bit

#Annotate versions in
fig.text(0.214, 0.92, 'AP-3', va='center',ha='center')
fig.text(0.53, 0.92, 'AP-4', va='center',ha='center')
fig.text(0.845, 0.92, 'AP-5', va='center',ha='center')

fig.text(0.01,0.78,'Winter',va='center',ha='center', rotation='vertical')
fig.text(0.01,0.3,'Summer',va='center',ha='center', rotation='vertical')
# Make winter month 
db = pd.DataFrame()
s = '12/1/2009'
e = '2/28/2010'

#s = '6/1/2009'
#e = '8/31/2009'
                    
dates = pd.date_range(start=s,end=e)
db['datetime'] = dates
db = db.set_index('datetime')
db['data'] = 5

for i,abc in zip([1,2,3,4,5,6],['(a)','(b)','(c)','(d)','(e)','(f)']):
    ax = fig.add_subplot(2,3,i)
    plt.legend(prop={'size': 10})
    if i == 4:
        plt.legend(prop={'size': 10})
        print('leg')
    else:
        ax.get_legend().remove()
        print('no leg')
    #plt.rcParams["figure.figsize"] = (8,4)
    plt.tight_layout() # spaces the plots out a bit
    
    ax.set_xlabel('')        # Gets rid of the 'DateTime' x label and replaces with a space
    #ax.set_title(str('Winter'),fontsize=12) # sets the titles of individ plots as the season, and makes the font smaller
    #plt.legend(prop={'size': 10})#,loc=3) # Places the legend in the lower left corner at a size of 10
    sze = 10 #size of annotation text
    
    # Set letter denoting plot
    ax.text(.07, 1.23,abc,fontsize = 14, ha='right', va='center', transform=ax.transAxes)
    
    db.plot(kind='line', style='-', ax=ax, color=['black', 'blue'])
    
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    #ax.xaxis.labelpad = 100
    # format x axis
    myFmt = DateFormatter("%b")
    months = mdates.MonthLocator() 
    days = mdates.DayLocator(bymonthday=(1,1))  
    ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_minor_locator(days)
    ax.set_xlim(s,e) # set limits in the hopes of removing doubled last label
    
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
