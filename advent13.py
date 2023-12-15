#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/13

Usage:
cat advent13.input | ./advent13.py
"""

import sys
import time

def main ():
    input = sys.stdin.read().strip().split('\n')

    valleys = parse_valleys(input)

    print("Part 1:", part1(valleys))
    # 34821
    print("Part 2:", part2(valleys))
    # 21480 too low
    # 27336 too low
    # 40804 too high


def part1 (valleys):
    sum = 0
    for v in valleys:
        #print(v)
        valley = Valley(v)
        sum += valley.get_mirror_axis() * 100
        valley.swap_rows_and_columns()
        sum += valley.get_mirror_axis()
    return sum


def part2 (valleys):
    sum = 0
    for v in valleys:
        #print(v)
        valley = Valley(v)

        valley.set_allowed_smudge(1)
        original_smudged = valley.get_mirror_axis() * 100
        valley.set_allowed_smudge(0)
        original_unsmudged = valley.get_mirror_axis() * 100

        valley.swap_rows_and_columns()

        # Try to find a solution with smudge:
        valley.set_allowed_smudge(1)
        swapped_smudged = valley.get_mirror_axis()
        valley.set_allowed_smudge(0)
        swapped_unsmudged =  valley.get_mirror_axis()
    
        if original_smudged > 0 and swapped_smudged > 0:
            raise Exception("Double solution possible for smudged")
        
        if original_unsmudged > 0 and swapped_unsmudged > 0:
            raise Exception("Double solution possible for unsmudged")
        
        if original_smudged + swapped_smudged > 0:
            sum += original_smudged + swapped_smudged
        else:
            sum += original_unsmudged + swapped_unsmudged

    
        
    return sum


def parse_valleys(input):
    valleys = []
    valley = []
    for line in input:
        if line == "":
            valleys.append(valley)
            valley = []
        else:
            valley.append(line)
    valleys.append(valley)
    return valleys



class Valley:

    def __init__ (self, rows):
        self.rows = rows
        self.allowed_smudge = 0
        self.free_smudge = 0

    def get_mirror_axis (self):
        for i in range(len(self.rows)-1):
            self.free_smudge = self.allowed_smudge
            if self._compare_rows(self.rows[i],self.rows[i+1]):
                #print("potentail match")
                if self.check_mirror(i):
                    #print("match")
                    if self.free_smudge == 0:
                        return i+1
                    else :
                        return 0
        return 0

    def check_mirror (self, position):
        for j in range(2, int((len(self.rows)+1)/2)):
            #print("checking", j)
            if position - j +1 >= 0:
                if position + j < len(self.rows):
                    if not self._compare_rows(self.rows[position-j+1], self.rows[position+j]):
                        return False
        return True
    
    def swap_rows_and_columns (self):
        swapped = []
        for row in self.rows:
            for i in range(len(row)):
                if i < len(swapped):
                    swapped[i] += row[i]
                else:
                    swapped.append(row[i])
        #print(swapped)
        self.rows = swapped

    def set_allowed_smudge (self, allowed_smudge):
        self.allowed_smudge = allowed_smudge
        self.free_smudge = allowed_smudge

    def _compare_rows (self, row1, row2):
        #print(row1)
        #print(row2)
        differences = sum([1 for i in range(len(row1)) if row1[i] != row2[i]])
        #print("differences", differences)
        if differences > self.free_smudge:
            return False
        else:
            self.free_smudge -= differences
        #print("match")
        return True


if __name__ == '__main__':
    main()