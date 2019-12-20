#!/usr/bin/env python3

import sys
import math
import re

from grid import Grid


infile = open(sys.argv[1])

from intcode import IntCodeVM
from threading import Thread
from queue import Queue
from grid import Grid


def run_vm(vm):
    vm.run()


def read_memory(f):
    line = f.readline()
    return [int(x) for x in line.split(",")]

CHARS = {0: ' ', 1: '#'}

class BeamReader:
    def scan(self, pos):
        qin = Queue()
        qout = Queue()
        qin.put(pos[0])
        qin.put(pos[1])
        vm = IntCodeVM(self.memory, qin, qout)
        vm.run()
        return qout.get()
        
    def __init__(self, memory):
        self.memory = memory
        
    def map(self, start_x, width, start_y, height):
        grid = Grid()
        for x in range(start_x, start_x + width):
            for y in range(start_y, start_y + height):
                pos = (x, y)
                gridpos = (x-start_x, y-start_y)
                grid[gridpos] = CHARS[self.scan(pos)]

        return grid
        
    def find_bottom(self, x):
        y = x
        while y >= 0:
            beam = self.scan((x, y))
            if beam:
                return y
            y -= 1
        return None

    def beam_right_of(self, pos):
        beam = self.scan(pos)
        if not beam:
            return 0

        right = 0
        while beam:
            right += 1
            beam = self.scan((pos[0] + right, pos[1]))
        return right
        

class IntReader:
    def __init__(self):
        self.buffer = []

    def put(self, value):
        print(value)

    def get(self):
        return int(input())

infile = open(sys.argv[1])
memory = read_memory(infile)

#i = IntReader()
#vm = IntCodeVM(memory, i, i)
#vm.run()

reader = BeamReader(memory)

#grid = reader.map(580, 200, 450, 200)
#grid.print()

for x in range(1040,1200):
    h = reader.find_bottom(x)
    candidate = (x, h-99)
    right = reader.beam_right_of(candidate)
    print(f"{x}: h={h}, pos={candidate}, width={right}")
    if right == 100:
        print(f"fit at {candidate}: {candidate[0] * 10000 + candidate[1]}")
        exit(0)

# 584 * 10000 + 462
