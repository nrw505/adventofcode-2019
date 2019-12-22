#!/usr/bin/env python3

import sys
import itertools
import math

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

class FactoryDeck:
    def __init__(self, length):
        self.length = length

    def nth(self, n):
        return n

class DealtIntoNewStack:
    def __init__(self, previous):
        self.previous = previous
        self.length = previous.length

    def nth(self, n):
        return self.previous.nth(self.length - n - 1)

class Cut:
    def __init__(self, previous, cut):
        self.previous = previous
        self.length = previous.length
        self.cut = cut

    def nth(self, n):
        return self.previous.nth((n + self.cut) % self.length)

class DealtWithIncrement:
    def __init__(self, previous, increment):
        self.previous = previous
        self.length = previous.length
        self.increment = increment
        self.modinv = modinv(self.increment, self.length)

    def nth(self, n):
        previndex = (self.modinv * n) % self.length
        return self.previous.nth(previndex)

#cards = DealtIntoNewStack(FactoryDeck(10))
#print([cards.nth(n) for n in range(cards.length)])

#cards = Cut(FactoryDeck(10), 3)
#print([cards.nth(n) for n in range(cards.length)])

#cards = Cut(FactoryDeck(10), -4)
#print([cards.nth(n) for n in range(cards.length)])

#cards = DealtWithIncrement(FactoryDeck(10), 3)
#print([cards.nth(n) for n in range(cards.length)])

def process_file(deck, fh):
    for line in fh:
        line = line.strip("\n")
        parts = line.split(" ")
        #print(line)
        if line == "deal into new stack":
            deck = DealtIntoNewStack(deck)
        elif parts[0] == 'cut':
            num = int(parts[1])
            deck = Cut(deck, num)
        elif parts[0] == 'deal' and parts[1] == 'with' and parts[2] == 'increment':
            num = int(parts[3])
            deck = DealtWithIncrement(deck, num)
        #print([deck.nth(n) for n in range(deck.length)])
    return deck

decksize = 119315717514047
cards = FactoryDeck(decksize)
#cards = FactoryDeck(10007)
#cards = FactoryDeck(10)

infile = open(sys.argv[1])
cards = process_file(cards, infile)

#print([cards.nth(n) for n in range(cards.length)])
#exit(0)


x = 2020
y = cards.nth(2020)

infile.seek(0)
cards = process_file(cards, infile)

z = cards.nth(2020)

print(f"x = {x}")
print(f"y = {y}")
print(f"z = {z}")

a = ((z - y) * modinv(y - x, decksize)) % decksize

print(f"a = {a}")

b = (y - a * x) % decksize

print(f"b = {b}")

def mathy_nth(n):
    return ((a * n) + b) % decksize
# double check

i1 = mathy_nth(2020)

print(f"i1 = {i1}")
assert i1 == y

i2 = mathy_nth(i1)

print(f"i2 = {i2}")
assert i2 == z

def mathy_nth_after_k_iterations(k, n):
    return (
        pow(a, k, decksize) * n +
        ((pow(a, k, decksize) - 1) * modinv(a - 1, decksize) * b) % decksize
    ) % decksize

print(mathy_nth_after_k_iterations(101741582076661, 2020))
