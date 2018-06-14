# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 13:34:41 2018

@author: booort, ruhugu
"""

from networkx import Graph, DiGraph, simple_cycles, find_cycle, cycle_basis
import networkx as nx
from collections import defaultdict
import csv

# Define functions
# ========================================
""" This functions has been modified from the function simple_cycles
    in networkx package, which is distributed under a BSD license.
        networkx github page: https://github.com/networkx/

"""
def simple_cycles_undirected(G, maxlength=float('inf')):
    # TODO: Update docs!
    """Find simple cycles (elementary circuits) of a undirected graph.

    A `simple cycle`, or `elementary circuit`, is a closed path where
    no node appears twice. Two elementary circuits are distinct if they
    are not cyclic permutations of each other.

    This is a nonrecursive, iterator/generator version of Johnson's
    algorithm [1]_.  There may be better algorithms for some cases [2]_ [3]_.

    Parameters
    ----------
    G : NetworkX Graph
       A undirected graph

    maxlength : int
       Maximum length of the cycle.

    Returns
    -------
    cycle_generator: generator
       A generator that produces elementary cycles of the graph.
       Each cycle is represented by a list of nodes along the cycle.

    Examples
    --------
    >>> edges = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2)]
    >>> G = nx.DiGraph(edges)
    >>> len(list(nx.simple_cycles(G)))
    5

    To filter the cycles so that they don't include certain nodes or edges,
    copy your graph and eliminate those nodes or edges before calling

    >>> copyG = G.copy()
    >>> copyG.remove_nodes_from([1])
    >>> copyG.remove_edges_from([(0, 1)])
    >>> len(list(nx.simple_cycles(copyG)))
    3


    Notes
    -----
    The implementation follows pp. 79-80 in [1]_.

    The time complexity is $O((n+e)(c+1))$ for $n$ nodes, $e$ edges and $c$
    elementary circuits.

    References
    ----------
    .. [1] Finding all the elementary circuits of a directed graph.
       D. B. Johnson, SIAM Journal on Computing 4, no. 1, 77-84, 1975.
       https://doi.org/10.1137/0204007
    .. [2] Enumerating the cycles of a digraph: a new preprocessing strategy.
       G. Loizou and P. Thanish, Information Sciences, v. 27, 163-182, 1982.
    .. [3] A search strategy for the elementary cycles of a directed graph.
       J.L. Szwarcfiter and P.E. Lauer, BIT NUMERICAL MATHEMATICS,
       v. 16, no. 2, 192-204, 1976.

    See Also
    --------
    cycle_basis
    """
    def _unblock(thisnode, blocked, B):
        stack = set([thisnode])
        while stack:
            node = stack.pop()
            if node in blocked:
                blocked.remove(node)
                stack.update(B[node])
                B[node].clear()

    # Johnson's algorithm requires some ordering of the nodes.
    # We assign the arbitrary ordering given by the strongly connected comps
    # There is no need to track the ordering as each node removed as processed.
    # Also we save the actual graph so we can mutate it. We only take the
    # edges because we do not want to copy edge and node attributes here.
    # Create a symemtric directed graph from the given undirected one
    subG = type(G.to_directed())(G.edges())
    sccs = list(nx.strongly_connected_components(subG))
    while sccs:
        scc = sccs.pop()
        # order of scc determines ordering of nodes
        startnode = scc.pop()
        # Processing node runs "circuit" routine from recursive version
        path = [startnode]
        blocked = set()  # vertex: blocked from search?
        closed = set()   # nodes involved in a cycle
        blocked.add(startnode)
        B = defaultdict(set)  # graph portions that yield no elementary circuit
        stack = [(startnode, list(subG[startnode]))]  # subG gives comp nbrs
        while stack:
            thisnode, nbrs = stack[-1]
            if nbrs and (len(path) <= maxlength):
                nextnode = nbrs.pop()
                if nextnode == startnode:
                    yield path[:]
                    closed.update(path)
#                        print "Found a cycle", path, closed
                elif nextnode not in blocked:
                    path.append(nextnode)
                    stack.append((nextnode, list(subG[nextnode])))
                    closed.discard(nextnode)
                    blocked.add(nextnode)
                    continue
            # done with nextnode... look for more neighbors
            if not nbrs or (len(path) > maxlength):  # no more nbrs
                if thisnode in closed:
                    _unblock(thisnode, blocked, B)
                else:
                    for nbr in subG[thisnode]:
                        if thisnode not in B[nbr]:
                            B[nbr].add(thisnode)
                stack.pop()
#                assert path[-1] == thisnode
                path.pop()
        # done processing this node
        subG.remove_node(startnode)
        H = subG.subgraph(scc)  # make smaller to avoid work in SCC routine
        sccs.extend(list(nx.strongly_connected_components(H)))


def savecycles(filename, cycles_iter):
    with open(filename, "w") as file_out:
        for cycle in cycles_iter:
            for node in cycle:
                file_out.write("{0},".format(node))
                        
            file_out.write("\n")

def loadcycles(filename):
    cycles = list()
    with open(filename, "r") as file_in:
        for line in file_in:
            cycles.append(line.strip(",\n").split(","))

    return cycles


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


