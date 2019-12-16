#!/usr/bin/env python3

import sys
import math
import re

reactions = {
}

infile = open(sys.argv[1])
for line in infile:
    line = line.strip()
    (consumes, produces) = line.split(" => ")
    quantity, product = produces.split(' ')
    reactions[product] = [int(quantity), [consume.split(" ") for consume in consumes.split(", ")]]

def ore_to_make(item, count):
    if item == 'ORE':
        return count

    (scale, sources) = reactions[item]
    iterations = count // scale
    if count % scale != 0:
        iterations += 1

    return sum([ore_to_make(source[1], int(source[0])) for source in sources]) * iterations

def stuff_to_make(item, count):
    (scale, sources) = reactions[item]
    iterations = count // scale
    if count % scale != 0:
        iterations += 1
    stuff = {}
    for source in sources:
        stuff[source[1]] = int(source[0]) * iterations
    return stuff, (scale * iterations)

outstanding = {"FUEL": 1}
used = {}
left_over = {}

while len(outstanding.keys()) > 1 or "FUEL" in outstanding:
    items = list(outstanding.keys())
    for item in items:
        if item == 'ORE':
            continue
        count = outstanding[item]
        if item in left_over:
            if left_over[item] >= count:
                left_over[item] -= count
                del outstanding[item]
                continue
            count -= left_over[item]
            del left_over[item]
        (needed, produced) = stuff_to_make(item, count)
        for need in needed:
            if need not in outstanding:
                outstanding[need] = 0
            outstanding[need] += int(needed[need])
        del outstanding[item]
        if produced > count:
            if item not in left_over:
                left_over[item] = 0
            left_over[item] += (produced - count)

ore = outstanding["ORE"]
print(f"{ore} ore required")

