#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/4

Usage: cat advent04.input | python3 ./advent04.py

"""
import sys

def main ():

    input = sys.stdin.read().strip().split('\n')

    fully_contains = overlaps = 0
    for line in input:
        ((start1,end1),(start2,end2)) = tuple(tuple(int(x) for x in range.split("-")) for range in line.split(","))

        # Part One:
        if (start2 >= start1 and end2 <= end1) or (start1 >= start2 and end1 <= end2):
            fully_contains += 1

        # Part Two
        if (start1 >= start2 and start1 <= end2) or (start2 >= start1 and start2 <= end1):
            overlaps += 1

    print(fully_contains)
    # 424
    print(overlaps)
    # 804

if __name__ == '__main__':
    main()
