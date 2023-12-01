#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/1

Usage:
cat advent01.input | ./advent01.py
"""

import sys
import re


def main ():
    input = sys.stdin.read().strip().split('\n')

    print("Part 1:", part1(input))
    # 54561
    print("Part 2:", part2(input))
    # 54076


def part1 (input):
    sum = 0
    for line in input:
        digits = list(filter(lambda i: i.isdigit(), line))
        first_digit = int(digits[0])
        last_digit = int(digits[-1])
        sum = sum + first_digit * 10 + last_digit
    return sum


def part2 (input):
    sum = 0
    for line in input:
        line = replace_number_words_with_digits(line)
        digits = list(filter(lambda i: i.isdigit(), line))
        first_digit = int(digits[0])
        last_digit = int(digits[-1])
        sum = sum + first_digit * 10 + last_digit
    return sum


def replace_number_words_with_digits (line):
    # Problem here:
    # If we replace "two" with "2", we burn the "t" in "eightwo"
    # and the follow search for "eight" find "eigh2".
    # So we preserve the original string on both sides:
    line = re.sub(r"one", "one1one", line)
    line = re.sub(r"two", "two2two", line)
    line = re.sub(r"three", "three3three", line)
    line = re.sub(r"four", "four4four", line)
    line = re.sub(r"five", "five5five", line)
    line = re.sub(r"six", "six6six", line)
    line = re.sub(r"seven", "seven7seven", line)
    line = re.sub(r"eight", "eight8eight", line)
    line = re.sub(r"nine", "nine9nine", line)
    return line


if __name__ == '__main__':
    main()