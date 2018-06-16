import numpy as np
import networkx as nx
import collections
from lib import *
import csv
from matplotlib import pyplot as plt

# Load data
data = np.loadtxt("cycledistribution_sevaseviene.dat")
k = data[0]
nk_undirected = data[1]
nk_directed = data[2]


# Plot 
fig, ax = plt.subplots(figsize=(3*1.61, 3))
ax.set_xlabel("k")
ax.set_ylabel("F(k)")

ax.semilogy(k, nk_directed.astype(float)/nk_undirected, "o")

fig.tight_layout()

plt.show()



