import json
import random
import math
from copy import deepcopy
import timeit


def count_inversions(L):
    """Counts number of inversions in a number array.
    Implemented as per lecture slides. See algo1slides / Part 3."""

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


# ==============================================================================


def strassen_matrix_mult(X, Y):
    """Strassen's matrix multiplication approach.
    Implemented as per lecture slides. See algo1slides / Part 3."""

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


# ==============================================================================
# closest pair problem


def special_merge_sort(L, item):
    """This is needed for closest pairs algo below."""
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
    """Takes in an input of n points in the plane R2, of the form (x,y).
    Implemented as per lecture slides. See algo1slides / Part 3."""

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
x = [random.randint(-10**9, 10**9) for _ in range(10000)]
y = [random.randint(-10**9, 10**9) for _ in range(10000)]
P = list(zip(x, y))
print(ClosestPair(P))
"""
((393038850, 325890200), (393170221, 325934327))
[Finished in 0.685s]
"""
