# ==============================================================================
# SKIENA
import json
import random
import math
from copy import deepcopy
import timeit


def insertionSort(arr):
    # note we're not starting from 0 but from 1
    for i in range(1, len(arr)):
        # key is the element we're "pulling out" of the deck
        key = arr[i]
        # we're going to be comparing it to all the ones BEFORE, so i-1
        j = i - 1
        # we're going to iterate from j-1 to 0 comparing key to each elem
        # we know the previous elements are ALREADY SORTED
        # so as soon as we hit an element that key is bigger than, we terminate the loop
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        # and finally we insert the key
        arr[j + 1] = key


# arr = [12, 11, 13, 5, 6]
# insertionSort(arr)
# print(arr)

# ==============================================================================
# 1 INTRODUCTION

def karatsuba(x, y):
    """Simple implementation of karatsuba, without recursion."""
    n = max(len(str(x)), len(str(y)))
    n2 = n // 2

    # 1 get the digits
    a, b = x // 10 ** n2, x % 10 ** n2
    c, d = y // 10 ** n2, y % 10 ** n2
    # print(a, b, c, d)

    # 2 compute ac and bd
    ac = a * c
    bd = b * d

    # 3 compute ad+bc
    ad_bc = (a + b) * (c + d) - ac - bd

    # put everything togehter
    return ac * 10 ** n + ad_bc * 10 ** n2 + bd


def rec_karatsuba(x, y):
    """Recursive karatsuba implementation."""
    n = max(len(str(x)), len(str(y)))
    n2 = n // 2

    # print(f'x is {x}, y is {y}, n is {n}, n2 is {n2}')

    # base case
    if x < 10 or y < 10:
        return x * y
    else:
        # 1 get the digits
        a, b = x // 10 ** n2, x % 10 ** n2
        c, d = y // 10 ** n2, y % 10 ** n2
        # print(a, b, c, d)

        # 2 compute ac and bd
        ac = rec_karatsuba(a, c)
        bd = rec_karatsuba(b, d)

        # 3 compute ad+bc
        ad_bc = rec_karatsuba((a + b), (c + d)) - ac - bd

        # put everything togehter
        # NOTE: somewhy you need to use n2*2 here, not just n - this has to do with floor division of the coefficient we're doing above
        # This kinda makes sense. If we're breaking the problem up into 2 but the coefficient is floor divided to go back up we multiply the floor by 2 not the original coef.
        # more: https://stackoverflow.com/questions/42324419/karatsuba-multiplication-implementation
        return ac * 10 ** (n2 * 2) + ad_bc * 10 ** n2 + bd


# a = 5678
# b = 1234
a = 3141592653589793238462643383279502884197169399375105820974944592
b = 2718281828459045235360287471352662497757247093699959574966967627


# print(f'3rd grade is {a*b}')
# print(f'kara is {karatsuba(a, b)}')
# print(f'rec is {rec_karatsuba(a, b)}')

# print(timeit.timeit(lambda: a*b, number=10))  # quickest at -06
# print(timeit.timeit(lambda: karatsuba(a, b), number=10))  # second quickest at -05
# print(timeit.timeit(lambda: rec_karatsuba(a, b), number=10))  # slowest at 0.027s

# ==============================================================================
# 2 ASYMPTOTIC ANALYSIS


def merge_sort(L):
    def merge(a, b):
        # the running time of merge routine is O(n) with n being total length of a+b

        i, j = 0, 0
        c = []

        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                c.append(a[i])
                i += 1
            elif b[j] < a[i]:
                c.append(b[j])
                j += 1

        # option 1
        # if a[i:]:
        #     c.extend(a[i:])
        # if b[j:]:
        #     c.extend(b[j:])

        # option 2
        while i < len(a):
            c.append(a[i])
            i += 1
        while j < len(b):
            c.append(b[j])
            j += 1
        return c

    # this part is O(logn), thus together merge sort is O(nlogn)
    if len(L) <= 1:
        return L
    else:
        mid = len(L) // 2  # for odd numbers one becomes shorter one longer
        # print(f"mid is {mid}, right side is {L[mid:]}")
        left = merge_sort(L[:mid])
        right = merge_sort(L[mid:])
        # print(f"left is {left}, right is {right}")
        return merge(left, right)


def better_merge_sort(L):
    # optimizations:
    # 1 no subroutine
    # 2 mutating list in place rather than doing append / extend
    # 3 remove slicing in if statements, only in final extends
    # 4 restructure the main loop to have a single if
    # NOTE I think this is overoptimization here... I think the above already achieves the main optimization effect that we go from n**2 to nlogn

    if len(L) <= 1:
        return L
    else:
        n = len(L)
        mid = n // 2
        left = better_merge_sort(L[:mid])
        right = better_merge_sort(L[mid:])
        i, j = 0, 0

        # not afraid of while True coz there are returns statements that will kick us out of the loop
        # while True:
        #     if left[i] <= right[j]:
        #         L[k] = left[i]
        #         k += 1
        #         i += 1
        #         if i == len(left):
        #             L[k:] = right[j:]
        #             return L
        #     else:
        #         L[k] = right[j]
        #         k += 1
        #         j += 1
        #         if j == len(right):
        #             L[k:] = left[i:]
        #             return L

        for k in range(n):
            # print(left, right, k)
            if left[i] <= right[j]:
                L[k] = left[i]
                i += 1
                if i == len(left):
                    L[k + 1:] = right[j:]  # NOTE we have to use k+1
                    return L
            else:
                L[k] = right[j]
                j += 1
                if j == len(right):
                    L[k + 1:] = left[i:]
                    return L


# L = [5,3,8,9,1,7,0,2,6,4]
# print(merge_sort(L))


# ==============================================================================
# 3 DIVIDE + CONQUER ALGOS

def count_inversions(L):
    inversion_counter = 0

    def count(L):
        if len(L) <= 1:
            return L
        else:
            n = len(L)
            mid = n // 2
            left = count(L[:mid])
            right = count(L[mid:])

            i, j = 0, 0

            nonlocal inversion_counter

            for k in range(n):
                # print(left, right, k)
                if left[i] <= right[j]:
                    L[k] = left[i]
                    i += 1
                    if i == len(left):
                        L[k + 1:] = right[j:]  # NOTE we have to use k+1
                        return L
                else:
                    L[k] = right[j]
                    j += 1

                    # this is the interesting part
                    # every time we execute this side of the branch - there's some number of elements on LHS that are inversed
                    # specifiaclly everything post i, that didn't yet get copied over
                    # so we count them and increment the counter
                    inversion_counter += len(left) - i

                    if j == len(right):
                        L[k + 1:] = left[i:]
                        return L

    count(L)

    return inversion_counter


# L = list(reversed(range(6)))
# print(L)
# print(count_inversions(L))

# with open('integers.txt') as f:
#     txt = [int(i.strip('\n')) for i in f.readlines()]
#     print(count_inversions(txt))

def strassen_matrix_mult(X, Y):
    def split_up(X):
        mid = len(X) // 2
        A = X[:mid][0][:mid][0]
        B = X[:mid][0][mid:][0]
        C = X[mid:][0][:mid][0]
        D = X[mid:][0][mid:][0]
        return A, B, C, D

    if type(X) == int:
        return X * Y
    else:
        A, B, C, D = split_up(X)
        E, F, G, H = split_up(Y)

        # 7 instead of 8 recursive calls
        P1 = strassen_matrix_mult(A, (F - H))
        P2 = strassen_matrix_mult((A + B), H)
        P3 = strassen_matrix_mult((C + D), E)
        P4 = strassen_matrix_mult(D, (G - E))
        P5 = strassen_matrix_mult((A + D), (E + H))
        P6 = strassen_matrix_mult((B - D), (G + H))
        P7 = strassen_matrix_mult((A - C), (E + F))

        # add back up
        Q1 = P5 + P4 - P2 + P6
        Q2 = P1 + P2
        Q3 = P3 + P4
        Q4 = P1 + P5 - P3 - P7

        return [[Q1, Q2], [Q3, Q4]]


# X = [[1, 2], [3, 4]]
# Y = [[5, 6], [7, 8]]
# print(strassen_matrix_mult(X, Y))
# a = np.array(X)
# b = np.array(Y)
# print(a@b)


def special_merge_sort(L, item):
    if len(L) <= 1:
        return L
    else:
        n = len(L)
        mid = n // 2
        left = special_merge_sort(L[:mid], item)
        right = special_merge_sort(L[mid:], item)
        i, j = 0, 0
        for k in range(n):
            # print(left[i][item])
            if left[i][item] <= right[j][item]:
                L[k] = left[i]
                i += 1
                if i == len(left):
                    L[k + 1:] = right[j:]  # NOTE we have to use k+1
                    return L
            else:
                L[k] = right[j]
                j += 1
                if j == len(right):
                    L[k + 1:] = left[i:]
                    return L


OneDP = list(reversed([1, 5, 7, 10, 21, 22]))


# ==============================================================================
# 1d version


def OneDClosestPair(P):
    # 1 - sort the points
    P = better_merge_sort(P)

    # 2 iterate through consecutive points and see which one is closest
    d = {}
    for i in range(1, len(P)):  # linear
        d[(P[i - 1], P[i])] = P[i] - P[i - 1]
    return min(d.keys(), key=(lambda k: d[k]))


# print(OneDClosestPair(OneDP))


# ==============================================================================
# 2d version

def distance(p1, p2):
    """Calculates the distance between 2 points in the format (x,y)"""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# print(distance((1, 1), (4, 5)))


# NOTE: THIS IS A REALLY BAD IMPLEMENTATION. INCREASED ALGO TIME FROM <1S TO 80S
# MORAL OF THE STORY - IF EFFICIENCY IN QUESTION, DON'T USE PYTHON DICTIONARIES
# def brute(Px):
#     d = {}
#     for i in range(1, len(P)):
#         d[(P[i-1], P[i])] = distance(P[i-1], P[i])
#     d[(P[0], P[-1])] = distance(P[0], P[-1])
#     return min(d.keys(), key=(lambda k: d[k]))


def brute(Px):
    base_d = distance(Px[0], Px[1])
    p1, p2 = Px[0], Px[1]
    if len(Px) == 2:
        return p1, p2
    for i in range(len(Px) - 1):
        for j in range(i + 1, len(Px)):
            if i != 0 and j != 1:  # this is our base condition above, non need to re-do
                d = distance(Px[i], Px[j])
                if d < base_d:
                    base_d = d
                    p1, p2 = Px[i], Px[j]
    return p1, p2


def ClosestSplitPair(Px, Py, mn, delta):
    # find middle
    x_bar = Px[len(Px) // 2][0]

    # our window of operations (Sy) = middle +- delta
    window = (x_bar - delta, x_bar + delta)
    Sy = []
    for i in range(len(Py)):
        if window[0] <= Py[i][0] <= window[1]:
            Sy.append(Py[i])

    # iterate to find smallest pair within 7 of them
    # NOTE: this is the crux of the algorithm - there is a math proof that says 7 items is enough
    for i in range(len(Sy) - 1):
        for j in range(i + 1, min(i + 7, len(Sy))):
            p, q = Sy[i], Sy[j]
            if distance(p, q) < delta:
                delta = distance(p, q)
                mn = (p, q)

    p, q = mn
    return p, q, delta


def ClosestPair(P):
    """Takes in an input of n points in the plane R2, of the form (x,y)"""

    # Sort input based on both x and y. The reason we can do this is because we want our algo to be nlogn, so making it 2nlogn makes no difference
    # NOTE: needs to be done outside of the recursive function
    Px = special_merge_sort(P[:], 0)
    Py = special_merge_sort(P[:], 1)

    def InternalClosestPair(Px, Py):
        # he said base case = 3 points or smaller. This is because if you go below 3 you can end up with a P that's 1 point (3 = 2+1) and then you can't calculate distance
        # 1 - base case
        if len(Px) <= 3:
            b = brute(Px)
            return b
        else:
            # at least 4 points in the input
            # 2 - split into halves
            mid = len(Px) // 2
            Qx = Px[:mid]
            Rx = Px[mid:]

            # 3 - select the relevant bits from Qy
            midpoint = Px[mid][0]
            Qy = []
            Ry = []
            for y in Py:
                if y[0] <= midpoint:
                    Qy.append(y)
                else:
                    Ry.append(y)

            # 4 - recursion
            p1, q1 = InternalClosestPair(Qx, Qy)
            p2, q2 = InternalClosestPair(Rx, Ry)

            # 5 - find smallest distance between the two
            d1 = distance(p1, q1)
            d2 = distance(p2, q2)
            if d1 < d2:
                mn = p1, q1
                delta = d1
            else:
                mn = p2, q2
                delta = d2

            # 5 split points
            p3, q3, delta = ClosestSplitPair(Px, Py, mn, delta)

            # compare
            # print(f"Qx is {Qx}, Rx is {Rx}")
            # print(f"Qy is {Qy}, Ry is {Ry}")
            # print(f"LEFT side returned {p1}, {q1}, {distance(p1, q1)}")
            # print(f"RIGHT side returned {p2}, {q2}, {distance(p2, q2)}")
            # print(f"MID returned {p3}, {q3}, {distance(p3, q3)}")
            # print('-'*10)

            return p3, q3

    return InternalClosestPair(Px, Py)


# random.seed(1)
# x = [random.randint(-10**9, 10**9) for _ in range(10000)]
# y = [random.randint(-10**9, 10**9) for _ in range(10000)]
# P = list(zip(x, y))
# print(ClosestPair(P))
"""
((393038850, 325890200), (393170221, 325934327))
[Finished in 0.685s]
"""


# ==============================================================================
# 5 - Quicksort


def partition(A, l, r):
    """Performs linear, ie O(n) amount of work.
    MY OWN IMPLEMENTATION
    This one sorts IN PLACE = hence O(1) memory efficient.
    """
    # 1 first element
    # p = A[l]

    # 2 last element
    # p = A[r-1]
    # A[r-1], A[l] = A[l], A[r-1]

    # # 3 choose median of first, last middle
    # first = A[l]
    # last = A[r-1]
    # middle = A[math.ceil((r-l)/2)-1+l]
    # elems = sorted([("first", first), ("last", last), ("middle", middle)], key=lambda x: x[1])
    # p = elems[1][1]
    # chosen = elems[1][0]
    # if chosen == 'first':
    #     pass
    # elif chosen == 'last':
    #     A[r - 1], A[l] = A[l], A[r - 1]
    # elif chosen == "middle":
    #     A[l], A[math.ceil((r-l)/2)-1+l] = A[math.ceil((r-l)/2)-1+l], A[l]

    # 4 randomized implementation
    rand = random.randint(l, r - 1)
    p = A[rand]
    A[rand], A[l] = A[l], A[
        rand]  # note how we have to flip the pivoted number into position #1

    i = l + 1  # start i one to the right of where left begins
    for j in range(l + 1, r):
        if A[j] < p:
            A[j], A[i] = A[i], A[j]
            i += 1
    i -= 1  # need this since we're overshooting the index by 1 every time
    A[l], A[i] = A[i], A[l]
    return i  # need to return this otherwise can't run the func below


def quicksort(A, l, r):
    if r - l <= 1:
        return
    i = partition(A, l, r)
    quicksort(A, l, i)  # remember i is excluded, hence not i-1
    quicksort(A, i + 1, r)


def short_but_expensive_quicksort(A):
    """This one copies arrays, so less memory efficient.
    Also DOES NOT USE RANDOMIZATION"""
    if len(A) <= 1:
        return A
    return short_but_expensive_quicksort([x for x in A[1:] if x < A[0]]) + \
           [A[0]] + \
           short_but_expensive_quicksort([x for x in A[1:] if x >= A[0]])


# L = list(reversed(range(10)))
# random.shuffle(L)
# quicksort(L, 0, len(L))
# print(L)
# z = short_but_expensive_quicksort(L)
# print(z)

comparisons = 0


def quicksort_with_comparisons(A, l, r):
    global comparisons
    if r - l <= 1:
        return
    i = partition(A, l, r)
    comparisons += r - l - 1  # -1 coz exclude p
    quicksort_with_comparisons(A, l, i)  # remember i is excluded, hence not i-1
    quicksort_with_comparisons(A, i + 1, r)


# with open('quicksort.txt') as f:
#     L = [int(i.strip('\n')) for i in f.readlines()]
#     # L = [8,2,4,5,7,1]
#     quicksort_with_comparisons(L, 0, len(L))
#     print(comparisons)


# ==============================================================================
# 8 - linear time selection

def randomized_selection(A, l, r, i):
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
# 9.5 correct but not quick enough to run 200k. With 1k seems to get the right answer tho

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