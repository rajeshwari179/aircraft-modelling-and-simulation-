# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 18:06:24 2022

@author: paubo
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
df = pd.read_excel('DragPolarResults2.xlsx', sheet_name = None) # read all sheets


Altitudes = [0,4000,6000,10000,14000,18000]
Mach = [0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5,1.7,1.9]
AoA = 4
sweep = list(range(1,66,3))

num_Mach = len(Mach)
num_Altitude = len(Altitudes)


for Alt in Altitudes:
    CL = []
    CD = []
    LD = []
    for key in df.keys():
        CL.append(df[key].loc[(df[key]['Altitude'] == Alt) &(df[key]['AoA'] == AoA)]['CL'])
        CD.append(df[key].loc[(df[key]['Altitude'] == Alt) &(df[key]['AoA'] == AoA)]['CD'])
        LD.append(df[key].loc[(df[key]['Altitude'] == Alt) &(df[key]['AoA'] == AoA)]['L/D'])
    CL = np.array(CL)
    CL = CL.flatten()
    CD = np.array(CD)
    CD = CD.flatten()
    LD = np.array(LD)
    LD = LD.flatten()    
    for i in range(0,num_Mach):
        plt.plot(sweep,CL[i::num_Mach], label="Mach = "+ str(Mach[i]))
        plt.xlabel("Sweep [deg]")
        plt.ylabel("CL [-]")
    plt.title("CL vs Sweep at Altitude = " + str(Alt) + " m" +  " and AoA = " + str(AoA) + " deg")
    plt.legend()
    plt.savefig("CL vs Sweep at Altitude = " + str(Alt) + " m" +  " and AoA = " + str(AoA) + " deg.png", bbox_inches = "tight")
    plt.show()
    for i in range(0,num_Mach):
        plt.plot(sweep,CD[i::num_Mach], label="Mach = "+ str(Mach[i]))
        plt.xlabel("Sweep [deg]")
        plt.ylabel("CD [-]")
    plt.title("CD vs Sweep at Altitude = " + str(Alt) + " m" + " and AoA = " + str(AoA) + " deg")
    plt.legend()
    plt.savefig("CD vs Sweep at Altitude = " + str(Alt) + " m" + " and AoA = " + str(AoA) + " deg.png", bbox_inches = "tight")
    plt.show()
    for i in range(0,num_Mach):
        plt.plot(sweep,LD[i::num_Mach], label="Mach = "+ str(Mach[i]))
        plt.xlabel("Sweep [deg]")
        plt.ylabel("LD [-]")
    plt.title("LD vs Sweep at Altitude = " + str(Alt) + " m" + " and AoA = " + str(AoA) + " deg")
    plt.legend()
    plt.savefig("LD vs Sweep at Altitude = " + str(Alt) + " m" +  " and AoA = " + str(AoA) + " deg.png", bbox_inches = "tight")
    plt.show()    