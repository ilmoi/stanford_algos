import random
from Course2_Week1 import *

# ==============================================================================
# papadimitriou approach

def match(clause, index):
    if clause < 0 and not index:
        return True
    elif clause > 0 and index:
        return True
    else:
        return False

def vanilla_papadimitriou(L, original_n):
    """
    Papadimitriou solution to the SAT problem.
    Implemented as per lecture slides. See algo2slides / Part 19.
    """
    # decided to work with indexes starting at 1, not 0

    # note have to use len(L) not len(vars) because otherwise can't ref by index
    assignment = ["index from 1"] + [bool(random.getrandbits(1)) for _ in range(original_n)]

    for n in range(2*len(L)**2):
        # counting
        print(f"{n}/{2*len(L)**2} way there!")

        # go through each clause check if valid
        for clause in L:
            clause1, clause2 = clause[0], clause[1]
            index1, index2 = assignment[abs(clause1)], assignment[abs(clause2)]

            # if find an unsatisfied clause
            if not match(clause1, index1) and not match(clause2, index2):
                # pick one variable at random to flip and exit the inner loop
                flip_clause = clause1 if bool(random.getrandbits(1)) else clause2
                assignment[abs(flip_clause)] = not assignment[abs(flip_clause)]
                break
        else: #nobreak - all clauses satisfied
            print('hooray')
            return assignment


def smarter_papa(clauses):
    # if a variable is ALWAYS negated/accepted / NEVER negated / accepted
    # we can throw away any clauses involving it
    # that's because we effectively know what to set it to
    # we can re-do this procedure multiple times, each time removing clauses containing such "one sided" variables
    # here's the explanation that drove it home for me:

    """
    For people who were confused like me for the reduction method,
    you have to run the reduction method many times (I ran 200 times).
    For example, if your initial clauses are : (1, 2), (-1, 3), (2, -3), (-3, 5), (-3, -5), (3,5).
    First round of reduction, you can remove clause containing 2 since 2 only has one representation (never negated).
    So you have(-1,3), (-3,5), (-3,-5), (3,5) left after first reduction. For next round of reduction,
    you can remove clauses containing 1 (negated) because it only has one type of representation.
    In the end, you only have (-3,5) , (-3,-5), (3,5)left. I hope this helps!
    """

    original_n = len(clauses) #we need this later, when we run vanilla papa

    valid_clauses = clauses
    len_clauses = len(valid_clauses)
    len_new_clauses = float("inf")

    # iterate until we stop reducing
    while len_clauses != len_new_clauses:
        len_clauses = len(valid_clauses)

        # populate two lists, one with positive mentions, one with negative
        negated = [0 for _ in range(len(clauses) + 1)] #+1 because indexing from 1
        accepted = [0 for _ in range(len(clauses) + 1)]  # +1 because indexing from 1
        for c in valid_clauses:
            c1, c2 = c[0], c[1]
            index_c1, index_c2 = abs(c1), abs(c2)
            if c1 < 0:
                negated[index_c1] += 1
            else:
                accepted[index_c1] += 1
            if c2 < 0:
                negated[index_c2] += 1
            else:
                accepted[index_c2] += 1

        # filter for newly valid clauses - ones that only involve conflicting variables
        new_valid_clauses = []
        for c in valid_clauses:
            c1, c2 = c[0], c[1]
            index_c1, index_c2 = abs(c1), abs(c2)
            # if either of the lists didn't get a mention, we know it's a one-sided variable
            # if either of the 2 clauses contains a 1-sided variable, we can remove the entire clause because we know how to win it
            if (not accepted[index_c1] or not negated[index_c1]) or (not accepted[index_c2] or not negated[index_c2]):
                continue
            new_valid_clauses.append(c)

        # update and recount
        len_new_clauses = len(new_valid_clauses)
        print(len(new_valid_clauses))
        valid_clauses = new_valid_clauses[:]

    print(valid_clauses)

    # from here we can run traditional papa algo, on a significantly reduced clause number
    vanilla_papadimitriou(valid_clauses, original_n)

# ==============================================================================
# reducing to strongly connected components (SCC) problem approach

def scc_2sat(clauses):
    # part 1 - build the graph
    # in this part we're going to build a connected graph out of SAT constraints
    # exactly how it's done is described here -> https://www.geeksforgeeks.org/2-satisfiability-2-sat-problem/
    # tl;dr; for every constraint we build 2 edges (if not first constraint -> second, if not second -> first)

    # build the edges
    edges = []
    for c in clauses:
        c1, c2 = c[0], c[1]
        e1, e2 = [-c1, c2], [-c2, c1]
        edges.append(e1)
        edges.append(e2)

    # install temp labels
    # NOTE: kosaraju expects nodes to be passed in with labels 0 through n. So I have to change negative labels to make them positive label + n
    for e in edges:
        if e[0] < 0:
            e[0] = abs(e[0]) + n
        if e[1] < 0:
            e[1] = abs(e[1]) + n

    # --------------------------------------------------------------------------
    # part 2 - check for paths
    # if X and NOT X are in the same connected component, this means there's a path from X to NOT X and vice versa.
    # that's a problem because this means our constraints form in such a way to imply X => NOT X and vv
    # in other words this means the SAT can't be satisfied

    scc = kosaraju(edges)
    for i in range(1, n+1):
        if scc[i] == scc[i+n]:
            print('oh no, trouble! POSITIVE AND NEGATIVE NODES IN SAME SCC! SAT CANT BE SATISFIED!')
            break
    else:
        print('all goodz')



# ==============================================================================
# RUNNING & DATA
# random.seed(1)

with open('2sat5.txt') as f:
    lines = f.readlines()
    txt = []
    for line in lines[1:]:
        line = line.strip('\n').strip(' ').split()
        line = [int(w) for w in line]
        txt.append(line)
    # smarter_papa(txt)
    scc_2sat(txt)

# 1 is a yes
# 2 is a no
# 3 is a yes
# 4 is a yes
# 5 is a no
# 6 is a no
# 101100