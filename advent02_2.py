#!/usr/bin/env python3

# Usage: cat advent02.input | ./advent02_2.py

"""

https://adventofcode.com/2021/day/2

Calculate the horizontal position and depth you would have after following the
planned course. What do you get if you multiply your final horizontal position
by your final depth?

In addition to horizontal position and depth, you'll also need to track a third
value, aim, which also starts at 0. The commands also mean something entirely
different than you first thought:

    down X increases your aim by X units.
    up X decreases your aim by X units.
    forward X does two things:
        It increases your horizontal position by X units.
        It increases your depth by your aim multiplied by X.

"""

import sys

depth = horizontal = aim = 0
for line in sys.stdin:
    (command,argument) = line.split()
    if command == "down": aim += int(argument)
    if command == "up": aim -= int(argument)
    if command == "forward":
        horizontal += int(argument)
        depth += aim * int(argument)

print(depth, horizontal, depth * horizontal)
