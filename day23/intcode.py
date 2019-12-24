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

    def __init__(self, memory, input, output, memory_length=(2 ** 20)):
        self.memory = [0] * memory_length
        self.memory[0 : len(memory)] = memory
        self.input = input
        self.output = output
        self.ip = 0
        self.relative_base = 0

    def value(self, parameter, mode):
        if mode == 0:
            return self.memory[parameter]
        if mode == 1:
            return parameter
        if mode == 2:
            return self.memory[self.relative_base + parameter]
        raise IntCodeVM.InvalidMode(f"Invalid mode {mode}")

    def address(self, parameter, mode):
        if mode == 0:
            return parameter
        if mode == 2:
            return self.relative_base + parameter
        raise IntCodeVM.InvalidMode(f"Invalid address mode {mode}")

    def get_parameter_addr(self, offset):
        opcode = self.memory[self.ip]
        mode = (opcode // (10 ** (1 + offset))) % 10
        a = self.memory[self.ip + offset]
        addr = self.address(a, mode)
        return addr

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
        elif operation == 9:  # ADJ-REL-BASE
            self.relative_base += self.get_a()
            self.ip += 2
        elif operation == 99:
            self.ip += 1
            raise IntCodeVM.Stop()

    def run(self):
        try:
            while True:
                self.step()
        except IntCodeVM.Stop as _ex:
            return


class IntIO:
    def get():
        return int(input())

    def put(value):
        print(value)


class StdIO:
    def __init__(self):
        self.buffer = []

    def put(self, value):
        if value > 255:
            print(f"Non-ASCII: {value}")
        print(chr(value), end="")

    def get(self):
        if not self.buffer:
            self.buffer = [ord(c) for c in input()] + [10]
        c = self.buffer[0]
        self.buffer = self.buffer[1:]
        return c
        

def debug_vm(f):
    line = open(sys.argv[1]).readline()
    memory = [int(x) for x in line.split(",")]

    io = IntIO()
    vm = IntCodeVM(memory, io, io)


if __name__ == "__main__":
    infile = open(sys.argv[1])
    vm = debug_vm(infile)
    vm.run()
