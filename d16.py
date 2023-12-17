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


def get_forward(i, j, dir):
    if dir == 0:
        return i, j + 1
    elif dir == 1:
        return i + 1, j
    elif dir == 2:
        return i, j - 1
    elif dir == 3:
        return i - 1, j
    return None


def energize(beams):
    steps = 0
    last = 0
    seen = set()
    seen_keys = set()
    while True:
        keys = []
        for key in beams:
            if key not in seen_keys:
                keys.append(key)
        if len(keys) == 0:
            break
        for key in keys:
            i, j, dir = key
            count = beams[key]
            seen_keys.add(key)

            if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
                continue

            seen.add((i, j))
            beams[key] = 0

            if grid[i][j] == '.':
                i2, j2 = get_forward(i, j, dir)
                beams[(i2, j2, dir)] = beams.get((i2, j2, dir), 0) + count
            elif grid[i][j] == '/':
                if dir == 0:
                    new_dir = 3
                elif dir == 1:
                    new_dir = 2
                elif dir == 2:
                    new_dir = 1
                elif dir == 3:
                    new_dir = 0
                else:
                    new_dir = -1
                i2, j2 = get_forward(i, j, new_dir)
                beams[(i2, j2, new_dir)] = beams.get((i2, j2, new_dir), 0) + count
            elif grid[i][j] == '\\':
                if dir == 0:
                    new_dir = 1
                elif dir == 1:
                    new_dir = 0
                elif dir == 2:
                    new_dir = 3
                elif dir == 3:
                    new_dir = 2
                else:
                    new_dir = -1
                i2, j2 = get_forward(i, j, new_dir)
                beams[(i2, j2, new_dir)] = beams.get((i2, j2, new_dir), 0) + count
            elif grid[i][j] == '-':
                if dir == 0 or dir == 2:
                    i2, j2 = get_forward(i, j, dir)
                    beams[(i2, j2, dir)] = beams.get((i2, j2, dir), 0) + count
                else:
                    i2, j2 = get_forward(i, j, 0)
                    i3, j3 = get_forward(i, j, 2)
                    beams[(i2, j2, 0)] = beams.get((i2, j2, 0), 0) + count
                    beams[(i3, j3, 2)] = beams.get((i3, j3, 2), 0) + count
            elif grid[i][j] == '|':
                if dir == 1 or dir == 3:
                    i2, j2 = get_forward(i, j, dir)
                    beams[(i2, j2, dir)] = beams.get((i2, j2, dir), 0) + count
                else:
                    i2, j2 = get_forward(i, j, 1)
                    i3, j3 = get_forward(i, j, 3)
                    beams[(i2, j2, 1)] = beams.get((i2, j2, 1), 0) + count
                    beams[(i3, j3, 3)] = beams.get((i3, j3, 3), 0) + count

    return len(seen)


lines = readFile("d16input.txt")
#lines = readFile("test.txt")
grid = gdu.convert_to_grid(lines)
beams = {(0, 0, 0):  1}

print(energize(beams))

best = 0
for i in range(len(grid)):
    beams = {(i, 0, 0): 1}
    result = energize(beams)
    if result > best:
        best = result
    beams = {(i, len(grid[i]) - 1, 2): 1}
    result = energize(beams)
    if result > best:
        best = result
for j in range(len(grid[0])):
    beams = {(0, j, 1): 1}
    result = energize(beams)
    if result > best:
        best = result
    beams = {(len(grid) - 1, j, 3): 1}
    result = energize(beams)
    if result > best:
        best = result
print(best)
