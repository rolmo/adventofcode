#!/usr/bin/env python3

# Usage: cat advent03.input | ./advent03_1.py

"""
Each bit in the gamma rate can be determined by finding the most common bit in
the corresponding position of all numbers in the diagnostic report.
If the most common bit is 1, the first bit of the gamma rate is 1.
If the most common bit is 0, the first bit of the gamma rate is 0.

The epsilon rate is calculated in a similar way; rather than use the most common
bit, the least common bit from each position is used.
"""

import sys

# Read input to list and find longest value
max_length = 0
list = []
for line in sys.stdin:
    max_length = max(len(line.strip()), max_length)
    list.append(int(line, 2))

gamma = epsilon = 0
for bit_pos in range(max_length):
    count_true = count_false = 0
    for value in list:
        #if get_bit(value, bit_pos):
        if value & (1 << bit_pos):
            count_true += 1
        else:
            count_false +=1
    if count_true > count_false:
        gamma += 0 | (1<<bit_pos)
    else:
        epsilon += 0 | (1<<bit_pos)

print("Gamma: {}, Epsilon: {}, Product: {}".format(gamma, epsilon, gamma*epsilon))
# Gamma: 844, Epsilon: 3251, Product: 2743844
