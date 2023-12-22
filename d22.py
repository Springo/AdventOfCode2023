import heapq


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def count_dependencies(brick_locs, dependents, dependencies, key):
    disint = {key}
    q = [(brick_locs[key], key)]

    while len(q) > 0:
        _, k = heapq.heappop(q)
        if k not in dependents:
            continue

        for k2 in dependents[k]:
            all_gone = True
            for k3 in dependencies[k2]:
                if k3 not in disint:
                    all_gone = False

            if all_gone:
                disint.add(k2)
                heapq.heappush(q, (brick_locs[k2], k2))

    return len(disint) - 1


bricks = []
lines = readFile("d22input.txt")
for line in lines:
    ls = line.split('~')
    c1 = tuple([int(x) for x in ls[0].split(',')])
    c2 = tuple([int(x) for x in ls[1].split(',')])
    if c1[2] <= c2[2]:
        bricks.append((c1, c2))
    else:
        bricks.append((c2, c1))

bricks = sorted(bricks, key=lambda x: x[0][2])

grid = [[0] * 10 for _ in range(10)]
covered = [[-1] * 10 for _ in range(10)]
brick_locs = []
stable = set()
dependents = dict()
dependencies = dict()

for i, (c1, c2) in enumerate(bricks):
    x1, y1, z1 = c1
    x2, y2, z2 = c2
    cover_set = set()
    if x1 != x2:
        largest = 0
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if grid[x][y1] > largest:
                largest = grid[x][y1]
        for x in range(min(x1, x2), max(x1, x2) + 1):
            c = covered[x][y1]
            if c != -1 and grid[x][y1] == largest:
                cover_set.add(c)
                if c not in dependents:
                    dependents[c] = set()
                dependents[c].add(i)
                if i not in dependencies:
                    dependencies[i] = set()
                dependencies[i].add(c)
            covered[x][y1] = i
            grid[x][y1] = largest + (z2 - z1 + 1)
        brick_locs.append(largest)
    else:
        largest = 0
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if grid[x1][y] > largest:
                largest = grid[x1][y]
        for y in range(min(y1, y2), max(y1, y2) + 1):
            c = covered[x1][y]
            if c != -1 and grid[x1][y] == largest:
                cover_set.add(c)
                if c not in dependents:
                    dependents[c] = set()
                dependents[c].add(i)
                if i not in dependencies:
                    dependencies[i] = set()
                dependencies[i].add(c)
            covered[x1][y] = i
            grid[x1][y] = largest + (z2 - z1 + 1)
        brick_locs.append(largest)
    stable.add(i)
    if len(cover_set) == 1:
        element = next(iter(cover_set))
        if element in stable:
            stable.remove(element)

print(len(stable))
total = 0
for key in dependents:
    total += count_dependencies(brick_locs, dependents, dependencies, key)
print(total)
