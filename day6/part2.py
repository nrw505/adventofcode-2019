#!/usr/bin/env python3

import sys


class SpaceObject:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def direct_orbit(self):
        return self.parent

    def indirect_orbits(self):
        if self.parent is None:
            return []

        return self.parent.indirect_orbits() + [self.parent]

    def __str__(self):
        return self.name

    def distance(self, ancestor):
        if ancestor == self.parent:
            return 0
        return self.parent.distance(ancestor) + 1


objects = {}

infile = open(sys.argv[1])
for line in infile:
    (parent, child) = line.strip().split(")")
    if parent not in objects:
        objects[parent] = SpaceObject(parent, None)
    if child not in objects:
        objects[child] = SpaceObject(child, None)
    objects[child].parent = objects[parent]

me = objects["YOU"]
santa = objects["SAN"]

my_indirects = me.indirect_orbits()

common = santa.parent
while common not in my_indirects:
    common = common.parent

distance = santa.distance(common) + me.distance(common)

print(f"{distance} transfers to intercept Santa")
