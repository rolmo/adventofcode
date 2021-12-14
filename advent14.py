#!/usr/bin/env python3

# Usage: cat advent14.input | ./advent14.py

"""
https://adventofcode.com/2021/day/14
"""

import sys
from collections import defaultdict

# First line of input contains the polymer template
template=sys.stdin.readline().strip()

# dict with replacements:
replacements = {}
for line in sys.stdin:
    if line.strip():
        (search,insert) = line.strip().split(" -> ")
        replacements[search]=insert

# First, we split the template "abcdef" --> "ab", "bc", "cd", "de", "ef":
# So we double each char (but not the first/last) - we fix this later
count_of_pairs = defaultdict(int)
for split_at in range(len(template)-1):
    pair = template[split_at:split_at+2]
    count_of_pairs[pair] += 1
last_char = template[-1]

# Strategy (example for replacement "ab -> i")
# - first, we expand "ab" to "aib"
# - then we split to "ai" and "ib"
# A "ab" in step x expands to "ai" and "ib" in step x+1
for step in range(40):
    new_count_of_pairs = defaultdict(int)
    for pair, count in count_of_pairs.items():
        left  = pair[0] + replacements[pair]
        right = replacements[pair] + pair[1]
        new_count_of_pairs[left] += count
        new_count_of_pairs[right] += count
    count_of_pairs = new_count_of_pairs

# Because we double the inner chars with each split (see above),
# we count now only to the first char of each pair (and add the last char of the
# template)
# (We get the same result if we count the 2nd char of each pair and add the
# first char of the template)
count_of_chars = defaultdict(int)
for pair, count in count_of_pairs.items():
    count_of_chars[pair[0]] += count
count_of_chars[last_char] += 1

least = min(count_of_chars.values())
most  = max(count_of_chars.values())
print(most-least)
