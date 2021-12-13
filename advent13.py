#!/usr/bin/env python3

# Usage: cat advent13.input | ./advent13.py


"""
https://adventofcode.com/2021/day/13

"""

import sys
import re
from dataclasses import dataclass


def main():

    instruction = Instruction()
    folds = []

    dot_pattern = re.compile('^(\d+),(\d+)$')
    fold_pattern = re.compile('^fold along (x|y)=(\d+)$')

    for line in sys.stdin:
        match = re.search(dot_pattern, line.strip())
        if match:
            instruction.add_dot(int(match.group(1)),int(match.group(2)))
        else:
            match = re.search(fold_pattern, line.strip())
            if match:
                folds.append(Fold(match.group(1),int(match.group(2))))


    for fold in folds:
        instruction.fold(fold)
        print(len(instruction.dots))
        # After first fold: 842

    instruction.display()
    # BFKRCJZU



class Instruction:

    def __init__ (self):
        #self.dots = []
        self.dots = set()


    def add_dot (self,x,y):
        #self.dots.append(Dot(x,y))
        self.dots.add(Dot(x,y))


    def fold (self, fold):
        #print("Fold:",fold.direction,fold.coordinate)
        if fold.direction == "x":
            self.fold_x(fold.coordinate)
        elif fold.direction == "y":
            self.fold_y(fold.coordinate)
        else:
            raise UnknownFoldDirection


    def fold_x (self, fold_x):
        temp = set()
        for dot in self.dots:
            if dot.x > fold_x:
                dot.x = (2*fold_x)-dot.x
            temp.add(dot)
        self.dots = temp


    def fold_y (self, fold_y):
        temp = set()
        for dot in self.dots:
            if dot.y > fold_y:
                dot.y = (2*fold_y)-dot.y
            temp.add(dot)
        self.dots = temp


    def display (self):
        max_x = max_y = 0
        for dot in self.dots:
            max_x = max(max_x,dot.x)
            max_y = max(max_y,dot.y)
        matrix = []
        for y in range(max_y+1):
            row = []
            for x in range(max_x+1):
                row.append(' ')
            matrix.append(row)
        for dot in self.dots:
            matrix[dot.y][dot.x] = "#"
        for row in matrix:
            for col in row:
                print(f"{col:2}", end="")
            print()



@dataclass
class Dot:
    x: int
    y: int

    def __str__ (self):
        return f"{self.x},{self.y}"

    def __hash__(self):
      return hash((self.x, self.y))


@dataclass
class Fold:
    direction: str
    coordinate: int


if __name__ == '__main__':
    main()
