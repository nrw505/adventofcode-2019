#!/usr/bin/env python3

import sys
import math
import re
import time

from grid import Grid
from grid3 import Grid3

infile = open(sys.argv[1])

start = Grid()
start.read_from(infile)

def adjacent(pos, grid):
    ret = [
        x
        for x in [
            (pos[0] + 1, pos[1], pos[2]),
            (pos[0] - 1, pos[1], pos[2]),
            (pos[0], pos[1] + 1, pos[2]),
            (pos[0], pos[1] - 1, pos[2]),
        ]
        if x in grid
    ]

    # If we're on the outer edge, we have neighbours around the middle
    # of our enclosing grid.
    if pos[0] == 0:
        ret.append((1, 2, pos[2] - 1))
    if pos[0] == 4:
        ret.append((3, 2, pos[2] - 1))
    if pos[1] == 0:
        ret.append((2, 1, pos[2] - 1))
    if pos[1] == 4:
        ret.append((2, 3, pos[2] - 1))

    # If we're on the inner edge, we have many neighbours from the
    # grid we enclose
    if pos[0] == 2 and pos[1] == 1:
        ret.extend([(x, 0, pos[2] + 1) for x in range(5)])
    if pos[0] == 2 and pos[1] == 3:
        ret.extend([(x, 4, pos[2] + 1) for x in range(5)])
    if pos[0] == 1 and pos[1] == 2:
        ret.extend([(0, y, pos[2] + 1) for y in range(5)])
    if pos[0] == 3 and pos[1] == 2:
        ret.extend([(4, y, pos[2] + 1) for y in range(5)])

    return ret
    
def iterate(pre):
    post = Grid3(default='.')

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

empty = Grid()
for x in range(5):
    for y in range(5):
        empty[(x, y)] = '.'
empty[(2,2)] = '?'

start[(2,2)] = '?'
current = Grid3(default='.')

def extend_if_necessary(grid):
    # if the bottom or top layer has any life, add a layer so we check
    # for migration to previously-unrecorded layers.
    z = grid.min_z()
    if any([grid[x] == '#' for x in grid.places if x[2] == z]):
        grid.add_z_layer(z - 1, empty)
    z = grid.max_z()
    if any([grid[x] == '#' for x in grid.places if x[2] == z]):
        grid.add_z_layer(z + 1, empty)

current.add_z_layer(0, start)
extend_if_necessary(current)

n = 0
#while str(current) not in states:
while n != 200:
    states.append(str(current))
    print(f"State {n}")
    print(current)
    n += 1
    current = iterate(current)
    extend_if_necessary(current)

print(f"At state {n}")
print(current)
live = len([x for x in current.places if current[x] == '#'])
print(f"live = {live}")
