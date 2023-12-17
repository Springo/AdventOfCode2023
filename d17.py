import heapq

import grid_util as gdu


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def shortest_path(grid, min_adj, max_adj):
    q = [(0, 0, 0, 0, 0)]
    heapq.heapify(q)
    seen = {(0, 0, 0, 0)}
    while len(q) > 0:
        dist, i, j, dir, streak = heapq.heappop(q)
        for new_dir in [0, 1, 2, 3]:
            if new_dir == (dir + 2) % 4:
                continue
            i2, j2 = gdu.grid_project(grid, i, j, new_dir * 2, step=1)
            if i2 is None:
                continue
            new_streak = 1
            if new_dir == dir:
                if streak >= max_adj:
                    continue
                else:
                    new_streak = streak + 1
            else:
                if streak < min_adj:
                    continue

            if i2 == len(grid) - 1 and j2 == len(grid[0]) - 1:
                return dist + grid[i2][j2]

            key = (i2, j2, new_dir, new_streak)
            if key not in seen:
                heapq.heappush(q, (dist + grid[i2][j2], i2, j2, new_dir, new_streak))
                seen.add(key)
    return -1


lines = readFile("d17input.txt")
grid = gdu.convert_to_grid(lines)
print(shortest_path(grid, min_adj=0, max_adj=3))
print(shortest_path(grid, min_adj=4, max_adj=10))
