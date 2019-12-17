#!/usr/bin/env python3

def fft(numbers):
    size = len(numbers)
    output = [0] * size

    output[size - 1] = numbers[size - 1]
    for i in range(size - 1, 0, -1):
        output[i - 1] = (numbers[i - 1] + output[i]) % 10
    return output


infile = open(sys.argv[1])
line = infile.readline()

numbers = [int(c) for c in line] * 10000
offset = int("".join([str(c) for c in numbers[0:7]]))

print(f"len is {len(numbers)}")
print(f"offset is {offset}")
numbers = numbers[offset:]
for i in range(100):
    numbers = fft(numbers)
    print(f"done iteration {i}")

message = numbers[0:8]

print("".join([str(c) for c in message]))
