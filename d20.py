from collections import deque
from copy import deepcopy
import math


def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def apply_pulse(modules, pulse_check=None):
    low_n = 0
    high_n = 0
    pulsed = False
    q = deque([(None, "broadcaster", False)])

    while len(q) > 0:
        in_key, out_key, pulse = q.popleft()
        if pulse:
            high_n += 1
        else:
            low_n += 1

        if pulse_check is not None:
            if out_key in pulse_check:
                if not pulse:
                    pulsed = True
        if out_key not in modules:
            continue

        m_type, m_state, m_outs = modules[out_key]
        if m_type == 'b':
            for out in m_outs:
                q.append(("broadcaster", out, pulse))
        elif m_type == '%':
            if not pulse:
                modules[out_key] = (m_type, not m_state, m_outs)
                for out in m_outs:
                    q.append((out_key, out, not m_state))
        elif m_type == '&':
            m_state[in_key] = pulse
            new_pulse = True
            for key in m_state:
                new_pulse = new_pulse and m_state[key]
            for out in m_outs:
                q.append((out_key, out, not new_pulse))
        else:
            print("AHHHH")

    return low_n, high_n, pulsed


modules = {}
mod_pa = {}
lines = readFile("d20input.txt")
for line in lines:
    ls = line.split(' -> ')
    dest = ls[1].split(', ')
    if ls[0] == 'broadcaster':
        modules["broadcaster"] = ('b', None, dest)
    else:
        if ls[0][0] == '%':
            modules[ls[0][1:]] = ('%', False, dest)
        elif ls[0][0] == '&':
            modules[ls[0][1:]] = ('&', {}, dest)

for key in modules:
    if key not in mod_pa:
        mod_pa[key] = []

    m_type, m_state, m_outs = modules[key]
    for out in m_outs:
        if out not in mod_pa:
            mod_pa[out] = []
        mod_pa[out].append(key)

        if out in modules:
            m_type_2, m_state_2, m_outs_2 = modules[out]
            if m_type_2 == '&':
                m_state_2[key] = False

orig_modules = deepcopy(modules)


low_n_total = 0
high_n_total = 0
for i in range(1000):
    low_n, high_n, _ = apply_pulse(modules)
    low_n_total += low_n
    high_n_total += high_n
print(low_n_total * high_n_total)


modules = deepcopy(orig_modules)


i = 0
first_iters = []
while True:
    low_n, high_n, pulsed = apply_pulse(modules, pulse_check=mod_pa[mod_pa["rx"][0]])
    i += 1
    if pulsed:
        first_iters.append(i)

    if len(first_iters) == 4:
        break

print(math.lcm(*first_iters))
