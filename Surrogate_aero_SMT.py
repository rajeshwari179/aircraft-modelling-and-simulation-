import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model 
import pandas as pd


# Set up inputs and outputs

db = pd.read_excel('DragPolarResults3.xlsx')  
cond1 = (db['Mach']>1.0)

Sweep = db.loc[cond1,'Sweep'].to_numpy().flatten()
AoA = db.loc[cond1,'AoA'].to_numpy().flatten()
Altitude = db.loc[cond1,'Altitude'].to_numpy().flatten()
Mach = db.loc[cond1,'Mach'].to_numpy().flatten()
CL = db.loc[cond1,'CL'].to_numpy().flatten()
CD = db.loc[cond1,'CD'].to_numpy().flatten()


# The training set

datapoints2 = np.array((Altitude,AoA,Mach,Sweep,CL,CD)).T
X = datapoints2[:,0:4]
Lift_coeff = datapoints2[:,-2]
Drag_coeff = datapoints2[:,-1]

# 4 degree polynomial features
deg_of_poly = 2
poly = PolynomialFeatures(degree=deg_of_poly)
X_ = poly.fit_transform(X)
# Fit linear model
clf = linear_model.LinearRegression()
clf.fit(X_, Lift_coeff)


print(clf.coef_[0],"+",clf.coef_[1],"*h","+",clf.coef_[2],"*alpha","+",clf.coef_[3],"*M","+",clf.coef_[4],"*sweep","+",clf.coef_[5],"*h**2","+",clf.coef_[6],"*h*alpha","+",clf.coef_[7],"*h*M","+",clf.coef_[8],"*h*sweep","+",clf.coef_[9],"*alpha**2","+",clf.coef_[10],"*alpha*M","+",clf.coef_[11],"*alpha*sweep","+",clf.coef_[12],"*M**2","+",clf.coef_[13],"*M*sweep","+",clf.coef_[14],"*sweep**2")

print("")

print(clf.coef_[1],"+",clf.coef_[5],"*h*2","+",clf.coef_[6],"*alpha","+",clf.coef_[7],"*M","+",clf.coef_[8],"*sweep")

print("")

print(clf.coef_[2],"+", clf.coef_[6],"*h","+",clf.coef_[9],"*alpha*2","+",clf.coef_[10],"*M","+",clf.coef_[11],"*sweep")

print("")

print(clf.coef_[3],"+",clf.coef_[7],"*h","+",clf.coef_[10],"*alpha","+",clf.coef_[12],"*M*2","+",clf.coef_[13],"*sweep")

print("")

print(clf.coef_[4],"+",clf.coef_[8],"*h","+",clf.coef_[11],"*alpha","+",clf.coef_[13],"*M","+",clf.coef_[14],"*sweep*2")

print("")
