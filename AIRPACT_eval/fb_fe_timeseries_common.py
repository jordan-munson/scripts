# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 08:56:22 2019

@author: Jordan Munson
"""
import matplotlib as mpl
#mpl.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import time

starttime = time.time()
begin_time = time.time()

#Set directory
inputDir = r'E:/Research/AIRPACT_eval/'
stat_path = r'E:/Research/scripts/Urbanova/statistical_functions.py'
exec(open(stat_path).read())

# Set plot parameters
mpl.rcParams['font.family'] = 'calibri'  # the font used for all labelling/text
mpl.rcParams['font.size'] = 10 # 10 for paper. 28 for presentations
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

# load data
df_com = pd.read_csv(inputDir+'AQS_data/df_com_aplong.csv').drop('Unnamed: 0', axis=1)
df_com.loc[:,'O3_mod'] = pd.to_numeric(df_com.loc[:,'O3_mod'], errors='coerce')
df_com.loc[:,'PM2.5_mod'] = pd.to_numeric(df_com.loc[:,'PM2.5_mod'], errors='coerce')
df_com.loc[:,'O3_obs'] = pd.to_numeric(df_com.loc[:,'O3_obs'], errors='coerce')
df_com.loc[:,'PM2.5_obs'] = pd.to_numeric(df_com.loc[:,'PM2.5_obs'], errors='coerce')
df_com['datetime'] = pd.to_datetime(df_com['datetime'])
df_com['AQSID'] = df_com['AQSID'].astype(str)

# read in common sites
df_aqsid_o3 = pd.read_csv(inputDir+'/o3_aqsid.csv',dtype=str).drop('Unnamed: 0', axis=1) # load in AQSID that are present for all versions of AIRPACT. This is created later in the script.
df_aqsid_pm = pd.read_csv(inputDir+'/pm_aqsid.csv',dtype=str).drop('Unnamed: 0', axis=1) # load in AQSID that are present for all versions of AIRPACT. This is created later in the script.

print('Data loading section done')
#%%

##############################################################################
#Run stats for duration of airpact
##############################################################################
exec(open(stat_path).read())
#Plot data
#Function to help move spines
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
list_of_columns_for_stats = ['Forecast Mean', 'Observation Mean', 'MB','ME','FB [%]','FE [%]', "RMSE", "R^2 [-]",'Forecast 98th','Observation 98th','version','unit','species']
aq_stats_com = pd.DataFrame(list_of_columns_for_stats)
aq_stats_com.index = list_of_columns_for_stats
aq_stats_com = aq_stats_com.drop(0,1)      
stats_pm_rural = aq_stats_com
stats_pm_urban = aq_stats_com
stats_pm_suburban = aq_stats_com
stats_ozone_rural = aq_stats_com
stats_ozone_urban = aq_stats_com
stats_ozone_suburban = aq_stats_com

stats_pm_rural.name = 'PM2.5 Rural'
stats_pm_urban.name = 'PM2.5 Urban'
stats_pm_suburban.name = 'PM2.5 Suburban'
stats_ozone_rural.name = 'Ozone Rural'
stats_ozone_urban.name = 'Ozone Urban'
stats_ozone_suburban.name = 'Ozone Suburban'

# monthly stats
    
years = [2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
months = [1,2,3,4,5,6,7,8,9,10,11,12]    
pollutant = ['O3','PM2.5']

for species in pollutant:
    da = df_com.copy().dropna(subset=['Location Setting'])
    da['AQSID'] = da['AQSID'].astype(str)
    if species == 'O3': # only use sites common
        da = pd.merge(da,df_aqsid_o3,on='AQSID')
    else:
        da = pd.merge(da,df_aqsid_pm,on='AQSID')
        
    for setting in settings:    #list(set(da['Location Setting'])):
        if species == 'O3':
            var_units = 'ppb'
        else:
            var_units = 'ug/m3'
        for year in years:  
            if year == 2009 or year == 2010 or year == 2011 or year == 2012:
                version = 'AP-3'
            if year == 2013 or year == 2014 or year == 2015:
                version = 'AP-4'
            if year == 2016 or year == 2017 or year == 2018:
                version = 'AP-5'
                
            for month in months:
                d = da.loc[da['Location Setting']==setting]
                
                d.loc[:,species+'_mod'] = pd.to_numeric(d.loc[:,species+'_mod'], errors='coerce')
                d=d.reset_index()
                site_type = d.loc[0,'Location Setting']        
                d.drop('AQSID',1)
                d=d.set_index('datetime')
                year = str(year)
                month = str(month)
                mask = (d.index > year+'-'+month+'-1') & (d.index <= year+'-'+month+'-28')
                d=d.loc[mask]
                
                df_stats=d
    
                 #Calculate Statistics. Organized the way they are so as to make plotting easier
                df_stats = df_stats.reset_index(drop=True)
                df_stats = df_stats.ix[:,[species+'_mod',species+'_obs','AQSID']]

                df_stats = df_stats.dropna()
                df_stats['diff'] = df_stats[species+'_obs'].abs()-df_stats[species+'_mod'].abs()
                df_stats = df_stats.drop(df_stats[df_stats['diff'] == 0].index)
                try:
                    #Run stats functions
                    #aq_stats = stats(df_stats, species+'_mod', species+'_obs')
                    #aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', year+'_'+species+'_'+site_type)     
                    #aq_stats_com = pd.merge(aq_stats_com,aq_stats, how = 'inner', left_index = True, right_index = True) 
                    name = str(year+'-'+month)
                    if species == 'PM2.5':
                        if site_type == 'RURAL':
                            aq_stats = stats_version(df_stats, species+'_mod', species+'_obs')
                            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', name)   
                            aq_stats = aq_stats.T
                            aq_stats['version'] = version
                            aq_stats['unit'] = var_units
                            aq_stats['species'] = species
                            aq_stats = aq_stats.T
                            stats_pm_rural = pd.merge(stats_pm_rural,aq_stats, how = 'inner', left_index = True, right_index = True)
    
                        elif site_type == 'URBAN AND CENTER CITY':
                            aq_stats = stats_version(df_stats, species+'_mod', species+'_obs')
                            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', name) 
                            aq_stats = aq_stats.T
                            aq_stats['version'] = version
                            aq_stats['unit'] = var_units
                            aq_stats['species'] = species
                            aq_stats = aq_stats.T
                            stats_pm_urban = pd.merge(stats_pm_urban,aq_stats, how = 'inner', left_index = True, right_index = True)
                   
                        elif site_type == 'SUBURBAN':
                            aq_stats = stats_version(df_stats, species+'_mod', species+'_obs')
                            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', name)  
                            aq_stats = aq_stats.T
                            aq_stats['version'] = version
                            aq_stats['unit'] = var_units
                            aq_stats['species'] = species
                            aq_stats = aq_stats.T
                            stats_pm_suburban = pd.merge(stats_pm_suburban,aq_stats, how = 'inner', left_index = True, right_index = True)
                    
                    else:
                        if site_type == 'RURAL':
                            aq_stats = stats_version(df_stats, species+'_mod', species+'_obs')
                            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', name)  
                            aq_stats = aq_stats.T
                            aq_stats['version'] = version
                            aq_stats['unit'] = var_units
                            aq_stats['species'] = species
                            aq_stats = aq_stats.T
                            stats_ozone_rural = pd.merge(stats_ozone_rural,aq_stats, how = 'inner', left_index = True, right_index = True)
    
                        elif site_type == 'URBAN AND CENTER CITY':
                            aq_stats = stats_version(df_stats, species+'_mod', species+'_obs')
                            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', name)  
                            aq_stats = aq_stats.T
                            aq_stats['version'] = version
                            aq_stats['unit'] = var_units
                            aq_stats['species'] = species
                            aq_stats = aq_stats.T
                            stats_ozone_urban = pd.merge(stats_ozone_urban,aq_stats, how = 'inner', left_index = True, right_index = True)
                   
                        elif site_type == 'SUBURBAN':
                            aq_stats = stats_version(df_stats, species+'_mod', species+'_obs')
                            aq_stats.columns = aq_stats.columns.str.replace(species+'_mod', name)  
                            
                            aq_stats = aq_stats.T
                            aq_stats['version'] = version
                            aq_stats['unit'] = var_units
                            aq_stats['species'] = species
                            aq_stats = aq_stats.T
                            
                            stats_ozone_suburban = pd.merge(stats_ozone_suburban,aq_stats, how = 'inner', left_index = True, right_index = True)
                    
    
                except (ZeroDivisionError):
                    pass
                
                print(species+  ' '+ year+' '+month+' '+site_type)


stats_pm_rural = stats_pm_rural.T
stats_pm_urban = stats_pm_urban.T
stats_pm_suburban = stats_pm_suburban.T
stats_ozone_rural = stats_ozone_rural.T
stats_ozone_urban = stats_ozone_urban.T
stats_ozone_suburban = stats_ozone_suburban.T

# Save stats           
stats_pm_rural.to_csv(inputDir+'/stats/PM_rural_monthly_common.csv')   
stats_pm_urban.to_csv(inputDir+'/stats/PM_urban_monthly_common.csv')   
stats_pm_suburban.to_csv(inputDir+'/stats/PM_suburban_monthly_common.csv')   

stats_ozone_rural.to_csv(inputDir+'/stats/O3_rural_monthly_common.csv')   
stats_ozone_urban.to_csv(inputDir+'/stats/O3_urban_monthly_common.csv')   
stats_ozone_suburban.to_csv(inputDir+'/stats/O3_suburban_monthly_common.csv')  

#%%
#########################
#Plot stats using monthly values
########################
stats_pm_rural.name = 'PM2.5 Rural'
stats_pm_urban.name = 'PM2.5 Urban'
stats_pm_suburban.name = 'PM2.5 Suburban'
stats_ozone_rural.name = 'Ozone Rural'
stats_ozone_urban.name = 'Ozone Urban'
stats_ozone_suburban.name = 'Ozone Suburban'

# If a "KeyError" occurs on a FE, it may be because you're using "stats" and not "stats_version" Just change to "FE" and such and it will run
ozone_max_fe = max([max(stats_ozone_rural['FE [%]']),max(stats_ozone_urban['FE [%]']),max(stats_ozone_suburban['FE [%]'])])
ozone_max_fb = max([max(stats_ozone_rural['FB [%]']),max(stats_ozone_urban['FB [%]']),max(stats_ozone_suburban['FB [%]'])])
ozone_max_r2 = max([max(stats_ozone_rural['R^2 [-]']),max(stats_ozone_urban['R^2 [-]']),max(stats_ozone_suburban['R^2 [-]'])])

pm_max_fe = max([max(stats_pm_rural['FE [%]']),max(stats_pm_urban['FE [%]']),max(stats_pm_suburban['FE [%]'])])+5
pm_max_fb = max([max(stats_pm_rural['FB [%]']),max(stats_pm_urban['FB [%]']),max(stats_pm_suburban['FB [%]'])])+10
pm_max_r2 = max([max(stats_pm_rural['R^2 [-]']),max(stats_pm_urban['R^2 [-]']),max(stats_pm_suburban['R^2 [-]'])])
#Plot some statistics
stat_list = [stats_ozone_rural,stats_ozone_urban,stats_ozone_suburban,stats_pm_rural,stats_pm_urban,stats_pm_suburban]
for dataframe in stat_list:
    d=dataframe
    d.index= pd.to_datetime(d.index,yearfirst=True)
    fig,ax=plt.subplots(1,1, figsize=(12,4))
    ax.set_title(str(dataframe.name)+' FE and FB')
           
    # Identify which axis is what
    axis1 = 'FE [%]'
    axis2 = 'nan'
    axis3 = 'FB [%]'
    axis4 = 'R^2 [-]'
    
    #Start the extra axis
    #par1 = ax.twinx()
    #par2 = ax.twinx()
    par3 = ax.twinx()

    #Set the location of the extra axis
    #par1.spines["right"].set_position(("axes", 1.1)) # red one
    #par2.spines["left"].set_position(("axes", -0.1)) # red one
    par3.spines["right"].set_position(('axes',1))

    #make_patch_spines_invisible(par1)
    #make_patch_spines_invisible(par2)
    make_patch_spines_invisible(par3)
    
    #Move spines
    #par1.spines["right"].set_visible(True)
    #par1.yaxis.set_label_position('right')
    #par1.yaxis.set_ticks_position('right')

    #par2.spines["left"].set_visible(True)
    #par2.yaxis.set_label_position('left')
    #par2.yaxis.set_ticks_position('left')

    par3.spines["right"].set_visible(True)
    par3.yaxis.set_label_position('right')
    par3.yaxis.set_ticks_position('right')
    
    #Select which data to plot, label, and color
    p1, = ax.plot(d[axis1], 'b-', label = axis1)
    #p2, = par1.plot(d['RMSE'], 'r-', label = 'RMSE')
   # p3, = par2.plot(d[axis3], 'g-', label = axis3)
    p4, = par3.plot(d[axis3], 'darkorange', label = axis3) #r^2 will always be this axis, and it's just easier to hard code the label
    
    #Set the y axis values
    if dataframe.name in ['Ozone Rural','Ozone Urban','Ozone Suburban']: #Ozone
        ax.set_ylim(0, ozone_max_fe)
        #par1.set_ylim(0, 20)
        par3.set_ylim(ozone_max_fb*-1, ozone_max_fb)
        #par3.set_ylim(1, 0)
    else:   #PM
        ax.set_ylim(0, pm_max_fe)
        #par1.set_ylim(0, 40)
        par3.set_ylim(pm_max_fb*-1, pm_max_fb)
        #par3.set_ylim(1, 0)
    
    #Label the y axis
    ax.set_ylabel(axis1)
    #par1.set_ylabel('RMSE')
    #par2.set_ylabel(axis3)
    par3.set_ylabel(axis3)
    
    #Sets color of labels
    ax.yaxis.label.set_color(p1.get_color())
    #par1.yaxis.label.set_color(p2.get_color())
    #par2.yaxis.label.set_color(p3.get_color())
    par3.yaxis.label.set_color(p4.get_color())
    
    #Settings for the tics
    tkw = dict(size=4, width=1.5)
    ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
    #par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    #par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    par3.tick_params(axis='y', colors=p4.get_color(), **tkw)
    ax.tick_params(axis='x', **tkw)
    plt.grid(True)
    plt.savefig(inputDir+'/plots/stats/'+dataframe.name+'_monthly_stats.png',  pad_inches=0.1, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # Plot r^2
    fig,ax=plt.subplots(1,1, figsize=(12,4))
    ax.set_title(str(dataframe.name)+' $r^2$')
    p4, = ax.plot(d[axis4], 'g-', label = '$r^2$')
    ax.set_ylim(0,1)
    ax.set_ylabel('$r^2$')
    ax.yaxis.label.set_color(p4.get_color())
    ax.tick_params(axis='y', colors=p4.get_color(), **tkw)
    plt.grid(True)
    plt.savefig(inputDir+'/plots/stats/'+dataframe.name+'_monthly_r2_stats.png',  pad_inches=0.1, bbox_inches='tight')
    plt.show()
    plt.close()

#%%
end_time = time.time()
print("Run time was %s minutes"%(round((end_time-begin_time)/60)))
print('done')