#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/3

Usage: cat advent03.input | ./advent03.py

"""

import sys

def main1 ():

    result = 0
    for line in sys.stdin:
        items = line.strip()
        compartment1 = items[0:int(len(items)/2)]
        compartment2 = items[int(len(items)/2):]
        for c in compartment1:
            if c in compartment2:
                result += my_ord(c)
                break # we stop for the first duplicate (assume there are only identical duplicates)
    print(result)
    # 8298


def main2 ():

    result = 0
    input = sys.stdin.read().strip().split('\n')
    for group in range(int(len(input)/3)):
        # We convert to set to reduce each list to uniq items:
        rucksack1 = set(input[group*3])
        rucksack2 = set(input[group*3 + 1])
        rucksack3 = set(input[group*3 + 2])
        batch = None
        for c1 in rucksack1:
            for c2 in rucksack2:
                if c1 == c2:
                    for c3 in rucksack3:
                        if c1 == c3:
                            batch = c1
                            break
        result += my_ord(batch)
    print(result)
    # 2708            


def my_ord (char):
    # "a" has ord 97, but should 1
    if ord(char) > 96:
        return ord(char) - 96
    # "A" has ord 65, but should 27
    return ord(char) - 38


if __name__ == '__main__':
    main2()
