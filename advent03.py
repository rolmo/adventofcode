#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/3

Usage:
cat advent03.input | ./advent03.py
"""

import sys
from dataclasses import dataclass

def main ():
    input = sys.stdin.read().strip().split('\n')

    print("Part 1:", part1(input))
    # 528819
    print("Part 2:", part2(input))
    # 80403602


def part1 (input):
    numbers, symbols = parse_input(input)
    
    sum = 0
    for num in numbers:
        all_adjacent = num.get_all_adjacent()
        for pos in all_adjacent:
            if pos in symbols:
                sum = sum + num.num
    return sum

def part2 (input):
    numbers, symbols = parse_input(input)
    sum = 0
    for pos_symbol in symbols:
        if symbols[pos_symbol] == '*':
            adjacebts = 0
            mul = 1
            for num in numbers:
                for pos_num in num.get_all_adjacent():
                    if pos_num == pos_symbol:
                        adjacebts = adjacebts + 1
                        mul = mul * num.num
            if adjacebts == 2:
                sum = sum + mul
    return sum


def parse_input (input):
    numbers = []
    symbols = {}
    buffer = pos = None
    y = 0
    for line in input:
        x = 0
        y = y + 1
        if buffer:
            numbers.append(Num_With_Pos(int(buffer), pos))
            buffer = None
        for char in line:
            x = x + 1
            if char.isnumeric():
                if buffer:
                    buffer = buffer + char
                else:
                    buffer = char
                    pos = (x, y)
            else:
                if buffer:
                    numbers.append(Num_With_Pos(int(buffer), pos))
                    buffer = None
                if char == '.':
                    continue
                symbols[(x, y)] = char
    return (numbers, symbols)


@dataclass
class Num_With_Pos:

    num: int
    pos: tuple

    def get_all_adjacent (self):
        positions = set()
        (x, y) = self.pos
        for rx in range(x - 1, x + len(str(self.num)) + 1):
            for ry in range(y -1, y+2):
                positions.add((rx, ry))
        return positions



if __name__ == '__main__':
    main()