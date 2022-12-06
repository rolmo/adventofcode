#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/6

Usage: cat advent06.input | python3 ./advent06.py

"""

START_OF_PACKET_MARKER_LENGTH = 4
START_OF_MESSAGE_MARKER_LENGTH = 14


import sys

input = sys.stdin.read().strip()

for n in range(len(input)):
    if len(set(input[n:n+START_OF_PACKET_MARKER_LENGTH])) == START_OF_PACKET_MARKER_LENGTH:
        print("START_OF_PACKET_MARKER:", n+START_OF_PACKET_MARKER_LENGTH, input[n:n+START_OF_PACKET_MARKER_LENGTH])
        break

for n in range(len(input)):
    if len(set(input[n:n+START_OF_MESSAGE_MARKER_LENGTH])) == START_OF_MESSAGE_MARKER_LENGTH:
        print("START_OF_MESSAGE_MARKER_LENGTH:", n+START_OF_MESSAGE_MARKER_LENGTH, input[n:n+START_OF_MESSAGE_MARKER_LENGTH])
        break
