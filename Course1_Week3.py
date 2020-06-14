import json
import random
import math
from copy import deepcopy
import timeit


# ==============================================================================
# Quicksort


def partition(A, l, r):
    """
    Needed for quicksort below.
    Performs linear, ie O(n) amount of work.
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
    """Randomized quicksort algo.
    Implemented as per lecture slides. See algo1slides / Part 6."""

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


with open('quicksort.txt') as f:
    L = [int(i.strip('\n')) for i in f.readlines()]
    # L = [8,2,4,5,7,1]
    quicksort_with_comparisons(L, 0, len(L))
    print(comparisons)



