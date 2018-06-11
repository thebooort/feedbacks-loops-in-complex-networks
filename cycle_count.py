#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 13:52:00 2018

@author: from stackexhange
"""
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

graph = { 1: [2, 3, 5], 2: [1], 3: [1], 4: [2], 5: [2] }
cycles = [[node]+path  for node in graph for path in dfs(graph, node, node)]
print(len(cycles)) #feedback loops

