#!/usr/bin/env python3

import sys

start = 124075
end = 580769

def has_adjacent(candidate):
    for x in range(len(candidate)-1):
        if (candidate[x] == candidate[x+1] and
            (x==0 or candidate[x-1] != candidate[x]) and
            (x==len(candidate)-2 or candidate[x+2] != candidate[x])):
            return True
    return False

def is_valid(candidate):
    if int(candidate) < start or int(candidate) > end:
        return False
    if not has_adjacent(candidate):
        return False
    return True

# The rest of the digits all have to be larger than the right-most
# digit so far
def candidates_starting_with(start):
    if len(start) > 5:
        return [start]
    last_digit = int(start[-1])
    next_steps = [start + str(x) for x in range(last_digit, 10)]
    flat = []
    for x in next_steps:
        flat += candidates_starting_with(x)
    return flat


candidates = []
# We know it has to start with 1 to 5, so generate all the candidates
# that match the ever-increasing-digits rule
for x in range(1, 6):
    candidates += candidates_starting_with(str(x))
    
valid = [c for c in candidates if is_valid(c)]
print(f"{len(valid)} valid codes")
