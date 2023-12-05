def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


lines = readFile("d04input.txt")

card_wins = []
card_nums = []
for line in lines:
    ls = line.split(": ")
    ls2 = ls[1].split(" | ")
    win_nums = set([int(x) for x in ls2[0].split()])
    my_nums = [int(x) for x in ls2[1].split()]
    card_wins.append(win_nums)
    card_nums.append(my_nums)

score = 0
card_count = [1] * len(card_wins)
for i in range(len(card_count)):
    win_count = 0
    for n in card_nums[i]:
        if n in card_wins[i]:
            win_count += 1
    if win_count > 0:
        score += (2 ** (win_count - 1))
    for j in range(win_count):
        card_count[i + j + 1] += card_count[i]

print(score)
print(sum(card_count))
