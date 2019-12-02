#!/usr/bin/env python3
import sys
import math

def fuel_for_mass(mass):
    fuel_required = math.floor(mass / 3) - 2
    return fuel_required


total_fuel_required = 0
for line in sys.stdin:
    mass = int(line)
    total_fuel_required += fuel_for_mass(mass)

print(f"Total fuel required: {total_fuel_required}")
