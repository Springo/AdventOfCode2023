import sys
sys.setrecursionlimit(100000)


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def check_match(line, spacings):
    ls = line.split('.')
    ind = 0
    for g in ls:
        if len(g) == 0:
            continue
        if ind >= len(spacings):
            return False
        if len(g) == spacings[ind]:
            ind += 1
        else:
            return False
    if ind < len(spacings):
        return False
    return True


def count_matches_slow(line, spacings):
    count = 0
    line_len = line.count('?')
    for combo in range(2 ** line_len):
        bs = bin(combo)[2:]
        bs = "".join(['0'] * (line_len - len(bs))) + bs
        new_line = ""
        ind = 0
        for c in line:
            if c == '?':
                if bs[ind] == '0':
                    new_line += "."
                elif bs[ind] == '1':
                    new_line += "#"
                else:
                    print("AHHH")
                ind += 1
            else:
                new_line += c
        if check_match(new_line, spacings):
            count += 1
    return count


def count_matches(line, spacings, memo):
    def check_fit(line, count):
        if count > len(line):
            return False
        for i in range(count):
            if line[i] == '.':
                return False
        if count < len(line) and line[count] == '#':
            return False
        return True

    key = (line, tuple(spacings))
    if key in memo:
        return memo[key]

    if len(spacings) == 0:
        for c in line:
            if c == '#':
                return 0
        return 1

    if len(line) == 0:
        return 0

    total = 0
    if check_fit(line, spacings[0]):
        if len(line) == spacings[0]:
            if len(spacings) == 1:
                total += 1
        else:
            total += count_matches(line[spacings[0] + 1:], spacings[1:], memo)

    if line[0] != '#':
        total += count_matches(line[1:], spacings, memo)

    memo[key] = total
    return total

lines = readFile("d12input.txt")
total = 0
for line in lines:
    ls = line.split()
    spacings = [int(x) for x in ls[1].split(',')]
    memo = dict()
    l_inp = "".join(list(ls[0] + "?") * 5)[:-1]
    spacings = spacings * 5
    count = count_matches(l_inp, spacings, memo)
    print("{}, {}: {}".format(l_inp, spacings, count))
    total += count
print(total)
