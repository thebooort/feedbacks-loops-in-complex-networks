# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 13:34:41 2018

@author: booort, ruhugu
"""

from networkx import Graph, DiGraph, simple_cycles, find_cycle, cycle_basis
import csv


# Read CSV file

def csv2dict(filename, delimiter=";"):
    """Reads a 2-column csv file into a dict.

    The value in the first column is used as dictionary key. The value 
    of the dict entry is a list with the value of the second column.
    If several rows have the value in the first column, their 
    second column values are stored in the same list.

    Parameters
    ----------
        filename : str
            Name of the file to be read.

        delimiter : str
            Delimiter used in the csv file.

    """
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)

        dictionary = {}

        for entry in reader:
            key = entry[0]
            value = entry[1]

            # If the key is already in the dict, append the value
            # to the list
            if key in dictionary:
                dictionary[key].append(value)
            # In other case, create a new dict entry
            else:
                dictionary[key] = [value, ]

    return dictionary

"""
OJITO definitiva contiene un sample mucho mas grande de una red de twitter
mi ordenador no tira no con ella, por eso está comentada

"""

# Get the information from both files
dictionary1 = csv2dict("sevaseviene2network.csv", delimiter=";")
#dictionary2 = csv2dict("Definitiva.csv", delimiter=";")

# These function transform the dictionary to a directed graph networkx-style

DG1 = DiGraph(dictionary1)
#DG2 = DiGraph(dictionary2)

# These function transform the dictionary to an undirected graph networkx-style

undirected1=Graph(DG1)
#undirected2=Graph(DG2)

# These functions counts all the feedback cycles in our graph

feedback_cycle_list_DG1=(list(simple_cycles(DG1)))
#cycle_list_DG2=(list(simple_cycles(DG2)))

# Finally this part should gets all loops via networkx function

cycle_list_DG1=(list(cycle_basis(undirected1)))
#cycle_list_DG2=(list(simple_cycles(DG2)))

print(len(feedback_cycle_list_DG1))
print(len(cycle_list_DG1))


feedback_number=[0,0,0,0,0,0,0,0,0,0] # feedback_number[i]=number of cycle with i+1 longitude

#counting feedback numbers 
for i in range(0,len(feedback_cycle_list_DG1)):
    if len(list(feedback_cycle_list_DG1[i]))==1:
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





