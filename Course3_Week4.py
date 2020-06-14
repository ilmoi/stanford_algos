V=[3,2,4,4]
W=[4,3,2,3]


def knapsack(V, W, W_total):
    """DP Solution to the knapsack problem.
    Implemented as per lecture slides. See algo2slides / Part 11."""

    A = [[0 for _ in range(W_total)] for _ in range(len(V))]
    # print(A)

    # special case of 1st item
    for w in range(W_total):
        if w+1 >= W[0]:  # note the w+1
            A[0][w] = V[0]
    # print(A)

    # special case of 2nd item
    for w in range(W_total):
        if w+1 >= W[1]:
            A[1][w] = max(A[0][w], V[1])
        else:
            A[1][w] = A[0][w]
    # print(A)

    # the rest
    for i in range(2, len(A)):
        # print(f"----i is {i}")
        for w in range(W_total):
            # print(f"w is {w}")
            if w+1 >= W[i]:
                current_w = W[i]
                A[i][w] = max(A[i-1][w], A[i-1][max(0, w-current_w)] + V[i])
            else:
                A[i][w] = A[i-1][w]
        # print(A[i][-1])
    # print(A)
    print(A[-1][-1])


# knapsack(V, W, 6)


def smarter_knapsack(V, W, W_total):
    """This knapsack impl. saves space by constantly re-using same 3 cols instead of len(W_total).
    This was a necessary optimization for the larger coding assignment."""

    A = [[0 for _ in range(W_total)] for _ in range(3)]
    print(A)

    # special case of 1st item
    for w in range(W_total):
        if w+1 >= W[0]:  # note the w+1
            A[0][w] = V[0]
    # print(A)

    # special case of 2nd item
    for w in range(W_total):
        if w+1 >= W[1]:
            A[1][w] = max(A[0][w], V[1])
        else:
            A[1][w] = A[0][w]
    # print(A)

    # the rest
    j = 0
    for i in range(2, len(V)):
        print(f"----actual i is {i}, fake i is {i-j}")
        i -= j
        for w in range(W_total):
            # if w % 500000 == 0:
                # print(f"w is {w}")
            if w+1 >= W[i+j]:
                current_w = W[i+j]
                A[i][w] = max(A[i-1][w], A[i-1][max(0, w-current_w)] + V[i+j])
            else:
                A[i][w] = A[i-1][w]
        A[0]=A[1][:]
        A[1]=A[2][:]
        j += 1
        # print(A[i][-1])
    # with open('temp_save2.txt', 'w') as f:
    #     f.write(str(A))
    # print(A)
    print(A[-1][-1])

# smarter_knapsack(V,W,6)

# with open('mwis.txt') as f:
#     lines = f.readlines()
#     lines = [int(l.strip('\n')) for l in lines[1:]]
#     print(lines[:10])
#     vertices = [1, 2, 3, 4, 17, 117, 517, 997]
#     vertices_to_test = []
#     for v in vertices:
#         vertices_to_test.append(lines[v-1])
#     print(vertices_to_test)
#     rec = dynamic_prog(lines)
#     answer = [1 if i in rec else 0 for i in vertices_to_test]
#     print(answer)
#

with open('knapsack_big.txt') as f:
    lines = f.readlines()
    V = []
    W = []
    for line in lines[1:]:
        split_line = line.strip('\n').strip('').split()
        v, w = int(split_line[0]), int(split_line[1])
        V.append(v)
        W.append(w)
    # smarter_knapsack(V,W,2000000)
    # smarter_knapsack(V, W, 10000)

# ==============================================================================
# optimal BST problem
weights = [0.05,0.4,0.08,0.04,0.1,0.1,0.23]
weights2 = [0.2,0.05,0.17,0.1,0.2,0.03,0.25]
print(sum(weights2))
# print(len(weights))
def optimal_BST(weights):
    """My solution to the optimal binary search tree problem.
    Coded it up as part of solving one of the tests.
    Implemented as per lecture slides. See algo2slides / Part 13."""

    A = [[None for _ in range(len(weights))] for _ in range(len(weights))]
    # outer one = i
    # inner one = j
    print(A)

    # base case
    for i in range(len(weights)):
        A[i][i] = weights[i]
    print(A)

    for s in range(len(weights)): #0 to n-1
        # s represents j - i
        for i in range(len(weights)): #1 to n, but less one for indexing
            j = min(i+s, len(weights)-1)
            relevant_weights = weights[i:j+1]
            sum_of_weights = sum(relevant_weights)
            rs = []
            for r in range(i,j+1):
                # print(f"i is {i}, j+1 ir {j+1}")
                if r-1 <0:
                    C_left = 0
                    if r+1 > j:
                        C_right = 0
                    else:
                        C_right = A[r + 1][j]
                elif r+1 > j+1:
                    if i > r-1:
                        C_left = 0
                    else:
                        C_left = A[i][r - 1]
                    C_right = 0
                else:
                    if i > r-1:
                        C_left = 0
                    else:
                        C_left = A[i][r-1]
                    if r+1 > j:
                        C_right = 0
                    else:
                        C_right = A[r+1][j]
                rs.append(C_left+C_right)
            A[i][j] = sum_of_weights + min(rs)
    print(A[0][-1])


optimal_BST(weights2)