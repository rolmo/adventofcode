#!/usr/bin/env python3

# Usage: cat advent02.input | ./advent02_b.py

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
