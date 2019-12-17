#!/usr/bin/env python3

def pattern_for_element(element):
    return [0] * element + [1] * element + [0] * element + [-1] * element


def fft(numbers):
    output = []
    for i in range(len(numbers)):
        pattern = pattern_for_element(i + 1)
        while len(pattern) < len(numbers) + 1:
            pattern = pattern * 2

        pattern = pattern[1:]
        parts = []
        for j in range(len(numbers)):
            parts.append(numbers[j] * pattern[j])
        output.append(int(str(sum(parts))[-1]))

    return output

infile = open(sys.argv[1])
line = infile.readline()
numbers = [int(c) for c in line]

for i in range(100):
    numbers = fft(numbers)

print("".join([str(c) for c in numbers[0:8]]))
