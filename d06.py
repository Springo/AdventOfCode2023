import math
from time import time


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def get_result(times, distances):
    total = 1
    for i in range(len(times)):
        count = 0
        time = times[i]
        for t in range(time):
            if (time - t) * t > distances[i]:
                count += 1
        total *= count
    return total


def get_result_2(times, distances):
    total = 1
    for i in range(len(times)):
        t = times[i]
        d = distances[i]
        r1 = math.ceil((-t + (t ** 2 - 4 * d) ** 0.5) * 0.5) - 1
        r2 = math.floor((-t - (t ** 2 - 4 * d) ** 0.5) * 0.5) + 1
        total *= (r1 - r2 + 1)
    return total


lines = readFile("d06input.txt")
times = [int(x) for x in lines[0].split(":")[1].strip().split()]
distances = [int(x) for x in lines[1].split(":")[1].strip().split()]

print(get_result(times, distances))
print(get_result_2(times, distances))

times = [int("".join(map(str, times)))]
distances = [int("".join(map(str, distances)))]

t1 = time()
print(get_result(times, distances))
t2 = time()
print("original time: {}".format(t2 - t1))
t1 = time()
print(get_result_2(times, distances))
t2 = time()
print("new time: {}".format(t2 - t1))
