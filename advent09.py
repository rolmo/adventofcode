#!/usr/bin/env python3

# Usage: cat advent09.input | ./advent09.py


"""

https://adventofcode.com/2021/day/9

Part 1:

    The risk level of a low point is 1 plus its height.

    Find all of the low points on your heightmap. What is the sum of the risk
    levels of all low points on your heightmap?


Part 2:

    Find the three largest basins and multiply their sizes together
"""

import sys
import time
from dataclasses import dataclass

def main():

    data = []
    for line in sys.stdin:
        data_line = []
        for n in line.strip():
            data_line.append(Cell(int(n)))
        data.append(data_line)

    sum_of_minimum = 0
    num_of_minimum = 0
    basin_sizes = []
    for row in range(len(data)):
        for col in range(len(data[row])):
            pos=(row,col)
            value = get_pos(data,pos).number
            n = get_pos(data, north(pos)).number
            s = get_pos(data, south(pos)).number
            w = get_pos(data, west(pos)).number
            e = get_pos(data, east(pos)).number
            if value < min(n, s, w, e):
                data[row][col].low_point = True
                # print("Minimum: {} ({},{})".format(value, row+1, col+1))
                num_of_minimum += 1
                sum_of_minimum += (value + 1)

                basin_size = find_basin_members(data, pos)
                # print("Basin-Size:", basin_size)
                basin_sizes.append(basin_size)

    # Print the colored map:
    for row in data:
        for col in row:
            print(col, end="")
        print()

    # Part 1:
    print("num of low points: ", num_of_minimum)
    print("sum of low points+1: ", sum_of_minimum)
    # num of low points:  239
    # sum of low points+1:  560

    # Part 2:
    basin_sizes.sort(reverse=True)
    (basin1,basin2,basin3) = basin_sizes[0:3]
    print("Largest basins:", basin1,basin2,basin3, "Product: ", basin1 * basin2 * basin3)
    # Largest basins: 103 97 96 Product:  959136




def find_basin_members (data, pos):
    if get_pos(data, pos).basin_member:
        # position is already markes as basin_member
        return 0
    if get_pos(data, pos).number >= 9:
        return 0
    size = 1  # the position itself
    get_pos(data, pos).basin_member = True  # mark the position as counted
    # Check each direction:
    size += find_basin_members (data, north(pos))
    size += find_basin_members (data, south(pos))
    size += find_basin_members (data, west(pos))
    size += find_basin_members (data, east(pos))
    return size


def north(pos):
    return (pos[0]-1,pos[1])

def south(pos):
    return (pos[0]+1,pos[1])

def west(pos):
    return (pos[0],pos[1]-1)

def east(pos):
    return (pos[0],pos[1]+1)

def get_pos(data,pos):
    # We return 9 as outer border
    if pos[0] < 0 or pos[0] >= len(data): return Cell(9)
    if pos[1] < 0 or pos[1] >= len(data[pos[0]]): return Cell(9)
    return data[pos[0]][pos[1]]


@dataclass
class Cell:
    number: int
    low_point: bool = False
    basin_member: bool = False

    def __str__ (self):
        """
            print low_points in blue and masin members in cyan:
        """
        if self.low_point:
            return f"\033[;1m\033[1;34m{self.number:2}\033[0m"
        if self.basin_member:
            return f"\033[1;36m{self.number:2}\033[0m"
        return f"{self.number:2}"



if __name__ == '__main__':
    main()
