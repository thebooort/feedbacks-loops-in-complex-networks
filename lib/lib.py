import csv
import networkx as nx
import numpy as np
from collections import defaultdict

# Define functions
# ========================================
""" These functions have been modified from the function simple_cycles
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

    Note: this functions counts loops of size bigger than 2 twice, one 
    for each direction.

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
    G_dir = G.to_directed()
    subG = type(G_dir)(G_dir.edges())
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
                if (nextnode == startnode) and (len(path)>2):
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

def F(k,gamma):
    """
    Equation that gives the theoretical approximation of the fraction loops thata
    are feedback loops
    k= loop length
    gamma= parameter
    
    returns the result
    """
    return 2*np.exp(k/2*np.log(gamma*(1-gamma))+k/24*(np.log(gamma/(1-gamma)))**2)


def cyclic_eulerian_novec(l, k):
    """Calculates the cyclic Eulerian number of order k for l ascents.

    """
    # Checks if the result have been memorized
    if (l, k) in cyclic_eulerian_novec.cache:
        result = cyclic_eulerian_novec.cache[(l, k)]
    # Else, calculate it
    else:
        if (l == 0) or (l >= k):
            result = 0
        else:
            result = (float(k*(k - l))/(k - 1)*cyclic_eulerian(l - 1, k - 1) 
                    + float(l*k)/(k - 1)*cyclic_eulerian(l, k - 1))
            
            # Store the result in the cache
            cyclic_eulerian_novec.cache[(l, k)] = result

    return result

cyclic_eulerian_novec.cache = {(0, 1) : 1}

cyclic_eulerian = np.vectorize(cyclic_eulerian_novec)

def F_exact_novec(k, gamma):
    """Calculates the exact value of the fraction of feedback loops.

    Note: this function is not vectorized.

    """
    suma = 0
    for l in range(int(k) + 1):
        suma += float(cyclic_eulerian(l, k))/np.math.factorial(k)*(
                np.power(gamma, l)*np.power(1 - gamma, k - l)
                + np.power(gamma, k - l)*np.power(1 - gamma, l))

    return suma

# Vectorize function
F_exact = np.vectorize(F_exact_novec)

      
