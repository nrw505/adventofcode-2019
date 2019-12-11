#!/usr/bin/env python3

import sys
import math

from intcode import IntCodeVM

infile = open(sys.argv[1])


class Robot:
    def __init__(self, memory):
        self.brain = IntCodeVM(memory, self, self)
        self.white = set()
        self.black = set()
        self.location = (0, 0)
        self.direction = (0, -1)
        self.put_state = 0
        self.white.add(self.location)

    def get(self):
        "What colour is the current location?"
        if self.location in self.white:
            return 1
        return 0

    def put(self, value):
        "Take input from the brain"
        if self.put_state == 0:
            # What to paint
            if value == 0:
                if self.location in self.white:
                    self.white.remove(self.location)
                self.black.add(self.location)
            elif value == 1:
                if self.location in self.black:
                    self.black.remove(self.location)
                self.white.add(self.location)
            else:
                raise Exception("unexpected paint instruction")
            self.put_state = 1
        elif self.put_state == 1:
            # How to turn
            if value == 0:
                # turn left
                self.direction = (-self.direction[1], self.direction[0])
            elif value == 1:
                # turn right
                self.direction = (self.direction[1], -self.direction[0])
            else:
                raise Exception("unexpected turn instruction")
            self.put_state = 0
            self.location = (
                self.location[0] + self.direction[0],
                self.location[1] + self.direction[1],
            )
        else:
            raise Exception("state machine fail")

    def run(self):
        "Go!"
        self.brain.run()


line = open(sys.argv[1]).readline()
memory = [int(x) for x in line.split(",")]

robot = Robot(memory)
robot.run()

positions = robot.white.union(robot.black)

min_x = min([loc[0] for loc in positions])
min_y = min([loc[1] for loc in positions])
max_x = max([loc[0] for loc in positions])
max_y = max([loc[1] for loc in positions])

origin_x = -min_x
origin_y = -min_y

width = max_x - min_x + 1
height = max_y - min_y + 1

canvas = []
for y in range(height):
    canvas.append([" "] * width)

for position in robot.black:
    canvas[origin_y + position[1]][origin_x + position[0]] = " "

for position in robot.white:
    canvas[origin_y + position[1]][origin_x + position[0]] = "#"

for line in canvas:
    line.reverse()
    print("".join(line))
