# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:58:31 2022

@author: Bogdan
"""

import glob
import pandas as pd
import re
 
# specifying the path to csv files
path = "C:\\Users\\Bogdan\\Downloads\\Trial"
 
# csv files in the path
file_list = glob.glob(path + "/*.xls")
 
# list of excel files we want to merge.
# pd.read_excel(file_path) reads the 
# excel data into pandas dataframe.
excl_list = []
 
for file in file_list:
    df = pd.read_excel(file)
    param = re.findall('-?\d+\.?\d*',file)
    df['Sweep'] = param[0]
    df['TipChord'] = param[1]
    df['Twist'] = param[2]
    df.to_excel(file, index=False)
    excl_list.append(pd.read_excel(file))
    
 
# concatenate all DataFrames in the list
# into a single DataFrame, returns new
# DataFrame.
excl_merged = pd.concat(excl_list, ignore_index=True)
 
# exports the dataframe into excel file
# with specified name.
excl_merged.to_excel('Results_Final.xlsx', index=False)