#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/8

Usage:
cat advent08.input | ./advent08.py
"""

import sys
import re
import numpy as np

def main ():
    input = sys.stdin.read().strip().split('\n')
    (instructions, network) = parse_input(input)

    print("Part 1:", part1(instructions, network))
    # 18827
    print("Part 2:", part2(instructions, network))
    # 20220305520997

def part1 (instructions, network):
    steps = 0
    instructions = Instructions(instructions)
    field = "AAA"
    for instruction in instructions:
        if field == "ZZZ":
            break
        left, right = network[field]
        if instruction == "L":
            field = left
        elif instruction == "R":
            field = right
        steps += 1
        #print(steps, field, instruction, instructions.pointer)
    return steps


def part2 (instructions, network):
    instructions = Instructions(instructions)
    fields = [x for x in network.keys() if x.endswith("A")]
    steps_for_field = []
    # print(fields)
    for field in fields:
        #print("Starting with", field)
        instructions.pointer = 0
        steps = 0
        for instruction in instructions:
            left, right = network[field]
            if instruction == "L":
                field = left
            elif instruction == "R":
                field = right
            steps += 1
            if field.endswith("Z"):
                #print("Found", field, "in", steps, "steps")
                break
        steps_for_field.append(steps)
    #print(steps_for_field)
    arr = np.array(steps_for_field)
    return np.lcm.reduce(arr)


def parse_input (input):
    instructions = input[0]
    network = {}
    for line in input[2:]:
        matches = re.match(r'^(\w+) = \((\w+), (\w+)\)$', line)
        if matches:
            (field, left, right) = matches.groups()
            network[field] = (left, right)
        else:
            print("Error parsing line:", line)
    return instructions, network



class Instructions:

    def __init__ (self, instructions):
        self.instructions = instructions

    def __iter__ (self):
        self.pointer = 0
        return self

    def __next__ (self):
        if self.pointer >= len(self.instructions):
            self.pointer = 0
        instruction = self.instructions[self.pointer]
        self.pointer += 1
        return instruction


if __name__ == '__main__':
    main()