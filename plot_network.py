from matplotlib import pyplot as plt
from networkx import Graph, DiGraph, simple_cycles, find_cycle, cycle_basis
import networkx as nx
from collections import defaultdict
from lib import *
import csv

# Load data
# ========================================
# Get the information from both files
dictionary1 = csv2dict("sevaseviene2network.csv", delimiter=";")
#dictionary2 = csv2dict("Definitiva.csv", delimiter=";")

# These function transform the dictionary to a directed graph networkx-style
DG1 = DiGraph(dictionary1)

# Remove nodes with out degree 0
remove = [node for node in DG1.nodes if DG1.out_degree(node) == 0]
DG1.remove_nodes_from(remove)

nx.draw_random(DG1, node_size=100)

plt.savefig("trabajo/network_sevaseviene.png")
