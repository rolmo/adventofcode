#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/16

Usage:
cat advent16.input | ./advent16.py
"""

import sys
from dataclasses import dataclass

def main ():
    input = sys.stdin.read().strip().split('\n')

    print("Part 1:", part1(input))
    # 7562
    print("Part 2:", part2(input))
    # 7793


def part1 (input):
    grid = Grid(input)
    #print(grid)
    grid.follow_beam(0, 0, 'E')
    return grid.get_energized_tiles()


def part2 (input):
    grid = Grid(input)
    max_x = grid.max_x
    max_y = grid.max_y
    # Horizontal (upper and lower edge):
    max_energized_tiles = 0
    for x in range(grid.max_x + 1):
        for check_y in [(0,'S'), (max_y,'N')]:
            grid = Grid(input)
            grid.follow_beam(x, check_y[0], check_y[1])
            result = grid.get_energized_tiles()
            max_energized_tiles = max(max_energized_tiles, result)
    # Vertical (left and right edge):
    for y in range(grid.max_y + 1):
        for check_x in [(0,'E'), (max_x,'W')]:
            grid = Grid(input)
            grid.follow_beam(check_x[0], y, check_x[1])
            result = grid.get_energized_tiles()
            max_energized_tiles = max(max_energized_tiles, result)
    return max_energized_tiles



class Grid:

    def __init__(self, input):
        self._tiles = {}
        for y in range(len(input)):
            self.max_y = y
            for x in range(len(input[y])):
                self.max_x = x
                self._tiles[(x, y)] = Tile(input[y][x])


    def __str__(self):
        s = ""
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                s += str(self._tiles[(x, y)])
            s += "\n"
        return s


    def follow_beam(self, x, y, direction):
        self.beams = [(x, y, direction)]
        #while True:
        for n in range(12000):
            self._follow_beams()
            if len(self.beams) == 0:
                break
        #print(self.beams)


    def _follow_beams(self):
        #print("Beams:", self.beams)
        for beam in self.beams[:]:
            x, y, direction = beam
            tile = self._tiles[(x, y)]
            tile.energized = True
            if tile.has_beam_to(direction):
                # we follow already this beam - remove it
                self.beams.remove(beam)
            else:
                tile._beam_to[direction] = True
                new_directions = tile.get_new_directions(direction)
                #print("New directions:", new_directions)
                self.beams.remove(beam)
                for new_direction in new_directions:
                    new_x, new_y = self._get_new_position(x, y, new_direction)
                    if new_x is not None:
                        self.beams.append((new_x, new_y, new_direction))


    def _get_new_position(self, x, y, direction):
        if direction == 'N':
            if y == 0:
                return None, None
            return x, y-1
        elif direction == 'S':
            if y == self.max_y:
                return None, None
            return x, y+1
        elif direction == 'E':
            if x == self.max_x:
                return None, None
            return x+1, y
        elif direction == 'W':
            if x == 0:
                return None, None
            return x-1, y

    def get_energized_tiles(self):
        energized_tiles = 0
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                if self._tiles[(x, y)].energized:
                    energized_tiles += 1
        return energized_tiles

 
@dataclass
class Tile:

    def __init__(self, c):
        self.c = c
        self.energized = False
        self._beam_to = {'N': False, 'S': False, 'E': False, 'W': False}

    def __str__(self):
        return self.c
    
    def has_beam_to(self, direction):
        return self._beam_to[direction]

    def get_new_directions(self, direction):
        new_directions = []
        if self.c == '.':
            # For a ".", the beam passes through the tile without changing direction.
            new_directions = [direction]
        elif self.c == '|':
            if direction == 'N' or direction == 'S':
                new_directions = [direction]
            elif direction == 'E' or direction == 'W':
                new_directions = ['N', 'S']
        elif self.c == '-':
            if direction == 'N' or direction == 'S':
                new_directions = ['E', 'W']
            elif direction == 'E' or direction == 'W':
                new_directions = [direction]
        elif self.c == '/':
            if direction == 'N':
                new_directions = ['E']
            elif direction == 'S':
                new_directions = ['W']
            elif direction == 'E':
                new_directions = ['N']
            elif direction == 'W':
                new_directions = ['S']
        elif self.c == '\\':
            if direction == 'N':
                new_directions = ['W']
            elif direction == 'S':
                new_directions = ['E']
            elif direction == 'E':
                new_directions = ['S']
            elif direction == 'W':
                new_directions = ['N']
        return new_directions


if __name__ == '__main__':
    main()