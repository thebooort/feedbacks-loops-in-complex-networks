# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 13:34:41 2018

@author: booort, ruhugu
"""

from networkx import Graph, DiGraph, simple_cycles, find_cycle, cycle_basis
import networkx as nx
from collections import defaultdict
from lib import *
import csv

"""
OJITO definitiva contiene un sample mucho mas grande de una red de twitter
mi ordenador no tira no con ella, por eso esta comentada

"""

# Load data
# ========================================
# Get the information from both files
dictionary1 = csv2dict("sevaseviene2network.csv", delimiter=";")
#dictionary2 = csv2dict("Definitiva.csv", delimiter=";")

# These function transform the dictionary to a directed graph networkx-style
DG1 = DiGraph(dictionary1)
#DG2 = DiGraph(dictionary2)

# Remove nodes with out degree 0
remove = [node for node in DG1.nodes if DG1.out_degree(node) <= 0]
DG1.remove_nodes_from(remove)

# These function transform the dictionary to an undirected graph networkx-style
undirected1 = DG1.to_undirected()
#undirected2 = DG2.to_undirected()


# Count cycles
# ==============================
# These functions counts all the feedback cycles in our graph
feedback_cycle_list_DG1 = (list(simple_cycles(DG1)))
#cycle_list_DG2 = (list(simple_cycles(DG2)))


# Finally this part should gets all loops via networkx function
cycle_list_DG1 = simple_cycles_undirected(undirected1, maxlength=10)


# Save cycles to file
# ========================================
# Save directed cycles
savecycles("sevaseviene_directedcycles.dat", feedback_cycle_list_DG1)
# Save undirected cycles
savecycles("sevaseviene_undirectedcycles.dat", cycle_list_DG1)


# Play with the data
# ========================================
print(len(feedback_cycle_list_DG1))
#print(len(cycle_list_DG1))

# feedback_number[i]=number of cycle with i+1 longitude
feedback_number = [0,0,0,0,0,0,0,0,0,0] 

#counting feedback numbers 
for i in range(0,len(feedback_cycle_list_DG1)):
    if len(list(feedback_cycle_list_DG1[i])) == 1:
        feedback_number[0]+=1
    elif len(list(feedback_cycle_list_DG1[i]))==2:
        feedback_number[1]+=1
    elif len(list(feedback_cycle_list_DG1[i]))==3:
        feedback_number[2]+=1
    elif len(list(feedback_cycle_list_DG1[i]))==4:
        feedback_number[3]+=1
    elif len(list(feedback_cycle_list_DG1[i]))==5:
        feedback_number[4]+=1
    elif len(list(feedback_cycle_list_DG1[i]))==6:
        feedback_number[5]+=1
    elif len(list(feedback_cycle_list_DG1[i]))==7:
        feedback_number[6]+=1
print(feedback_number)


