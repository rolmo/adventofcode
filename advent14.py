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
        (s,r) = line.strip().split(" -> ")
        rs = s[0] + r + s[1]
        replacements[s]=r  #((s,r,rs))

# We split the template "abcde" --> "ab", "bc", "cd", "de":
count_of_pairs = defaultdict(int)
for split_at in range(len(template)-1):
    pair = template[split_at:split_at+2]
    count_of_pairs[pair] += 1
last_char = template[-1]

for step in range(40):
    new_count_of_pairs = defaultdict(int)
    for pair, count in count_of_pairs.items():
        left  = pair[0] + replacements[pair]
        right = replacements[pair] + pair[1]
        new_count_of_pairs[left] += count
        new_count_of_pairs[right] += count
    count_of_pairs = new_count_of_pairs

count_of_chars = defaultdict(int)
for pair, count in count_of_pairs.items():
    count_of_chars[pair[0]] += count
count_of_chars[last_char] += 1

least = min(count_of_chars.values())
most  = max(count_of_chars.values())
print(most-least)
