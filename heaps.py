import random


def max_heapify(h, top):
    # no children case
    if top*2 > len(h):
        return
    # one kid case
    elif top*2+1 > len(h):
        current_top = h[top - 1]
        max_ = h[top * 2 - 1]
        i = 0
    # two kids case
    else:
        current_top = h[top-1]
        child1 = h[top*2-1]
        child2 = h[top*2+1-1]
        # print(f"top is {current_top}, kids are {child1} and {child2}")
        if child1 > child2:
            max_, i = child1, 0
        else:
            max_, i = child2, 1
    # decide if swap
    if current_top < max_:
        # print(f'swapping {h[top-1]} and {h[top * 2 - 1 + i]}')
        h[top-1], h[top*2-1+i] = h[top*2-1+i], h[top-1]
        max_heapify(h, top*2+i)


def build_a_heap(h):
    for i in reversed(range(len(h))):
        max_heapify(h, i+1)


def insert(h, n):
    h.append(n)
    def insert_sub(h, n):
        kid_index = h.index(n)
        if kid_index == 0:
            return
        father_index = (kid_index+1)//2-1
        father = h[father_index]
        # print(f"kid is {n} at {kid_index}, father is {father} at {father_index}")
        if father < n:
            h[kid_index], h[father_index] = h[father_index], h[kid_index]
            insert_sub(h, n)
    insert_sub(h, n)


def delete_the_root(h):
    # swap root and last value
    h[0], h[len(h)-1] = h[len(h)-1], h[0]
    # remove last value
    h.pop()
    # print(h)
    max_heapify(h,1)


# ==============================================================================
# heap DS from here https://runestone.academy/runestone/books/published/pythonds/Trees/BinaryHeapImplementation.html

class MaxBinHeap:
    def __init__(self):
        self.heapList = [0] #need to initialize with 1 element to shift all elements by 1, to make calculations easier
        self.currentSize = 0 #0 above is a dummy element, that's why this is started at 0 not 1

    def percUp(self, i):
        # iterative version seems more elegant than my recursive one
        while i//2 > 0: #while there are still kids
            if self.heapList[i] > self.heapList[i//2]: #if kid bigger than parent
                self.heapList[i], self.heapList[i//2] = self.heapList[i//2], self.heapList[i] #then swap
            i = i//2 #now look at kid's kid

    def insert(self, k):
        self.heapList.append(k)
        self.currentSize += 1
        self.percUp(self.currentSize)

    def percDown(self, i):
        while i*2 <= self.currentSize:
            # print(f"i*2 is {i*2}")
            mc = self.max_child(i)
            if self.heapList[i] < self.heapList[mc]: #if parent smaller than child
                self.heapList[i], self.heapList[mc] = self.heapList[mc], self.heapList[i]
            i = mc

    def max_child(self, i):
        if i*2+1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2] > self.heapList[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1

    def del_max(self):
        # interesting so 0 seems to act like a buffer
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize -= 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def build_heap(self, alist):
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [0] + alist[:]
        while i > 0:
            self.percDown(i)
            i -= 1
        return self.heapList


# ==============================================================================
# MIN
class MinBinHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0

    def percUp(self, i):
        while i//2 > 0: #while there are still kids
            if self.heapList[i] < self.heapList[i//2]: #if kid SMALLER than parent
                self.heapList[i], self.heapList[i//2] = self.heapList[i//2], self.heapList[i] #then swap
            i = i//2 #now look at kid's kid

    def insert(self, k):
        self.heapList.append(k)
        self.currentSize += 1
        self.percUp(self.currentSize)

    def percDown(self, i):
        while i*2 <= self.currentSize:
            mc = self.min_child(i)
            if self.heapList[i] > self.heapList[mc]: #if parent BIGGER than child
                self.heapList[i], self.heapList[mc] = self.heapList[mc], self.heapList[i]
            i = mc

    def min_child(self, i):
        if i*2+1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2] < self.heapList[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1

    def del_max(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize -= 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def build_heap(self, alist):
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [0] + alist[:]
        while i > 0:
            self.percDown(i)
            i -= 1
        return self.heapList


# ==============================================================================
# applying

if __name__ == "__main__":
    random.seed(1)
    heap = random.sample(list(range(100)), k=10)
    heap2 = heap[:]

    # my version
    print(heap)
    print('max-heapifying 18')
    max_heapify(heap, 1)
    print(heap)

    print('building a heap...')
    build_a_heap(heap)
    print(heap)

    print('inserting 100...')
    insert(heap, 100)
    print(heap)

    print('deleting root...')
    delete_the_root(heap)
    print(heap)

    # their version
    print("-" * 50)

    mbh = MaxBinHeap()
    print(heap2)
    print('building a heap...')
    mbh.build_heap(heap2)
    print(mbh.heapList)

    print('inserting 100...')
    mbh.insert(100)
    print(mbh.heapList)

    print('deleting root...')
    mbh.del_max()
    print(mbh.heapList)

    print('-'*50)

    # mbh2 = MaxBinHeap()
    # mbh2.build_heap([9, 6, 5, 2, 3])
    # print(mbh2.heapList)

    mbh3 = MinBinHeap()
    mbh3.build_heap([9, 6, 5, 2, 3])
    print(mbh3.heapList)