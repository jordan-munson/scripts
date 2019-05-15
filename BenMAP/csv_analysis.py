# -*- coding: utf-8 -*-
"""
Created on Tue May 14 14:52:58 2019

@author: Jordan Munson
"""

import pandas as pd

inputDir = r'C:/Users/riptu/Documents/My BenMAP-CE Files/Result/APVR/AIRPACT/'

# Read in data
mon_2010 = pd.read_csv(inputDir + '2010_mon_csv.CSV')
mon_2011 = pd.read_csv(inputDir + '2011_mon_csv.CSV')
mon_2012 = pd.read_csv(inputDir + '2012_mon_csv.CSV')
mon_2013 = pd.read_csv(inputDir + '2013_mon_csv.CSV')
mon_2014 = pd.read_csv(inputDir + '2014_mon_csv.CSV')
mon_2015 = pd.read_csv(inputDir + '2015_mon_csv.CSV')
mon_2016 = pd.read_csv(inputDir + '2016_mon_csv.CSV')
mon_2017 = pd.read_csv(inputDir + '2017_mon_csv.CSV')
mon_2018 = pd.read_csv(inputDir + '2018_mon_csv.CSV')


# =============================================================================
# CA = 6
# ID = 16
# MT = 30
# NV = 32
# OR = 41
# UT = 49
# WA = 53
# WY = 56
# =============================================================================
#percent_mortality['Col'] = mon_2010['Col']
# =============================================================================
# Percent mortality
# =============================================================================
# Set up combined df
percent_mortality = pd.DataFrame()
percent_mortality['state'] = ['WY','WA','UT','OR','NV','MT','ID','CA'] # Data only contains state number, this labels them

# Calculate percent mortality
percent_mortality['2010'] = mon_2010['Point Estimate']/mon_2010['Population']*100*-1
percent_mortality['2011'] = mon_2011['Point Estimate']/mon_2011['Population']*100*-1
percent_mortality['2012'] = mon_2012['Point Estimate']/mon_2012['Population']*100*-1
percent_mortality['2013'] = mon_2013['Point Estimate']/mon_2013['Population']*100*-1
percent_mortality['2014'] = mon_2014['Point Estimate']/mon_2014['Population']*100*-1
percent_mortality['2015'] = mon_2015['Point Estimate']/mon_2015['Population']*100*-1
percent_mortality['2016'] = mon_2016['Point Estimate']/mon_2016['Population']*100*-1
percent_mortality['2017'] = mon_2017['Point Estimate']/mon_2017['Population']*100*-1
percent_mortality['2018'] = mon_2018['Point Estimate']/mon_2018['Population']*100*-1
percent_mortality=percent_mortality.set_index('state',drop=True).T.drop(['WY'],axis=1)

ax=percent_mortality.plot()
ax.set_xlabel('Year')
ax.set_ylabel('% Mortality')
ax.set_title('Changes in Mortality due to $PM_{2.5}$')
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5)) # Places legend outside of plot to the right

# Verticle lines at significatn wildfire years
ax.axvline(x=2,color='black',linewidth=0.5)
ax.axvline(x=5,color='black',linewidth=0.5)
ax.axvline(x=7,color='black',linewidth=0.5)
# =============================================================================
# straight mortality
# =============================================================================
mortality = pd.DataFrame()
mortality['state'] = ['WY','WA','UT','OR','NV','MT','ID','CA'] # Data only contains state number, this labels them

# Make point estimate positive for an easier to understand plot
mortality['2010'] = mon_2010['Point Estimate']*-1
mortality['2011'] = mon_2011['Point Estimate']*-1
mortality['2012'] = mon_2012['Point Estimate']*-1
mortality['2013'] = mon_2013['Point Estimate']*-1
mortality['2014'] = mon_2014['Point Estimate']*-1
mortality['2015'] = mon_2015['Point Estimate']*-1
mortality['2016'] = mon_2016['Point Estimate']*-1
mortality['2017'] = mon_2017['Point Estimate']*-1
mortality['2018'] = mon_2018['Point Estimate']*-1
mortality=mortality.set_index('state',drop=True).T.drop(['WY'],axis=1)

ax=mortality.plot()
ax.set_xlabel('Year')
ax.set_ylabel('# of Deaths')
ax.set_title('Mortality due to $PM_{2.5}$')
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5)) # Places legend outside of plot to the right

# Verticle lines at significatn wildfire years
ax.axvline(x=2,color='black',linewidth=0.5)
ax.axvline(x=5,color='black',linewidth=0.5)
ax.axvline(x=7,color='black',linewidth=0.5)











