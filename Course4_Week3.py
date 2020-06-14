# heuristic for TSM
import math


def distance(city1, city2):
    # print(city1, city2)
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def better_merge_sort(L, current):
    """Wow this really is a ton slower than the built-in sorted().
    Ended up not using for that reasons."""

    if len(L) <= 1:
        return L
    else:
        n = len(L)
        mid = n // 2
        left = better_merge_sort(L[:mid], current)
        right = better_merge_sort(L[mid:], current)
        i, j = 0, 0

        for k in range(n):
            if distance(left[i][1], current[1]) < distance(right[j][1],
                                                           current[1]):
                L[k] = left[i]
                i += 1
                if i == len(left):
                    L[k + 1:] = right[j:]
                    return L
            elif distance(left[i][1], current[1]) > distance(right[j][1],
                                                             current[1]):
                L[k] = right[j]
                j += 1
                if j == len(right):
                    L[k + 1:] = left[i:]
                    return L
            else:
                if left[i][0] <= right[j][0]:
                    L[k] = left[i]
                    i += 1
                    if i == len(left):
                        L[k + 1:] = right[j:]
                        return L
                else:
                    L[k] = right[j]
                    j += 1
                    if j == len(right):
                        L[k + 1:] = left[i:]
                        return L


def tsm_heuristic(coords):
    """Heuristic solution to the TSM problem. Not 100% correct, but much much faster.
    Implemented as per lecture slides. See algo2slides / Part 18.
    (note they didn't actually show the TSM algo, but it was described in the exercise itself)"""

    start = coords.pop(0)
    print(f"starting at {start}")
    current = start
    total_d = 0
    j = 0
    while len(coords) > 0:
        print(j)
        j += 1
        coords = better_merge_sort(coords, current)
        new = coords.pop(0)
        # print(new)
        total_d += distance(current[1], new[1])
        current = new
    total_d += distance(current[1], start[1])
    print(total_d)


# ==============================================================================
# RUNNING & DATA

coords = [(1, (1, 2)), (5, (5, 6)), (3, (5, 6)), (4, (6, 7)), (2, (2, 3))]
# tsm_heuristic(coords)

with open('nn.txt') as f:
    lines = f.readlines()
    final_lines = []
    for line in lines[1:]:
        split_line = line.strip('\n').strip('').split()
        split_line = [int(split_line[0]),[float(split_line[1]), float(split_line[2])]]
        final_lines.append(split_line)
    # final_lines = final_lines[1:]
    print(final_lines[:5])
    tsm_heuristic(final_lines)
