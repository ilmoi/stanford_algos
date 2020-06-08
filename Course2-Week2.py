import random

class MinBinHeap:
    """Modified version of MinBinHeap
    takes in tuples with (node_name, node_distance)"""

    def __init__(self):
        self.heapList = [[0,0]]
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
        self.heapList = [[0,0]] + alist[:]
        while i > 0:
            self.percDown(i)
            i -= 1

    def rebuild(self):
        # print(f"before rebuilding - {self.heapList}")
        self.build_heap(self.heapList[1:])
        # print(f"AFTER rebuilding - {self.heapList}")


with open("dijkstra_data.txt") as f:
    lines = f.readlines()
    final_lines = []
    for line in lines:
        line = line.split('\t')
        first = line[0]
        rest = line[1:]
        # print(rest)
        elems = []
        for e in rest:
            # final_lines.append(int(e.split(',')))
            if e != '\n':
                e = e.split(',')
                e = [int(i) for i in e]
                elems.append(e)
        # print(elems)
        final_lines.append(elems)
    # print(final_lines)
actual_G = final_lines

toy_G = [
    [[1,4],[7,8]],
    [[0,4],[2,8],[7,11]],
    [[1,8],[8,2],[5,4],[3,7]],
    [[2,7],[4,9],[5,14]],
    [[3,9],[5,10]],
    [[4,10],[3,14],[2,4],[6,2]],
    [[8,6],[7,1],[5,2]],
    [[6,1],[8,7],[1,11],[0,8]],
    [[2,2],[7,7],[6,6]]
]
# need to adjust index by 1
for i in range(len(toy_G)):
    for j in range(len(toy_G[i])):
        toy_G[i][j][0] +=1
# print(toy_G)

# dijkstra's algo
def dijkstra(G):
    # create min hip backbone
    n = len(G)
    nodes = []
    for i in range(1, n+1):
        nodes.append([i, float("inf")])
    # fix the first node
    nodes[0][1] = 0
    # build the initial one
    mbh = MinBinHeap()
    mbh.build_heap(nodes)
    print(mbh.heapList)

    saved_distances = {}

    while len(mbh.heapList) > 1:
        # pick a vertex
        extracted_tup = mbh.del_min()
        extracted_vertex = extracted_tup[0]
        extracted_distance = extracted_tup[1]
        saved_distances[extracted_vertex] = extracted_distance
        print(extracted_vertex)

        # update neighbors
        for vertex, distance in G[extracted_vertex-1]:
            for tup in mbh.heapList:
                if tup[0] == vertex:
                    if tup[1] > extracted_distance + distance:
                        tup[1] = extracted_distance + distance

            # clean up edges
            G[vertex-1].remove([extracted_vertex, distance])

        # rebuild the heap
        mbh.rebuild()
        print(mbh.heapList)

    print(saved_distances)
    return saved_distances


dist = dijkstra(actual_G)
output = [7,37,59,82,99,115,133,165,188,197]
# output = [4,7,2]
print([dist[k] for k in output])