import numpy as np
import networkx as nx
import collections
from scipy import optimize as spo
from lib import *
import csv
from matplotlib import pyplot as plt

# Parameters
gamma_article = 0.967
kmax = 10  # Maximum cycle order
kmin_reg = 3
kmax_reg = 5
n_randomizations = 5

# Load data
data = np.loadtxt("cycledistribution_sevaseviene.dat")
ks = data[0]  # Ignore order 0 and order 1
nk_undirected = data[1]
nk_directed = data[2]

data_rand = np.loadtxt("cycledistribution_rand_sevaseviene.dat")
nk_directed_rand = data_rand[1]

# Recalculate cycle distribution
#undirected_cycles = loadcycles("sevaseviene_undirectedcycles.dat")
#directed_cycles = loadcycles("sevaseviene_directedcycles.dat")
#
#nk2_undirected = np.zeros(kmax + 1)
#nk2_directed = np.zeros(kmax + 1)
#for cycle in undirected_cycles:
#    k = len(cycle)
#    if k <= kmax:
#        nk2_undirected[k] += 1
#for cycle in directed_cycles:
#    k = len(cycle)
#    if k <= kmax:
#        nk2_directed[k] += 1


# Calculate experimental F(k)
F_exp = nk_directed.astype(float)/nk_undirected

# Calculate F(k) for randomized network
F_rand = nk_directed_rand.astype(float)/nk_undirected

# Find least squares estimation for gamma
obj_fun = lambda gamma, ks: (
        F_exact(ks[kmin_reg:kmax_reg], gamma) - F_exp[kmin_reg:kmax_reg])
sol = spo.least_squares(obj_fun, 0.9, bounds=(0, 1), args=(ks,))
gamma_ls = sol.x
print("Least squares estimation for gamma is {0}".format(gamma_ls))


# Plot 
fig, ax = plt.subplots(figsize=(3.5*1.61, 3.5))
ax.set_xlabel("k")
ax.set_ylabel("F(k)")
ax.set_xlim((2, kmax))

ax.semilogy(ks, F_exp, "o", label="Data")
ax.semilogy(ks, F_rand, "s", label="Randomization")

ax.semilogy(
        ks, F_exact(ks, gamma_ls), "+", label=r"$F(k, \gamma_{\mathrm{LS}})$")
ax.semilogy(
        ks, F(ks, gamma_ls), label=r"$F_{\mathrm{asym}}(k, \gamma_{\mathrm{LS}})$")

ax.semilogy(
        ks, F_exact(ks, gamma_article), "x",
        label=r"$F(k, \gamma_{\mathrm{article}})$")
ax.semilogy(
        ks, F(ks, gamma_article),
        label=r"$F_{\mathrm{asym}}(k, \gamma_{\mathrm{article}})$")

ax.legend()
fig.tight_layout()

fig.savefig("trabajo/F_sevaseviene.png")



