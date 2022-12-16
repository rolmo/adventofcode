#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/14

Usage: cat advent14.input | python3 ./advent14.py

"""
import sys
from dataclasses import dataclass


def main ():
    input = sys.stdin.read().strip().split("\n")

    # Part 1:

    cave = Cave()
    for line in input:
        coordinates = [x for x in map(string_to_point, line.split(" -> "))]
        cave.add_path(coordinates)

    units = 0
    while cave.sand_unit():
        units += 1
        #print(cave)

    print("Number of sand units:", units)
    # Number of sand units: 1298

    # Part 2:

    cave = Cave()
    for line in input:
        coordinates = [x for x in map(string_to_point, line.split(" -> "))]
        cave.add_path(coordinates)
    cave.add_floor()

    units = 0
    while cave.sand_unit():
        units += 1
        #if units % 100 == 0:
        #    print(cave)

    print("Number of sand units:", units)
    # Number of sand units: 25585


def string_to_point (string):
    (x,y) = string.split(",")
    return Point(int(x),int(y))


@dataclass
class Point:
    x: int
    y: int

    def __init__ (self, x,y) -> None:
        self.x = x
        self.y = y

    def __hash__ (self) -> int:
        return self.x * 1000000 + self.y

    def next (self):
        return Point(self.x,self.y+1)

    def next_left (self):
        return Point(self.x-1,self.y+1)

    def next_right (self):
        return Point(self.x+1,self.y+1)

    def down (self):
        self.y += 1

    def down_left (self):
        self.y += 1
        self.x -= 1

    def down_right (self):
        self.y += 1
        self.x += 1


class Cave:
    sand_sporn = Point(500,0)

    def __init__(self) -> None:
        self.cave = set()
        self.sand = set() 
        self.min_x = None
        self.max_x = None
        self.max_y = None

    def add_path (self,coordinates):
        for pos in range(len(coordinates)-1):
            self.add_edge(coordinates[pos],coordinates[pos+1])

    def sand_unit (self):
        sand_unit = Point(Cave.sand_sporn.x,Cave.sand_sporn.y)
        if sand_unit in self.sand:
            return False
        for y in range(self.max_y):
            if (not sand_unit.next() in self.cave) and (not sand_unit.next() in self.sand):
                sand_unit.down()
            elif (not sand_unit.next_left() in self.cave) and (not sand_unit.next_left() in self.sand):
                sand_unit.down_left()
            elif (not sand_unit.next_right() in self.cave) and (not sand_unit.next_right() in self.sand):
                sand_unit.down_right()
            else:
                self.sand.add(sand_unit)
                return True
        return False

    def add_edge (self, p1, p2):
        if not self.min_x:
            self.min_x = min(p1.x,p2.x)
        else:
            self.min_x = min(p1.x,p2.x,self.min_x)
        if not self.max_x:
            self.max_x = max(p1.x,p2.x)
        else:
            self.max_x = max(p1.x,p2.x,self.max_x)
        if not self.max_y:
            self.max_y = max(p1.y,p2.y)
        else:
            self.max_y = max(p1.y,p2.y,self.max_y)
        if p1.x == p2.x:
            # vertical edge
            for y in range(min(p1.y, p2.y),max(p1.y, p2.y)+1):
                self.cave.add(Point(p1.x,y))
        elif p1.y == p2.y:
            # horizontal
            for x in range(min(p1.x, p2.x),max(p1.x, p2.x)+1):
                self.cave.add(Point(x,p1.y))
        else:
            # diagonal edges not allowed:
            raise

    def add_floor (self):
        self.max_y += 2
        self.min_x = Cave.sand_sporn.x - self.max_y
        self.max_x = Cave.sand_sporn.x + self.max_y
        for x in range(self.min_x, self.max_x+1):
            self.cave.add(Point(x,self.max_y))

    def __str__ (self):
        out = ""
        for y in range (self.max_y + 1):
            for x in range (self.min_x, self.max_x+1):
                if Point(x,y) in self.cave:
                    out += "#"
                elif Point(x,y) in self.sand:
                    out += "o"
                elif Point(x,y) == Cave.sand_sporn:
                    out += "+"
                else:
                    out += "."
            out += "\n"
        return out



if __name__ == '__main__':
    main()
