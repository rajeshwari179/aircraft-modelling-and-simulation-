# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 22:23:16 2022

@author: paubo
"""

import pandas as pd
import numpy as np


xls =  pd.ExcelFile('DragPolarResultsFull.xlsx')
df_main = pd.DataFrame()
for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet)
    df['Sweep'] = sheet
    df_main = df_main.append(df)
df_main['Sweep'] = df_main['Sweep'].str.replace(r'[^0-9]+', '')
df_main.to_excel("DragPolarResultsFull2.xlsx", index=False) 