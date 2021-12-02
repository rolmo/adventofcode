#!/usr/bin/env python3

# Usage: cat advent01.input | ./advent01.py

import sys

last = None
increase = 0
for line in sys.stdin:
    value = int(line)
    if last and value > last:
        increase += 1
    last = value

print(increase)
