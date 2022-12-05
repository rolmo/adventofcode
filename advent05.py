#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/5

Usage: cat advent05.input | python3 ./advent05.py

"""

import sys
import re

def main ():

    input = sys.stdin.read().split('\n')

    # Part1:
    (stack_lines,command_lines) = readinput(input)
    stacks = parse_stacks(stack_lines)
    commands = parse_commands1(command_lines)

    for command in commands:
        move1(command, stacks)
    
    for stack in stacks:
        print(stack[-1], end="")
    print()
    # BSDMQFLSP



    # Part2:
    (stack_lines,command_lines) = readinput(input)
    stacks = parse_stacks(stack_lines)
    commands = parse_commands2(command_lines)

    for command in commands:
        move2(command, stacks)
    
    for stack in stacks:
        print(stack[-1], end="")
    print()
    # PGSQBFLDP


def move1 (command, stacks):
    item = stacks[command['from'] - 1].pop()
    stacks[command['to'] - 1].append(item)


def move2 (command, stacks):
    items = stacks[command['from'] - 1][len(stacks[command['from'] - 1]) - command['count']:]
    stacks[command['from'] - 1] = stacks[command['from'] - 1][:len(stacks[command['from'] - 1]) - command['count']]
    stacks[command['to'] - 1] = stacks[command['to'] - 1] + items


def readinput (input):
    stack_lines = []
    command_lines = []
    for line in input:
        if "[" in line:
            stack_lines.append(line)
        if "move" in line:
            command_lines.append(line)
    return stack_lines, command_lines


def parse_commands1 (commands_input):
    commands = []
    for line in (commands_input):
        match = re.match("move (\d+) from (\d+) to (\d+)", line)
        if match:
            for c in range(int(match.group(1))):
                move = {
                    "from":  int(match.group(2)),
                    "to":    int(match.group(3))
                }
                commands.append(move)
        else:
            print("WRONG:",line)
    return commands


def parse_commands2 (commands_input):
    commands = []
    for line in (commands_input):
        match = re.match("move (\d+) from (\d+) to (\d+)", line)
        if match:
            move = {
                "count": int(match.group(1)),
                "from":  int(match.group(2)),
                "to":    int(match.group(3))
            }
            commands.append(move)
        else:
            print("WRONG:",line)
    return commands


def parse_stacks (stack_input):
    stacks = [[] for i in range(9)]
    for line in reversed(stack_input):
        for pos in range(9):
            item = line[pos*4+1]
            if item != " ":
                stacks[pos].append(item)
    return stacks



if __name__ == '__main__':
    main()
