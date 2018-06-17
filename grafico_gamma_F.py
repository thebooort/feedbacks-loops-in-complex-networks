#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 12:33:04 2018

@author: booort
"""
import numpy as np
import matplotlib.pyplot as plt
from math import exp, log
import matplotlib.path as mpath

#code for the creation of the  gama\F(k,gamma) graph

def F(k,gamma):
    """
    Equation that give the theoretical approximation of the fraction loops thata
    are feddback loops
    k= loop length
    gamma= parameter
    
    returns the result
    """
    return 2*exp(k/2*log(gamma*(1-gamma))+k/24*(log(gamma/(1-gamma)))**2)


fig = plt.figure()
i=2
prediction=[]
for gamma in range(1,10):
    prediction.append(F(i,gamma/10))
plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],prediction, '--r', marker="o", markersize=7,label="k=2")

i=3
prediction=[]
for gamma in range(1,10):
    prediction.append(F(i,gamma/10))
plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],prediction, '--b', marker="o", markersize=7,label="k=3")

i=4
prediction=[]
for gamma in range(1,10):
    prediction.append(F(i,gamma/10))
plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],prediction, '--g', marker="o", markersize=7,label="k=4")

i=5
prediction=[]
for gamma in range(1,10):
    prediction.append(F(i,gamma/10))
plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],prediction, '--y', marker="o", markersize=7,label="k=5")    
    
#plotting    

ax = fig.add_subplot(111)

ax.set_title('Grafica comparativa')

ax.set_xlabel(r'$\gamma$')
ax.set_ylabel(r'$F(k,\gamma$')
plt.legend()
plt.show()
