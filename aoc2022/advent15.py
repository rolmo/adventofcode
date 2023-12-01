#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/15

Usage: cat advent15.input | python3 ./advent15.py

"""
import sys
from dataclasses import dataclass
import re

PATTERN = re.compile(r"Sensor at x=(?P<sx>[-\d]+), y=(?P<sy>[-\d]+): closest beacon is at x=(?P<bx>[-\d]+), y=(?P<by>[-\d]+)")

def main ():
    input = sys.stdin.read().strip().split("\n")

    used_pos = set()
    min_x = min_y = max_x = max_y = None
    for line in input:
        match = re.match(PATTERN, line)
        if match:
            sx = int(match.group("sx"))
            sy = int(match.group("sy"))
            bx = int(match.group("bx"))
            by = int(match.group("by"))
            sensor = Sensor((sx,sy),(bx,by))
            if min_x:
                min_x = min(sensor.min_x(),min_x)
            else:
                min_x = sensor.min_x()
            if max_x:
                max_x = max(sensor.max_x(),max_x)
            else:
                max_x = sensor.max_x()
            r = sensor.get_points_on_y(10)  # (2000000)
            for x in r:
                used_pos.add(x)
        else:
            raise Exception("Unexpected input: "+line) 


    print(min_x, max_x, len(used_pos))

class Sensor:

    def __init__ (self, sensor, beacon) -> None:
        self.sensor = sensor
        self.beacon = beacon
        self.radius = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    
    def get_points_on_y (self, y_row):
        remain_radius = self.radius - abs(self.sensor[1] - y_row)
        left = self.sensor[0] - remain_radius
        right = self.sensor[0] + remain_radius
        return range(left, right+1)

    def min_x (self):
        return self.sensor[0] - self.radius

    def max_x (self):
        return self.sensor[0] + self.radius



if __name__ == '__main__':
    main()
