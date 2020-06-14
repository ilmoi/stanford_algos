# Floyd-Warshall

# need too much memory - 1000 nodes = 1m combinations = 1bn loops
def floyd_warshall(edges):
    """As per lecture slides. Unfortunately needs too much memory to run on my laptop, so never got to check correctness."""

    # get length
    v = list(sorted(set([e[0] for e in edges] + [e[1] for e in edges])))
    n = len(v)

    # create adj list rep
    # NOTE - it's a directed graph, so only one way
    vv = [[] for _ in range(n)]
    costs = [[] for _ in range(n)]
    for e in edges:
        vv[e[0]].append(e[1])
        costs[e[0]].append(e[2])

    # make the array
    A = [[[None for _ in range(n)] for _ in range(n)] for _ in range(n)]

    # set the base case
    for i in range(n):
        for j in range(n):
            # if there is a direct edge FROM I TO J
            if j in vv[i]:
                index_j = vv[i].index(j)
                A[i][j][0] = costs[i][index_j]
            else:
                A[i][j][0] = float("inf")
        A[i][i][0] = 0
    print(A)

    # actual loop
    for k in range(1, n):
        print(k)
        for i in range(n):
            for j in range(n):
                # print(i,j,k)
                A[i][j][k] = min(A[i][j][k-1], A[i][k][k-1] + A[k][j][k-1])

    # return diagonal entries, and the minimum!
    diagonal = [A[i][i][n-1] for i in range(n)]
    print(f"the min diagonal is {min(diagonal)}")

    # return shortest shortest path
    shortest_shortest_path = float("inf")
    contenders = []
    for i in range(n):
        for j in range(n):
            if i != j:
                contenders.append(A[i][j][n-1])
    print(f"shortest shortest path is {min(contenders)}")


# ==============================================================================
# dijkstra with heap implementation

class MinBinHeap:
    """Modified version of MinBinHeap
    takes in tuples with (node_name, node_distance).
    It's needed for the below johnson's algo."""

    def __init__(self):
        self.heapList = [["na","na"]]
        self.currentSize = 0

    def percUp(self, i):
        while i//2 > 0: #while there are still kids
            if self.heapList[i][1] < self.heapList[i//2][1]: #if kid SMALLER than parent
                self.heapList[i], self.heapList[i//2] = self.heapList[i//2], self.heapList[i] #then swap
            i = i//2 #now look at kid's kid

    def insert(self, k):
        self.heapList.append(k)
        self.currentSize += 1
        self.percUp(self.currentSize)

    def percDown(self, i):
        while i*2 <= self.currentSize:
            mc = self.min_child(i)
            if self.heapList[i][1] > self.heapList[mc][1]: #if parent BIGGER than child
                self.heapList[i], self.heapList[mc] = self.heapList[mc], self.heapList[i]
            i = mc

    def min_child(self, i):
        if i*2+1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2][1] < self.heapList[i*2+1][1]:
                return i * 2
            else:
                return i * 2 + 1

    def del_min(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize -= 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def build_heap(self, alist):
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [["na","na"]] + alist[:]
        while i > 0:
            self.percDown(i)
            i -= 1

    def rebuild(self):
        # print(f"before rebuilding - {self.heapList}")
        self.build_heap(self.heapList[1:])
        # print(f"AFTER rebuilding - {self.heapList}")

def dijkstra(edges, s):
    """This is a modified dijkstra adaptation from Course2-Week2.
    It uses indexing starting with 0, not 1.
    I also removed "clean edges" functionality which was causing bugs.
    It's needed for the below johnson's algo."""

    # get length
    v = list(sorted(set([e[0] for e in edges] + [e[1] for e in edges])))
    n = len(v)

    # create adj list rep
    # NOTE - it's a directed graph, so only one way
    G = [[] for _ in range(n)]
    for e in edges:
        G[e[0]].append([e[1],e[2]])

    # create min hip backbone
    n = len(G)
    nodes = []
    for i in range(n):
        nodes.append([i, float("inf")])
    # fix the first node
    nodes[s][1] = 0
    # build the initial one
    mbh = MinBinHeap()
    mbh.build_heap(nodes)

    saved_distances = [None] * n

    while len(mbh.heapList) > 1:
        # pick a vertex
        extracted_tup = mbh.del_min()
        extracted_vertex = extracted_tup[0]
        extracted_distance = extracted_tup[1]
        saved_distances[extracted_vertex] = extracted_distance

        # update neighbors
        for vertex, distance in G[extracted_vertex]:
            for tup in mbh.heapList:
                if tup[0] == vertex:
                    if tup[1] > extracted_distance + distance:
                        tup[1] = extracted_distance + distance

        # rebuild the heap
        mbh.rebuild()
        # print(f"NEW heaplist is {mbh.heapList}")

    # print(f"dijkstra produces {saved_distances}")
    return saved_distances


# ==============================================================================
# bellman ford

def bellman_ford(edges, s):
    """Implementation of bellman ford shortest path algo.
    As per lecture slides. See algo2slides / Part 14.
    It's needed for the below johnson's algo."""

    # get length
    v = list(sorted(set([e[0] for e in edges] + [e[1] for e in edges])))
    n = len(v)

    # create adj list rep
    # NOTE - it's a directed graph, so only one way
    out = [[] for _ in range(n)]
    in_ = [[] for _ in range(n)]
    costs = [[] for _ in range(n)]
    in_costs = [[] for _ in range(n)]

    for e in edges:
        out[e[0]].append(e[1])
        costs[e[0]].append(e[2])
        in_[e[1]].append(e[0])
        in_costs[e[1]].append(e[2])

    # make the array
    A = [[None for _ in range(n)] for _ in range(n+1)]
    # inner array = all vs for a given i
    # outer array = all is

    # base case
    # whenever i == 0, the distance is infinity
    for i in range(n):
        A[0][i] = float("inf")
    # except i with itself, then distance is 0
    A[0][s] = 0
    # print(A)

    for i in range(1, n+1):
        # print(i)
        for v in range(n):
            # scan through all incoming edges for a given node
            incoming = []
            # print(v, in_[v])
            for incoming_v in in_[v]:
                incoming_v_weight = A[i-1][incoming_v] #A[i-1][w]
                # print(incoming_v_weight)
                incoming_v_index = in_[v].index(incoming_v)
                incoming_v_cost = in_costs[v][incoming_v_index] #Cwv
                incoming.append(incoming_v_weight + incoming_v_cost)
            if not incoming:
                incoming=[float("inf")]
            # print(f"competing: {A[i-1][v], min(incoming)}")
            A[i][v] = min(A[i-1][v], min(incoming))

    # check no cycles
    # print(A[-1] == A[-2])

    # answer
    print(f"BF produces {A[-1]}")
    return A[-1]







# ==============================================================================
# johnson's algo
def johnsons(edges):
    """Uses BF to adjust paths first, then runs
    n iterations of Dijkstra.
    Implementation as per lecture slides. See algo2slides / Part 15"""

    # form G' by adding new edges with length 0
    V = list(sorted(set([e[0] for e in edges] + [e[1] for e in edges])))
    n = len(V)
    temp_edges = edges[:]
    for v in V:
        temp_edges.append([n, v, 0])
    print(temp_edges)

    # run bellman ford from source vertex s
    shortest_BF = bellman_ford(temp_edges, 6)
    shortest_BF = shortest_BF[:-1]
    print(shortest_BF)

    # for each vertex v define Pv = length of shortest path s->v in G'
    # for each edge ce define ce' as ce + pu - pv
    out = [[] for _ in range(n)]
    costs = [[] for _ in range(n)]
    new_edges = []
    for e in edges:
        out[e[0]].append(e[1])
        from_ = e[0]
        to_ = e[1]
        from_p = shortest_BF[from_]
        to_p = shortest_BF[to_]
        new_cost = e[2]+from_p-to_p
        costs[e[0]].append(new_cost)
        new_edges.append([e[0],e[1],new_cost])
    print(costs)
    # print(new_edges)

    # for each vertex u run dijkstra with edge lengths ce' and compute shortest path to all d'
    A = [None for _ in range(n)]
    for u in range(n):
        print(u)
        A[u] = dijkstra(new_edges,u)
    print(A)

    # for each pair u v d(uv) = d'(uv) - pu + pv
    # AND find the shortest path while at it
    ssp = float("inf")
    for u in range(n):
        print(u)
        for v in range(n):
            A[u][v] = A[u][v] - shortest_BF[u] + shortest_BF[v]
            if A[u][v] < ssp:
                ssp = A[u][v]
    # print(A)
    print(ssp)


# ==============================================================================
# DATASETS AND RUNNING
# ALL INDEX ADJUSTMENTS DONE HERE - ALL DATA STARTS WITH 0

Test_edges = [[1,2,10],[2,3,100],[1,5,10],[1,4,20],[3,4,5]]
lecture_graph_JH = [[0,1,-2],[1,2,-1],[2,0,4],[2,3,2],[2,4,-3],[5,3,1],[5,4,-4]]
lecture_graph_BF = [[0,1,2],[0,2,4],[1,2,1],[1,3,2],[3,4,2],[2,4,4]]

# g1 has a negative cycle
# g2 has a negative cycle
# g3 does NOT.
with open('g3.txt') as f:
    edges = [j.strip('\n').split(' ') for j in f.readlines()[1:]]
    for i in range(len(edges)):
        for j in range(len(edges[i])):
            edges[i][j] = int(edges[i][j])
    edges = [[e[0] - 1, e[1] - 1, e[2]] for e in edges]
    # print(edges[:5])
    johnsons(edges)

# floyd_warshall(Test_edges)
# bellman_ford(lecture_graph_BF, 3)
# dijkstra(lecture_graph_BF, 3)
# johnsons(lecture_graph_JH)