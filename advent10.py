#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/10

Usage: cat advent10.input | python3 ./advent10.py

"""
import sys

def main ():
    input = sys.stdin.read().strip().split("\n")

    next_value = 1
    register = []
    for command in input:
        if command == "noop":
            register.append(next_value)
        else:
            # only "addx":
            arg = int(command.split(" ")[1])
            register.append(next_value)
            register.append(next_value)
            next_value += arg
            
    # Part1:
    sum_signal_strength = 0
    for cycle in range(20,221,40):
        sum_signal_strength += cycle * register[cycle - 1]

    print("Sum of signal strength:", sum_signal_strength)
    # Sum of signal strength: 12560

    # Part2:
    for row in range(6):
        for col in range(40):
            x = register[row*40+col]
            if abs(col - x) <= 1:
                print("#", end="")
            else:
                print(" ", end="")
        print("")
    # Output:
    # PLPAFBCL


if __name__ == '__main__':
    main()
