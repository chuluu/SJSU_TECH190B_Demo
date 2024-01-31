# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:56:18 2024

@author: JavadiR
"""

import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

class Name():
    def __init__(self):
        ...
        
    def fnc1(self):
        ...
        
    def fnc2(self):
        ...

class BasicStatistics():
    def __init__(self):
        None
        
    def get_avg(self,arr):
        return sum(arr)/len(arr)
    
    def get_SD(self,arr):
        return np.std(arr)
    
class SolderPadDataProcessing(BasicStatistics):
    def __init__(self,csvname):
        self.csvname = csvname
        self.df = None
        self.df_dict = None
        self.KeyValues = None
        
    def get_df(self):
        self.df = pd.read_csv(self.csvname)
        self.titles = list(self.df.head(0))
        return self.df,self.titles
    
    def df_to_dict(self):
        df_dict = {}
        for ii in range(len(self.titles)):
            df_dict.update({self.titles[ii] : list(self.df[self.titles[ii]])})
        
        self.df_dict = df_dict
        return df_dict
    
    def ObtainKeyVariables(self,names):
        SD_dict = {}
        AVG_Dict = {}
        MAX_Dict = {}
        MIN_Dict = {}
        for name in names:
            sd = self.get_SD(self.df_dict[name])
            average = self.get_avg(self.df_dict[name])
            
            SD_dict.update({name : sd   })
            AVG_Dict.update({name : average   })
            MAX_Dict.update({name : max(self.df_dict[name]) })
            MIN_Dict.update({name : min(self.df_dict[name])   })
            
        KeyValues = {'SD' : SD_dict , 'Average' : AVG_Dict,
                     'Max' : MAX_Dict, 'Min' : MIN_Dict}
        
        self.KeyValues = KeyValues
        return KeyValues
    
    def PrintTables(self,names):
        df = pd.DataFrame(self.KeyValues)
        print(df)
        print('')
        print('{:<2} & {:<10} & {:<10} & {:<10} \\\\ '.format('','Volume (%)','Height (um)', 'Area (%)'))
        print('{:<2} & {:<10} & {:<10} & {:<10} \\\\ '.format('SD',round(self.KeyValues['SD'][names[0]],2),round(self.KeyValues['SD'][names[1]],2),round(self.KeyValues['SD'][names[2]],2)))
        print('{:<2} & {:<10} & {:<10} & {:<10} \\\\ '.format('Average',round(self.KeyValues['Average'][names[0]],2),round(self.KeyValues['Average'][names[1]],2),round(self.KeyValues['Average'][names[2]],2)))
        print('{:<2} & {:<10} & {:<10} & {:<10} \\\\ '.format('Min',self.KeyValues['Min'][names[0]],self.KeyValues['Min'][names[1]],self.KeyValues['Min'][names[2]]))
        print('{:<2} & {:<10} & {:<10} & {:<10} \\\\ '.format('Max',self.KeyValues['Max'][names[0]],self.KeyValues['Max'][names[1]],self.KeyValues['Max'][names[2]]))

    def scatter_plot(self,x_name,y_name):
        self.df.plot(kind = 'scatter', x = x_name, y = y_name)
      
    def histogram(self,names,avg=False):
        color = ['r','g','b','k','y']
        ii = 0
        for value in names:
            self.df[value].plot(kind = 'hist',color=color[ii])
            ii = ii+1

        plt.legend(names) 
        plt.xlabel('value')
        ii = 0

        for value in names:
            if avg == True:
                plt.vlines(self.KeyValues['Average'][value], 0,5000, linestyles='dashed',color=color[ii])
                #ax.annotate(value,(self.KeyValues['Average'][value]+5,4000))
            else:
                None
                    
            ii = ii+1
                
        
    def ID_plotting(self,names):
        color = ['r','g','b','k','y']
        ii = 0
        for value in names:
            self.df[value].plot(kind = 'line', x = 'ID',color=color[ii])
            ii = ii+1
        plt.legend(names) 
        plt.xlabel('Pad ID')
        plt.ylabel('Unit %')
        
        
        
if __name__ == '__main__':
    #csvname = "https://github.com/chuluu/SJSU_TECH190B_Demo/blob/main/Test_Data_noheader.csv?raw=true"
    csvname = "Test_Data_noheader.csv"
    
    SPD = SolderPadDataProcessing(csvname)
    SPD.get_df()
    print(SPD.titles)
    print('')
    
    names = ['Volume(%)','Height(um)','Area(%)']
    names = [SPD.titles[2],SPD.titles[3],SPD.titles[4]]
    
    df_dict = SPD.df_to_dict()
    SPD.ObtainKeyVariables(names)
    SPD.PrintTables(names)
    SPD.ID_plotting(names)
    fig, ax = plt.subplots()
    SPD.histogram(names,True)


# =============================================================================
# #%%
# plt.close('all')
# 
# df = pd.read_csv("Test_Data_noheader.csv")
# #download_file = "https://github.com/chuluu/SJSU_TECH190B_Demo/blob/main/Test_Data_noheader.csv?raw=true"
# #df = pd.read_csv(download_file,index_col=0)
# vall = list(df.head(0))
# 
# type_graph = 'line'
# display = [['ID','Height(um)'],['ID','Area(%)'],['ID','Volume(%)']]
# #showing_graphs = ['Volume(%)','Height(um)']
# 
# fig, ax = plt.subplots()
# 
# for ii in range(len(display)):
#     showing_graphs = display[ii]
# 
#     if type_graph == 'hist':
#         for value in showing_graphs:
#             df[value].plot(kind = type_graph)
#         ax.hlines(3000, 120,.5, linestyles='dashed')
#         ax.annotate('average',(-0.4,3010))
#         ax.legend(showing_graphs)
#         
#     elif type_graph == 'scatter':
#         df.plot(kind = 'scatter', x = showing_graphs[0], y = showing_graphs[1])
#     
#         
#     elif type_graph == 'line':
#         df.plot(kind = 'line', x = showing_graphs[0], y = showing_graphs[1],ax=ax)
#         
#     else:
#         raise ValueError('Name does not exist')
#         
# 
# =============================================================================
