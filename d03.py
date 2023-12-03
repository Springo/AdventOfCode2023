import grid_util as gdu


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

lines = readFile("d03input.txt")

grid = gdu.convert_to_grid(lines)
count = 0
gears = dict()
num = ""
symb = False
geared = set()
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] in nums:
            num = num + str(grid[i][j])
            neighs = gdu.get_neighbors(grid, i, j, indices=True)
            for ns in neighs:
                neigh = grid[ns[0]][ns[1]]
                if neigh != '.' and neigh not in nums:
                    symb = True
                if neigh == '*':
                    geared.add(ns)
        else:
            if symb:
                count += int(num)
            if len(num) > 0:
                for ns in geared:
                    if ns not in gears:
                        gears[ns] = []
                    gears[ns].append(int(num))

            num = ""
            symb = False
            geared = set()


print(count)

gearsum = 0
for gear in gears:
    if len(gears[gear]) == 2:
        gearsum += gears[gear][0] * gears[gear][1]

print(gearsum)
