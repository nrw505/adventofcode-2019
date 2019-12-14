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
        self.score = 0
        self.ball = None
        self.paddle = None

    def place(self, x, y, tile):
        if x == -1 and y == 0:
            self.score = tile
            return

        if y >= self.height:
            for i in range(y - len(self.positions) + 1):
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

        if CODES[tile] == BALL:
            self.ball = (x, y)
        if CODES[tile] == PADDLE:
            self.paddle = (x, y)

    def get(self):
        self.refresh()
        if self.paddle[0] < self.ball[0]:
            return 1
        if self.paddle[0] > self.ball[0]:
            return -1
        return 0

    def put(self, value):
        self.inputs.append(value)
        if len(self.inputs) == 3:
            self.place(*self.inputs)
            self.inputs = []

    def print(self):
        for line in self.positions:
            print("".join(line))

    def refresh(self):
        print("\x1b[0;0H")
        self.print()
        print(f"  Score: {self.score}")


infile = open(sys.argv[1])
line = infile.readline()
memory = [int(x) for x in line.split(",")]

screen = Screen()
vm = IntCodeVM(memory, screen, screen)
vm.memory[0] = 2
vm.run()

blocks = len(screen.places)
screen.refresh()


print(f"{screen.score} final score")
