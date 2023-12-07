from functools import cmp_to_key


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def comp_hands(wildcard=False):
    def rank(h):
        js = 0
        for c in h:
            if c == 'J':
                js += 1

        l1 = 0
        l2 = 0
        c1 = h[0]
        sim = 1
        for c in h[1:]:
            if c == c1:
                sim += 1
            else:
                if not wildcard or c1 != 'J':
                    if sim > l1:
                        l2 = l1
                        l1 = sim
                    elif sim > l2:
                        l2 = sim
                sim = 1
                c1 = c
        if not wildcard or c1 != 'J':
            if sim > l1:
                l2 = l1
                l1 = sim
            elif sim > l2:
                l2 = sim
        if wildcard:
            l1 += js

        if l1 == 5:
            return 6
        elif l1 == 4:
            return 5
        elif l1 == 3:
            if l2 == 2:
                return 4
            else:
                return 3
        elif l1 == 2:
            if l2 == 2:
                return 2
            else:
                return 1
        else:
            return 0

    def c_val(c):
        if c.isdigit():
            return int(c)
        else:
            if c == 'T':
                return 10
            elif c == 'J':
                if wildcard:
                    return 1
                else:
                    return 11
            elif c == 'Q':
                return 12
            elif c == 'K':
                return 13
            elif c == 'A':
                return 14
            else:
                return -1

    def comp(h1, h2):
        r1 = rank(sorted(h1))
        r2 = rank(sorted(h2))

        if r1 > r2:
            return 1
        elif r2 > r1:
            return -1
        else:
            for i in range(len(h1)):
                cv1 = c_val(h1[i])
                cv2 = c_val(h2[i])
                if cv1 > cv2:
                    return 1
                elif cv2 > cv1:
                    return -1
        return 0

    return comp


def get_result(hands, bids, wildcard):
    s_hands = sorted(hands, key=cmp_to_key(comp_hands(wildcard)))
    total = 0
    for i in range(len(s_hands)):
        total += (i + 1) * bids[s_hands[i]]
    return total


lines = readFile("d07input.txt")
hands = []
bids = dict()
for line in lines:
    ls = line.split()
    hands.append(ls[0])
    bids[ls[0]] = int(ls[1])

print(get_result(hands, bids, False))
print(get_result(hands, bids, True))
