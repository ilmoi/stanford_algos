# median maintenance
import random


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
        self.heapList = [0] + alist[:]
        while i > 0:
            self.percDown(i)
            i -= 1
        return self.heapList


# ==============================================================================
def calc_median(L):
    """Median maintenance algo.
    Implemented as per lecture slides. See algo1slides / Part 12."""

    h_low = MaxBinHeap() #supports extract max
    h_high = MinBinHeap() #supports extract min

    medians = []
    j = 1
    for i in L:
        len_low = len(h_low.heapList)
        len_high = len(h_high.heapList)

        # starting condition
        if len_low == 1 and len_high == 1:
            h_low.insert(i)
            m_low = h_low.heapList[1]
        elif len_high == 1:
            if i < m_low:
                h_low.insert(i)
                m_low = h_low.heapList[1]
            else:
                h_high.insert(i)
                m_high = h_high.heapList[1]
        else:
            # if bigger put into high heap
            if i > m_low:
                h_high.insert(i)
                m_high = h_high.heapList[1]
            # if smaller put into small heap
            elif i < m_high:
                h_low.insert(i)
                m_low = h_low.heapList[1]
            # if in between put into either one
            else:
                h_low.insert(i) #picked whichever
                m_low = h_low.heapList[1]

        # if heaps differ by 2, fix imbalance
        if abs(len(h_low.heapList) - len(h_high.heapList)) > 1:
            if len(h_low.heapList) > len(h_high.heapList):
                e = h_low.del_max()
                h_high.insert(e)
            else:
                e = h_high.del_min()
                h_low.insert(e)
            m_high = h_high.heapList[1]
            m_low = h_low.heapList[1]

        if j % 2 == 0:
            median = h_low.heapList[1]
        else:
            if len(h_low.heapList) > len(h_high.heapList):
                median = h_low.heapList[1]
            else:
                median = h_high.heapList[1]

        medians.append(median)

        # print('-'*20)
        # print(h_low.heapList)
        # print(h_high.heapList)
        # print(f"median on the {j} round is {median}")
        # print(len(h_low.heapList))
        # print(len(h_high.heapList))
        j += 1
        # if j % 100 == 0:
        #     print(j)

    total = sum(medians)
    print(total)
    mod_total = total % 10000
    print(mod_total)


random.seed(1)
L = [random.randint(1,100) for _ in range(10)]
# calc_median(L)


with open("median.txt") as f:
    txt = f.readlines()
    txt = [int(t.strip('\n')) for t in txt]
    # print(txt)
    # print(len(txt))
    calc_median(txt)