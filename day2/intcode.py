#!/usr/bin/env python3

import sys


class IntCodeVM:
    class Stop(Exception):
        pass

    def __init__(self, memory):
        self.memory = memory
        self.ip = 0

    def step(self):
        (opcode, in1, in2, out) = self.memory[self.ip : self.ip + 4]
        if opcode is None:
            raise IntCodeVM.Stop()

        if opcode == 1:
            self.memory[out] = self.memory[in1] + self.memory[in2]
            self.ip += 4
        elif opcode == 2:
            self.memory[out] = self.memory[in1] * self.memory[in2]
            self.ip += 4
        elif opcode == 99:
            self.ip += 1
            raise IntCodeVM.Stop()

    def run(self):
        try:
            while True:
                self.step()
        except IntCodeVM.Stop as _ex:
            return


line = open("input").readline()
memory = [int(x) for x in line.split(",")]

for noun in range(100):
    for verb in range(100):
        newmem = memory.copy()
        newmem[1] = noun
        newmem[2] = verb
        vm = IntCodeVM(newmem)
        vm.run()
        result = vm.memory[0]
        if result == 19690720:
            print(f"{noun:<2}{verb:<2}")
