import itertools
import math


def distance(city1, city2):
    """Calculates distance between two cities."""

    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x1-x2)**2+(y1-y2)**2)


def tsm(coords):
    """DP Solutions to the TSM problem. Can only run on small (<25 cities) datasets.
    Implemented as per lecture slides. See algo2slides / Part 17."""

    # create the matrix to be filled in
    n = len(coords)
    A = {}

    # base case
    # impossible to get to any vertex other than starting with 0 moves
    # getting from starting point to itself = 0 moves
    starting_vertex = coords[0]
    rem_coords = coords[1:] #first vertex stays constant no matter what
    A[(starting_vertex,)] = [0] + [float("inf")] * (n-1)
    # print(A)

    # main loop
    print(A)
    x = 0
    for m in range(1,n):
        # generate all subsets exluding i, but then add i on top to all of them
        subsets = list(itertools.combinations(rem_coords, m))
        for s_index, subset in enumerate(subsets):
            # counting
            if x % 10000 == 0:
                print(x)
            x+=1

            # prepare the dict key for hashing
            subset = (starting_vertex,) + subset
            subset = tuple(sorted(subset, key=lambda x: x[0]))

            # initialize the dict value
            A[subset] = [float("inf")] * n

            # go through each potential j in each subset
            for j in subset:
                # i and j can't be the same, so we skip that case
                if j == starting_vertex:
                    continue

                # exlcude j, because we want to find all i-k options, k being on the way to j
                subset_without_j = tuple(sorted([s for s in subset if s != j]))
                j_index = coords.index(j)
                min_k = float("inf")

                # check all intermediate points k for the smallest one
                for k in subset_without_j:
                    k_index = coords.index(k)
                    contender = A[subset_without_j][k_index] + distance(j,k)
                    if contender < min_k:
                        min_k = contender

                # assign the smallest one to the right index in the matrix
                A[subset][j_index] = min_k

    print(A)

    # have to do a second loop to calculate reverse distances
    x = 0
    for m in range(1, n):
        subsets = list(itertools.combinations(rem_coords, m))
        for s_index, subset in enumerate(subsets):
            if x % 10000 == 0:
                print(x)
            x+=1
            subset = (starting_vertex,) + subset
            subset = tuple(sorted(subset, key=lambda x: x[0]))
            for j in subset:
                # i and j can't be the same, so we skip that case
                if j == starting_vertex:
                    continue
                j_index = coords.index(j)
                d = distance(coords[0], coords[j_index])
                A[subset][j_index] += d

    final = A[tuple(sorted(coords))]
    print(final)
    print(min(final))


# ==============================================================================
coords = [(1,2),(5,6),(6,7),(2,3)]
# coords = [(1,2),(5,6),(6,7)]
tsm(coords)

# with open('tsp.txt') as f:
#     lines = f.readlines()
#     final_lines = []
#     for line in lines:
#         split_line = line.strip('\n').strip('').split()
#         split_line = tuple([float(s) for s in split_line])
#         final_lines.append(split_line)
#     final_lines = final_lines[1:]
#     print(final_lines)
#     tsm(final_lines)