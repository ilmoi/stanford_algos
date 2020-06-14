import json
import random
import math
from copy import deepcopy
import timeit


# ==============================================================================
# Linear time selection


def randomized_selection(A, l, r, i):
    """Solves the problem of selection = output ith order statistics.
    Implemented as per lecture slides. See algo1slides / Part 8."""
    if r - l == 1:
        return A[0]

    # print(f'OLD state of A is {A}, OLD iter is {A[l:r]}')
    j = partition(A, l, r)
    # print(f'NEW state of A is {A}, NEW iter is {A[l:r]}, just tried j {j}')

    if j == i:
        return A[j]
    elif j > i:
        return randomized_selection(A, l, j, i)
    else:
        return randomized_selection(A, j + 1, r, i)


# random.seed(1)
# A = list(range(10))
# random.shuffle(A)
# print(A)
# print(randomized_selection(A, 0, len(A), 5))


# ==============================================================================
# 9 - graphs

# =============================================
# 9.1 data structs to work with

Simple_G = {
     0: [1, 2],
     1: [0, 2, 3],
     2: [0, 1, 3],
     3: [1, 2]
     }

Medium_G = {
    0:[1,5],
    1:[0,5,2],
    2:[1,4,3],
    3:[2,4],
    4:[5,2,3],
    5:[0,1,4]
}

Real_G = {}
with open('mincut.txt') as f:
    txt = [x for x in f.readlines()]
    for line in txt:
        line_a = line.split('\t')
        label = int(line_a[0])
        adj = line_a[1:-1] #strip first label and last '\n'
        Real_G[label] = [int(a) for a in adj]

# =============================================
# 9.2 playing with data strucs

# 9.2.1
graph = {0: [1, 2],
         1: [0],
         2: [0]
         }

weights = {
    (0, 1): 50,
    (0, 2): 30,
    (1, 2): 15
}

# 9.2.2
class AdjNode:
    def __init__(self, value):
        self.v = value
        self.next = None

class Graph:
    def __init__(self, num):
        self.V = num  # how many vertices it has
        self.graph = [None] * self.V

    def add_edge(self, one, two):
        node = AdjNode(one)
        node.next = self.graph[two]
        self.graph[two] = node

        node = AdjNode(two)
        node.next = self.graph[one]
        self.graph[one] = node

    def print_graph(self):
        for i in range(self.V):
            print(f'Vertex {i}: ', end="")
            temp = self.graph[i]
            while temp:
                print(f' --> {temp.v}', end="")
                temp = temp.next
            print('\n')

# V = 5
# graph = Graph(V)
# graph.add_edge(0,1)
# graph.add_edge(0,2)
# graph.add_edge(0,3)
# graph.add_edge(1,2)
# graph.print_graph()
#
# medium_graph = Graph(len(G_medium))
# for key, value in list(G_medium.items()):
#     for v in value:
#         medium_graph.add_edge(key,v)
# medium_graph.print_graph()

# =============================================
# 9.3 first, non-efficient impl

def random_contraction(G):
    """Random contraction algo.
    Returns minimum cut.
    Implemented as per lecture slides. See algo1slides / Part 9."""

    while len(G) > 2:
        i = random.choice(list(G.keys()))  # actual item, not index
        j = G[i][random.randint(0, len(G[i]) - 1)]  # actual item, not index

        # pick one branch and expand it
        G[i].extend(G[j])  # append
        G[i] = [x for x in G[i] if x != i and x != j]  # prune

        # kill the other branch
        del G[j]

        # create a new key representation
        new_dig = str(i) + str(j) #need to convert to str otherwise leading 0 lost

        # insert new keys into branches
        for key, value in list(G.items()):
            for v in range(len(value)):
                if value[v] == j or value[v] == i:
                    G[key][v] = new_dig

        # insert new key into keys themselves
        G[str(i) + str(j)] = G[i]
        del G[i]
    return (G, len(G[list(G.keys())[0]]))

def run_the_fucker(G):
    """It's a whole shebang to make it working..."""

    print('running...')
    n = len(G)  # number of nodes
    N = round(n ** 2 * math.log(n))
    print(f"N is {N}")
    saved_G = deepcopy(G)  # have to use deepcopy since dict of lists
    returns = []

    for i in range(N):
        print(f'current run is {i}')
        G, len_G = random_contraction(G)
        returns.append((G, len_G))
        G = deepcopy(saved_G)

    min_ = min([x[1] for x in returns])
    print(f"minimum number of crossing edges is {min_}")

    valid_returns = filter(lambda x: x[1] == min_, returns)
    print(f"full list of valid returns is:")
    for x in list(valid_returns):
        print(x[0])
    print('done!')

# =============================================
# 9.4 better, but not good enough (also wrong)
iter=0
def efficient_random_contraction(G):

    zombies = set([])
    swaps = []

    while len(G) > 2:
        i = random.choice(list(G.keys()))  # actual item, not index
        j = G[i][random.randint(0, len(G[i]) - 1)]  # actual item, not index

        global iter
        iter+=1
        print(f'iteration is {iter}')
        # print(f"G is {G}")
        print(f"picked i= {i} and j= {j}, that is the edge {i}-{j}")

        # fix zombies - this is my way of getting around having to loop through entire dict
        while j in zombies:
            print(f'picked a zombie!!!! {j}')
            relevant_swap = [swap for swap in swaps if swap[1] == j][0]
            j = relevant_swap[0]
            print(f"updated j to {j}, so really the edge is {i}-{j}")

        # recognize self-loop
        if i == j:
            continue

        zombies.add(j)
        swaps.append((i,j))

        # pick one branch and expand it
        G[i].extend(G[j])  # append
        G[i] = [x for x in G[i] if x != i and x != j]  # prune

        # kill the other branch
        del G[j]

    print(len(G[list(G.keys())[0]]))
    return len(G[list(G.keys())[0]])

def efficiently_run_the_fucker(G):
    print('running...')
    n = len(G)  # number of nodes
    N = round(n ** 2 * math.log(n))
    print(f"N is {N}")
    saved_G = deepcopy(G)  # have to use deepcopy since dict of lists
    returns = []

    for i in range(N):
        if i % 100 == 0:
            print(f'current run is {i}')
        returns.append(efficient_random_contraction(G))
        G = deepcopy(saved_G)

    print(returns)
    print(min(returns))
    print('done!')


# efficiently_run_the_fucker(Medium_G)

# random.seed(1)
efficient_random_contraction(Real_G)



# =============================================
# 9.5 correct but not VERY SLOW. Ultimately I used this one to submit my final answer.

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

    for i in range(N):
        if i % 100 == 0:
            print(f'current run is {i}')
        # print(edges)
        # print(nodes)
        returns.append(super_efficient_contraction(edges, nodes))
        edges = deepcopy(save_edges)
        nodes = deepcopy(save_nodes)

    print(min(returns))
    print('done!')

# super_efficiently_run_the_fucker(edges, nodes)