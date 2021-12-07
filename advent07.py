#!/usr/bin/env python3

# Usage: cat advent06.input | ./advent06.py


"""
https://adventofcode.com/2021/day/7


Part1:

Align all positions to the same position.
Consume as little fuel as possible
Fuel consumption is linear with distance

Part2:

Fuel consumption is the Gaussian sum of distance

"""

import sys
import time
import statistics

def main():


    start_positions=list(map(int, sys.stdin.readline().strip().split(',')))

    start_time = time.time()
    (position, fuel) = linear_via_median(start_positions)
    end_time = time.time()


    print("Best target position (linear fuel consumption): {}; Fuel: {} (consumed time: {} ms)".format(position, fuel, 1000 * (end_time - start_time)))
    # Best target position (linear fuel consumption): 317; Fuel: 331067 (consumed time: 0.25 ms)

    start_time = time.time()
    (position, fuel) = gauss_fuel_consumption(start_positions)
    end_time = time.time()

    print("Best target position (gauss fuel consumption): {}; Fuel: {} (consumed time: {} ms)".format(position, fuel, 1000 * (end_time - start_time)))
    # Best target position (gauss fuel consumption): 458; Fuel: 92881128 (consumed time: 51.6 ms)


def gauss_fuel_consumption (positions):

    gauss_sum = lambda x: int(x*(x+1)/2)

    # Strategie:
    # We split the list at the median in two sub lists ("left_positions" (decreased order) and "right_positions" (increased order)).
    # - We start with "left_positions" (median ... 0) and test each position as long as the fuel consumption falls.
    # - We stop when the fuel consumtion raises
    # - Then we loop over the list "right_positions" (median ... max) as long as we get lower fuel consumption
    # - Again: we stop when the fuel consumtion raises

    max_position = max(positions)
    median = int(statistics.median(positions))
    left_positions = list(range(median,0,-1))
    right_positions = list(range(median,max_position+1))
    min_fuel = None
    for target_pos in left_positions:
        fuel = 0
        for pos in positions:
            fuel += gauss_sum(abs(target_pos-pos))
        if not min_fuel or fuel < min_fuel:
            best_position = target_pos
            min_fuel = fuel
        if min_fuel != None and fuel > min_fuel:
            break
    for target_pos in right_positions:
        fuel = 0
        for pos in positions:
            fuel += gauss_sum(abs(target_pos-pos))
        if not min_fuel or fuel < min_fuel:
            best_position = target_pos
            min_fuel = fuel
        if min_fuel != None and fuel > min_fuel:
            break

    return(best_position, min_fuel)


def linear_via_median (positions):
    median = int(statistics.median(positions))
    fuel = 0
    for pos in positions:
        fuel += abs(median-pos)
    return (median,fuel)


if __name__ == '__main__':
    main()
