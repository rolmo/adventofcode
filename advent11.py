#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/11

Usage:
cat advent11.input | ./advent11.py
"""

import sys

def main ():
    input = sys.stdin.read().strip().split('\n')

    # Part1:
    space = Space(input)
    space.expand()
    print(space.get_distances())
    # 9974721

    # Part2:
    space = Space(input)
    space.expand(1000000)
    print(space.get_distances())
    # 702770569197


class Space:

    def __init__ (self, input):
        self.galaxies = []
        self.rows_with_galaxies = set()
        self.cols_with_galaxies = set()
        row_number = 0
        for line in input:
            col_number = 0
            for symbol in line:
                if symbol == '#':
                    self.galaxies.append([row_number, col_number])
                    self.rows_with_galaxies.add(row_number)
                    self.cols_with_galaxies.add(col_number)
                col_number += 1
            row_number += 1
            self.cols = col_number
        self.rows = row_number


    def expand (self, distance=2):
        for row in range(self.rows-1, -1, -1):
            if not row in self.rows_with_galaxies:
                self._move_galaxies(row, "down", distance-1)
        for col in range(self.cols-1, -1, -1):
            if not col in self.cols_with_galaxies:
                self._move_galaxies(col, "right", distance-1)


    def _move_galaxies (self, threshold, down_right, distance):
        direction = {'down': 0, 'right': 1}[down_right]
        for galaxy in self.galaxies:
            if galaxy[direction] > threshold:
                galaxy[direction] += distance


    def get_distances (self):
        distance = 0
        number_of_galaxies = len(self.galaxies)
        for g_from in range(number_of_galaxies - 1):
            for g_to in range(g_from + 1, number_of_galaxies):
                distance += self._get_distance(g_from, g_to)
        return distance


    def _get_distance (self, g_from, g_to):
        return abs(self.galaxies[g_from][0] - self.galaxies[g_to][0]) + abs(self.galaxies[g_from][1] - self.galaxies[g_to][1])


if __name__ == '__main__':
    main()