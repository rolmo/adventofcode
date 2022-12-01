#!/usr/bin/env python3

# Usage: cat advent02.input | ./advent02_1.py

"""

https://adventofcode.com/2021/day/2

Calculate the horizontal position and depth you would have after following the
planned course. What do you get if you multiply your final horizontal position
by your final depth?

"""

import sys

depth = horizontal = 0
for line in sys.stdin:
    (command,argument) = line.split()
    if command == "down": depth += int(argument)
    if command == "up": depth -= int(argument)
    if command == "forward": horizontal += int(argument)

print(depth, horizontal, depth * horizontal)
