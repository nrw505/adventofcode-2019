#!/usr/bin/env python3

import sys
import itertools
import queue
from threading import Thread

class IntCodeVM:
    class Stop(Exception):
        pass

    class InvalidMode(Exception):
        pass

    class InvalidDestination(Exception):
        pass

    def __init__(self, memory, input=None, output=None):
        self.memory = memory.copy()
        self.ip = 0
        self.input = input
        self.output = output

    def value(self, parameter, mode):
        if mode == 0:
            return self.memory[parameter]
        if mode == 1:
            return parameter
        raise IntCodeVM.InvalidMode(f"Invalid mode {mode}")

    def get_parameter_addr(self, offset):
        return self.memory[self.ip + offset]

    def get_parameter(self, offset):
        opcode = self.memory[self.ip]
        mode = (opcode // (10 ** (1 + offset))) % 10
        p = self.memory[self.ip + offset]
        value = self.value(p, mode)
        return value

    def get_a(self):
        "Get the A (first) parameter"
        return self.get_parameter(1)

    def get_a_addr(self):
        "Get the A (first) parameter"
        return self.get_parameter_addr(1)

    def get_b(self):
        "Get the B (second) parameter"
        return self.get_parameter(2)

    def get_b_addr(self):
        "Get the B (second) parameter"
        return self.get_parameter_addr(2)

    def get_c(self):
        "Get the C (third) parameter"
        return self.get_parameter(3)

    def get_c_addr(self):
        "Get the C (third) parameter"
        return self.get_parameter_addr(3)

    def get_input(self):
        return self.input.get()

    def put_output(self, value):
        self.output.put(value)

    def step(self):
        opcode = self.memory[self.ip]
        if opcode is None:
            raise IntCodeVM.Stop()

        operation = opcode % 100

        if operation == 1:  # ADD
            self.memory[self.get_c_addr()] = self.get_a() + self.get_b()
            self.ip += 4
        elif operation == 2:  # MUL
            self.memory[self.get_c_addr()] = self.get_a() * self.get_b()
            self.ip += 4
        elif operation == 3:  # INPUT
            self.memory[self.get_a_addr()] = self.get_input()
            self.ip += 2
        elif operation == 4:  # OUTPUT
            self.put_output(self.get_a())
            self.ip += 2
        elif operation == 5:  # JUMP-IF-TRUE
            if self.get_a() != 0:
                self.ip = self.get_b()
            else:
                self.ip += 3
        elif operation == 6:  # JUMP-IF-FALSE
            if self.get_a() == 0:
                self.ip = self.get_b()
            else:
                self.ip += 3
        elif operation == 7:  # LESS-THAN
            if self.get_a() < self.get_b():
                self.memory[self.get_c_addr()] = 1
            else:
                self.memory[self.get_c_addr()] = 0
            self.ip += 4
        elif operation == 8:  # EQUALS
            if self.get_a() == self.get_b():
                self.memory[self.get_c_addr()] = 1
            else:
                self.memory[self.get_c_addr()] = 0
            self.ip += 4
        elif operation == 99:
            self.ip += 1
            raise IntCodeVM.Stop()

    def run(self):
        try:
            while True:
                self.step()
        except IntCodeVM.Stop as _ex:
            return


infile = open(sys.argv[1])

line = open(sys.argv[1]).readline()
memory = [int(x) for x in line.split(",")]

def run_vm(vm):
    vm.run()

queues = [queue.Queue() for x in range(5)]
signals = []
for phase_set in itertools.permutations(range(5, 10)):
    vms = [
        IntCodeVM(memory.copy(), input=queues[i], output=queues[(i+1) % 5])
        for i in range(5)
    ]
    for i in range(5):
        queues[i].put(phase_set[i])

    threads = [Thread(target=run_vm, args=[vm]) for vm in vms]
    for thread in threads:
        thread.start()

    queues[0].put(0)
    for thread in threads:
        thread.join()

    signals.append(queues[0].get())
    
print(f"total is {max(signals)}")
