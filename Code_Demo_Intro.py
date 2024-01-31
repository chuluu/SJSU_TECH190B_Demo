# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 18:20:12 2024

@author: JavadiR
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def average(arr):
    return sum(arr)/len(arr)

'Intro section (simple variables discussion)'

#%% Datatypes variables
x = 1
y = 1.0
z = 'apple'

# quick math with variables
xy = x+y
print('x = {}, type: {}'.format(x,type(x)))
print('y = {}, type: {}'.format(y,type(y)))
print('x + y = {}, type: {}'.format(xy,type(xy)))
print('')

#%% Datastructures list
xyz_list = [x,y,z]
print('list: {}'.format(xyz_list))
print('variable x: {}, list index 0: {}'.format(x,xyz_list[0]))
print('variable z: {}, list index 2: {}'.format(z,xyz_list[2]))
print('')

#%% Datastructures dictionary
xyz_dict = {'int': x, 'float': y, 'string' : z}
print('dictionary: {}'.format(xyz_dict))
print('variable y: {}, dict ind float: {}'.format(y,xyz_dict['float']))
print('variable z: {}, dict ind string: {}'.format(z,xyz_dict['string']))
print('')

#%% how do we process data
# Combine the two list in dictionary
index = [1,2,3,4,5]
gpa   = [3.1,3.5,4.0,2.2,2.9]
xyz_dict = {'student': index, 'gpa': gpa}
print('gpa dictionary: {}'.format(xyz_dict))

#%% doing some math to data
gpa_avg = average(xyz_dict['gpa'])
print('average: {}'.format(gpa_avg))


#%% plotting
xyz_df = pd.DataFrame(xyz_dict)
ax = xyz_df.plot.bar(x='student', y='gpa', rot=0)
ax.hlines(gpa_avg, 6,-1, linestyles='dashed',color='k')
ax.annotate('average',(-0.4,gpa_avg+0.2))



