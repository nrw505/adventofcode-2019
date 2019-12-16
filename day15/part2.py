#!/usr/bin/env python3

import sys
import math
import re

from intcode import IntCodeVM
from threading import Thread
from queue import Queue

UNKNOWN = " "
EMPTY = "."
OXYGEN = "*"
WALL = "#"

class Room:
    def __init__(self):
        self.places = {(0,0): EMPTY}

    def place(self, x, y, tile):
        self.places[(x, y)] = tile

    def print(self):
        min_x = min([loc[0] for loc in self.places])
        min_y = min([loc[1] for loc in self.places])
        max_x = max([loc[0] for loc in self.places])
        max_y = max([loc[1] for loc in self.places])
        
        origin_x = -min_x
        origin_y = -min_y

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        canvas = []
        for y in range(height):
            canvas.append([" "] * width)

        for place in self.places:
            canvas[origin_y + place[1]][origin_x + place[0]] = self.places[place]

        for line in canvas:
            print("".join(line))
        

def run_vm(vm):
    vm.run()

def adjacent(place):
    return [(place[0], place[1] - 1),
            (place[0], place[1] + 1),
            (place[0] - 1, place[1]),
            (place[0] + 1, place[1])]

DIRECTIONS = { 1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0) }
REVERSE = {1: 2, 2: 1, 3: 4, 4: 3}

class Mapper:
    def __init__(self, memory):
        self.output_queue = Queue()
        self.input_queue = Queue()
        # _our_ output queue is _their_ input queue and vice versa
        self.vm = IntCodeVM(memory, self.output_queue, self.input_queue)
        self.thread = Thread(target=run_vm, args=[self.vm])
        self.thread.start()
        self.room = Room()
        self.robot = (0,0)
        self.path = [(0,0)]

    def recursive_map(self, direction):
        start_pos = self.robot
        dest_pos = (self.robot[0] + DIRECTIONS[direction][0],
                    self.robot[1] + DIRECTIONS[direction][1])

        
        if dest_pos in self.path:
            return

        self.output_queue.put(direction)
        result = self.input_queue.get()
        if result == 0:
            self.room.place(dest_pos[0], dest_pos[1], WALL)
            return
        if result == 1:
            self.room.place(dest_pos[0], dest_pos[1], EMPTY)
            self.robot = dest_pos
            self.path.append(self.robot)
            for d in [1, 2, 3, 4]:
                self.recursive_map(d)
            self.output_queue.put(REVERSE[direction])
            result = self.input_queue.get()
            if result != 1:
                raise Exception("Failed to reverse!")
            self.robot = start_pos
            self.path.pop()
            return
        if result == 2:
            self.room.place(dest_pos[0], dest_pos[1], OXYGEN)
            self.oxygen = dest_pos
            print(f"Found Oxygen after {len(self.path)} steps")
            self.output_queue.put(REVERSE[direction])
            result = self.input_queue.get()
            if result != 1:
                raise Exception("Failed to reverse!")
            return
        raise Exception(f"Unknown response {response}")

    def mapit(self):
        for d in [1, 2, 3, 4]:
            self.recursive_map(d)

    def fill(self):
        minutes = 0
        empty = [place for place in self.room.places if self.room.places[place] == EMPTY]
        oxygen = [place for place in self.room.places if self.room.places[place] == OXYGEN]
        while empty:
            for place in oxygen:
                for adj in adjacent(place):
                    if self.room.places[adj] == EMPTY:
                        self.room.places[adj] = OXYGEN
            empty = [place for place in self.room.places if self.room.places[place] == EMPTY]
            oxygen = [place for place in self.room.places if self.room.places[place] == OXYGEN]
            minutes += 1
        
        print(f"full after {minutes} mintues")
        

infile = open(sys.argv[1])
line = infile.readline()
memory = [int(x) for x in line.split(",")]

mapper = Mapper(memory)
mapper.mapit()
mapper.room.print()
mapper.fill()
