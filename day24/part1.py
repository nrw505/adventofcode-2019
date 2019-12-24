#!/usr/bin/env python3

import sys
import math
import re
import time

from grid import Grid

infile = open(sys.argv[1])

start = Grid()
start.read_from(infile)

def adjacent(pos, grid):
    ret = [
        x
        for x in [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1),
        ]
        if x in grid
    ]
    return ret
    
def iterate(pre):
    post = Grid()
    for pos in pre.places:
        live_nearby = len([x for x in adjacent(pos, pre) if pre[x] == '#'])
        post[pos] = pre[pos]
        if pre[pos] == '#' and live_nearby != 1:
            post[pos] = '.'
        if pre[pos] == '.' and live_nearby in (1,2):
            post[pos] = '#'
    return post

def biodiversity_rating(grid):
    score = 0
    for pos in [x for x in grid.places if grid[x] == '#']:
        score += 2 ** (pos[0] + pos[1] * 5)
    return score

states = []

current = start
n = 0
while str(current) not in states:
    states.append(str(current))
    print(f"State {n}")
    print(current)
    n += 1
    current = iterate(current)

print(f"Final state is {n}")
prev = states.index(str(current))
print(f"Repeats from state {prev}")
print(current)
print(f"rating = {biodiversity_rating(current)}")
