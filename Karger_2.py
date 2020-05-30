""" THIS PRODUCES THE CORRECT ANSWER BUT IS NOT EFFICIENT ENOUGH TO RUN FOR 200K.
WITH 1K RUNS IT WORKED AND PRODUCED 17.
"""

import math
from copy import deepcopy
import random

Real_G = {}
with open('mincut.txt') as f:
    txt = [x for x in f.readlines()]
    for line in txt:
        line_a = line.split('\t')
        label = int(line_a[0])
        adj = line_a[1:-1] #strip first label and last '\n'
        Real_G[label] = [int(a) for a in adj]

SELECTOR = Real_G
edges = {}
i = 1
for key, value in list(SELECTOR.items()):
    for v in value:
        edge = sorted([key, v])
        if edge not in list(edges.values()):
            edges[i] = edge
            i+=1

nodes = {}
for n in range(1, len(SELECTOR)+1): #IMPORTANT!!!!!! WHEN USING REAL_G NEED TO SET START +1 AND END +1, THIS IS BECAUSE THE FILE BEGINS WITH LINE 1 AND ENDS WITH 200 NOT 0 AND 199
    nodes[n] = []
    for key, value in list(edges.items()):
        if n in value:
            nodes[n].append(key)

def super_efficient_contraction(edges, nodes):
    while len(nodes) > 2:
        e_key, e_value = random.choice(list(edges.items()))
        first, second = e_value[0], e_value[1]
        # print(f'killing edge {e_key}, first is {first}, second is {second}')

        # clean up nodes
        nodes[first].remove(e_key)
        nodes[second].remove(e_key)

        # edges
        edges_to_clean = nodes[second]
        del edges[e_key]

        # nodes again
        nodes[first].extend(nodes[second])
        del nodes[second]

        # clean up edges - we need to replace old refs with new
        # print(f"edges to clear are {edges_to_clean}")
        if edges_to_clean:
            for e in edges_to_clean:
                # print(f'old edge is {edges[e]}')
                for i in range(len(edge)):
                    if edges[e][i] == second:
                        edges[e][i] = first
                # print(f'new edge is {edges[e]}')

                # now lets remove self referencing edges
                set_ = set(edges[e])
                if len(set_) == 1:

                    # print(f'yikes, this edge is a loop! ABOUT TO DELETE {edges[e]}')
                    del edges[e]

                    (s,) = set_
                    # print(f'but we also need to remove ref to edge {e} from node {nodes[s]}')
                    while e in nodes[s]:
                        nodes[s].remove(e)

    # print(f">>> resulting edges are {edges}")
    # print(f">>> resulting nodes are {nodes}")

    # I'll do the minimum amount of work to get the minimum cut
    v = list(nodes.values())[0] #only need one of them
    return len(v)

# random.seed(1)
# super_efficient_contraction(edges, nodes)

def super_efficiently_run_the_fucker(edges, nodes):
    print('running...')
    n = len(nodes)  # number of nodes
    N = round(n ** 2 * math.log(n))
    print(f"N is {N}")
    save_edges = deepcopy(edges)  # have to use deepcopy since dict of lists
    save_nodes = deepcopy(nodes)
    returns = []

    for i in range(1000):
        if i % 100 == 0:
            print(f'current run is {i}')
        # print(edges)
        # print(nodes)
        returns.append(super_efficient_contraction(edges, nodes))
        edges = deepcopy(save_edges)
        nodes = deepcopy(save_nodes)

    print(returns)
    print(min(returns))
    print('done!')

super_efficiently_run_the_fucker(edges, nodes)