import grid_util as gdu


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def move_grid(grid):
    new_grid = []
    for j in range(len(grid[0])):
        new_line = []
        cur_load = len(grid)
        for i in range(len(grid)):
            if grid[i][j] == 'O':
                new_line.append('O')
                cur_load -= 1
            elif grid[i][j] == '#':
                cur_load = len(grid) - i - 1
                x = len(new_line)
                while x < i:
                    new_line.append('.')
                    x += 1
                new_line.append('#')
        x = len(new_line)
        while x < len(grid):
            new_line.append('.')
            x += 1
        new_grid.append(new_line)
    return gdu.transpose(new_grid)


def cycle(grid):
    g = grid
    for i in range(4):
        g = gdu.rotate(move_grid(g), 1)
    return g


def get_score(grid):
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'O':
                total += len(grid) - i
    return total


lines = readFile("d14input.txt")
grid = gdu.convert_to_grid(lines)
print(get_score(move_grid(grid)))


seen = dict()
scores = dict()
done = False
g = grid
count = 0
ser = ""
while not done:
    g = cycle(g)
    ser = gdu.serialize(g)
    if ser in seen:
        done = True
    else:
        seen[ser] = count
        scores[count] = get_score(g)
        count += 1

cycle_length = count - seen[ser]
print(scores[(1000000000 - seen[ser]) % cycle_length + seen[ser] - 1])
