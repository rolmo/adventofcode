#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/4

Usage: cat advent04.input | python3 ./advent04.py

"""
15-48,7-16
import sys

def main ():

    input = sys.stdin.read().strip().split('\n')

    fully_contains = overlaps = 0
    for line in input:
        (range1,range2) = line.split(",")
        (start1,end1) = range1.split("-")
        (start2,end2) = range2.split("-")
        (start1,end1,start2,end2) = (int(start1),int(end1),int(start2),int(end2))

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
