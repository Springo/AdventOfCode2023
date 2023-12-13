import graph_util as gu
# functions: transpose, bfs, top_sort, scc
import grid_util as gdu
# functions: convert_to_grid, serialize, get_neighbors, count_val, grid_project


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def adj_man_dist(i1, j1, i2, j2, expand_i, expand_j, exp_size):
    raw_dist = abs(i1 - i2) + abs(j1 - j2)
    for i in expand_i:
        if min(i1, i2) < i < max(i1, i2):
            raw_dist += exp_size
    for j in expand_j:
        if min(j1, j2) < j < max(j1, j2):
            raw_dist += exp_size
    return raw_dist


def get_all_distances(gals, exp_size):
    total = 0
    for i in range(len(gals)):
        for j in range(i + 1, len(gals)):
            i1, j1 = gals[i]
            i2, j2 = gals[j]
            total += adj_man_dist(i1, j1, i2, j2, expand_i, expand_j, exp_size)
    return total


lines = readFile("d11input.txt")
grid = gdu.convert_to_grid(lines)

gals = []
expand_i = []
expand_j = []
for k in range(len(grid)):
    ex_i = True
    ex_j = True
    for i in range(len(grid)):
        if grid[i][k] != '.':
            ex_i = False
    for j in range(len(grid[k])):
        if grid[k][j] != '.':
            ex_j = False
    if ex_i:
        expand_j.append(k)
    if ex_j:
        expand_i.append(k)

for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == '#':
            gals.append((i, j))

print(get_all_distances(gals, 1))
print(get_all_distances(gals, 999999))
