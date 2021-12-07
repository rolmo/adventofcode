#!/usr/bin/env python3

# Usage: cat advent06.input | ./advent06.py


"""
https://adventofcode.com/2021/day/7

Part1:

Align all positions to the same position.
Use as few fuel as possible
Fuel consumption is linear to the distance

Part2:

Fuel consumption is gauss sum uf the distance

"""

import sys

def main():

    gauss_sum = lambda x: int(x*(x+1)/2)

    start_positions=list(map(int, sys.stdin.readline().strip().split(',')))
    max_position = max(start_positions)
    min_fuel_dist = min_fuel_gauss = None
    for target_pos in range(max_position+1):
        fuel_dist = fuel_gauss = 0
        for pos in start_positions:
            dist = abs(target_pos-pos)
            fuel_dist  += dist
            fuel_gauss += gauss_sum(dist)
        if not min_fuel_dist or fuel_dist < min_fuel_dist:
            best_position_dist = target_pos
            min_fuel_dist = fuel_dist
        if not min_fuel_gauss or fuel_gauss < min_fuel_gauss:
            best_position_gauss = target_pos
            min_fuel_gauss = fuel_gauss

    print("Best target position (linear fuel consumption): {}; Fuel: {}".format(best_position_dist, min_fuel_dist))
    # Best target position (linear fuel consumption): 317; Fuel: 331067
    print("Best target position (gauss fuel consumption): {}; Fuel: {}".format(best_position_gauss, min_fuel_gauss))
    # Best target position (gauss fuel consumption): 458; Fuel: 92881128

if __name__ == '__main__':
    main()
