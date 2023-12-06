#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/6

Usage:
cat advent06.input | ./advent06.py
"""

import sys
import re
from dataclasses import dataclass


def main ():

    input = sys.stdin.read().strip().split('\n')
    races1 = parse_input(input)
    races2 = parse_input(input, ignore_spaces=True)

    print("Part 1:", part1(races1))
    # 840336
    print("Part 2:", part1(races2))
    # 41382569


def part1 (races):
    product = 1
    for race in races:
        product = product * race.get_number_of_options_with_better_distance()
    return product


def parse_input (input, ignore_spaces=False):
    line_data = {}
    for line in input:
        metric, values = line.split(':')
        if ignore_spaces:
            values = values.replace(" ", "")
        numbers = [int(x) for x in re.split('\s+', values.strip())]
        line_data[metric] = numbers
    races = []
    for i in range(len(line_data['Time'])):
        races.append(Race(line_data['Time'][i], line_data['Distance'][i]))
    return races


@dataclass
class Race:
    time: int
    distance: int
    speed_after_time: int = 1  

    def distance_after_time (self, time):
        speed = time * self.speed_after_time
        race_time = self.time - time
        distance = speed * race_time
        return distance
    
    def get_number_of_options_with_better_distance (self):
        options = 0
        for time in range(self.time):
            distance = self.distance_after_time(time)
            if distance > self.distance:
                options += 1
        return options


if __name__ == '__main__':
    main()