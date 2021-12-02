#!/usr/bin/env python3

# Usage: cat advent02.input | ./advent02.py

import sys

depth = horizontal = 0
for line in sys.stdin:
    (command,argument) = line.split()
    if command == "down": depth += int(argument)
    if command == "up": depth -= int(argument)
    if command == "forward": horizontal += int(argument)

print(depth, horizontal, depth * horizontal)
