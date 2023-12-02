#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/2

Usage:
cat advent02.input | ./advent02.py
"""

import sys


def main ():
    input = sys.stdin.read().strip().split('\n')

    print("Part 1:", part1(input))
    # 3059
    print("Part 2:", part2(input))
    # 65371


def part1 (input):
    bag = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    sum = 0
    for line in input:
        game = Game(line)
        if game.is_possible(bag):
            sum = sum + game.number
    return sum


def part2 (input):
    sum = 0
    for line in input:
        game = Game(line)
        sum = sum + game.power_of_minimum_color()
    return sum



class Game:

    def __init__ (self, line):
        self.subsets = []
        self.parse_line(line)


    def parse_line (self, line):
        (label, subsets) = line.split(':')
        (trash, game_number) = label.split(' ')
        self.number = int(game_number)
        for subset in subsets.split(';'):
            self.subsets.append(Subset(subset))


    def power_of_minimum_color (self):
        minimum_color = {}
        for subset in self.subsets:
            for color in subset.color:
                num = subset.color[color]
                if color not in minimum_color:
                    minimum_color[color] = num
                else:
                    minimum_color[color] = max(minimum_color[color], num)
        power = 1
        for color in minimum_color:
            power = power * minimum_color[color]
        return power


    def is_possible (self, bag):
        for subset in self.subsets:
            for color in subset.color:
                if color not in bag:
                    return False
                if bag[color] < subset.color[color]:
                    return False
        return True


    def __str__ (self):
        s = "Game {}:\n".format(self.number)
        for subset in self.subsets:
            s = s + "-----\n"
            s = s + str(subset)
        return s



class Subset:

    def __init__ (self, line):
        self.color = {}
        self.parse_line(line)


    def parse_line (self, line):
        for color in line.split(','):
            (num, color) = color.strip().split(' ')
            self.color[color] = int(num)


    def __str__ (self):
        s = ""
        for color in self.color:
            s = s + "{} {}\n".format(color, self.color[color])
        return s


if __name__ == '__main__':
    main()