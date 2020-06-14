# Minimizing sum of completion times
# remember completion times take into account all previous
# schedule in decreasing order of weight - length
# if equal difference schedule one with higher weight first

Test = [(1,1),(3,5),(5,3), (4,2), (8,6)]

def special_merge_sort(L, L2):
    """Adjusted for use from first course."""

    if len(L) <= 1:
        return L, L2
    else:
        n = len(L)
        mid = n // 2
        left, left2 = special_merge_sort(L[:mid], L2[:mid])
        right, right2 = special_merge_sort(L[mid:], L2[mid:])
        i, j = 0, 0
        for k in range(n):
            if left[i] > right[j]:
                L[k] = left[i]
                L2[k] = left2[i]
                i += 1
                if i == len(left):
                    L[k + 1:] = right[j:]
                    L2[k + 1:] = right2[j:]
                    return L, L2
            elif left[i] < right[j]:
                L[k] = right[j]
                L2[k] = right2[j]
                j += 1
                if j == len(right):
                    L[k + 1:] = left[i:]
                    L2[k + 1:] = left2[i:]
                    return L, L2
            else:
                if left2[i][0] >= right2[j][0]:
                    L[k] = left[i]
                    L2[k] = left2[i]
                    i += 1
                    if i == len(left):
                        L[k + 1:] = right[j:]
                        L2[k + 1:] = right2[j:]
                        return L, L2
                else:
                    L[k] = right[j]
                    L2[k] = right2[j]
                    j += 1
                    if j == len(right):
                        L[k + 1:] = left[i:]
                        L2[k + 1:] = left2[i:]
                        return L, L2


def min_completion(A):
    """Algo to solve the scheduling problem.
    Implemented as per lecture slides. See algo2slides / Part 4."""

    # calc differences, O(n)
    B = [None] * len(A)
    for i, tup in enumerate(A):
        diff = tup[0]/tup[1]
        B[i] = diff

    # sort, O(nlogn)
    print(B, A)
    B, A = special_merge_sort(B, A)
    print(B, A)

    total_c_time = 0
    total_times = []
    for i in range(len(A)):
        if i == 0:
            total_wait_time = A[i][1]
        else:
            total_wait_time = A[i][1] + total_times[i-1]
        total_times.append(total_wait_time)
        c_time = A[i][0] * total_wait_time
        total_c_time += c_time

    print(total_times)
    print(total_c_time)


# min_completion(Test)

with open('jobs.txt') as f:
    jobs = [j.strip('\n').split(' ') for j in f.readlines()[1:]]
    for i in range(len(jobs)):
        for j in range(len(jobs[i])):
            jobs[i][j] = int(jobs[i][j])

    # print(jobs)
    min_completion(jobs)


# ==============================================================================

with open('prims_edges.txt') as f:
    prims_edges = [j.strip('\n').split(' ') for j in f.readlines()[1:]]
    for i in range(len(prims_edges)):
        for j in range(len(prims_edges[i])):
            prims_edges[i][j] = int(prims_edges[i][j])

Test_edges = [[1,2,10],[2,3,100],[1,5,10],[1,4,20], [3,4,5]]

class MinBinHeap:
    """Modified version of MinBinHeap
    takes in tuples with (node1, node2, edge weight)"""
    def __init__(self):
        self.heapList = [[0,0,0]]
        self.currentSize = 0

    def percUp(self, i):
        while i//2 > 0: #while there are still kids
            if self.heapList[i][2] < self.heapList[i//2][2]: #if kid SMALLER than parent
                self.heapList[i], self.heapList[i//2] = self.heapList[i//2], self.heapList[i] #then swap
            i = i//2 #now look at kid's kid

    def insert(self, k):
        self.heapList.append(k)
        self.currentSize += 1
        self.percUp(self.currentSize)

    def percDown(self, i):
        while i*2 <= self.currentSize:
            mc = self.min_child(i)
            if self.heapList[i][2] > self.heapList[mc][2]: #if parent BIGGER than child
                self.heapList[i], self.heapList[mc] = self.heapList[mc], self.heapList[i]
            i = mc

    def min_child(self, i):
        if i*2+1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2][2] < self.heapList[i*2+1][2]:
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

    # new method:)
    def del_second_elem(self, elem):
        for i in range(1, len(self.heapList)):
            if self.heapList[i][1] == elem:
                self.heapList[i], self.heapList[-1] = self.heapList[-1], self.heapList[i]
                retval = self.heapList.pop()
                self.currentSize -= 1
                # just run both! one will be correct other do nothing
                self.percUp(i)
                self.percDown(i)
                return retval

    def build_heap(self, alist):
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [[0,0,0]] + alist[:]
        while i > 0:
            self.percDown(i)
            i -= 1

    def rebuild(self):
        # print(f"before rebuilding - {self.heapList}")
        self.build_heap(self.heapList[1:])
        # print(f"AFTER rebuilding - {self.heapList}")

# ABANDONED THE HEAP APPROACH - CBA REBUILDLING THE EDGES INTO NODES
# mbh = MinBinHeap()
# mbh.build_heap(Test_edges)
# print(mbh.heapList)
# mbh.del_second_elem(2)
# print(mbh.heapList)

# def heap_spanning_tree(edges):
#     # sorted set, nlogn
#     V = sorted(set([e[0] for e in edges] + [e[1] for e in edges]))
#     # print(V)
#     # build the adjacent list
#     VV = [[] for _ in range(len(V))]
#     for e in range(len(edges)):
#         first_elem, second_elem, weight = edges[e][0], edges[e][1], edges[e][2]
#         # print(first_elem, second_elem)
#         VV[first_elem-1].append((second_elem, weight))
#         VV[second_elem-1].append((first_elem, weight))
#     # print(VV)
#
#     X = [1]
#     T = [] #holds selected so far edge
#     mbh = MinBinHeap()
#     mbh.build_heap([e for e in edges if e[0] == 1])
#     print(mbh.heapList)
#
#     while X != V:
#         next_edge = mbh.del_min()
#         next_x = next_edge[1]
#         X.append(next_x)
#         T.append(next_edge)
#
#         last_added = X[-1]
#         his_neighbors = VV[last_added-1]
#         rebuilt_edges = [[last_added, n[0], n[1]] for n in his_neighbors]
#         for edge in rebuilt_edges:
#             mbh.insert(edge)
#
#
#
# heap_spanning_tree(Test_edges)

def naive_spanning_tree(edges):
    """Naive (not using heaps) implementation of min spanning trees algo.
    Like the name suggests finds a minimum spanning tree.
    Implemented as per lecture slides. See algo2slides / Part 5."""

    V = sorted(set([e[0] for e in edges] + [e[1] for e in edges]))
    X = [1]
    T = [] #holds selected so far edge
    while len(X) < len(V):
        current_min = float("inf")
        current_edge = None
        for edge in edges:
            if ((edge[0] in X and edge[1] not in X) or (edge[1] in X and edge[0] not in X)) and edge[2] < current_min:
                current_min = edge[2]
                current_edge = edge
        if current_edge[0] in X:
            X.append(current_edge[1])
        else:
            X.append(current_edge[0])
        T.append(current_edge)
    print(X)
    print(T)
    print(sum([t[2] for t in T]))


naive_spanning_tree(prims_edges)

