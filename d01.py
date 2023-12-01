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


digits = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def instr(s, w, pos):
    if len(w) > len(s) - pos:
        return False
    else:
        return s[pos:pos + len(w)] == w

# PART 1
lines = readFile("d01input.txt")
total = 0
for line in lines:
    small = -1
    for c in line:
        try:
            small = int(c)
            break
        except:
            continue

    big = -1
    for c in line[::-1]:
        try:
            big = int(c)
            break
        except:
            continue
    total += int(str(small) + str(big))

print(total)


# PART 2
total = 0
for line in lines:
    small = -1
    for i in range(len(line)):
        c = line[i]
        try:
            small = int(c)
            break
        except:
            found = False
            for dig in digits:
                if instr(line, dig, i):
                    small = digits[dig]
                    found = True
            if found:
                break

    big = -1
    for j in range(len(line)):
        i = len(line) - j - 1
        c = line[i]
        try:
            big = int(c)
            break
        except:
            found = False
            for dig in digits:
                if instr(line, dig, i):
                    big = digits[dig]
                    found = True
            if found:
                break
    print(small)
    print(big)
    total += int(str(small) + str(big))

print(total)
