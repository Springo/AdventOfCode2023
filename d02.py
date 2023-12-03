def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


lines = readFile("d02input.txt")

count = 0
power = 0
for (i, line) in enumerate(lines):
    line = line.split(':')[1]
    line = line[1:]

    valid = True
    red_count = 0
    green_count = 0
    blue_count = 0

    ls = line.split(';')
    for l1 in ls:
        red = 0
        blue = 0
        green = 0
        l1s = l1.split(', ')
        for l2 in l1s:
            l2s = l2.split()
            if l2s[1] == "red":
                red += int(l2s[0])
            elif l2s[1] == "green":
                green += int(l2s[0])
            elif l2s[1] == "blue":
                blue += int(l2s[0])

        if red > 12 or green > 13 or blue > 14:
            valid = False
        red_count = max(red_count, red)
        green_count = max(green_count, green)
        blue_count = max(blue_count, blue)

    if valid:
        count += i + 1
    power += red_count * green_count * blue_count

print(count)
print(power)
