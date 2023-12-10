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


def bfs(grid, key, loop, s_left, s_right):
    if key[0] < 0 or key[0] >= len(grid):
        return set()
    if key[1] < 0 or key[1] >= len(grid[0]):
        return set()
    if key in loop or key in s_left or key in s_right:
        return set()

    explored = set()
    q = [key]
    explored.add(key)
    while len(q) > 0:
        i, j = q.pop(0)
        for i2, j2 in gdu.get_neighbors(grid, i, j, indices=True):
            if (i2, j2) not in explored and (i2, j2) not in loop:
                q.append((i2, j2))
                explored.add((i2, j2))
    return explored


def get_ori(start, end):
    si, sj = start
    ei, ej = end
    if si > ei:
        return 0
    if si < ei:
        return 2
    if sj > ej:
        return 3
    if sj < ej:
        return 1
    return -1


def update_sets(grid, cur, s_left, s_right, ori, loop):
    i, j = cur
    if grid[i][j] == 'S':
        return s_left, s_right
    elif grid[i][j] == '-':
        s1 = bfs(grid, (i - 1, j), loop, s_left, s_right)
        s2 = bfs(grid, (i + 1, j), loop, s_left, s_right)
        if ori == 1:
            s_l_new = s1
            s_r_new = s2
        elif ori == 3:
            s_l_new = s2
            s_r_new = s1
    elif grid[i][j] == '|':
        s1 = bfs(grid, (i, j - 1), loop, s_left, s_right)
        s2 = bfs(grid, (i, j + 1), loop, s_left, s_right)
        if ori == 0:
            s_l_new = s1
            s_r_new = s2
        elif ori == 2:
            s_l_new = s2
            s_r_new = s1
    elif grid[i][j] == 'F':
        s1 = bfs(grid, (i - 1, j), loop, s_left, s_right)
        s2 = bfs(grid, (i, j - 1), loop, s_left, s_right)
        if ori == 0:
            s_l_new = s1 | s2
            s_r_new = set()
        elif ori == 3:
            s_l_new = set()
            s_r_new = s1 | s2
    elif grid[i][j] == 'J':
        s1 = bfs(grid, (i + 1, j), loop, s_left, s_right)
        s2 = bfs(grid, (i, j + 1), loop, s_left, s_right)
        if ori == 2:
            s_l_new = s1 | s2
            s_r_new = set()
        elif ori == 1:
            s_l_new = set()
            s_r_new = s1 | s2
    elif grid[i][j] == 7:
        s1 = bfs(grid, (i - 1, j), loop, s_left, s_right)
        s2 = bfs(grid, (i, j + 1), loop, s_left, s_right)
        if ori == 1:
            s_l_new = s1 | s2
            s_r_new = set()
        elif ori == 0:
            s_l_new = set()
            s_r_new = s1 | s2
    elif grid[i][j] == 'L':
        s1 = bfs(grid, (i + 1, j), loop, s_left, s_right)
        s2 = bfs(grid, (i, j - 1), loop, s_left, s_right)
        if ori == 3:
            s_l_new = s1 | s2
            s_r_new = set()
        elif ori == 2:
            s_l_new = set()
            s_r_new = s1 | s2
    return s_left | s_l_new, s_right | s_r_new


def traverse_loop(adj_list, start, loop=None):
    prev = start
    cur = adj_list[start][0]
    count = 1
    loop_set = set()
    exp_left = set()
    exp_right = set()
    ori = get_ori(prev, cur)
    if loop is not None:
        exp_left, exp_right = update_sets(grid, cur, exp_left, exp_right, ori, loop)
    else:
        loop_set.add(cur)
    while cur != start:
        for nex in adj_list[cur]:
            if nex != prev:
                prev = cur
                cur = nex
                count += 1
                ori = get_ori(prev, cur)
                if loop is not None:
                    exp_left, exp_right = update_sets(grid, cur, exp_left, exp_right, ori, loop)
                else:
                    loop_set.add(cur)
                break
    if loop is not None:
        return len(exp_left), len(exp_right)
    else:
        return count, loop_set



lines = readFile("d10input.txt")
#lines = readFile("test.txt")
grid = gdu.convert_to_grid(lines)

adj_list = dict()
si = None
sj = None
for i in range(len(grid)):
    for j in range(len(grid[i])):
        adj_list[(i, j)] = []
        if i > 0 and (grid[i][j] == '|' or grid[i][j] == 'L' or grid[i][j] == 'J'):
            adj_list[(i, j)].append((i - 1, j))
        if j < len(grid[i]) - 1 and (grid[i][j] == '-' or grid[i][j] == 'L' or grid[i][j] == 'F'):
            adj_list[(i, j)].append((i, j + 1))
        if i < len(grid) - 1 and (grid[i][j] == '|' or grid[i][j] == 'F' or grid[i][j] == 7):
            adj_list[(i, j)].append((i + 1, j))
        if j > 0 and (grid[i][j] == '-' or grid[i][j] == 'J' or grid[i][j] == 7):
            adj_list[(i, j)].append((i, j - 1))
        if grid[i][j] == 'S':
            si = i
            sj = j

options = gdu.get_neighbors(grid, si, sj, indices=True)
for opt in options:
    if (si, sj) in adj_list[opt]:
        adj_list[(si, sj)].append(opt)


dist, loop_set = traverse_loop(adj_list, (si, sj))
print(dist // 2)
l1, l2 = traverse_loop(adj_list, (si, sj), loop_set)
print(l2)
