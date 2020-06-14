import itertools

Test_edges = [[1,2,10],[2,3,100],[1,5,10],[1,4,20],[3,4,5]]

def clustering(edges, k):
    """
    clustering algo for computing a max-spacing-k-clustering
    Implemented as per lecture slides. See algo2slides / Part 7.
    """

    # create nodes O(m)
    # for each node assign itself as the group O(n)
    clusters = sorted(set([e[0] for e in edges] + [e[1] for e in edges]))
    # print(clusters)

    # create a dict with counts for each cluster (so we know how to pick smallest)
    cluster_counts = {}
    cluster_pointers = {}
    for c in clusters:
        cluster_counts[c] = cluster_counts.get(c, 1)
        cluster_pointers[c] = [c]
    # print(cluster_counts)
    # print(cluster_pointers)

    # sort edges O(mlogm)
    edges = sorted(edges, key=lambda x: x[2])
    # print(edges[:50])

    # while number of clusters > k
    while len(cluster_counts) > k:
        # print(f"len is {len(cluster_counts)}")
        # pick the next smallest edge
        next_edge = edges[0]
        edges = edges[1:]
        # print(next_edge)

        # check if it would create a cycle (if both edges in same cluster)
        v1, v2 = next_edge[0], next_edge[1]
        c1, c2 = clusters[v1-1], clusters[v2-1] #the two clusters they belong to
        # print(f'chosen edge is {v1}-{v2}, clusters are {c1}, {c2}')
        if c1 == c2:
            # if yes, pop it from edge list (we can't use it)
            # print(f'DO NOTHING')
            pass
        else:
            # if not, pop it from edge list and adjust the smaller pointer
            if cluster_counts[c1] < cluster_counts[c2]:
                # print(f"killing cluster {c1}, pointers are {cluster_pointers[c1]}")
                for pointer in cluster_pointers[c1]:
                    clusters[pointer-1] = c2
                    cluster_pointers[c2].append(pointer)
                    # print(f">>>{clusters[c]}")
                cluster_counts[c2] += cluster_counts[c1]
                del cluster_counts[c1]
                del cluster_pointers[c1]
            else:
                # print(f"killing cluster {c2}, pointers are {cluster_pointers[c2]}")
                for pointer in cluster_pointers[c2]:
                    clusters[pointer-1] = c1
                    cluster_pointers[c1].append(pointer)
                cluster_counts[c1] += cluster_counts[c2]
                del cluster_counts[c2]
                del cluster_pointers[c2]

        # print('-'*100)
        # print(f"assigned clusters are {clusters}")
        # print(f"## are {cluster_counts}")
        # print(f"pointers are {cluster_pointers}")
        # print(edges)

    print(f"## are {cluster_counts}")
    print(edges[:50])

    flag = True
    while flag:
        next_edge = edges[0]
        edges = edges[1:]

        v1, v2 = next_edge[0], next_edge[1]
        c1, c2 = clusters[v1 - 1], clusters[v2 - 1]

        if c1 != c2:
            print(c1, c2, next_edge[2])
            flag = False

# clustering(Test_edges, 2)

# with open('clustering1.txt') as f:
#     edges = [j.strip('\n').split(' ') for j in f.readlines()[1:]]
#     for i in range(len(edges)):
#         for j in range(len(edges[i])):
#             edges[i][j] = int(edges[i][j])
#     print(edges[:5])
    # clustering(edges, 4)

# ==============================================================================
Test_bits = [[0,0,0], [0,0,0], [1,1,1]]
def hamming_distance(L1, L2):
    distance = 0
    for i in range(len(L1)):
        distance += abs(L1[i] - L2[i])
    return distance


def calc_clusters(nodes):
    """My first naive implementation for the advanced clustering problem with 24 bits.
    Not fast enough."""

    # start an empty dict that will hold nodes
    buckets = {}
    for i in range(25):
        buckets[i] = []
    print(buckets)

    j = 0 #counter
    i = 0 #number of cluster
    clusters = {}

    # take the node
    # calc its sum
    # assign to appropriate sum bucket
    for node in nodes:
        node_sum = sum(node)
        # print(f"node is {node}, sum is {node_sum}")
        if j % 1000 == 0:
            print(j)
        j+=1

        # it COULD be within 2 bits of 2 previous sum buckets, and 2 consecutive sum buckets
        # calc the distance with all members there
        # if with some member distance is <3
        # assign them the same cluster
        for relevant_sum in range(max(node_sum-2,0), min(node_sum+2, 24)+1):
            # print(f"relevant sum is {relevant_sum}")
            for relevant_node in buckets[relevant_sum]:
                if hamming_distance(node, relevant_node) <= 2:
                    # print(f"found a match between {node} and {relevant_node}")
                    hashed_node = ''.join([str(n) for n in node])
                    hashed_relevant_node = ''.join([str(n) for n in relevant_node])
                    clusters[hashed_node] = clusters[hashed_relevant_node]
                    break
            else:
                continue
            break
        else: #this triggers if we went through both loops and didn't find a pair
            # else assign their own
            hashed_node = ''.join([str(n) for n in node])
            clusters[hashed_node] = i
            i += 1

        buckets[node_sum].append(node)

    # print(buckets)
    # print(clusters)
    print(f"THERE ARE {i} CLUSTERS")


# calc_clusters(Test_bits)


raw = ["000", "001", "111", "100", "11101"]
from networkx.utils import union_find

def clustering2(raw):
    """Correct, functional implementation for the advanced clustering problem.
    We were given a bunch of 24 bit numbers and had to cluster them into clusters with distance <=2
    Bases on Hamming distance.
    Implementation wasn't given in lecture slides, but I used forums to figure it out.
    """

    # convert nums to ints
    # populate a dict with it
    map = {}
    keys = []
    j=0

    # prepare bitmaps
    single_bitmaps = [1 << i for i in range(24)]
    double_bitmaps = []
    for tup in list(itertools.combinations(range(24), 2)):
        first_pass = 1 << tup[0]
        second_pass = 1 << tup[1]
        double_bitmaps.append(first_pass^second_pass)
    print(double_bitmaps)

    # use bitmaps to generate XORs
    # stick the entire thing into a dict
    # dist0: set(dist0, dist1, dist2)
    for r in raw:
        if j % 1000 == 0:
            print(j)
        j+=1
        int_r = int(r,2)
        keys.append(int_r)
        # print(int_r)
        map[int_r] = []
        map[int_r].extend([int_r^i for i in single_bitmaps])
        map[int_r].extend([int_r^i for i in double_bitmaps])
        # print(map[int_r])
    print("map made!")

    # create a uf with same number of keys as dict
    uf = union_find.UnionFind(keys)

    # start merging
    j = 0 #reset j
    for key in keys:
        if j % 1000 == 0:
            print(j)
        j+=1
        for matching_key in map[key]:
            if matching_key in map:
                uf.union(key,matching_key)

    # convert to set to find number of distinct groups
    s = set([uf[i] for i in uf])
    print(s)
    print(len(s))

# clustering2(raw)

with open('clustering2.txt') as f:
    output = []
    for line in f.readlines():
        line = line.strip('\n').strip(' ')
        letters = line.replace(' ',"")
        # letters = [int(l) for l in letters]
        output.append(letters)
    output = output[1:]
    clustering2(output)