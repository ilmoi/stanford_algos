# with open('SCC.txt') as f:
#     Big_G = []
#     for l in f.readlines():
#         edge = l.strip('\n').strip().split(' ')
#         for e in range(len(edge)):
#           edge[e] = int(edge[e])
#         Big_G.append(edge)
# print(Big_G)

num_nodes = 875715
gr = [[] for i in range(num_nodes)]

file = open('SCC.txt', 'r')
data = file.readlines()
for line in data:
    items = line.split()
    gr[int(items[0])] += [int(items[1])]
    gr[int(items[1])] += [int(items[0])]

print(gr)