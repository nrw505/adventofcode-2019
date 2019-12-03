#!/usr/bin/env python3

import sys


class WireSpace:
    def __init__(self):
        self.point = (0, 0)
        self.counter = 0
        self.wire = set([self.point])
        self.distances = {}

    def extend(self, instruction):
        direction = instruction[0]
        count = int(instruction[1:])

        increment = (0, 0)
        if direction == "U":
            increment = (0, 1)
        elif direction == "D":
            increment = (0, -1)
        elif direction == "L":
            increment = (-1, 0)
        elif direction == "R":
            increment = (1, 0)
        else:
            raise Exception(f"bad direction {direction}")

        for _ in range(count):
            self.point = (self.point[0] + increment[0], self.point[1] + increment[1])
            self.counter += 1
            self.wire.add(self.point)
            if self.point not in self.distances:
                self.distances[self.point] = self.counter

    def process(self, instructions):
        for instruction in instructions:
            self.extend(instruction)


infile = open(sys.argv[1])

wire_1 = WireSpace()
wire_2 = WireSpace()

wire_1_def = infile.readline()
wire_2_def = infile.readline()

wire_1_instructions = wire_1_def.split(",")
wire_2_instructions = wire_2_def.split(",")

wire_1.process(wire_1_instructions)
wire_2.process(wire_2_instructions)

intersection = wire_1.wire.intersection(wire_2.wire)
intersection.remove((0, 0))


def distance_from_origin(point):
    return abs(point[0]) + abs(point[1])


def distance_via_path(point):
    return wire_1.distances[point] + wire_2.distances[point]


closest = min(intersection, key=distance_via_path)

print(f"closest is {distance_via_path(closest)} away")
