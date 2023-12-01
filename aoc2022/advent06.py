#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/6

Usage: cat advent06.input | python3 ./advent06.py

"""

START_OF_PACKET_MARKER_LENGTH = 4
START_OF_MESSAGE_MARKER_LENGTH = 14

import sys

def main ():
    input = sys.stdin.read().strip()
    print (find_uniq_marker(START_OF_PACKET_MARKER_LENGTH, input))
    print (find_uniq_marker(START_OF_MESSAGE_MARKER_LENGTH, input))

def find_uniq_marker (length, input):
    for n in range(len(input) - length):
        if len(set(input[n:n+length])) == length:
            return n+length

if __name__ == '__main__':
    main()
