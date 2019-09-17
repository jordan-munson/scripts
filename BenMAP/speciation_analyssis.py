# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 13:44:39 2019

@author: riptu
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import geopandas as gpd

inputDir = r'E:\Research\Benmap/'
plotDir = inputDir+'plots/'
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'
shp_name = r'E:\Research\Benmap\benmap_shapefile_output/Krewski.shp'

counties = gpd.read_file(shp_name)
counties = counties.rename(columns={"COL": "Col",'ROW':'Row'})

AECIJ_2016 = pd.read_csv(inputDir +'output/speciation/2016_BASE_NARA_AIRPACT_speciation_benmap_AECIJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 
ANH4IJ_2016 = pd.read_csv(inputDir +'output/speciation/2016_BASE_NARA_AIRPACT_speciation_benmap_ANH4IJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 
ANO3IJ_2016 = pd.read_csv(inputDir +'output/speciation/2016_BASE_NARA_AIRPACT_speciation_benmap_ANO3IJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 
APOCIJ_2016 = pd.read_csv(inputDir +'output/speciation/2016_BASE_NARA_AIRPACT_speciation_benmap_APOCIJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 
ASO4IJ_2016 = pd.read_csv(inputDir +'output/speciation/2016_BASE_NARA_AIRPACT_speciation_benmap_ASO4IJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 

AECIJ_2017 = pd.read_csv(inputDir +'output/speciation/2017_BASE_NARA_AIRPACT_speciation_benmap_AECIJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 
ANH4IJ_2017 = pd.read_csv(inputDir +'output/speciation/2017_BASE_NARA_AIRPACT_speciation_benmap_ANH4IJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 
ANO3IJ_2017 = pd.read_csv(inputDir +'output/speciation/2017_BASE_NARA_AIRPACT_speciation_benmap_ANO3IJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 
APOCIJ_2017 = pd.read_csv(inputDir +'output/speciation/2017_BASE_NARA_AIRPACT_speciation_benmap_APOCIJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 
ASO4IJ_2017 = pd.read_csv(inputDir +'output/speciation/2017_BASE_NARA_AIRPACT_speciation_benmap_ASO4IJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 

AECIJ_2018 = pd.read_csv(inputDir +'output/speciation/2018_BASE_NARA_AIRPACT_speciation_benmap_AECIJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 
ANH4IJ_2018 = pd.read_csv(inputDir +'output/speciation/2018_BASE_NARA_AIRPACT_speciation_benmap_ANH4IJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 
ANO3IJ_2018 = pd.read_csv(inputDir +'output/speciation/2018_BASE_NARA_AIRPACT_speciation_benmap_ANO3IJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 
APOCIJ_2018 = pd.read_csv(inputDir +'output/speciation/2018_BASE_NARA_AIRPACT_speciation_benmap_APOCIJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 
ASO4IJ_2018 = pd.read_csv(inputDir +'output/speciation/2018_BASE_NARA_AIRPACT_speciation_benmap_ASO4IJ_QuarterlyMean.csv').drop(columns =['Metric', 'Seasonal Metric', 'Annual Metric'], axis=1) 


# =============================================================================
# Data modification
# =============================================================================
def conv_to_year(df,name):
    # new data frame with split value columns 
    new = df["Values"].str.split(",", n = 4, expand = True)
    new[0] = pd.to_numeric(new[0])
    new[1] = pd.to_numeric(new[1])
    new[2] = pd.to_numeric(new[2])
    new[3] = pd.to_numeric(new[3])
    
    new['avg'] = new.mean(axis=1)
    # making separate first name column from new data frame 
    df[name]= new['avg'] 
      
    # Dropping old Name columns 
    df.drop(columns =["Values"], inplace = True) 
    return df

    
species = ['AECIJ','ANH4IJ','ANO3IJ','APOCIJ','ASO4IJ']
years = ['2016','2017','2018']

AECIJ_2016_yearly = conv_to_year(AECIJ_2016,'AECIJ_2016')
ANH4IJ_2016_yearly = conv_to_year(ANH4IJ_2016,'ANH4IJ_2016').drop(columns =['Row', 'Column'], axis=1)  # drop row and column here so that the concat works
ANO3IJ_2016_yearly = conv_to_year(ANO3IJ_2016,'ANO3IJ_2016').drop(columns =['Row', 'Column'], axis=1) 
APOCIJ_2016_yearly = conv_to_year(APOCIJ_2016,'APOCIJ_2016').drop(columns =['Row', 'Column'], axis=1) 
ASO4IJ_2016_yearly = conv_to_year(ASO4IJ_2016,'ASO4IJ_2016').drop(columns =['Row', 'Column'], axis=1) 

AECIJ_2017_yearly = conv_to_year(AECIJ_2017,'AECIJ_2016').drop(columns =['Row', 'Column'], axis=1) 
ANH4IJ_2017_yearly = conv_to_year(ANH4IJ_2017,'ANH4IJ_2017').drop(columns =['Row', 'Column'], axis=1) 
ANO3IJ_2017_yearly = conv_to_year(ANO3IJ_2017,'ANO3IJ_2017').drop(columns =['Row', 'Column'], axis=1) 
APOCIJ_2017_yearly = conv_to_year(APOCIJ_2017,'APOCIJ_2017').drop(columns =['Row', 'Column'], axis=1) 
ASO4IJ_2017_yearly = conv_to_year(ASO4IJ_2017,'ASO4IJ_2017').drop(columns =['Row', 'Column'], axis=1) 

AECIJ_2018_yearly = conv_to_year(AECIJ_2018,'AECIJ_2016').drop(columns =['Row', 'Column'], axis=1) 
ANH4IJ_2018_yearly = conv_to_year(ANH4IJ_2018,'ANH4IJ_2018').drop(columns =['Row', 'Column'], axis=1) 
ANO3IJ_2018_yearly = conv_to_year(ANO3IJ_2018,'ANO3IJ_2018').drop(columns =['Row', 'Column'], axis=1) 
APOCIJ_2018_yearly = conv_to_year(APOCIJ_2018,'APOCIJ_2018').drop(columns =['Row', 'Column'], axis=1) 
ASO4IJ_2018_yearly = conv_to_year(ASO4IJ_2018,'ASO4IJ_2018').drop(columns =['Row', 'Column'], axis=1) 

df_com = pd.concat([AECIJ_2016_yearly,ANH4IJ_2016_yearly,ANO3IJ_2016_yearly,APOCIJ_2016_yearly,ASO4IJ_2016_yearly,
                    AECIJ_2017_yearly,ANH4IJ_2017_yearly,ANO3IJ_2017_yearly,APOCIJ_2017_yearly,ASO4IJ_2017_yearly,
                    AECIJ_2018_yearly,ANH4IJ_2018_yearly,ANO3IJ_2018_yearly,APOCIJ_2018_yearly,ASO4IJ_2018_yearly],axis=1)
df_com = df_com.rename(columns={"Column": "Col"})
df_com = pd.merge(df_com,counties,on=['Col','Row'])
#%%
# =============================================================================
# lOAD IN DATA FROM BENNMAP
# =============================================================================
drop_list = [ #'Delta',
 'Mean',
 'Baseline',
 'Percent of Baseline',
 'Standard Deviation',
 'Variance',
 'Percentile 2.5',
 'Percentile 7.5',
 'Percentile 12.5',
 'Percentile 17.5',
 'Percentile 22.5',
 'Percentile 27.5',
 'Percentile 32.5',
 'Percentile 37.5',
 'Percentile 42.5',
 'Percentile 47.5',
 'Percentile 52.5',
 'Percentile 57.5',
 'Percentile 62.5',
 'Percentile 67.5',
 'Percentile 72.5',
 'Percentile 77.5',
 'Percentile 82.5',
 'Percentile 87.5',
 'Percentile 92.5',
 'Percentile 97.5', 
 'Start Age','Author',
 'Endpoint Group',
 'End Age',
 'Version',
 'Endpoint',
 'Point Estimate',
 'Pollutant']

df_species = pd.DataFrame(columns=['Col', 'Row', 'Population', 'Delta', 'Pollutant', 'Year'])
for name in species:
    for year in years:
        d = pd.read_csv(r'C:\Users\riptu\Documents\My BenMAP-CE Files\Result\APVR\Speciation/'+name+'_'+year+'.CSV').drop(drop_list,axis=1)      
        d['Pollutant'] = name
        d['Year'] = year
        
        d1 = d[d['Col'] == 53]
        d2 = d[d['Col'] == 16]
        d3 = d[d['Col'] == 41]
        d = pd.concat([d1,d2,d3])
        
        df_species = pd.concat([df_species,d])
df_species = df_species.rename(columns={'Delta':'Concentration'})    
siteid = pd.read_csv(r'E:\Research\AIRPACT_eval\aqs_sites/aqs_sites.csv').drop(['Site Number', 'Land Use','Location Setting', 'Latitude','Longitude',
 'Datum',
 'Elevation',
 'Site Established Date',
 'Site Closed Date',
 'Met Site State Code',
 'Met Site County Code',
 'Met Site Site Number',
 'Met Site Type',
 'Met Site Distance',
 'Met Site Direction',
 'GMT Offset',
 'Owning Agency',
 'Local Site Name',
 'Address',
 'Zip Code',
 'City Name',
 'CBSA Name',
 'Tribe Name',
 'Extraction Date'],axis=1)   
    
# Create a dataframe of state/county codes
siteid_1 = siteid[siteid['State Code'] == '53'].drop_duplicates(['County Code'])
siteid_2 = siteid[siteid['State Code'] == '41'].drop_duplicates(['County Code'])
siteid_3 = siteid[siteid['State Code'] == '16'].drop_duplicates(['County Code'])

siteid = pd.concat((siteid_1,siteid_2))
siteid = pd.concat((siteid,siteid_3))
siteid = siteid.rename(columns={"State Code": "Col", "County Code": "Row"})
siteid['Col'] = pd.to_numeric(siteid['Col'])

df_species = pd.merge(df_species,siteid)

#%%

    # =============================================================================
# Plot df_table
# =============================================================================
# Barplot
#functions = ['Mortality','Asthma Exacerbation','Emergency Room Visits  Respiratory','filler']
pollutants = ['AECIJ','ANH4IJ','ANO3IJ','APOCIJ','ASO4IJ']
years = ['2016','2017','2018']
inc_or_per = ['incidence']#,'percent']
for iop in inc_or_per:
    #for species in pollutants:   
            function = 'Speciation'
            fig = plt.figure(figsize=(7.5,6),dpi=100)
            
            for year,i in zip(years,[1,2,3]):
                # select data
                d = df_species.copy()
                #d['Endpoint Group'] = d['Endpoint Group'].astype(str)
# =============================================================================
#                 d = d.loc[d['Pollutant'] == species]
#                 d = d.loc[d['Year'] == year]
# =============================================================================
                # seperate dataframes
                d1 = d.copy()
                d2 = d.copy()
                d3 = d.copy()
                d4 = d.copy()
                d5 = d.copy()
                d1 = d1.loc[d1['Pollutant'] == 'AECIJ']
                d1 = d1.loc[d1['Year'] == year]
                d1 = d1.sort_values(by='Concentration', ascending=False).reset_index(drop=True)
                d2 = d2.loc[d2['Pollutant'] == 'ANH4IJ']
                d2 = d2.loc[d2['Year'] == year]
                d2 = d2.sort_values(by='Concentration', ascending=False).reset_index(drop=True)
                d3 = d3.loc[d3['Pollutant'] == 'ANO3IJ']
                d3 = d3.loc[d3['Year'] == year]
                d3 = d3.sort_values(by='Concentration', ascending=False).reset_index(drop=True)
                d4 = d4.loc[d4['Pollutant'] == 'APOCIJ']
                d4 = d4.loc[d4['Year'] == year]
                d4 = d4.sort_values(by='Concentration', ascending=False).reset_index(drop=True)
                d5 = d5.loc[d5['Pollutant'] == 'ASO4IJ']
                d5 = d5.loc[d5['Year'] == year]
                d5 = d5.sort_values(by='Concentration', ascending=False).reset_index(drop=True)
                
                
                
                
                d1 = d1.sort_values(by='Concentration', ascending=False).reset_index(drop=True) # Sort by DEQ for consistency                
                d1 = d1.head(20).sort_values(by='County Name', ascending=True)  
                county_names = d1['County Name']
                county_names=pd.DataFrame(county_names).head(20) # need the head, otherwise there is an odd last row
                county_names['State Name'] = d1['State Name']
                d2 = pd.merge(d2,county_names).sort_values(by='County Name', ascending=True) # This ensures the same counties are used
                d3 = pd.merge(d3,county_names).sort_values(by='County Name', ascending=True)
                d4 = pd.merge(d4,county_names).sort_values(by='County Name', ascending=True)
                d5 = pd.merge(d5,county_names).sort_values(by='County Name', ascending=True)
# =============================================================================
#                 d2 = d2.sort_values(by='Concentration', ascending=False).reset_index(drop=True) # Sort by DEQ for consistency                
#                 d2 = d2.head(20)
#                 d3 = d3.sort_values(by='Concentration', ascending=False).reset_index(drop=True) # Sort by DEQ for consistency                
#                 d3 = d3.head(20)
#                 d4 = d4.sort_values(by='Concentration', ascending=False).reset_index(drop=True) # Sort by DEQ for consistency                
#                 d4 = d4.head(20)
#                 d5 = d5.sort_values(by='Concentration', ascending=False).reset_index(drop=True) # Sort by DEQ for consistency                
#                 d5 = d5.head(20)
# =============================================================================
                ymax = max(d1['Concentration'])
                labels = d1['County Name']
                x = np.arange(len(d1['Col']))  # the label locations
                
                width = 0.35  # the width of the bars
                
                ax = fig.add_subplot(3,1,i)
                dist = 1.3
                if iop == 'incidence':
                    rects1 = ax.bar(x - width/dist, d1['Concentration'], width, label='AECIJ')
                    rects2 = ax.bar(x - width/dist/2, d2['Concentration'], width, label='ANH4IJ')
                    rects3 = ax.bar(x, d3['Concentration'], width, label='ANO3IJ')
                    rects4 = ax.bar(x + width/dist/2, d2['Concentration'], width, label='APOCIJ')
                    rects5 = ax.bar(x + width/dist, d2['Concentration'], width, label='ASO4IJ')
                    ax.set_ylim(0, ymax+1)
                else:
                    rects1 = ax.bar(x - width/1.5, d['mod_'+year]/d['Population']*100, width, label='Model')
                    rects2 = ax.bar(x, d['mon_'+year]/d['Population']*100, width, label='Monitor')
                    rects3 = ax.bar(x + width/1.5, d['DEQ']/d['Population']*100, width, label='DEQ')
                    ax.set_ylim(0, .07) # .13 for PM mortality, 0.07 for Ozone
                    
                
                
                #Label plot
                if i ==1:
                    ax.legend()
                    ax.set_title('2016 (a)')
                if i ==2:
                    ax.set_ylabel('\u03BCg m$^{-3}$')
                    ax.set_title('2017 (b)')
                if i ==3:
                    plt.xticks(x, labels, rotation='vertical')
                    ax.set_title('2018 (c)')
                else:
                    plt.xticks(x, '', rotation='vertical')
                ax.tick_params(axis='x', which='both', length=0)
    
            #fig.tight_layout()
            plt.savefig(plotDir + 'barplots/'+'speciation'+'_'+iop+'_barplot.png')
            plt.show()
#%%
# =============================================================================
# # =============================================================================
# #         Other type of barplot
# # =============================================================================
# # Barplot
# columns = ['County Name',
#  'Endpoint Group',
#  'Pollutant',
#  'Population',
#  'State Name',
#  'Year',
#  'mon_2016',
#  'mon_2017',
#  'mon_2018',
#  'pollutant_monitor',
#  'mod_2016',
#  'mod_2017',
#  'mod_2018',
#  'pollutant_model',
#  'DEQ',
#  'pollutant_DEQ']
# functions = ['Mortality','Asthma Exacerbation','Emergency Room Visits  Respiratory','filler']
# pollutants = ['PM2.5', 'Ozone']
# years = ['2016','2017','2018']
# inc_or_per = ['percent']
# for iop in inc_or_per:
#     for species in pollutants:  
#         fig = plt.figure(figsize=(7.5,6),dpi=100)
#         for year,i in zip(years,[1,2,3]):
#             ax = fig.add_subplot(3,1,i)
#             
#                     
#             # select data
#             d = df_table.copy()
#             d['Endpoint Group'] = d['Endpoint Group'].astype(str)
#             d = d.loc[d['Pollutant'] == species]
#             d = d.sort_values(by='DEQ', ascending=False).reset_index(drop=True) # Sort by DEQ for consistency
#             d = d.loc[d['Year'] == year]
#             d = d.loc[d['County Name'] == 'King']
#             labels = d['Endpoint Group'].replace('Emergency Room Visits  Respiratory', 'ER Visits, Respiratory')
#             x = np.arange(len(d['County Name']))  # the label locations
#             width = 0.35  # the width of the bars
# 
#             ymax = .1
#                 
# 
#             rects1 = ax.bar(x - width/1.5, d['mod_'+year]/d['Population']*100, width, label='Model')
#             rects2 = ax.bar(x, d['mon_'+year]/d['Population']*100, width, label='Monitor')
#             rects3 = ax.bar(x + width/1.5, d['DEQ']/d['Population']*100, width, label='DEQ')
#             #ax.set_ylim(0, ymax) # .13 for PM mortality, 0.07 for Ozone
#             
#             plt.yscale('log')
#             ax.set_ylim(0.001, 1000)
#                 
#                 
#             #Label plot
#             if i ==1:
#                 ax.legend()
#                 ax.set_title('2016 (a)')
#             if i ==2:
#                 ax.set_ylabel('Incidence' +' [%]')
#                 ax.set_title('2017 (b)')
#             if i ==3:
#                 plt.xticks(x, labels)
#                 ax.set_title('2018 (c)')
#             else:
#                 plt.xticks(x, '', rotation='vertical')
#             ax.tick_params(axis='x', which='both', length=0)
#     
#         #fig.tight_layout()
#         #function_save = function.replace(" ", "_")
#         plt.savefig(plotDir + 'barplots/'+species+'_'+iop+'_king_barplot.png')
#         plt.show()
# 
# #%%
# 
# # Scatter plot
# health_stats = pd.DataFrame(['Forecast Mean','Observatio Mean','MB','ME','FB [%]','FE [%]','NMB [%]','NME [%]','RMSE','R^2 [-]','Forecast 98th','Observation 98th'])
# health_stats = health_stats.set_index(0)
# for species in pollutants:  
#     fig = plt.figure(figsize=(7.5,10),dpi=100)
#     for function,k in zip(functions,[0,3,6,9]):
#         
#         if function == 'filler': 
#             if species == 'PM2.5':
#                 function = 'Work Loss Days'
#             else:
#                 function = 'School Loss Days'
#                 
#         for year,i in zip(years,[1,2,3]):
#             # select data
#             d = df_table.copy()
#             d['Endpoint Group'] = d['Endpoint Group'].astype(str)
#             d = d.loc[d['Pollutant'] == species].loc[d['Endpoint Group'] == function]
#             d = d.sort_values(by='DEQ', ascending=False).reset_index(drop=True) # Sort by DEQ for consistency
#             d = d.loc[d['Year'] == year]#.head(20)
#             
#             labels = d['County Name']
#             x = np.arange(len(d['County Name']))  # the label locations
#             width = 0.35  # the width of the bars
#             size= 25
#             j = i+k
#             ax = fig.add_subplot(4,3,j)
#             
#             d = d.dropna(subset=['DEQ','mod_'+year,'mon_'+year])
#             rects1 = ax.scatter(d['DEQ'],d['mod_'+year], label='Model',s=size,alpha = 0.7)
#             rects2 = ax.scatter(d['DEQ'],d['mon_'+year], label='Monitor',s=size, alpha = 0.7)
#             
#             # find best fit line and run stats
#             z1 = np.polyfit(d['DEQ'],d['mod_'+year], 1)
#             z2 = np.polyfit(d['DEQ'],d['mon_'+year], 1)
#             mod_stats = stats_version(d, 'mod_'+year, 'DEQ')
#             mod_stats = mod_stats.rename(columns={'mod_'+year:'Model_'+year+'_'+species+ '_'+function})
#             mon_stats = stats_version(d, 'mon_'+year, 'DEQ')
#             mon_stats = mon_stats.rename(columns={'mon_'+year:'Monitor_'+year+'_'+species + '_'+function})
#             health_stats = pd.merge(health_stats,mon_stats, left_index=True,right_index=True)
#             health_stats = pd.merge(health_stats,mod_stats, left_index=True,right_index=True)
#             
#             r2_mod = mod_stats['Model_'+year+'_'+species+ '_'+function][9]
#             r2_mon = mon_stats['Monitor_'+year+'_'+species+ '_'+function][9]
#             text_string = '\n'.join((
#                 r'Mod $%.2f$' % (r2_mod, ),
#                 r'Mon $%.2f$' % (r2_mon, )))
# 
# 
#             # place a text box in upper right in axes coords
#             ax.text(0.6, 0.25, text_string, transform=ax.transAxes,
#             verticalalignment='top')#, bbox=props)
# 
#             plt.plot([-200, 20000000], [-200, 20000000], 'k-',linewidth=0.7)
# 
#             ax.set_xlim(0, max(d['mod_'+year]))
#             ax.set_ylim(0, max(d['mod_'+year]))
#             ax.set_aspect('equal')
#             #Label plot
#             if j ==1:
#                 ax.legend()
#                 ax.set_title('2016')
#             if j ==2:
#                 ax.set_title('2017')
#             if j==3:
#                 ax.set_title('2018')
#             if j == 11:
#                 ax.set_xlabel('DEQ')
#                 
#             if i ==1:                
#                 ax.set_ylabel(function)
# 
#             #else:
#                 #plt.xticks(x, '', rotation='vertical')
#             #ax.tick_params(axis='x', which='both', length=0)
# 
#     fig.tight_layout()
#     function_save = function.replace(" ", "_")
#     plt.savefig(plotDir + 'scatter/'+species+'_scatter.png')
#     plt.show()
# health_stats = health_stats.T
# health_stats = health_stats.drop(['Observation 98th','Forecast 98th','NMB [%]','NME [%]'],axis=1)
# #%%
# # Print total values
# years = ['2016','2017','2018']
# metrics= ['mod_2016','mod_2017','mod_2018','mon_2016','mon_2017','mon_2018','DEQ']
# for species in pollutants:
#     print(species)
#     for year in years:
#         print(year)
#         for metric in metrics:
#             try:
#                 print(sum(df_table.loc[df_table['Pollutant'] == species].loc[df_table['Endpoint Group'] == 'Mortality'].loc[df_table['Year'] == year].dropna(subset=[metric])[metric]))
#             except:
#                 continue
# #%%
# 
# 
# 
# # Print total values
# years = ['2016','2017','2018']
# metrics= ['pollutant_model','pollutant_monitor','pollutant_DEQ']
# for species in pollutants:
#     print(species)
#     for year in years:
#         print(year)
#         for metric in metrics:
#             try:
#                 print(np.mean(df_table.loc[df_table['Pollutant'] == species].loc[df_table['Endpoint Group'] == 'Mortality'].loc[df_table['Year'] == year].dropna(subset=[metric])[metric]))
#             except:
#                 continue
# 
# 
# #%%
# # =============================================================================
# # Plot all things - DEQ, Model, Monitor
# # =============================================================================
# 
# 
# 
# 
# # Plotting section
# #fig.suptitle('2018 PNW PM$_{2.5}$ Health Impacts',y=0.93,fontsize=20,ha='center') # title
# #
# #fig.text(0.06, 0.5, 'Latitude', va='center', rotation='vertical')
# #fig.text(0.5, 0.09, 'Longitude', va='center', ha = 'center')
# #fig.text(0.265, 0.82, 'Incidence', va='center', ha = 'center',fontsize=18)
# #fig.text(0.685, 0.82, '% Incidence', va='center', ha = 'center',fontsize=18)
# 
# 
# 
# endpoints = ['Mortality'] # sets the endpoints we are looking at
# pollutants = ['PM2.5']
# # Add subplots
# for pollutant in pollutants:
#     for endpoint in endpoints:
#         fig = plt.figure(figsize=(6,4),dpi=150)
#         for year,i,j,k in zip(years,[1,2,3],[4,5,6],[7,8,9]):  
#             
#             # Colorbar
#             #divider = make_axes_locatable(ax)
#             cax = divider.append_axes("right", size="5%", pad=0.2) # depends on the user needs
#             alpha = 0.7
#             linewidth = 1
#             
#         
#             d = df_table.copy()
#             d = pd.merge(d,counties)
#             d = gpd.GeoDataFrame(d)
#             
#             
#             vmax = 250
#             vmin = 0
#                  
#             ax = fig.add_subplot(3,3,i)
#             plt.title(year)
#             im = d.loc[d['Endpoint Group'] == endpoint].loc[d['Pollutant'] == pollutant].dropna(subset=['mon_'+year]).plot(column='mon_'+year, cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
#             states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,linewidth=linewidth,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
#             
#             ax = fig.add_subplot(3,3,j)
#             #plt.title(year)
#             im = d.loc[d['Endpoint Group'] == endpoint].loc[d['Pollutant'] == pollutant].dropna(subset=['mod_'+year]).plot(column='mod_'+year, cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
#             states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,linewidth=linewidth,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
#             
#             ax = fig.add_subplot(3,3,k)
#             #plt.title(year)
#             im = d.loc[d['Endpoint Group'] == endpoint].loc[d['Pollutant'] == pollutant].dropna(subset=['DEQ']).plot(column='DEQ', cmap=cmap, edgecolor=edgecolor, legend=True,ax=ax,vmin=vmin,vmax=vmax)
#             states = df_states.plot(column = 'zeros',cmap='Greys', legend=False,linewidth=linewidth,ax=ax,vmin=vmin,vmax=vmax,facecolor='none',edgecolor='black',alpha=alpha)
#             
#     
#         #fig.tight_layout() # spaces the plots out a bit
#         plt.show()
#         plt.close()
# d = pd.merge(df_table,counties)
# d.to_csv(r'E:\Research\Benmap\output/df_table.csv')
# 
# =============================================================================
