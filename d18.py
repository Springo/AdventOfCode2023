from shapely.geometry import Polygon


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def decode(hex_val):
    value = int(hex_val[2:7], 16)
    return value, int(hex_val[7]) * 2


def convert_to_points(steps, dirs):
    points = []
    i = 0
    j = 0
    for k in range(len(steps)):
        step = steps[k]
        dir = dirs[k]
        if dir == 0:
            j += step
        elif dir == 2:
            i += step
        elif dir == 4:
            j -= step
        elif dir == 6:
            i -= step
        points.append((i, j))
    return points


def get_area(points):
    shape = Polygon(points)
    return int(shape.area + (shape.length / 2) + 1)


lines = readFile("d18input.txt")
conv_dir = {
    'R': 0,
    'D': 2,
    'L': 4,
    'U': 6
}

dirs_1 = []
steps_1 = []
dirs_2 = []
steps_2 = []
for line in lines:
    ls = line.split()
    dirs_1.append(conv_dir[ls[0]])
    steps_1.append(int(ls[1]))
    s2, d2 = decode(ls[2])
    dirs_2.append(d2)
    steps_2.append(s2)

print(get_area(convert_to_points(steps_1, dirs_1)))
print(get_area(convert_to_points(steps_2, dirs_2)))
