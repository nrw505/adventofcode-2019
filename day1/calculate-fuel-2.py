#!/usr/bin/env python3
import sys
import math

def fuel_for_mass(mass):
    fuel_required = math.floor(mass / 3) - 2
    if fuel_required <= 0:
        return 0;
    fuel_for_fuel = fuel_for_mass(fuel_required)
    return fuel_required + fuel_for_fuel


total_fuel_required = 0
for line in sys.stdin:
    mass = int(line)
    total_fuel_required += fuel_for_mass(mass)

print(f"Total fuel required: {total_fuel_required}")
