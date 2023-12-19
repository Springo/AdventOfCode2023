import graph_util as gu
# functions: transpose, bfs, top_sort, scc
import grid_util as gdu
# functions: convert_to_grid, serialize, get_neighbors, count_val, grid_project

from copy import deepcopy


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def eval_work(workflows, regs, work_key='in'):
    for ins in workflows[work_key][:-1]:
        reg, op, val, dest = ins
        in_val = regs[reg]
        if op == '>':
            if in_val > val:
                if dest == 'R':
                    return False
                elif dest == 'A':
                    return True
                return eval_work(workflows, regs, work_key=dest)
        elif op == '<':
            if in_val < val:
                if dest == 'R':
                    return False
                elif dest == 'A':
                    return True
                return eval_work(workflows, regs, work_key=dest)
        else:
            print("AHHH")
    dest = workflows[work_key][-1]
    if dest == 'R':
        return False
    elif dest == 'A':
        return True
    return eval_work(workflows, regs, work_key=dest)


def eval_work_b(workflows, reg_ranges, work_key='in'):
    accepts = []
    rejects = []

    cur_ranges = deepcopy(reg_ranges)
    for ins in workflows[work_key][:-1]:
        reg, op, val, dest = ins
        orig_a, orig_b = cur_ranges[reg]
        a = orig_a - val
        b = orig_b - val
        if op == '<':
            temp = a
            a = -b
            b = -temp
        if a > 0:
            if dest == 'R':
                rejects.append(cur_ranges)
                return accepts, rejects
            elif dest == 'A':
                accepts.append(cur_ranges)
                return accepts, rejects
            else:
                new_acc, new_rej = eval_work_b(workflows, reg_ranges, work_key=dest)
                accepts.extend(new_acc)
                rejects.extend(new_rej)
        elif b > 0:
            a_pass = 1
            b_pass = b
            a_fail = a
            b_fail = 0
            if op == '<':
                temp_pass = a_pass
                temp_fail = a_fail
                a_pass = -b_pass
                a_fail = -b_fail
                b_pass = -temp_pass
                b_fail = -temp_fail
            a_pass += val
            b_pass += val
            a_fail += val
            b_fail += val
            cur_ranges[reg] = (a_fail, b_fail)
            new_ranges = deepcopy(cur_ranges)
            new_ranges[reg] = (a_pass, b_pass)
            if dest == 'R':
                rejects.append(new_ranges)
            elif dest == 'A':
                accepts.append(new_ranges)
            else:
                new_acc, new_rej = eval_work_b(workflows, new_ranges, work_key=dest)
                accepts.extend(new_acc)
                rejects.extend(new_rej)
    dest = workflows[work_key][-1]
    if dest == 'R':
        rejects.append(cur_ranges)
    elif dest == 'A':
        accepts.append(cur_ranges)
    else:
        new_acc, new_rej = eval_work_b(workflows, cur_ranges, work_key=dest)
        accepts.extend(new_acc)
        rejects.extend(new_rej)
    return accepts, rejects


lines = readFile("d19input.txt")
ratings = []
workflows = {}
rate = False
for line in lines:
    if not rate:
        if len(line) > 0:
            ls = line.split('{')
            ls2 = ls[1][:-1].split(',')
            ins = []
            for x in ls2[:-1]:
                xs = x.split(':')
                reg = xs[0][0]
                op = xs[0][1]
                val = int(xs[0][2:])
                dest = xs[1]
                ins.append((reg, op, val, dest))
            ins.append(ls2[-1])
            workflows[ls[0]] = ins
        else:
            rate = True
    else:
        ls = line[1:-1].split(',')
        regs = {}
        for x in ls:
            ls2 = x.split('=')
            regs[ls2[0]] = int(ls2[1])
        ratings.append(regs)


total = 0
for rates in ratings:
    if eval_work(workflows, rates):
        for key in rates:
            total += rates[key]
print(total)


reg_bounds = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
accepts, rejects = eval_work_b(workflows, reg_bounds)
total = 0
for bound_set in accepts:
    combs = 1
    for key in bound_set:
        combs *= (bound_set[key][1] - bound_set[key][0] + 1)
    total += combs
print(total)
