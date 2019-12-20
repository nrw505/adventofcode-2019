#!/usr/bin/env python3

import sys
import math
import re
import operator
from collections import deque

from grid import Grid


infile = open(sys.argv[1])
grid = Grid()

start = None
keys = {}
doors = {}

y = 0
for line in infile:
    line = line.strip()
    x = 0
    for c in line:
        grid[(x, y)] = c
        if c == "@":
            start = (x, y)
        if "a" <= c <= "z":
            keys[c] = (x, y)
        if "A" <= c <= "Z":
            doors[c.lower()] = (x, y)
        x += 1
    y += 1


def adjacent(pos):
    return [
        x
        for x in [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1),
        ]
        if x in grid
    ]


def find_accessible_keys(pos, held_keys, distance=1, already_done=None):
    paths = {}
    blocking_doors = {}

    done = set()
    next_iteration = adjacent(pos)
    if already_done:
        done = already_done.copy()
        next_iteration = [doors[x] for x in doors if doors[x] in done]
        for x in next_iteration:
            done.remove(x)

    while next_iteration:
        this_iteration = next_iteration
        next_iteration = []
        for check in this_iteration:
            c = grid[check]
            done.add(check)
            if c == "#":
                continue
            if c.isupper() and c.lower() not in held_keys:
                blocking_doors[c.lower()] = distance
                continue
            if (
                c.islower()
                and c not in paths
                and c not in held_keys
            ):
                paths[c] = distance
            next_iteration.extend([x for x in adjacent(check) if x not in done])
        distance += 1

    return (paths, blocking_doors, done)

all_paths = {}
def generate_all_paths(pos, held_keys='', distance=1, done=None, already_blocking=''):
    if pos not in all_paths:
        all_paths[pos] = {}

    if not done:
        done = set()

    (paths, blocking_doors, done) = find_accessible_keys(pos, held_keys, distance, done)
    if not paths and not blocking_doors:
        return

    for path in paths:
        all_paths[pos][path] = { "distance": paths[path], "doors": held_keys }

    for door in blocking_doors:
        if door not in already_blocking:
            generate_all_paths(pos, held_keys + door, blocking_doors[door], done, blocking_doors.keys())


def accessible_keys(pos, held_keys):
    accessible = {}
    for key in all_paths[pos]:
        if key not in held_keys and set(all_paths[pos][key]["doors"]).issubset(set(held_keys)):
            accessible[key] = all_paths[pos][key]["distance"]
    return accessible


def leaf_length(pos, path):
    length = 0
    held = ""
    for k in path:
        acc = accessible_keys(pos, held)
        length += acc[k]
        pos = keys[k]
        held += k
    return length


leaf_lengths = {}

explore_from_cache = {}


def explore_from(pos, path):
    held = "".join([x for x in sorted(path)])
    cache_key = (pos, held)
    if cache_key in explore_from_cache:
        return explore_from_cache[cache_key]

    options = accessible_keys(pos, path)
    if not options:
        return (0, "")

    dists = {}
    paths = {}
    for option in options:
        (d, p) = explore_from(keys[option], path + option)
        dists[option] = d + options[option]
        paths[option] = option + p

    shortest = min(dists.items(), key=operator.itemgetter(1))[0]
    ret = (dists[shortest], paths[shortest])

    explore_from_cache[cache_key] = ret
    return ret

generate_all_paths(start)
for key in keys:
    generate_all_paths(keys[key])

(m, p) = explore_from(start, "")
print(f"Length: {m}")
print(f"Path: {p}")
