# -*- coding: utf-8 -*-
"""
Created on Thu May 10 12:23:19 2018

@author: Jordan Munson
"""
import pandas as pd
import numpy as np

#Calculate some statistics
#Create a test dataframe to ensure the functions are correct
df_test=pd.DataFrame()
df_test['M']= [5,6,5,11]
df_test['O']= [6,8,6,12]
#Normalized Mean Bias - NMB
def nmb(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']=df_new[name_var1]-df_new[name_var2]
    NMB=round((df_new['dif_var'].sum()/df_new[name_var2].sum())*100,2)
    return NMB
#Normalized Mean Error - NME
def nme(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']= abs(df_new[name_var1]-df_new[name_var2])
    NME=round((df_new['dif_var'].sum()/df_new[name_var2].sum())*100,2)
    return NME
    
#Root Mean Squared Error - RMSE
def rmse(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']= (df_new[name_var1]-df_new[name_var2])**(2)
    RMSE=round((df_new['dif_var'].sum()/len(df_new.index))**(0.5),2)
    return RMSE
    
#Coefficient of Determination - r^2
def r2(df,name_var1,name_var2):
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    top_var= ((df_new[name_var1]-np.mean(df_new[name_var1])) * (df_new[name_var2]-np.mean(df_new[name_var2]))).sum()
    bot_var= (((df_new[name_var1]-np.mean(df_new[name_var1]))**2).sum() * ((df_new[name_var2]-np.mean(df_new[name_var2]))**2).sum())**(.5)    
    r_squared=round(((top_var/bot_var)**2),2)
    return r_squared

#Fractional bias - FB
def fb(df,name_var1,name_var2):  #var1 is model var2 is observed    
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']=df_new[name_var1]-df_new[name_var2]
    df_new['sum_var']=df_new[name_var1]+df_new[name_var2]
# =============================================================================
#     df_new = df_new.drop(df_new[df_new.sum_var<=0].index) # Drop cells that are zero. These values cause infinity results
#     df_new = df_new.drop(df_new[df_new.dif_var==0].index) # Drop cells that are zero. These values cause infinity results 
# =============================================================================
    df_new = df_new.dropna()
    FB= round((df_new['dif_var']/df_new['sum_var']).sum()*(2/len(df_new.index))*100,2)
    return FB

#Fractional error - FE
def fe(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']=abs(df_new[name_var1]-df_new[name_var2])
    df_new['sum_var']=df_new[name_var1]+df_new[name_var2]
# =============================================================================
#     df_new = df_new.drop(df_new[df_new.sum_var<=0].index) # Drop cells that are zero. These values cause infinity results
#     df_new = df_new.drop(df_new[df_new.dif_var==0].index) # Drop cells that are zero. These values cause infinity results
# =============================================================================
    df_new = df_new.dropna()
    FE= round((df_new['dif_var']/df_new['sum_var']).sum()*(2/len(df_new.index))*100,2)
    return FE
    
#Mean bias - MB
def mb(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']=df_new[name_var1]-df_new[name_var2]
    MB=round((df_new['dif_var'].sum())/len(df_new.index),2)
    return MB

#Mean bias - ME
def me(df,name_var1,name_var2):  #var1 is model var2 is observed
    df_new=pd.DataFrame()
    df_new[name_var1]=df[name_var1]
    df_new[name_var2]=df[name_var2]
    df_new['dif_var']=df_new[name_var1]-df_new[name_var2]
    ME=round(abs(df_new['dif_var']).sum()/len(df_new.index),2)
    return ME

#Calculates and combines into a labeled dataframe    
def stats(df,name_var1,name_var2):
    NMB = nmb(df,name_var1,name_var2)
    NME = nme(df,name_var1,name_var2)
    RMSE = rmse(df,name_var1,name_var2)
    r_squared = r2(df,name_var1,name_var2)
    MB = mb(df,name_var1,name_var2)
    ME = me(df,name_var1,name_var2)
    FB = fb(df,name_var1,name_var2)
    FE = fe(df,name_var1,name_var2)
    g = pd.DataFrame([MB,ME,RMSE,FB,FE,NMB,NME,r_squared])
    g.index = ['MB','ME',"RMSE",'FB','FE',"NMB", "NME", "r_squared"]
    g.columns = [name_var1]
    return g
########### Below is an example of how these functions can be used
'''
#Run the stats function for the desired data
#Test_stats = stats(df_test,'M', 'O')
O3_1p33km_stats = stats(combined1, '1p33km_O3', 'm205_O3_Avg')
O3_4km_stats = stats(combined1, '4km_O3', 'm205_O3_Avg')
NO2_1p33km_stats = stats(combined1, '1p33km_NO2', 'm405_NO2_Avg')
NO2_4km_stats = stats(combined1, '4km_NO2', 'm405_NO2_Avg')
NO_1p33km_stats = stats(combined1, '1p33km_NO', 'm405_NO_Avg')
NO_4km_stats = stats(combined1, '4km_NO', 'm405_NO_Avg')
SO2_1p33km_stats = stats(combined1, '1p33km_SO2', 't100u_so2_Avg')
SO2_4km_stats = stats(combined1, '4km_SO2', 't100u_so2_Avg')

#Calculate stats for regression plots
O3_regression_stats = stats(combined1, '4km_O3', '1p33km_O3')
NO2_regression_stats = stats(combined1, '4km_NO2', '1p33km_NO2')
NO_regression_stats = stats(combined1, '4km_NO', '1p33km_NO')
SO2_regression_stats = stats(combined1, '4km_SO2', '1p33km_SO2')

#Combine the statistics
O3_stats = pd.merge(O3_1p33km_stats,O3_4km_stats, how = 'inner', left_index = True, right_index = True)
NO2_stats = pd.merge(NO2_1p33km_stats,NO2_4km_stats, how = 'inner', left_index = True, right_index = True)
NO_stats = pd.merge(NO_1p33km_stats,NO_4km_stats, how = 'inner', left_index = True, right_index = True)
SO2_stats = pd.merge(SO2_1p33km_stats,SO2_4km_stats, how = 'inner', left_index = True, right_index = True)
O3_NO2 = pd.merge(O3_stats,NO2_stats, how = 'inner', left_index = True, right_index = True)
SO2_NO = pd.merge(SO2_stats,NO_stats, how = 'inner', left_index = True, right_index = True)
Statistics = pd.merge(O3_NO2,SO2_NO, how = 'inner', left_index = True, right_index = True)

#Save Statistics to excel file
writer = pd.ExcelWriter('Statistics.xlsx')
Statistics.to_excel(writer, 'Sheet1')
writer.save()
'''
###########
#%%