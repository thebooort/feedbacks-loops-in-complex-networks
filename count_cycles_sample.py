# Cuenta cuantos ciclos no dirigidos hay para cada orden y cuantos ciclos
# dirigidos que correspondan con los no dirigidos anteriores.
# Esto es útil cuando sólo tenemos una muestra del conjunto total de 
# ciclos.

import numpy as np
import networkx as nx
import collections
from lib import *


# Parameters
# ========================================
max_order = 10


# Function definitions
# ========================================
def rotate(l, shift):
    return l[shift:] + l[:shift]

# Load data
undirected_cycles = loadcycles("sevaseviene_undirectedcycles.dat")
directed_cycles = loadcycles("sevaseviene_directedcycles.dat")

# 
n_undirected = len(undirected_cycles)

# Array to store the number of undirected cycles found of each order
nk_undirected = np.zeros(max_order + 1, dtype=int)
nk_directed = np.zeros(max_order + 1, dtype=int)

# For each undirected cycle find the corresponding directed cycle
for j_cycle, undirected_cycle in enumerate(undirected_cycles):
    print("{0}/{1}".format(j_cycle, n_undirected))
    cycle_order = len(undirected_cycle)
    nk_undirected[cycle_order] += 1
    found = False
    for directed_cycle in directed_cycles:
        # Check if it is a candidate
        candidate = (
                (len(directed_cycle) == len(undirected_cycle)) and
                (collections.Counter(directed_cycle) 
                        == collections.Counter(undirected_cycle)))

        if not candidate:
            continue

        for shift in range(cycle_order):
            found = (undirected_cycle == rotate(directed_cycle, shift))
            if found:
                nk_directed[cycle_order] += 1
                break

        if found:
            break
        
# Save data to file
data = np.vstack(
        (np.arange(max_order + 1, dtype=int), nk_undirected, nk_directed))

np.savetxt("cycledistribution_sevaseviene.dat", data, fmt="%6d")

            

