#!/usr/bin/env python3

# Usage: cat advent18.input | ./advent18.py

"""
https://adventofcode.com/2021/day/18
"""

import sys
from dataclasses import dataclass
import math
import time


def main():

    numbers = []
    for line in sys.stdin:
        numbers.append(Snailfish_Numbers(line.strip()))

    for number in numbers[1:]:
        print(number)
        print("---------------------------")
        numbers[0] += number
        print(numbers[0])



class Snailfish_Numbers:

    def __init__ (self, string):
        self.number = []
        level = 0
        for c in list(string):
            if c == '[':
                level += 1
            if c == ']':
                level -= 1
            if c.isnumeric():
                self.number.append(Element(int(c),level))

    def _incr_level (self):
        for e in self.number:
            e.level += 1

    def _reduce (self):
        print("Reduce")
        print(self)
        while self._must_reduced():
            self._explode()
            print("After explode")
            print(self)
            self._split()
            print("After split")
            print(self)


    def _split (self):
        for i in range(len(self.number)):
            if self.number[i].number > 9:
                left = Element(math.floor(self.number[i].number/2),self.number[i].level +1)
                right = Element(math.ceil(self.number[i].number/2),self.number[i].level +1)
                print("Split!", left, right)
                self.number[i] = left
                self.number.insert(i+1, right)
                return

    def _explode (self):
        for i in range(len(self.number)):
            if self.number[i].level > 4:
                # Incr left (if possible)
                if i > 0:
                    self.number[i-1].number += self.number[i].number
                # Remove eleemnt:
                self.number[i] = None
                # Incr. right (if possible:)
                if i + 2 <= len(self.number):
                    self.number[i+2].number += self.number[i+1].number
                # Set right to 0
                self.number[i+1].number = 0
                self.number[i+1].level -= 1
                break
        self.number = list(filter(lambda e: e != None, self.number))



    def _must_reduced (self):
        for e in self.number:
            if e.level > 4:
                return True
            if e.number > 9:
                return True

    def __str__ (self):
        numbers = levels = ""
        for e in self.number:
            numbers += f"{e.number:3}"
            levels  += f"{e.level:3}"
        return numbers + "\n" + levels + "\n"


    def __add__ (self, other):
        if len(self.number) > 0:
            self._incr_level()
        self.number += other.number
        self._reduce()
        return self


@dataclass
class Element:
    number: int
    level: int


if __name__ == '__main__':
    main()
