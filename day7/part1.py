#!/usr/bin/env python3

import sys
import itertools

class IntCodeVM:
    class Stop(Exception):
        pass

    class InvalidMode(Exception):
        pass

    class InvalidDestination(Exception):
        pass

    def __init__(self, memory, inputs=None):
        self.memory = memory.copy()
        self.ip = 0
        self.inputs = inputs.copy()
        self.inputs.reverse()
        self.outputs = []

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
        if not self.inputs:
            return int(input())
        return self.inputs.pop()

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
            self.outputs.append(self.get_a())
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

signals = []
for phase_set in itertools.permutations(range(5)):
    acc = 0
    for i in range(5):
        vm = IntCodeVM(memory.copy(), inputs=[phase_set[i], acc])
        vm.run()
        acc = vm.outputs[0]
    signals.append(acc)

print(f"total is {max(signals)}")
