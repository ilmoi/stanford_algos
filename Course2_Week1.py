from collections import deque

# ==============================================================================
# Old style data structures, same as in Course 1

Medium_G = {
    0:[1,5],
    1:[0,5,2],
    2:[1,4,3],
    3:[2,4],
    4:[5,2,3],
    5:[0,1,4]
}

SELECTOR = Medium_G
edges = {}
SELECTOR_i = 0 #IMPORTANT!!!!!! CHANGE THIS TO 1 WHEN RUNNING REAL_G
i = SELECTOR_i
for key, value in list(SELECTOR.items()):
    for v in value:
        edge = sorted([key, v])
        if edge not in list(edges.values()):
            edges[i] = edge
            i+=1

nodes = {}
for n in range(SELECTOR_i, len(SELECTOR)+SELECTOR_i):
    nodes[n] = []
    for key, value in list(edges.items()):
        if n in value:
            nodes[n].append(key)

edges[8] = [6,7]
nodes[6] = [8]
nodes[7] = [8]

# print(edges)
# print(nodes)


# ==============================================================================
# BFS

def BFS(nodes, edges, s):
    """Breadth-first search.
    Implemented as per lecture slides. See algo1slides / Part 10."""

    nodes_status = [False for _ in range(len(nodes))]
    distances = [None for _ in range(len(nodes))]
    # print(nodes_status)
    # s = 0
    Q = deque()
    Q.append(s)
    nodes_status[s] = True
    distances[s] = 0

    count_nodes = 0
    count_edges = 0

    while len(Q) > 0:
        v = Q.popleft()
        count_nodes += 1
        # print(f">> NODE is {v}")
        for e in nodes[v]:
            count_edges += 1
            edge = edges[e]
            id_v = edge.index(v)
            id_w = 1-id_v
            w = edge[id_w]
            # print(f"following edge {e} from {v} led to {w}")
            if nodes_status[w] != True:
                # print(f'adding {w}...')
                Q.append(w)
                nodes_status[w] = True
                distances[w] = distances[v]+1
            # else:
                # print(f'{w} already explored')
    # print(nodes_status)
    # print(distances)
    # print(f"explored {count_nodes} nodes and {count_edges} edges")
    return nodes_status

# BFS(nodes, edges, 0)

def connected_components(nodes, edges):
    nodes_component = [None for _ in range(len(nodes))]
    for i in range(len(nodes_component)):
        if not nodes_component[i]:
            found = BFS(nodes, edges, i)
            print(found)
            for f in range(len(found)):
                if found[f]:
                    nodes_component[f] = i+1
            print(f"nodes_component is {nodes_component}")
    return nodes_component

# connected_components(nodes, edges)


# ==============================================================================
# DFS

def DFS(nodes, edges, s):
    """Depth-first search.
    Implemented as per lecture slides. See algo1slides / Part 10."""

    count_nodes = 0
    count_edges = 0
    Q = deque()
    nodes_status = [False for _ in range(len(nodes))]

    def helper_dfs(nodes, edges, s):
        nonlocal count_nodes
        nonlocal count_edges
        nonlocal Q
        nonlocal nodes_status
        print(Q)
        Q.append(s)
        nodes_status[s] = True
        count_nodes += 1
        # print(f">> NODE is {s}")
        for e in nodes[s]:
            count_edges += 1
            edge = edges[e]
            id_s = edge.index(s)
            id_v = 1-id_s
            v = edge[id_v]
            # print(f"following edge {e} from {s} led to {v}")
            if nodes_status[v] != True:
                print(f'adding {v}...')
                helper_dfs(nodes, edges, v) #this puts v onto stack
                Q.pop() #this takes v off the stack
            # else:
                # print(f'{v} already explored')
        print(Q)
        return nodes_status
    return helper_dfs(nodes, edges, s)


# print(DFS(nodes, edges, 0))


# ==============================================================================
# ==============================================================================
# NEW STYLE DATA STRUCTURES - SAME AS IN PROGRAMMING ASSIGNMENT FOR C2W1
# 1 1
# 1 2
# 1 5
# 1 6
# 1 7
# 1 3
# 1 8
# 1 4
# 2 47646
# 2 47647
# where each row represents a unidirectional link

my_G = [
    [0,1],
    [1,2],
    [2,3],
    [0,5],
    [5,1],
    [5,4],
    [4,2],
    [4,3],
    [6,7],
    [7,6]
]

# ------------------------------------------------------------------------------
# lecture G

lecture_G = [
    [7,1],
    [4,7],
    [1,4],
    [9,7],
    [6,9],
    [3,6],
    [9,3],
    [8,6],
    [2,8],
    [5,2],
    [8,5]
]

def get_nodes(edges):
    # this implementation assumes that all nodes are mentioend at least once
    # first_nodes = [e[0] for e in edges]
    # second_nodes = [e[1] for e in edges]
    # first_nodes.extend(second_nodes)
    # nodes = list(set(first_nodes))

    # this implementation simply counts up to the largest node
    max_node = 0
    for e in edges:
        if e[0] > max_node:
            max_node = e[0]
        if e[1] > max_node:
            max_node = e[1]
    nodes = list(range(max_node+1))
    return nodes


def reverse_edges(edges):
    m = len(edges)  # O1
    for e in range(m):  # Om
        edges[e][0], edges[e][1] = edges[e][1], edges[e][0]
    return edges


# KEEP THIS HERE
for e in range(len(lecture_G)):
    for i in range(2):
        lecture_G[e][i] -= 1


def make_adj_nodes(edges):
    nodes = get_nodes(edges)
    # print(f"nodes are {nodes}")
    gr = [[] for _ in range(len(nodes))]
    for edge in edges:
        gr[int(edge[0])] += [int(edge[1])]
        # gr[int(edge[1])] += [int(edge[0])] #CANT USE THIS LINE!!! EDGES ARE ONE WAY!
    # print(gr)
    return gr


# lecture_gr = make_adj_nodes(lecture_G)
# print(lecture_gr)

# ------------------------------------------------------------------------------
# big G

# my loader
# has terrible loading time so I'm going to comment out
# with open('SCC.txt') as f:
#     Big_G = []
#     for l in f.readlines():
#         edge = l.strip('\n').strip().split(' ')
#         for e in range(len(edge)):
#           edge[e] = int(edge[e])-1 #NOTE the -1!!!! TO ALIGN COEFS!
#         Big_G.append(edge)
# # print(Big_G[:100])
# print('BIG LOADED')

# their loader
# num_nodes = 875715
# gr = [[] for i in range(num_nodes)]
# file = open('SCC.txt', 'r')
# data = file.readlines()
# for line in data:
#     items = line.split()
#     gr[int(items[0])] += [int(items[1])]
#     gr[int(items[1])] += [int(items[0])]
# print(gr)


# ==============================================================================
# DFS
def their_DFS(edges, s):
    # Q = deque()
    explored = set([])  # set has constant X in S operation

    def helper_dfs(edges, s):
        # nonlocal Q
        nonlocal explored
        # Q.append(s) # 0
        explored.add(s)  # O1, same as dict

        print(f">> NODE is {s}")
        for e in my_G:  # O(m)
            if e[0] == s:  # O1
                v = e[1]  # O1
                print(f"following edge {e} from {s} to {v}")
                if v not in explored:  # O1 since set
                    print(f'adding {v}...')
                    helper_dfs(edges, v)  # O n... hm so right now it's O n*m?
                else:
                    print(f'{v} already explored')
        # Q.pop()  # this removes v from stack
        # print(Q)  # empty
        return explored
    return helper_dfs(edges, s)

# NOTE 1 - won't work on their graph coz it's disconnected
# NOTE 2 - need to start their graphs off at 1, not 0
# print(their_DFS(Big_G, 1))

# ==============================================================================
# topological DFS
def topological_DFS(edges, s):
    """Computes topological ordering.
    Topological ordering is when eg you have a bunch of classes one pre-req for another
    and you need to decide on an order that satisfies all pre-req and lets you take the desired classes.
    Implemented as per lecture slides, see algo1slides / Part 10.
    """

    # all of the below just to get labels setup
    first_nodes = [e[0] for e in edges]
    second_nodes = [e[1] for e in edges]
    first_nodes.extend(second_nodes)
    vertices = list(set(first_nodes))
    labels = [None for _ in range(len(vertices))]
    current_label = vertices[-1]
    print(f"vertices are {vertices}")
    print(f"labels are {labels}")

    # Q = deque()
    explored = set([])  # set has constant X in S operation

    def helper_dfs(edges, s):
        # nonlocal Q
        nonlocal explored
        nonlocal labels
        nonlocal current_label
        # Q.append(s) # 0
        explored.add(s)  # O1, same as dict

        # print(f">> NODE is {s}")
        for e in edges:  # O(m)
            if e[0] == s:  # O1
                v = e[1]  # O1
                # print(f"following edge {e} from {s} to {v}")
                if v not in explored:  # O1 since set
                    # print(f'adding {v}...')
                    helper_dfs(edges, v)  # O n... hm so right now it's O n*m?
                # else:
                #     print(f'{v} already explored')
        labels[s] = current_label
        current_label -= 1
        # Q.pop()  # this removes v from stack
        # print(Q)  # empty
        return labels
    labels = helper_dfs(edges, s)
    print(f"resulting labels are {labels}")
    return labels

# print(topological_DFS(my_G, 0))

# ==============================================================================
# Kosaraju
def kosaraju(edges):
    """Kosaraju computes strongly connected components (SCCs) on a graph.
    An SCC is one where you can get from any node to any other node.
    Smallest case is just a single node (trivial example).
    Implemented as per lecture slides. See algo1slides / Part 10."""

    # I had to redefine DFS inside here because:
    # 1)nonlocal variables that can't be accessed using an externally-defined DFS
    # 2)this one is a little different to previous ones
    def better_interanl_DFS(adj_nodes, s):
        # print(f'better_internal_DFS called... with s {s}')
        # print(f'adj_nodes: {adj_nodes}')

        nonlocal explored
        nonlocal Ts
        nonlocal t
        nonlocal counter

        # initialize
        stack = deque()

        # deal with s node
        explored[s] = True
        if leaders[curr_leader]:
            leaders[curr_leader] +=1
        else:
            leaders[curr_leader] = 1
        actual_leaders[s] = curr_leader
        stack.append(s)

        # now the rest
        while len(stack) > 0:
            # assume this node is done, unless overturned in second IF below
            v = stack.pop()
            Ts[v] = t
            t += 1
            try:
                neighbors = adj_nodes[v]
                # print(f">> NODE is {v}, its neighbors are {neighbors}")
            except IndexError:
                # this is need for implementations where some nodes have NO edges (ie no neighbors!)
                # print(f'oops looks like {v} has no neighbors!')
                continue

            for n in neighbors:  # O(m)
                if not explored[n]:
                    # print(f'nice! {n} is OPEN. Switching over to {n}...')
                    counter += 1  # count number of explored nodes
                    print(f'counter is {counter}')

                    # nope, not done = ROLLBACK
                    stack.append(v)
                    Ts[v] = None
                    t -= 1

                    # instead use w as next v
                    stack.append(n)
                    explored[n] = True
                    if leaders[curr_leader]:
                        leaders[curr_leader] += 1
                    else:
                        leaders[curr_leader] = 1
                    actual_leaders[n] = curr_leader
                    break  # break out of inner loop
            #     else:
            #         print(
            #             f'{w} was already explored, continuing to look through edges...')
            # # else:
            #     print('OOOPS no edges found!
        # print(f'!!!!!!!state of leaders is {leaders}')

    # --------------------------------------------------------------------------
    # Pass 1
    # reverse arcs --> Grev
    Redges = reverse_edges(edges)
    m = len(Redges)
    print('REVERSE EDGES CREATED')

    # get node number
    R_adj_nodes = make_adj_nodes(Redges) #NOTE: this is the big change that allowed me to run kosaraju in linear time
    n = len(R_adj_nodes)
    print('NODES PREPARED')

    # initialize everything you need to
    Ts = [None for _ in range(n)]  # On
    explored = [None for _ in range(n)]  # On
    leaders = [0 for _ in range(n)]  # On
    actual_leaders = [None for _ in range(n)]  # On
    curr_leader = None
    t = 0
    counter = 0
    print('INIT DONE')

    # first loop on reverse G
    for node in range(n-1, -1, -1): #need -1 so that we go from n-1 to 0 #On
        if not explored[node]:
            curr_leader = node
            better_interanl_DFS(R_adj_nodes, node)
    # print('==' * 200)
    # print(f"Ts are {Ts}")
    preserve_Ts = Ts[:] #we need this later when calculating actual leaders
    print('FIRST LOOP DONE')

    # --------------------------------------------------------------------------
    # Pass 2
    # reverse arcs --> G
    edges = reverse_edges(Redges)

    # update edges with new labels
    # print(f"old edges are {edges}") #should be same ordering as ingested
    for e in range(m):  # O2m with beloe
        for i in range(2):  # coz each edge 2 numbers
            edges[e][i] = Ts[edges[e][i]]
    # print(f"new edges are {edges}") #should be new ordering as per Ts
    print('NEW EDGES DONE')

    adj_nodes = make_adj_nodes(edges)
    print('NEW NODES DONE')

    # reset important lists before second pass
    explored = [None for _ in range(n)]  # On
    leaders = [0 for _ in range(n)]  # On
    actual_leaders = [None for _ in range(n)]  # On
    counter = 0

    # 2nd iteration over nodes
    for node in range(n-1, -1, -1): #need -1 so that we go from n-1 to 0 #On
        if not explored[node]:
            # print(f"not explored yet {node}")
            curr_leader = node
            better_interanl_DFS(adj_nodes, node)
    # print(leaders) #should be final
    print('SECOND LOOP DONE')

    # --------------------------------------------------------------------------
    # Final part - returning "leaders"
    # the exercise asked what are the 5 largest connected components
    # the leaders array contains counts for each leader, to identify the largest
    leaders.sort(reverse=True)
    # print(f"adj nodes are {adj_nodes}")
    print(leaders[:5])

    # the actual_leaders array contains actual leader nodes for each node, indicating which SCC they belong to
    # (all nodes with the same leader = same SCC)
    # initially when actual_leaders are returned they are FOR THE NEW ORDERING, computed in first pass
    # so we first need to rever to original ordering
    correctly_ordered_actual_leaders = [None] * len(actual_leaders)
    for i, t in enumerate(preserve_Ts):
        correctly_ordered_actual_leaders[i] = actual_leaders[t]

    return correctly_ordered_actual_leaders


# kosaraju(Big_G)
# print(kosaraju(lecture_G))














# ==============================================================================
# NOTE THE BELOW WAS DONE TO HELP BUILD THE KOSARAJU. KOSARAJU ABOVE IS THE CROWN JEWEL OF THIS DOC.
# rethinking DFS without recursion
def better_BFS(edges, s):

    #initialize
    nodes = get_nodes(edges)
    explored = [False for _ in range(len(nodes))]
    Q = deque()

    # deal with s node
    explored[s] = True
    Q.append(s)

    # now the rest
    while len(Q) > 0:
        v = Q.popleft()  # O(1)
        print(f">> NODE is {v}")
        for e in edges:  # O(m)
            # note how here we need to allow edges BOTH ways (undirectional)
            w = None
            if e[0] == v:
                w = e[1]
            elif e[1] == v:
                w = e[0]
            if w:
                print(f"following edge {e} from {v} to {w}")
                if not explored[w]:  # get item O(1)
                    print(f'adding {w}...')
                    explored[w] = True
                    Q.append(w)
                else:
                    print(f'{w} already explored')
    return explored

# print(better_BFS(my_G, 0))


def better_DFS(edges, s):

    #initialize
    nodes = get_nodes(edges)
    adj_nodes = [[] for i in range(len(nodes))]
    explored = [False for _ in range(len(nodes))]
    stack = deque()

    # deal with s node
    explored[s] = True
    stack.append(s)

    # now the rest
    while len(stack) > 0:
        v = stack.pop()  # pick the last item
        print(f">> NODE is {v}")
        for e in edges:  # O(m)
            if e[0] == v and e[1] not in adj_nodes[v]:
                adj_nodes[v].append(e[1])  # visiting that edge
                w = e[1]  # select new v
                print(f"following edge {e} from {v} to {w}")

                if not explored[w]:  # get item O(1)
                    print(f'switching over to {w}...')
                    stack.append(v)
                    stack.append(w)
                    explored[w] = True
                    break  # break out of inner loop, we don't want more edges
                else:
                    print(f'{w} was already explored, continuing to look through edges...')
        else:
            print('OOOPS no edges found!')

    return explored

# print(better_DFS(lecture_G, 0))

# ==============================================================================
# making DFS run in O(n) time (yes, finally)


def faster_DFS(adj_nodes, s):

    #initialize
    explored = [False for _ in range(len(adj_nodes))]
    stack = deque()

    # deal with s node
    explored[s] = True
    stack.append(s)

    # now the rest
    while len(stack) > 0:
        v = stack.pop()  # pick the last item
        neighbors = adj_nodes[v]
        print(f">> NODE is {v}, its neighbors are {neighbors}")
        for n in neighbors:  # O(m)
            if not explored[n]:
                # adj_nodes[v].append(e[1])  # visiting that edge
                # w = e[1]  # select new v
                # print(f"following edge {e} from {v} to {w}")
                #
                # if not explored[w]:  # get item O(1)
                print(f'nice! {n} is OPEN. Switching over to {n}...')
                stack.append(v)
                stack.append(n)
                explored[n] = True
                break  # break out of inner loop, we don't want more edges
            else:
                print(f'{n} was already explored, continuing to look through edges...')
        else:
            print('OOOPS no edges found!')

    return explored


# print(faster_DFS(lecture_gr, 0))


"""
BIG TAKEAWAY:
THE THING THAT ACTUALLY ALLOWED ME TO MAKE DFS RUN IN LINEAR TIME WAS INGESTING NODES RATHER THAN EDGES
LOOK AT make_adj_nodes FUNCTION. THAT'S HOW I MADE IT WORK.
"""