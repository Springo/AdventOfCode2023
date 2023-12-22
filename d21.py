import graph_util as gu
# functions: transpose, bfs, top_sort, scc
import grid_util as gdu
# functions: convert_to_grid, serialize, get_neighbors, count_val, grid_project

from copy import deepcopy


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def adj_comp(orig_list, new_list=None, comp=1):
    if new_list is None:
        new_list = deepcopy(orig_list)
    if comp <= 1:
        return orig_list

    new_new_list = dict()
    for i, j in new_list:
        new_new_list[(i, j)] = set()
        for i2, j2 in new_list[(i, j)]:
            for i3, j3 in orig_list[(i2, j2)]:
                new_new_list[(i, j)].add((i3, j3))
    return adj_comp(orig_list, new_new_list, comp - 1)


def bfs(grid, start_i, start_j):
    explored = set()
    q = [(start_i, start_j, 0)]
    explored.add((start_i, start_j))
    total = 1
    while len(q) > 0:
        i, j, dist = q.pop(0)
        for i2, j2 in gdu.get_neighbors(grid, i, j, orth=True, indices=True):
            if (i2, j2) not in explored and grid[i2][j2] != '#' and dist < 64:
                if (dist + 1) % 2 == 0:
                    total += 1
                q.append((i2, j2, dist + 1))
                explored.add((i2, j2))
    return total


def bfs_3(grid, start_i, start_j):
    edge_dists = dict()
    explored = set()
    q = [(start_i, start_j, 0)]
    explored.add((start_i, start_j))
    while len(q) > 0:
        i, j, dist = q.pop(0)
        if i == 0 or i == len(grid) - 1 or j == 0 or j == len(grid[i]) - 1:
            edge_dists[(i, j)] = dist
        for i2, j2 in gdu.get_neighbors(grid, i, j, orth=True, indices=True):
            if (i2, j2) not in explored and grid[i2][j2] != '#':
                q.append((i2, j2, dist + 1))
                explored.add((i2, j2))
    return edge_dists


def bfs_2(grid, start_i, start_j, stop=3):
    dists = {(start_i, start_j, 0, 0): 0}
    q = [(start_i, start_j, 0, 0, 0)]
    while len(q) > 0:
        i, j, gi, gj, dist = q.pop(0)
        for dir in [0, 2, 4, 6]:
            gi2 = gi
            gj2 = gj
            i2, j2 = gdu.grid_project(grid, i, j, dir=dir)
            if i2 is None:
                if dir == 0:
                    gj2 += 1
                elif dir == 2:
                    gi2 += 1
                elif dir == 4:
                    gj2 -= 1
                elif dir == 6:
                    gi2 -= 1
                i2, j2 = gdu.grid_project(grid, i, j, dir=dir, wrap=True)

            if grid[i2][j2] != '#' and abs(gi2) <= stop and abs(gj2) <= stop:
                if (i2, j2, gi2, gj2) not in dists:
                    q.append((i2, j2, gi2, gj2, dist + 1))
                    dists[(i2, j2, gi2, gj2)] = dist + 1
    return dists



lines = readFile("d21input.txt")
grid = gdu.convert_to_grid(lines)

adj_list = dict()
start_i = None
start_j = None
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == 'S':
            start_i = i
            start_j = j
        adj_list[(i, j)] = set()
        for i2, j2 in gdu.get_neighbors(grid, i, j, orth=True, indices=True):
            if grid[i2][j2] != '#':
                adj_list[(i, j)].add((i2, j2))


print(len(grid))
print(len(grid[0]))
print(bfs(grid, start_i, start_j))


dists = bfs_2(grid, start_i, start_j)

h_gaps = dict()
v_gaps = dict()
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if (i, j, 0, 0) in dists:
            v_gaps[(i, j)] = dists[(i, j, 3, 3)] - dists[(i, j, 2, 3)]
            h_gaps[(i, j)] = dists[(i, j, 3, 3)] - dists[(i, j, 3, 2)]

steps = 26501365
count = 0
for i in range(len(grid)):
    for j in range(len(grid[i])):
        print(i, j)
        start_gi = -(steps // v_gaps[(i, j)]) - 1
        end_gi = steps // v_gaps[(i, j)] + 1
        start_gj = -(steps // h_gaps[(i, j)]) - 1
        end_gj = steps // h_gaps[(i, j)] + 1

        for gi in range(start_gi, end_gi + 1):
            for gj in range(start_gj, end_gj + 1):
                new_gi = gi
                v_stacks = 0
                if abs(gi) > 3:
                    new_gi = 3
                    v_stacks = gi - 3
                new_gj = gj
                h_stacks = 0
                if abs(gj) > 3:
                    new_gj = 3
                    h_stacks = gj - 3

                dist = dists[(i, j, new_gi, new_gj)] + v_gaps[(i, j)] * v_stacks + h_gaps[(i, j)] * h_stacks
                if dist % 2 == 1 and dist <= steps:
                    count += 1

print(count)
