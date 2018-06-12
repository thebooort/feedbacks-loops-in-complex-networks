#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 13:34:41 2018

@author: booort, ruhugu
"""
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


# Test the function
dictionary = csv2dict("sevaseviene2network.csv", delimiter=";")

for key in dictionary:
    print("{0}:".format(key))
    print(dictionary[key])
    print("===============================")


