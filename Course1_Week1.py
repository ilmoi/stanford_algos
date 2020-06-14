# ==============================================================================
# SKIENA
# I implemented the below when I dabbled with Skiena
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


def karatsuba(x, y):
    """Simple implementation of karatsuba, without recursion.
    Karatsuba is a way to more efficiently multiply two integers together.
    Implementation as per lecture slides. See algo1slides / Part 1.
    """
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


def merge_sort(L):
    """My first naive implementation of merge sort, with subroutine.
    See algo1slides / Part 1."""

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
    # as per my stackoverflow question.

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


L = [5,3,8,9,1,7,0,2,6,4]
print(merge_sort(L))