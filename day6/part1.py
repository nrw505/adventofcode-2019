#!/usr/bin/env python3

import sys


class SpaceObject:
    def __init__(self, parent=None):
        self.parent = parent

    def direct_orbit(self):
        return self.parent

    def indirect_orbits(self):
        if self.parent is None:
            return []

        return self.parent.indirect_orbits() + [self.parent]


objects = {}

infile = open(sys.argv[1])
for line in infile:
    (parent, child) = line.strip().split(")")
    if parent not in objects:
        objects[parent] = SpaceObject(None)
    if child not in objects:
        objects[child] = SpaceObject(None)
    objects[child].parent = objects[parent]

count = sum([len(o.indirect_orbits()) for o in objects.values()])

print(f"{count} direct and indirect orbits")
