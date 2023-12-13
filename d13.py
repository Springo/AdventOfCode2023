import grid_util as gdu


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def check_reflect(grid, row, errors_required=0):
    errors = 0
    d = min(row, len(grid) - row)
    for i in range(d):
        for j in range(len(grid[i])):
            if grid[row + i][j] != grid[row - i - 1][j]:
                errors += 1
                if errors > errors_required:
                    return False
    if errors < errors_required:
        return False
    return True


def scan_grids(grids, errors_required):
    total = 0
    for i, grid in enumerate(grids):
        for row in range(1, len(grid)):
            if check_reflect(grid, row, errors_required=errors_required):
                total += 100 * row

        new_grid = gdu.transpose(grid)
        for row in range(1, len(new_grid)):
            if check_reflect(new_grid, row, errors_required=errors_required):
                total += row
    return total


lines = readFile("d13input.txt")
grids = []
cur_grid = []
for line in lines:
    if len(line) > 0:
        cur_grid.append(line)
    else:
        grids.append(gdu.convert_to_grid(cur_grid))
        cur_grid = []
grids.append(gdu.convert_to_grid(cur_grid))

print(scan_grids(grids, 0))
print(scan_grids(grids, 1))
