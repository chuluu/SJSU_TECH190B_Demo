# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 20:46:00 2024

@author: Matthew Luu

Description: This code is used to take in solder pad data, then output
a usable gui for a customer to analyze different parts of the data.

Capabilities:
    Histogram:  value occurances
    Line graph: Pad ID vs. specific value
    Table: Outputs max, min, average, standard deviation
    
Key packages:
    tkinter: Python gui package
    Pandas: Python data formating package
    matplotlib: Plotting library
    numpy: for general math

Other goals / notes:
    The goal is to develop code for a usable product for a customer
    
"""



from tkinter import * 
from tkinter import ttk
from functools import partial
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import sys 
# Set backend plotting
%matplotlib inline 

def set_default():
    # Using seaborn's style
    plt.style.use('classic')
    width = 345
    fig_dim = [7,5]
    tex_fonts = {
        # Use LaTeX to write all text
        "text.usetex": False,
        "font.family": "sans",
        # Use 10pt font in plots, to match 10pt font in document
        "axes.labelsize": 20,
        "font.size": 14,
        # Make the legend/label fonts a little smaller
        "legend.fontsize": 18,
        "xtick.labelsize": 18,
        "ytick.labelsize": 18
    }
    
    plt.rcParams.update(tex_fonts)
    
    return fig_dim

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
        """
        print table of key values (dictionary to pandas dataframe )
        quick printing
        """
        df = pd.DataFrame(self.KeyValues)
        print(df)
        
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

def update_spd(ids):
    csvname = "Test_Data_noheader.csv"

    SPD = SolderPadDataProcessing(csvname)
    SPD.get_df()
    names = []
    for id_val in ids:
        names.append(SPD.titles[id_val])
    df_dict = SPD.df_to_dict()
    SPD.ObtainKeyVariables(names)
    
    return SPD,names

def plot_histo(fig,axis,canvas,toolbar,ids): 
    if fig.axes:
        fig.delaxes(fig.axes[0])
            
    # the figure that will contain the plot 
    SPD,names = update_spd(ids)
    SPD.histogram(names,avg = True)

    
    # creating the Tkinter canvas 
    # containing the Matplotlib figure   
    canvas.draw() 
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().pack() 
    
    toolbar.update() 
  
    # placing the toolbar on the Tkinter window 
    canvas.get_tk_widget().pack() 

def plot_line(fig,axis,canvas,toolbar,ids): 
    if fig.axes:
        fig.delaxes(fig.axes[0])
            
    # the figure that will contain the plot 
    SPD,names = update_spd(ids)
    SPD.ID_plotting(names)

    
    # creating the Tkinter canvas 
    # containing the Matplotlib figure   
    canvas.draw() 
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().pack() 
    
    toolbar.update() 
  
    # placing the toolbar on the Tkinter window 
    canvas.get_tk_widget().pack() 

    
def update_histo(figure,axisnew,canvas,toolbar):
    inp = selectdata.get(1.0, "end-1c") 
    displayinfo.delete("1.0","end")

    flag = 0
    if inp == 'vol':
        flag = 1
        ID = [2]
    elif inp == 'height':
        flag = 1
        ID = [3]
    elif inp == 'area':
        flag = 1
        ID = [4]
    elif inp == 'volarea':
        flag = 1
        ID = [2,4]
    elif inp == 'offset':
        flag = 1
        ID = [5,6]  
    else:
        flag = 0 
        
    if flag == 0:
        lbl.config(text = "Need Valid Data") 

    else:
        plot_histo(figure,axisnew,canvas,toolbar,ID)
        SPD,names = update_spd(ID)
        dframe = pd.DataFrame(SPD.KeyValues)
        displayinfo.pack(in_=top, side=LEFT) 
        displayinfo.insert(END,dframe)
        lbl.config(text = "Provided Input: {}".format(ID)) 
        

def update_line(figure,axisnew,canvas,toolbar):
    inp = selectdata.get(1.0, "end-1c") 
    displayinfo.delete("1.0","end")

    flag = 0
    if inp == 'vol':
        flag = 1
        ID = [2]
    elif inp == 'height':
        flag = 1
        ID = [3]
    elif inp == 'area':
        flag = 1
        ID = [4]
    elif inp == 'volarea':
        flag = 1
        ID = [2,4]
    elif inp == 'offset':
        flag = 1
        ID = [5,6]    
    else:
        flag = 0 
        
    if flag == 0:
        lbl.config(text = "Need Valid Data") 

    else:
        plot_line(figure,axisnew,canvas,toolbar,ID)
        SPD,names = update_spd(ID)
        dframe = pd.DataFrame(SPD.KeyValues)
        displayinfo.pack(in_=top, side=LEFT) 
        displayinfo.insert(END,dframe)
        lbl.config(text = "Provided Input: {}".format(ID)) 

      
if __name__ == '__main__':
    # Set up main window
    root = Tk() 
    root.geometry("1920x1080") 
    top = Frame(root)
    bottom = Frame(root)
    top.pack(side=TOP)
    bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
    
    # Set up figure canvas for matplotlib figures to be placed on
    figsize = set_default() # matplotlib label sizes

    figure, axisnew = plt.subplots(figsize=figsize)
    canvas = FigureCanvasTkAgg(figure, 
                               master = root) 
    toolbar = NavigationToolbar2Tk(canvas, 
                                   root) 
    
    # Set up the choices section info
    displayinfo = Text(root, height=5, width=50)
    selectdata  = Text(root, 
                       height = 5, 
                       width = 20) 
    selectdata.pack() 
      
    choices  = Text(root, 
                       height = 5, 
                       width = 20) 
    choices.pack()
    
    choices.insert(END,'choices: \nvol, area, height, \nvolarea, offset')

    # setting the title  
    root.title('Solder Pad Info Graphing') 
      
    # button that displays the plot 
    updateHisto = Button(master = root, 
                        height = 2,  
                        width = 10, 
                        text = "UpdateHisto",  
                        command = partial(update_histo,figure,axisnew,canvas,toolbar)) 
   
    updateHisto.pack() 
    updateHisto.pack(in_=top, side=LEFT)
    
    updateLine = Button(master = root, 
                        height = 2,  
                        width = 10, 
                        text = "UpdateLine",  
                        command = partial(update_line,figure,axisnew,canvas,toolbar)) 

    updateLine.pack() 
    updateLine.pack(in_=top, side=LEFT)
    
    lbl = Label(root, text = "") 
    lbl.pack() 
    
    quit_button = Button(master = root,  
                         command = root.destroy, 
                         height = 2,  
                         width = 10, 
                         text="Quit") 
    quit_button.pack(in_=top, side=LEFT)
    
    # run the gui 
    root.mainloop() 