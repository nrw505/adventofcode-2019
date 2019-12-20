#!/usr/bin/env python3

import sys
import math
import re

from grid import Grid


infile = open(sys.argv[1])
grid = Grid()

start = None
portals = {}
neighbours = {}

y = 0
for line in infile:
    line = line.strip("\n")
    x = 0
    for c in line:
        grid[(x, y)] = c
        x += 1
    y += 1


def adjacent(pos):
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
    if pos in neighbours:
        ret.append(neighbours[pos])
    return ret

def add_portal_endpoint(name, pos1, pos2):
    walkable = [pos for pos in set(adjacent(pos1) + adjacent(pos2)) if grid[pos] == '.'][0]
    if name not in portals:
        portals[name] = []

    portals[name].append(walkable)
    

def find_portals():
    for y in range(grid.max_y() + 1):
        for x in range(grid.max_x() + 1):
            a = grid[(x,y)]
            if a.isupper():
                if (x+1, y) in grid:
                    b = grid[(x+1, y)]
                    if b.isupper():
                        add_portal_endpoint(a+b,(x, y), (x+1, y))
                        continue
                if (x, y+1) in grid:
                    b = grid[(x, y+1)]
                    if b.isupper():
                        add_portal_endpoint(a+b,(x, y), (x, y+1))
                        continue

def connect_portals():
    for portal in portals:
        ends = portals[portal]
        (end1, end2) = ends
        neighbours[end1] = end2
        neighbours[end2] = end1

def breadth_first_distance(start, end):
    distance = 1
    done = set()
    next_iteration = adjacent(start)
    while next_iteration:
        this_iteration = next_iteration
        next_iteration = []
        for pos in this_iteration:
            done.add(pos)
            if grid[pos] != '.':
                continue
            if pos == end:
                return distance;
            next_iteration.extend([next for next in adjacent(pos) if next not in done])
        distance += 1
    return None
        
find_portals()
start = portals['AA'][0]
end   = portals['ZZ'][0]
del portals['AA']
del portals['ZZ']
connect_portals()

distance = breadth_first_distance(start, end)
print(f"distance is {distance}")
