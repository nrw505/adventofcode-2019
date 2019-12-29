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


def read_memory(f):
    line = f.readline()
    return [int(x) for x in line.split(",")]

infile = open(sys.argv[1])
memory = read_memory(infile)

io = StdIO()
vm = IntCodeVM(memory, io, io)

run_vm(vm)
