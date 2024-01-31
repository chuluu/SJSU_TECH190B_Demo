# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:56:18 2024

@author: Matthew Luu

Description: This code is used to take in solder pad data, then output
a report quality tables and figures for a LaTex final document

Capabilities:
    Histogram:  value occurances
    Line graph: Pad ID vs. specific value
    Table: Outputs max, min, average, standard deviation
    
Key packages:
    Pandas: Python data formating package
    matplotlib: Plotting library
    numpy: for general math
    
Other goals / notes:
    The goal is to develop code that when the csv updates, you will just need
    to hit the run button in order to continously get quality figures 
    and tables that you don't need to adjust 
"""

import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
# Set backend plotting
%matplotlib qt 

class Name():
    def __init__(self):
        ...
        
    def fnc1(self):
        ...
        
    def fnc2(self):
        ...

class BasicStatistics():
    """
    By: Matthew Luu
    
    This class does basic statistics, gets and average and standard deviation
    More capabilities can be added...
    
    """
    def __init__(self):
        None
        
    def get_avg(self,arr):
        return sum(arr)/len(arr)
    
    def get_SD(self,arr):
        return np.std(arr)
    
class SolderPadDataProcessing(BasicStatistics):
    """
    By: Matthew Luu
    
    This class takes in csv data, converts it to a dictionary,
    then obtains key variables, plots, and tables out of the csv
    
    Child Class: BasicStatistics for math throughout the work.
    
    """
    def __init__(self,csvname):
        self.csvname = csvname
        self.df = None
        self.df_dict = None
        self.KeyValues = None
        
    def get_df(self):
        """
        get pandas dataframe and title names on csv
        """
        self.df = pd.read_csv(self.csvname)
        self.titles = list(self.df.head(0))
        return self.df,self.titles
    
    def df_to_dict(self):
        """
        convert dataframe to a dictionary.
        """
        df_dict = {}
        for ii in range(len(self.titles)):
            df_dict.update({self.titles[ii] : list(self.df[self.titles[ii]])})
        
        self.df_dict = df_dict
        return df_dict
    
    def ObtainKeyVariables(self,names):
        """
        get average and SD
        """
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

        plt.legend(names,fancybox=True,frameon=True) 
        plt.xlabel('value')
        ii = 0

        for value in names:
            if avg == True:
                plt.vlines(self.KeyValues['Average'][value], 0,5000, linestyles='dashed',color=color[ii])
                #ax.annotate(value,(self.KeyValues['Average'][value]+5,4000))
            else:
                None
                    
            ii = ii+1
        plt.tight_layout()


        
    def ID_plotting(self,names):
        color = ['r','g','b','k','y']
        ii = 0
        for value in names:
            self.df[value].plot(kind = 'line', x = 'ID',color=color[ii])
            ii = ii+1
        plt.legend(names) 
        plt.xlabel('Pad ID')
        plt.ylabel('Unit %')
        plt.tight_layout()


        
def set_size(width, fraction=1):
    """Set figure dimensions to avoid scaling in LaTeX.

    Parameters
    ----------
    width: float
            Document textwidth or columnwidth in pts
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy

    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    # Width of figure (in pts)
    fig_width_pt = width * fraction

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio

    fig_dim = (fig_width_in, fig_height_in)

    return fig_dim
    

def set_latex_standard():
    # Using seaborn's style
    plt.style.use('seaborn-v0_8')
    width = 345
    fig_dim = set_size(420)

    tex_fonts = {
        # Use LaTeX to write all text
        "text.usetex": False,
        "font.family": "serif",
        # Use 10pt font in plots, to match 10pt font in document
        "axes.labelsize": 12,
        "font.size": 12,
        # Make the legend/label fonts a little smaller
        "legend.fontsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10
    }
    
    plt.rcParams.update(tex_fonts)

    return fig_dim

def set_default():
    # Using seaborn's style
    plt.style.use('classic')
    width = 345
    fig_dim = [10,7]
    tex_fonts = {
        # Use LaTeX to write all text
        "text.usetex": False,
        "font.family": "sans",
        # Use 10pt font in plots, to match 10pt font in document
        "axes.labelsize": 20,
        "font.size": 20,
        # Make the legend/label fonts a little smaller
        "legend.fontsize": 18,
        "xtick.labelsize": 18,
        "ytick.labelsize": 18
    }
    
    plt.rcParams.update(tex_fonts)
    
    return fig_dim

if __name__ == '__main__':
    # Change where I am getting data from
    csvname = "https://github.com/chuluu/SJSU_TECH190B_Demo/blob/main/Test_Data_noheader.csv?raw=true"
    #csvname = "Test_Data_noheader.csv"
    
    
    # Change figure defaults
    fig_dim = set_latex_standard()
    #fig_dim = set_default()
    
    # Set up main class
    SPD = SolderPadDataProcessing(csvname)
    SPD.get_df()
    print(SPD.titles)
    print('')
    
    # Gather title names
    names = ['Volume(%)','Height(um)','Area(%)']
    names = [SPD.titles[2],SPD.titles[3],SPD.titles[4]]
    
    
    # Get key information
    df_dict = SPD.df_to_dict()
    SPD.ObtainKeyVariables(names)
    SPD.PrintTables(names)

    # Plot
    fig, ax = plt.subplots(figsize = fig_dim)
    SPD.ID_plotting(names)
    fig, ax = plt.subplots(figsize = fig_dim)
    SPD.histogram(names,True)

# Old plotting
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
