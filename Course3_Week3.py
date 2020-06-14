# Trees
class Tree:
    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def map(self, fn):
        self.label = fn(self.label)
        for b in self.branches:
            b.map(fn)

    def __contains__(self, e):
        if self.label == e:
            return True
        for b in self.branches:
            if e in b:
                return True
        return False

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)

    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = '  ' * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str
        return print_tree(self).rstrip()

def height(t):
    """Returns the height of the tree == the len of longest branch."""

    # if is_leaf(t):
    #     return 0
    # else:
    #     heights = []
    #     for b in branches(t):
    #         heights.append(height(b))
    #     return 1 + max(heights)

    # write in one line
    return 1 + max([-1]+[height(b) for b in t.branches])

t = Tree(None,[Tree(1),Tree(2, [Tree(1), Tree(2)])])
# print(t)
# print(height(t))

def hacky_leaf(t):
    j = 0
    def hacky_first_leaf(t):
        nonlocal j
        if t.is_leaf():
            print(f"nice found a leaf {t.label}, j is {j}")
            raise(Exception("so fucking hacky"))
        else:
            j += 1
            return 1 + min([hacky_first_leaf(b) for b in t.branches])
    hacky_first_leaf(t)


# ==============================================================================
# Heap
class MinBinHeap:
    """Modified version of MinBinHeap
    takes in tuples with (node_name, node_value)"""

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


# ==============================================================================


L = [320,250,200,180,50]

def huffman(L):
    """Huffman codes problem (how to efficiently encode letters).
    Implemented as per lecture slides. See algo2slides / Part 9."""

    # Make tuples in O(n)
    LL = [(Tree(l), l) for l in L]
    # print(LL)

    # build heap in O(n) - coz we care about minimum
    mbh = MinBinHeap()
    mbh.build_heap(LL)
    # print(mbh.heapList)

    # until everything becomes a single tree, keep merging
    while len(mbh.heapList) > 2:
        first = mbh.del_min()
        second = mbh.del_min()
        t = Tree(None,[first[0], second[0]])
        mbh.insert((t, first[1]+second[1]))

    result = mbh.heapList[1][0]
    print(result)
    return result

# t = huffman(L)
# print(height(t))
# print(hacky_leaf(t))

# with open('huffman.txt') as f:
#     lines = f.readlines()
#     lines = [int(l.strip('\n')) for l in lines[1:]]
#     # print(lines[:10])
#     t = huffman(lines)
#     print(height(t)) #max height 19
#     print(hacky_leaf(t)) #min height 9


# ==============================================================================
L=[1,4,7,1,6,2,5,6]
# L=[1,4,8,8,14,14,19,20]

def dynamic_prog(L):
    """Dynamic programming solution to the max independent set problem.
    Implemented as per lecture slides. See algo2slides / Part 10."""

    A = [None] * len(L)
    # print(A)
    A[0] = L[0]
    A[1] = max(L[0], L[1])
    for i in range(2, len(A)):
        A[i] = max(A[i-1], A[i-2] + L[i])
    # print(A)

    # reconstruct
    rec = []
    i = len(A)-1
    while i >= 0:
        if i == 1:
            rec.append(L[i])
            break
        elif i == 0:
            rec.append(L[i])
            break
        # print(f"i is {i}")
        if A[i-1] >= A[i-2] + L[i]:
            i -= 1
        else:
            rec.append(L[i])
            i -= 2
    print(rec)
    return rec

dynamic_prog(L)

with open('mwis.txt') as f:
    lines = f.readlines()
    lines = [int(l.strip('\n')) for l in lines[1:]]
    print(lines[:10])
    vertices = [1, 2, 3, 4, 17, 117, 517, 997]
    vertices_to_test = []
    for v in vertices:
        vertices_to_test.append(lines[v-1])
    print(vertices_to_test)
    rec = dynamic_prog(lines)
    answer = [1 if i in rec else 0 for i in vertices_to_test]
    print(answer)

