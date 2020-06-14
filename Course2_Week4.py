# sum must be between -10 and 10, inclusive
# only distinct elems
Test_A = [3,5,7,5,4,20]

def count_matches(A):
    """Algo to count matches using hash tables.
    Implemented as per lecture slides. See algo1slides / Part 14."""

    hash_table = {}
    for i in A:
        hash_table[i] = 0
    print(hash_table)

    found_hash_table = {}

    for t in range(-10000, 10001):
        # if t % 500 == 0:
        print(f"t is {t}")
        for k in hash_table:
            # print(k)
            if t-k in hash_table and k != t-k:
                found_hash_table[t] = 1
                break
                # print(k, t-k)

    print(found_hash_table)
    print(len(found_hash_table))


# count_matches(Test_A)

with open('1milints.txt') as f:
    txt = [int(i.strip('\n')) for i in f.readlines()]
    print(txt[:10])
    count_matches(txt)

    #runs for 45 min