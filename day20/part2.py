#!/usr/bin/env python3

import sys
import math
import re

from grid import Grid
from grid3 import Grid3


#!/usr/bin/env python3

import sys
import math
import re

from grid import Grid


infile = open(sys.argv[1])
grid2 = Grid()
grid = Grid3()

start = None
portals = {}
neighbours = {}
max_z = 0

y = 0
for line in infile:
    line = line.strip("\n")
    x = 0
    for c in line:
        grid2[(x, y)] = c
        x += 1
    y += 1

def adjacent2(pos):
    return [
        x
        for x in [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1),
        ]
        if x in grid2
    ]

def adjacent(pos):
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
    if pos in neighbours:
        ret.append(neighbours[pos])
    return ret

def is_outer(pos):
    return pos[0] == 2 or pos[1] == 2 or pos[0] == (grid.max_x() - 2) or pos[1] == (grid.max_y() - 2)

def add_portal_endpoint(name, pos1, pos2):
    walkable = [pos for pos in set(adjacent2(pos1) + adjacent2(pos2)) if grid2[pos] == '.'][0]
    if name not in portals:
        portals[name] = []

    portals[name].append(walkable)
    

def find_portals():
    for y in range(grid2.max_y() + 1):
        for x in range(grid2.max_x() + 1):
            a = grid2[(x,y)]
            if a.isupper():
                if (x+1, y) in grid2:
                    b = grid2[(x+1, y)]
                    if b.isupper():
                        add_portal_endpoint(a+b,(x, y), (x+1, y))
                        continue
                if (x, y+1) in grid2:
                    b = grid2[(x, y+1)]
                    if b.isupper():
                        add_portal_endpoint(a+b,(x, y), (x, y+1))
                        continue

def connect_portals(z):
    def connect(a, b):
        if is_outer(a):
            if z > 0:
                neighbours[(a[0], a[1], z)] = (b[0], b[1], z-1)
        else:
            neighbours[(a[0], a[1], z)] = (b[0], b[1], z+1)

    for portal in portals:
        ends = portals[portal]
        (end1, end2) = ends
        connect(end1, end2)
        connect(end2, end1)

def find_max_z(places):
    return max([pos[2] for pos in places])

def breadth_first_distance(start, end):
    global max_z
    distance = 1
    done = set()
    next_iteration = adjacent(start)
    while next_iteration:
        this_iteration = next_iteration
        next_iteration = []

        # extend grid3 to another level if necessary
        this_max_z = find_max_z(this_iteration)
        while this_max_z > max_z:
            max_z += 1
            grid.add_z_layer(max_z, grid2)
            connect_portals(max_z)

        for pos in this_iteration:
            done.add(pos)
            if grid[pos] != '.':
                continue
            if pos == end:
                return distance;
            next_iteration.extend([next for next in adjacent(pos) if next not in done])
        print(f"checked up to {distance} steps")
        distance += 1
    return None
        
find_portals()
start = portals['AA'][0]
end   = portals['ZZ'][0]
start = (start[0], start[1], 0)
end   = (  end[0],   end[1], 0)
del portals['AA']
del portals['ZZ']

grid.add_z_layer(0, grid2)
connect_portals(0)

distance = breadth_first_distance(start, end)
print(f"distance is {distance}")
