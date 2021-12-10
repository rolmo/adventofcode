#!/usr/bin/env python3

# Usage: cat advent01.input | ./advent01_2.py

"""
https://adventofcode.com/2021/day/1

Count the number of times a depth measurement increases from the previous measurement
(We compare a window of 3 measurements)
"""

import sys
import collections

window_size = 3
shift_register = collections.deque([], window_size)

last = None
increased = 0
for line in sys.stdin:
    shift_register.append(int(line))
    if len(shift_register) == window_size:
        window_sum = 0
        for value in shift_register:
            window_sum += value
        if last and window_sum > last:
            increased += 1
        last = window_sum

print(increased)
