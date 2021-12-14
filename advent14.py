#!/usr/bin/env python3

# Usage: cat advent14.input | ./advent14.py

"""
https://adventofcode.com/2021/day/14
"""

import sys
import collections

# First line of input contains the polymer template
template=sys.stdin.readline().strip()

# dict with replacements:
replacements = {}

# Read the rest of the input and create all boards:
for line in sys.stdin:
    if line.strip():
        # Non empty line:
        (s,r) = line.strip().split(" -> ")
        rs = s[0] + r + s[1]
        replacements[s]=r  #((s,r,rs))

# We split the template "abcde" --> "ab", "bc", "cd", "de":
count_of_pairs = {}
for split_at in range(len(template)-1):
    pair = template[split_at:split_at+2]
    if pair in count_of_pairs:
        count_of_pairs[pair] += 1
    else:
        count_of_pairs[pair] = 1
last_char = template[-1]

for step in range(40):
    new_count_of_pairs = {}
    for pair, count in count_of_pairs.items():
        left  = pair[0] + replacements[pair]
        right = replacements[pair] + pair[1]
        if left in new_count_of_pairs:
            new_count_of_pairs[left] += count
        else:
            new_count_of_pairs[left] = count
        if right in new_count_of_pairs:
            new_count_of_pairs[right] += count
        else:
            new_count_of_pairs[right] = count
    count_of_pairs = new_count_of_pairs

count_of_chars={}
for pair, count in count_of_pairs.items():
    if pair[0] in count_of_chars:
        count_of_chars[pair[0]] += count
    else:
        count_of_chars[pair[0]] = count
count_of_chars[last_char] += 1

most = 0
least = None
for char, count in count_of_chars.items():
    if not least:
        least = count
    least = min(least,count)
    most = max(most,count)
print(most-least)
