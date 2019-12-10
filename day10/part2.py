#!/usr/bin/env python3

import sys
import math

infile = open(sys.argv[1])

data = []
counts = []

asteroids = set()

for line in infile:
    line = line.strip()
    data.append(line)
    counts.append([0] * len(line))

width = len(data[0])
height = len(data)

for y in range(height):
    for x in range(width):
        if data[y][x] == '#':
            asteroids.add((x, y))

print(f"got {len(asteroids)} asteroids")

def visible_from(asteroid):
    blocked = set()
    others = asteroids - set([asteroid])
    for other in others:
        vector = (other[0] - asteroid[0], other[1] - asteroid[1])
        scale = math.gcd(vector[0], vector[1])
        vector = (vector[0] / scale, vector[1] / scale)
        i = scale + 1
        while (0 <= asteroid[0] + (i * vector[0]) < width) and (0 <= asteroid[1] + (i * vector[1]) < height):
            blocked.add((asteroid[0] + (i * vector[0]), asteroid[1] + (i * vector[1])))
            i += 1
    return others - blocked


for asteroid in asteroids:
    can_see = visible_from(asteroid)
    counts[asteroid[1]][asteroid[0]] = len(can_see)

for line in counts:
    print("".join([str(x) for x in line]))

def count_for_asteroid(asteroid):
    return counts[asteroid[1]][asteroid[0]]
    
best = max(asteroids, key = count_for_asteroid)
count = count_for_asteroid(best)
print(f"best is {best} with {count}")

def angle_from(asteroid, other):
    vector = (other[0] - asteroid[0], other[1] - asteroid[1])

    if vector[0] >= 0 and vector[1] < 0:
        quadrant = 0
    if vector[0] > 0 and vector[1] >= 0:
        quadrant = 1
    if vector[0] <= 0 and vector[1] > 0:
        quadrant = 2
    if vector[0] < 0 and vector[1] <= 0:
        quadrant = 3

    if quadrant % 2 == 0:
        angle = math.atan(float(abs(vector[0])) / float(abs(vector[1])))
    else:
        angle = math.atan(float(abs(vector[1])) / float(abs(vector[0])))
    angle += (quadrant * math.pi / 2)

    return angle

origin = best

def angle_from_origin(asteroid):
    return angle_from(origin, asteroid)

destroyed = []
while len(asteroids) > 1:
    this_pass = list(visible_from(origin))
    this_pass.sort(key=angle_from_origin)
    destroyed = destroyed + this_pass
    asteroids = asteroids - set(this_pass)
    print(f"Laser destroyed {len(this_pass)} this pass")

#for d in destroyed:
#    print(repr(d))
print(f"200th was {destroyed[199]}")
