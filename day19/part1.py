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
        self.points = 0
        self.grid = Grid()
        for x in range(50):
            for y in range(50):
                pos = (x,y)
                print(f"scanning {pos}")
                res = self.scan(pos)
                c = " "
                if res > 0:
                    self.points += 1
                    c = "#"
                self.grid[pos] = c


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
print(reader.points)
reader.grid.print()
