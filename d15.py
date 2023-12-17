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


def hash(inp):
    val = 0
    for c in inp:
        val += ord(c)
        val *= 17
        val = val % 256
    return val


lines = readFile("d15input.txt")
#lines = readFile("test.txt")
total = 0
lines = lines[0].split(',')
for line in lines:
    total += hash(line)
print(total)


map = [[] for _ in range(256)]
for line in lines:
    print(map)
    if line.find("=") != -1:
        ls = line.split('=')
        name = ls[0]
        val = int(ls[1])
        found = False
        for i, (n2, val2) in enumerate(map[hash(name)]):
            if n2 == name:
                map[hash(name)][i] = (name, val)
                found = True
        if not found:
            map[hash(name)].append((name, val))
    if line.find("-") != -1:
        name = line[:-1]
        for n2, val in map[hash(name)]:
            if n2 == name:
                map[hash(name)].remove((n2, val))
                break

total = 0
for box in range(len(map)):
    for i, lens in enumerate(map[box]):
        total += (1 + box) * (i + 1) * (lens[1])
print(total)
