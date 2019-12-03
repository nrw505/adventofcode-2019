#!/usr/bin/env python3


class WireSpace:
    def __init__(self):
        self.point = (0, 0)
        self.wire = set([self.point])

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
            self.wire.add(self.point)

    def process(self, instructions):
        for instruction in instructions:
            self.extend(instruction)


infile = open("input")

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


def distance(point):
    return abs(point[0]) + abs(point[1])


closest = min(intersection, key=distance)

print(f"closest is {distance(closest)} away")
