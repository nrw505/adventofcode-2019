#!/usr/bin/env python3

import sys
import math
import re

from intcode import IntCodeVM


class Vector3:
    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"<x={self.x}, y={self.y}, z={self.z}>"


class Body:
    def __init__(self, line):
        line = line.strip()
        match = re.match("<x=([-0-9]+), y=([-0-9]+), z=([-0-9]+)>", line)
        if not match:
            raise Exception("Bad input")
        self.pos = Vector3(match.group(1), match.group(2), match.group(3))
        self.vel = Vector3(0, 0, 0)

    def apply_gravity_from(self, other):
        if other == self:
            return
        if self.pos.x < other.pos.x:
            self.vel.x += 1
        if self.pos.x > other.pos.x:
            self.vel.x -= 1
        if self.pos.y < other.pos.y:
            self.vel.y += 1
        if self.pos.y > other.pos.y:
            self.vel.y -= 1
        if self.pos.z < other.pos.z:
            self.vel.z += 1
        if self.pos.z > other.pos.z:
            self.vel.z -= 1

    def apply_velocity(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.pos.z += self.vel.z

    def potential_energy(self):
        return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)

    def kinetic_energy(self):
        return abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def matches(self, other):
        return str(self) == str(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"pos={self.pos}, vel={self.vel}"


bodies = []
x_start = None
y_start = None
z_start = None

stepnum = 0

x_repeat = None
y_repeat = None
z_repeat = None


def step():
    global stepnum, x_repeat, y_repeat, z_repeat
    for body in bodies:
        for other in bodies:
            body.apply_gravity_from(other)
    for body in bodies:
        body.apply_velocity()
    stepnum += 1

    if x_repeat is None:
        xstate = [(body.pos.x, body.vel.x) for body in bodies]
        if xstate == x_start:
            print(f"at step {stepnum}, X repeats")
            x_repeat = stepnum
    if y_repeat is None:
        ystate = [(body.pos.y, body.vel.y) for body in bodies]
        if ystate == y_start:
            print(f"at step {stepnum}, Y repeats")
            y_repeat = stepnum
    if z_repeat is None:
        zstate = [(body.pos.z, body.vel.z) for body in bodies]
        if zstate == z_start:
            print(f"at step {stepnum}, Z repeats")
            z_repeat = stepnum


infile = open(sys.argv[1])
for line in infile:
    bodies.append(Body(line))

x_start = [(body.pos.x, body.vel.x) for body in bodies]
y_start = [(body.pos.y, body.vel.y) for body in bodies]
z_start = [(body.pos.z, body.vel.z) for body in bodies]

for i in range(1000):
    step()

total_energy = 0
for body in bodies:
    print(body)
    total_energy += body.total_energy()

print(f"total energy = {total_energy}")

while x_repeat is None or y_repeat is None or x_repeat is None:
    step()
    if stepnum % 50000 == 0:
        print(stepnum)


def lcm(a, b):
    return (a * b) // math.gcd(a, b)


total_repeat = lcm(lcm(x_repeat, y_repeat), z_repeat)
print(f"repeats after {total_repeat}")
