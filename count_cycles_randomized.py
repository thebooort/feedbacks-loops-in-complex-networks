# Calculate the mean number of directed cycles for each order 
# in the randomized network

# -*- coding: utf-8 -*-

from networkx import Graph, DiGraph, simple_cycles, find_cycle, cycle_basis
import networkx as nx
import random 
from collections import defaultdict
from lib import *
import csv


# Parameters
# ========================================
n_randomizations = 1000
kmax = 10  # Maximum cycle order

# Load data
# ========================================
# Get the information from both files
dictionary1 = csv2dict("sevaseviene2network.csv", delimiter=";")

# These function transform the dictionary to a directed graph networkx-style
DG1 = DiGraph(dictionary1)

# Remove nodes with out degree 0
remove = [node for node in DG1.nodes if DG1.out_degree(node) <= 0]
DG1.remove_nodes_from(remove)

# Array to store the number of directed cycles found for each order 
# accumulated over randomizations
nksum_directed = np.zeros(kmax + 1, dtype=int)

for j_rand in range(n_randomizations):
    # Randomize the network
    edges = list(DG1.edges())
    for edge in edges:
        revert_edge = random.randint(0,1)
        if revert_edge:
            DG1.remove_edge(edge[0], edge[1])
            DG1.add_edge(edge[1], edge[0])

    # Find the cycles
    directed_cycles = list(nx.simple_cycles(DG1))

    # Store their distribution
    for cycle in directed_cycles:
        k = len(cycle)
        if k <= kmax:
            nksum_directed[k] += 1

# Calculate the mean number of cycles per order
nk_directed = nksum_directed.astype(float)/n_randomizations

# Save the results to file
data = np.vstack(
        (np.arange(kmax + 1, dtype=int), nk_directed))
np.savetxt("cycledistribution_rand_sevaseviene.dat", data, fmt="%6d")
