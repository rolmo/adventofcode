#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/15

Usage:
cat advent15.input | ./advent15.py
"""

import sys

def main ():
    chunks = sys.stdin.read().strip().split(',')

    print("Part 1:", part1(chunks))
    # 517551
    print("Part 2:", part2(chunks))
    # 286097


def part1 (chunks):
    sum = 0
    for chunk in chunks:
        value = hash(chunk)
        sum += value
    return sum


def part2 (chunks):
    boxes = [[] for n in range(256)]
    for chunk in chunks:
        if "-" in chunk:
            operation = "remove"
            label = chunk[:-1]
            box = hash(label)
            remove_from_box(boxes[box], label)
        if "=" in chunk:
            operation = "add"
            label, focal_length = chunk.split('=')
            box = hash(label)
            add_to_box(boxes[box], label, int(focal_length))
        # print("Box: {}, Operation: {}, Label: {}, Focal length: {}".format(box, operation, label, focal_length))
    return(focusing_power(boxes))


def hash (chunk):
    value = 0
    for char in chunk:
        value += ord(char)
        value *= 17
        value = value % 256
    return value


def add_to_box (box, label, focal_length):
    for i in range(len(box)):
        if box[i][0] == label:
            box[i][1] = focal_length
            return
    box.append([label, focal_length])


def remove_from_box (box, label):
    for i in range(len(box)):
        if box[i][0] == label:
            box.pop(i)
            return


def focusing_power (boxes):
    sum = 0
    box_number = 0
    for box in boxes:
        box_number += 1
        slot_number = 0
        for slot in box:
            slot_number += 1
            sum += box_number * slot_number * slot[1]
    return sum


if __name__ == '__main__':
    main()