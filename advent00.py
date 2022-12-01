#!/usr/bin/env python3

# Usage: cat advent01.input | ./advent01_1.py

"""
https://adventofcode.com/2022/day/1

Usage: cat advent00.input | ./advent00.py

"""

import sys
import collections


def main ():
    sum = max_sum = 0
    top3 = Top3()

    for line in sys.stdin:
        if line.strip():
            value = int(line)
            sum += value
        else:
            # Empty row: evaluate the sum:
            if sum > max_sum:
                max_sum = sum
            top3.insert_when_higher(sum)
            sum = 0
    # End of input:
    if sum > max_sum:
        max_sum = sum
    top3.insert_when_higher(sum)

    #### Part A ####
    print("Maximum is", max_sum)
    # Maximum is 71300

    #### Part B ####
    print("Sum for top 3:", top3.sum())
    # Sum for top 3: 209691



class Top3:

    def __init__(self) -> None:
        self.list = [0,0,0]
    
    def insert_when_higher(self, value) -> bool:
        if value > self.list[0]:
            self.list[0] = value
            self.list.sort()
            return True
        return False

    def sum (self) -> int:
        return sum(self.list)

    def __str__(self) -> str:
        return str(self.list)



if __name__ == '__main__':
    main()
