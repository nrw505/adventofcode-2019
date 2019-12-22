#!/usr/bin/env python3

import sys
import itertools
import math

def deal_new(deck):
    return list(reversed(deck))

def cut(deck, count):
    return list(itertools.chain(deck[count:], deck[0:count]))

def deal_with_increment(deck, increment):
    length = len(deck)
    new = [None] * length

    i = 0
    for card in deck:
        new[i] = card
        i = (i + increment) % length

    return new

cards = range(10007)
#cards = range(10)

infile = open(sys.argv[1])
for line in infile:
    line = line.strip("\n")
    parts = line.split(" ")
    #print(line)
    if line == "deal into new stack":
        cards = deal_new(cards)
    elif parts[0] == 'cut':
        num = int(parts[1])
        cards = cut(cards, num)
    elif parts[0] == 'deal' and parts[1] == 'with' and parts[2] == 'increment':
        num = int(parts[3])
        cards = deal_with_increment(cards, num)
    #print(cards)

#print(cards)
index = cards.index(2019)
print(index)
