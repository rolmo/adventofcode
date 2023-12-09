#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/9

Usage:
cat advent09.input | ./advent09.py
"""

import sys

def main ():
    input = sys.stdin.read().strip().split('\n')

    print("Part 1:", part1(input))
    # 1887980197
    print("Part 2:", part2(input))
    # 990

def part1 (input):
    sum = 0
    for line in input:
        oasis = Oasis([int(x) for x in line.split(' ')])
        oasis.append_value()
        sum += oasis.get_last_value()
    return sum

def part2 (input):
    sum = 0
    for line in input:
        oasis = Oasis([int(x) for x in line.split(' ')])
        oasis.prepend_value()
        sum += oasis.get_first_value()
    return sum


class Oasis:

    def __init__ (self, input):
        self.derivations = []
        self.derivations.append(input)
        self._derive()

    def _last_derivation_is_constant_null (self):
        return all([i == 0 for i in self.derivations[-1]])

    def _derive (self):
        if self._last_derivation_is_constant_null():
            return
        else:
            new = []
            for i in range(len(self.derivations[-1])-1):
                new.append(self.derivations[-1][i+1] - self.derivations[-1][i])
            self.derivations.append(new)
            self._derive()

    def append_value (self):
        self.derivations[-1].append(0)
        for i in range(-2, len(self.derivations)*-1-1, -1):
            self.derivations[i].append(self.derivations[i][-1]+self.derivations[i+1][-1])

    def  get_last_value (self):
        return self.derivations[0][-1]

    def prepend_value (self):
        self.derivations[-1].insert(0,0)
        for i in range(-2, len(self.derivations)*-1-1, -1):
            self.derivations[i].insert(0, self.derivations[i][0]-self.derivations[i+1][0])

    def  get_first_value (self):
        return self.derivations[0][0]


if __name__ == '__main__':
    main()