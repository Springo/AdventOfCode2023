import math


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


lines = readFile("d08input.txt")
commands = lines[0]
map = dict()
for line in lines[2:]:
    ls = line.split(' = ')
    lss = ls[1][1:-1].split(', ')
    map[ls[0]] = (lss[0], lss[1])

starts = []
cur = []
s_done = set()
loop_start = dict()
loop_length = dict()
for key in map:
    if key[-1] == 'A':
        starts.append(key)
        cur.append(key)

done = False
iter = 0
while not done:
    iter += 1
    for i in range(len(starts)):
        c = commands[(iter - 1) % len(commands)]
        if c =='L':
            cur[i] = map[cur[i]][0]
        else:
            cur[i] = map[cur[i]][1]

        if starts[i] not in s_done and cur[i][-1] == 'Z':
            if starts[i] not in loop_start:
                loop_start[starts[i]] = iter
            else:
                s_done.add(starts[i])
                loop_length[starts[i]] = iter - loop_start[starts[i]]

    if len(s_done) == len(starts):
        done = True

print(loop_start['AAA'])
print(math.lcm(*loop_length.values()))
