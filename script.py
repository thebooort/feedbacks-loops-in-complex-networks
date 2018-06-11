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


def F(k,gamma):
    """
    Equation that give the theoretical approximation of the fraction loops thata
    are feddback loops
    k= loop length
    gamma= parameter
    
    returns the result
    """
    return 2*exp(k/2*log(gamma*(1-gamma))+k/24*(log(gamma/(1-gamma)))**2)

gamma= 0.967  #experimental result in twitter


prediction=[]

for i in range(2,10):
    prediction.append(F(i,gamma))
    
    
    
#plotting    

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel(r'$k$')
ax.set_ylabel(r'$F(k)$')
ax.set_yscale('log')
plt.plot([2,3,4,5,6,7,8,9],prediction, '--r', marker="o", markersize=7,label="Prediction")
plt.legend()
plt.show()