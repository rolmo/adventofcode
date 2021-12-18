#!/usr/bin/env python3

# Usage: cat advent17.input | ./advent17.py

"""
https://adventofcode.com/2021/day/17
"""

import sys
import re
from dataclasses import dataclass


def main():
    # First line contains the whole input:
    # Example: target area: x=32..65, y=-225..-177
    line = sys.stdin.readline().strip()

    matches = re.search('^target area: x=(\d+)\.\.(\d+), y=([-+]?\d+)\.\.([-+]?\d+)$', line)
    if matches:
        x1 = int(matches.group(1))
        x2 = int(matches.group(2))
        y1 = int(matches.group(3))
        y2 = int(matches.group(4))
    else:
        raise SyntaxError("Error in input")

    target = Area(x1,x2,y1,y2)


    # Calculate the minimum x speed^:
    # The coordinate for step n is calculated according to this formula:
    # For step 3:
    # x = vx + (vx - 1) + (vx - 2)
    # For step n:
    # x = vx + (vx - 1) + (vx - 2) + (vx - 3) + ... + (vx - n)
    # Or:
    # x = (vx * n) - (n^2 - n)/2
    #
    # The formula above is only alowed for vx >= n
    # the maximum x is reached for vx = n (after this, vx remains at 0):
    #
    # x_max = vx^2 - vx^2/2 + vx/2
    # x_max = (vx^2)/2 + vx/2
    #
    # We test the minimum x to reach the target area (target.x1)
    for min_speed_x in range(target.x1):
        if (min_speed_x * min_speed_x + min_speed_x) / 2 >= target.x1:
            break

    print("Minimum speed-x to reach the target-x1 ({}): {}".format(target.x1,min_speed_x))

    # The maximim x-speed is target.x2 + 1
    # (because with this speed, the first step is already behind the target area)
    max_speed_x = target.x2
    print("Maximum speed-x to reach the target-x2 ({}): {}".format(target.x2,max_speed_x))


    # If we fire the sonde with a positive speed-y, the speed-y is -(speed_y)
    # when we are cross y=0.
    #
    # Example: for speed-y = 3
    # start:        y=0, speed-y= 3
    # After step 1: y=3, speed-y= 2
    # After step 2: y=5, speed-y= 1
    # After step 3: y=6, speed-y= 0
    # After step 4: y=6, speed-y=-1
    # After step 5: y=5, speed-y=-2
    # After step 6: y=3, speed-y=-3
    # ---- cross y = 0
    # After step 7: y=0, speed-y=-4
    # ...
    #
    # To hit to lower edge of the target area (target.y2), the maximum speed-y
    # can be: abs(target.y2)-1
    max_speed_y = abs(target.y2)
    print("Maximum speed-y to reach the target-y2 ({}): {}".format(target.y2,max_speed_y))

    # If we fire the sonde down, the maximum negative (=minimum) speed is target.y2
    min_speed_y = target.y2
    print("Minimum speed-y to reach the target-x2 ({}): {}".format(target.y2,min_speed_y))


    stop_x = target.x2
    stop_y = target.y2
    trajectory =Trajectory(stop_x,stop_y)

    num_of_hit_combinations = 0
    max_y = 0
    for x in range(min_speed_x,max_speed_x+1):
        for y in range(min_speed_y,max_speed_y):
            trajectory.set(x,y)
            hit = False
            for point in trajectory:
                max_y = max(max_y,point.y)
                if point.hit(target):
                    hit = True
                    num_of_hit_combinations += 1
                    break


    print("max-y:", max_y)
    # max-y: 25200

    print("num of hit combinations:", num_of_hit_combinations)
    # 3012



class Trajectory:

    def __init__ (self, max_x, min_y):
        """
        max_x and min_y is the right and the lower edge
        of the taget area ... below this coordinates, we stop
        the iteration because we can't get a hit there
        """
        self.max_x = max_x
        self.min_y = min_y

    def set (self, speed_x, speed_y):
        self.initial_speed_x = speed_x
        self.initial_speed_y = speed_y

    def __iter__ (self):
        self.x = 0
        self.y = 0
        self.speed_x = self.initial_speed_x
        self.speed_y = self.initial_speed_y
        return self

    def __next__ (self):
        self.x = self.x + self.speed_x
        if self.speed_x > 0:
            self.speed_x -= 1
        self.y = self.y + self.speed_y
        self.speed_y -= 1
        if self.x > self.max_x or self.y < self.min_y:
            raise StopIteration
        return Point(self.x, self.y)



@dataclass
class Point:
    x: int
    y: int

    def hit (self, area):
        if self.x >= area.x1 and self.x <= area.x2:
            if self.y <= area.y1 and self.y >= area.y2:
                return True
        return False



class Area:

    def __init__ (self, xa, xb, ya, yb):
        self.x1 = min(xa, xb)
        self.x2 = max(xa, xb)
        self.y1 = max(ya, yb)
        self.y2 = min(ya, yb)


if __name__ == '__main__':
    main()
