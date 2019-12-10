#!/usr/bin/env python3

import sys

infile = open(sys.argv[1])

class Layer:
    def __init__(self):
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

class Image:
    def __init__(self, width, height):
        self.layers = []
        self.width = width
        self.height = height

    def decode_layer(self, data):
        layer = Layer()
        for i in range(self.height):
            start = i * self.width
            end = (i+1) * self.width
            row = data[start : end]
            layer.add_row(row)
        return layer

    def read_from_file(self, io):
        layer_size = self.width * self.height
        data = io.read(layer_size)
        while len(data) == layer_size:
            layer = self.decode_layer(data)
            self.layers.append(layer)
            data = io.read(layer_size)



def count_digits(layer, char):
    digit_counts = [len([c for c in row if c == char]) for row in layer.rows]
    return sum(digit_counts)

def count_zero_digits(layer):
    return count_digits(layer, '0')

def count_one_digits(layer):
    return count_digits(layer, '1')

def count_two_digits(layer):
    return count_digits(layer, '2')

img = Image(25, 6)
img.read_from_file(infile)

min_zeroes_layer = min(img.layers, key=count_zero_digits)

ones = count_one_digits(min_zeroes_layer)
twos = count_two_digits(min_zeroes_layer)

res = ones * twos
print(f"check number is {res}")
