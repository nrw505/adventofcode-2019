#!/usr/bin/env python3

import sys
import math
import re

from intcode import IntCodeVM
from threading import Thread
from queue import Queue
from grid import Grid


def run_vm(vm):
    vm.run()


def read_memory(f):
    line = f.readline()
    return [int(x) for x in line.split(",")]


class GridReader:
    def __init__(self):
        self.pos = (0, 0)
        self.grid = Grid()

    def put(self, value):
        if value == 10:
            self.pos = (0, self.pos[1] + 1)
            return
        self.grid[self.pos] = chr(value)
        self.pos = (self.pos[0] + 1, self.pos[1])


infile = open(sys.argv[1])
memory = read_memory(infile)
reader = GridReader()
vm = IntCodeVM(memory, reader, reader)

vm.run()

reader.grid.print()


def adjacent(pos):
    return [
        (pos[0] + 1, pos[1]),
        (pos[0] - 1, pos[1]),
        (pos[0], pos[1] + 1),
        (pos[0], pos[1] - 1),
    ]


def find_intersections(grid):
    scaf = [pos for pos in grid.places if grid[pos] == "#"]
    intersections = []
    for candidate in scaf:
        adjacents = [grid[pos] for pos in adjacent(candidate) if pos in grid]
        if all([adj == "#" for adj in adjacents]) and len(adjacents) == 4:
            intersections.append(candidate)
    return intersections


intersections = find_intersections(reader.grid)
sumal = sum([pos[0] * pos[1] for pos in intersections])
print(sumal)
