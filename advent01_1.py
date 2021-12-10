#!/usr/bin/env python3

# Usage: cat advent01.input | ./advent01_1.py

"""
https://adventofcode.com/2021/day/1

Count the number of times a depth measurement increases from the previous measurement

"""

import sys

last = None
increase = 0
for line in sys.stdin:
    value = int(line)
    if last and value > last:
        increase += 1
    last = value

print(increase)
