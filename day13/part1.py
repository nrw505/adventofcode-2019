#!/usr/bin/env python3

import sys
import math
import re

from intcode import IntCodeVM

EMPTY = " "
WALL = "#"
BLOCK = "-"
PADDLE = "_"
BALL = "*"

CODES = {0: EMPTY, 1: WALL, 2: BLOCK, 3: PADDLE, 4: BALL}


class Screen:
    def __init__(self):
        self.height = 1
        self.width = 1
        self.positions = [[EMPTY]]
        self.inputs = []
        self.places = {}

    def place(self, x, y, tile):
        if y >= self.height:
            for i in range(y - self.height + 1):
                line = []
                for j in range(self.width):
                    line.append(EMPTY)
                self.positions.append(line)
            self.height = y - 1
        if x >= self.width:
            for line in self.positions:
                for j in range(x - len(line) + 1):
                    line.append(EMPTY)
            self.width = x - 1

        self.positions[y][x] = CODES[tile]
        if CODES[tile] == EMPTY:
            if (x, y) in self.places:
                del self.places[(x, y)]
        else:
            self.places[(x, y)] = CODES[tile]

    def get(self):
        pass

    def put(self, value):
        self.inputs.append(value)
        if len(self.inputs) == 3:
            self.place(*self.inputs)
            self.inputs = []

    def print(self):
        for line in self.positions:
            print("".join(line))


infile = open(sys.argv[1])
line = infile.readline()
memory = [int(x) for x in line.split(",")]

screen = Screen()
vm = IntCodeVM(memory, screen, screen)
vm.run()

blocks = len(screen.places)
breakpoint()

screen.print()

blocks = [k for (k, v) in screen.places.items() if v == BLOCK]
print(f"{blocks} blocks on screen")
