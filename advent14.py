#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/14

Usage:
cat advent14.input | ./advent14.py
"""

import sys
import time

def main ():
    input = sys.stdin.read().strip().split('\n')

    print("Part 1:", part1(input))
    # 106990
    print("Part 2:", part2(input))
    # 100531



def part1 (input):
    platform = Platform(input)
    platform.tilt_north()
    load = platform.get_load_north()
    return load



def part2 (input):
    """
    We assume that the result is repeated after various rounds at a certain interval
    So we flip the platform some time until we find a repeating pattern (After about 200 cycles). 
    Based on this, we can calculate the load for the cycle 1000000000
    """
    load_after = 1000000000
    
    platform = Platform(input)
    results = []
    for cycle in range(1, load_after+1):
        # north, west, south, east.
        for i in range(4):
            platform.tilt_north()
            platform.rotate_right()
        load = platform.get_load_north()
        #print(cycle, "Load:", load)
        results.append(load) 
        interval = check_for_repetition(results)
        if interval:
            #print("Repetition found after {} cycles. Interval = {}".format(cycle, interval))
            # Repetition found after 227 cycles. Interval = 39
            load = calculate_load_for_cycle(load_after, interval, cycle, results)
            break
    return load




def calculate_load_for_cycle (cycles, interval, repetition_in_cycle, results):
    remaining_cycles = cycles - repetition_in_cycle
    remain_after_loops = remaining_cycles % interval
    load = results[repetition_in_cycle - interval + remain_after_loops -1]
    return load


"""
ckeck for repetition of results
- we check for a pattern lenght from 1-100
- if the pattern repeats in the interval before, we return the interval length
"""
def check_for_repetition (results):
    if len(results) < 200:
        return None
    for i in range(2, 100):
        if results[-1] == results[-i]:
            interval = i-1
            all_match = True
            for j in range(100):
                if results[-1-j] != results[-i-j]:
                    all_match = False
                    continue
            if all_match:
                return interval
            else:
                continue
    return None



class Platform:

    def __init__ (self, input):
        self.rounded_rocks = []
        self.cube_shaped = []
        max_x = 0
        for y in range(len(input)):
            line = input[y]
            for x in range(len(line)):
                if y == 0:
                    self.rounded_rocks.append([])
                    self.cube_shaped.append([])
                if line[x] == 'O':
                    self.rounded_rocks[x].append(y)
                elif line[x] == '#':
                    self.cube_shaped[x].append(y)
                max_x = x
            self.max_edge = y
        if max_x != self.max_edge:
            raise Exception("max_x != max_y")

    def tilt_north (self):
        for x in range(len(self.rounded_rocks)):
            for i in range(len(self.rounded_rocks[x])):
                y = self.rounded_rocks[x][i]
                for potential_new_pos in range(y-1, -1, -1):
                    if potential_new_pos not in self.rounded_rocks[x] and potential_new_pos not in self.cube_shaped[x]:
                        self.rounded_rocks[x][i] = potential_new_pos
                    else:
                        break

    def get_load_north (self):
        load = 0
        for x in range(len(self.rounded_rocks)):
            for rock in self.rounded_rocks[x]:
                load_rock = self.max_edge - rock +1
                load += load_rock
        return load
    
    def rotate_right (self):
        new_rounded_rocks = []
        new_cube_shaped = []
        for n in range(self.max_edge+1):
            new_rounded_rocks.append([])
            new_cube_shaped.append([])
        for x in range(self.max_edge, -1, -1):
            for y in range(self.max_edge + 1):
                if y in self.rounded_rocks[x]:
                    new_rounded_rocks[self.max_edge - y].insert(0, x)
                if y in self.cube_shaped[x]:
                    new_cube_shaped[self.max_edge - y].insert(0, x)    
        self.rounded_rocks = new_rounded_rocks
        self.cube_shaped = new_cube_shaped

    def __str__(self) -> str:
        s = ""
        for y in range(self.max_edge+1):
            for x in range(len(self.rounded_rocks)):
                if y in self.rounded_rocks[x]:
                    s += 'O'
                elif y in self.cube_shaped[x]:
                    s += '#'
                else:
                    s += '.'
            s += '\n'
        return s



if __name__ == '__main__':
    main()