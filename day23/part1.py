#!/usr/bin/env python3

import sys
import math
import re
import time
from threading import Thread
from queue import Queue, Empty

infile = open(sys.argv[1])

from intcode import IntCodeVM, IntIO, StdIO


def run_vm(vm):
    vm.run()


node_count = 50
nodes = [None] * node_count


class NAT:
    def __init__(self):
        self.pkt = None

    def recv(self, x, y):
        self.pkt = (x, y)

    def run(self):
        while True:
            idles = [node for node in nodes if node.idle]
            if len(idles) == node_count:
                nodes[0].recv(self.pkt[0], self.pkt[1])
                print(f"NAT released {self.pkt} to node 0")


nat = NAT()


class NIC:
    def __init__(self, addr, memory):
        self.addr = addr
        self.addr_loaded = False
        self.pktin = Queue()
        self.vm = IntCodeVM(memory, self, self)
        self.thread = Thread(target=run_vm, args=[self.vm])
        self.state = 0
        self.idle = False
        self.dest = None
        self.x = None
        self.y = None
        self.reading = None

    def recv(self, x, y):
        print(f"{self.addr} received ({x}, {y})")
        self.pktin.put((x, y))

    def get(self):
        if not self.addr_loaded:
            self.addr_loaded = True
            return self.addr

        if self.reading is not None:
            ret = self.reading
            self.reading = None
            print(f"{self.addr} writing {ret}")
            return ret

        try:
            pair = self.pktin.get(timeout=0.01)
        except Empty:
            # print(f"{self.addr} is empty")
            self.idle = True
            return -1

        self.idle = False
        print(f"{self.addr} received {pair}")
        self.reading = pair[1]
        print(f"{self.addr} writing {pair[0]}")
        return pair[0]

    def put(self, value):
        if self.state == 0:
            self.dest = value
            self.state = 1
            print(f"{self.addr} -> {self.dest}: ", end="")
            return
        if self.state == 1:
            self.x = value
            print(f"X: {value}, ", end="")
            self.state = 2
            return
        if self.state == 2:
            self.y = value
            print(f"Y: {value}")
            if self.dest < len(nodes):
                nodes[self.dest].recv(self.x, self.y)
            if self.dest == 255:
                print(f"First Y to 255 is {value}")
                nat.recv(self.x, self.y)
            self.state = 0
            return
        raise Exception(f"unexpected state {state}")


def read_memory(f):
    line = f.readline()
    return [int(x) for x in line.split(",")]


infile = open(sys.argv[1])
memory = read_memory(infile)

for i in range(node_count):
    nodes[i] = NIC(i, memory)

for node in nodes:
    node.thread.start()

nat.run()
