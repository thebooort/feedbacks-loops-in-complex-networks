#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 13:52:00 2018

@author: from stackexhange
"""
from networkx import Graph, DiGraph, simple_cycles, find_cycle

#here it will be our dictionary
dictionary_we_have_created=dictionary
"""
#first function counts feedback loops

def dfs(graph, start, end):
    fringe = [(start, [])]
    while fringe:
        state, path = fringe.pop()
        if path and state == end:
            yield path
            continue
        for next_state in graph[state]:
            if next_state in path:
                continue
            fringe.append((next_state, path+[next_state]))


cycles = [[node]+path  for node in dictionary_we_have_created for path in dfs(dictionary_we_have_created, node, node)]
print(len(cycles)) #feedback loops
"""
# this one counts all loops

DG = DiGraph(dictionary_we_have_created)
print(len(list(simple_cycles(DG))))


try:
    find_cycle(DG, orientation='original')
except:
    pass



print(list(find_cycle(DG, orientation='ignore')))










