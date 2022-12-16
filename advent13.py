#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/13

Usage: cat advent13.input | python3 ./advent13.py

"""
import sys
from functools import cmp_to_key
from copy import deepcopy

def main ():
    input = sys.stdin.read().strip().split("\n")

    print(part_1([x for x in input]))
    # 5720

    print(part_2(input))
    # 23504



def part_1 (input):
    pair = 0
    sum = 0
    while len(input):
        pair += 1
        left = eval(input.pop(0))
        right = eval(input.pop(0))
        if compare(left, right) > 0:
            sum += pair
        if len(input):
            # Eat empty line:
            input.pop(0)
    
    return sum


def part_2 (input):

    pair_list = []
    for line in input:
        if len(line):
            pair_list.append(eval(line))
    pair_list.append([[2]])
    pair_list.append([[6]])
    pair_list.sort(key=cmp_to_key(compare),reverse=True)
    a = pair_list.index([[2]]) + 1
    b = pair_list.index([[6]]) + 1
    return a * b


def compare(origleft,origright):
    left = deepcopy(origleft)
    right = deepcopy(origright)

    # If the right list runs out of items first, the inputs are not in the right order.
    if len(left) > 0 and len(right) == 0:
        return -1
    # If the left list runs out of items first, the inputs are in the right order.
    if len(left) == 0 and len(right) > 0:
        return 1

    # End of both (sub)lists:
    if len(left) == 0 and len(right) == 0:
        return 0

    l = left.pop(0)
    r = right.pop(0)

    # If exactly one value is an integer, convert the integer to a list which contains that integer as its only value,
    # then retry the comparison.
    if isinstance(l, int) and isinstance(r, list):
        left.insert(0, [l])
        right.insert(0, r)
        return compare(left,right)

    if isinstance(l, list) and isinstance(r, int):
        left.insert(0, l)
        right.insert(0, [r])
        return compare(left,right)

    if isinstance(l, list) and isinstance(r, list):
        subresult = compare(l,r)
        if subresult != 0:
            return subresult
        else:
            return compare(left, right)

    # Both values are int:
    # If the left integer is lower than the right integer, the inputs are in the right order.
    if l < r:
        return 1
    # If the left integer is higher than the right integer, the inputs are not in the right order.
    if l > r:
        return -1
    # Otherwise, the inputs are the same integer; continue checking the next part of the input.
    return compare(left, right)



if __name__ == '__main__':
    main()

