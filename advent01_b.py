#!/usr/bin/env python3

# Usage: cat advent01.input | ./advent01_b.py

import sys

list = []
for line in sys.stdin:
    list.append(int(line))

window_size = 3
number_of_compares = len(list) - window_size

increased = 0
if number_of_compares > 0:
    for i in range(number_of_compares):
        if sum(list[i:i+window_size]) < sum(list[i+1:i+window_size+1]):
            increased += 1

print(increased)
