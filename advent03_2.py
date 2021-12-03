#!/usr/bin/env python3

# Usage: cat advent03.input | ./advent03_2.py

"""
Keep only numbers selected by the bit criteria for the type of rating value for
which you are searching. Discard numbers which do not match the bit criteria.
If you only have one number left, stop; this is the rating value for which you
are searching.
Otherwise, repeat the process, considering the next bit to the right.

The bit criteria depends on which type of rating value you want to find:

* To find oxygen generator rating, determine the most common value (0 or 1) in the
  current bit position, and keep only numbers with that bit in that position.
  If 0 and 1 are equally common, keep values with a 1 in the position being considered.

* To find CO2 scrubber rating, determine the least common value (0 or 1) in the
  current bit position, and keep only numbers with that bit in that position.
  If 0 and 1 are equally common, keep values with a 0 in the position being considered.
"""

import sys

def get_bit(value, pos):
    return value & (1 << pos)

def filter_list(list, pos, comparator):
    count_true = count_false = 0
    for value in list:
        if get_bit(value, pos):
            count_true += 1
        else:
            count_false += 1
    filtered_list = []
    for value in list:
        if count_true >= count_false:
            if comparator == "most common" and get_bit(value, pos):
                filtered_list.append(value)
            if comparator == "least common" and not get_bit(value, pos):
                filtered_list.append(value)
        else:
            if comparator == "most common" and not get_bit(value, pos):
                filtered_list.append(value)
            if comparator == "least common" and get_bit(value, pos):
                filtered_list.append(value)
    if pos > 0 and len(filtered_list) > 1:
        # Recursion:
        return filter_list(filtered_list, pos-1, comparator)
    else:
        # Recursion abort:
        return filtered_list[0]


# Read input to list and find longest value
max_length = 0
list = []
for line in sys.stdin:
    max_length = max(len(line.strip()), max_length)
    list.append(int(line, 2))

# Run filter (recursive):
o2 = filter_list(list, max_length - 1, "most common")
co2 = filter_list(list, max_length - 1, "least common")

print ("O2: {}, CO2: {}, Product: {}".format(o2, co2, o2*co2))
# O2: 1981, CO2: 3371, Product: 6677951
