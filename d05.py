def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def consolidate(r_in):
    s_r = sorted(r_in, key=lambda x: x[0])
    out = []
    l = s_r[0][0]
    r = s_r[0][1]
    for i in range(1, len(s_r)):
        l2 = s_r[i][0]
        r2 = s_r[i][1]
        if l2 > r:
            out.append((l, r))
            l = l2
        if r2 > r:
            r = r2
    out.append((l, r))
    return out


def range_out(map, keys, in_ranges):
    out_ranges = []
    for interval in in_ranges:
        l = interval[0]
        r = interval[1]
        done = False
        for key in keys:
            l_key = key[0]
            r_key = key[0] + key[1] - 1
            out_start = map[key]
            if l_key <= l <= r_key:
                if r <= r_key:
                    out_ranges.append((out_start + l - l_key, out_start + r - l_key))
                    done = True
                else:
                    out_ranges.append((out_start + l - l_key, out_start + r_key - l_key))
                    l = r_key + 1

        if not done:
            out_ranges.append((l, r))

    return consolidate(out_ranges)


def process_ranges(maps, keys, start_ranges):
    out_ranges = consolidate(start_ranges)
    for name in names:
        out_ranges = range_out(maps[name], keys[name], out_ranges)
    return out_ranges


lines = readFile("d05input.txt")

names = []
keys = dict()
maps = dict()
seeds = [int(x) for x in lines[0].split(': ')[1].split()]

new_map = dict()
new_keys = []
for line in lines[2:]:
    if len(line) <= 0:
        new_keys = sorted(new_keys, key=lambda x: x[0])
        maps[names[-1]] = new_map
        keys[names[-1]] = new_keys

    elif not line[0].isdigit():
        names.append(line)
        new_map = dict()
        new_keys = []
    else:
        ls = line.split()
        key = (int(ls[1]), int(ls[2]))
        new_keys.append(key)
        new_map[key] = int(ls[0])
new_keys = sorted(new_keys, key=lambda x: x[0])
maps[names[-1]] = new_map
keys[names[-1]] = new_keys

start_ranges = [(x, x) for x in seeds]
out_ranges = process_ranges(maps, keys, start_ranges)
print(out_ranges[0][0])

start_ranges = []
for i in range(0, len(seeds), 2):
    start_ranges.append((seeds[i], seeds[i] + seeds[i + 1] - 1))
out_ranges = process_ranges(maps, keys, start_ranges)
print(out_ranges[0][0])
