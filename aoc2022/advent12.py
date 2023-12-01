#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/12

Usage: cat advent12.input | python3 ./advent12.py

"""
import sys
from dataclasses import dataclass

def main ():
    input = sys.stdin.read().strip().split("\n")

    # Part 1

    map = Map(input)
    path = map.path(Map.Search_End)
    print(len(path)-1)
    # 490

    # Part 2

    # For part 2, we simply invert the map
    # a -> z     (97 -> 122)
    # z -> a     (122 -> 97)
    # E -> S
    # S -> z
    # But the we search for the first "z" as end of the path
    inverted = invert(input)
    map2 = Map(inverted)
    path2 = map2.path(Map.Search_Top)
    print(len(path2)-1)
    # 488


def invert(input):
    inverted = []
    for row in input:
        new = ""
        for char in row:
            if char == "E":
                new += "S"
            elif char == "S":
                new += "z"
            else:
                new += chr(ord("z") + ord("a") - ord(char))
        inverted.append(new)
    return inverted



class Map:

    Search_End = True
    Search_Top = False

    def __init__ (self, input):
        self.create_map(input)
    
    def create_map (self, input):
        self._map = {}
        row = 0
        for line in input:
            self._map[row] = {}
            col = 0
            for char in line:
                if  char == "S":
                    self._start = Point(col,row)
                    char = "a"
                if  char == "E":
                    self._end = Point(col,row)
                    char = "z"
                self._map[row][col] = Field(char, None)
                col += 1
            row +=1
        self.max_x = col -1
        self.max_y = row -1


    def path (self, mode):
        self.paths = [[self._start]] 
        while True:
            if len(self.paths) == 0:
                break
            path = self.paths.pop(0)
            for field in self._check_possible_fields(path[len(path)-1]):
                newpath = [field for field in path]
                newpath.append(field)
                if mode == Map.Search_End:
                    if field == self._end:
                        return newpath
                else:
                    if self.get_field(field).height == "z":
                        return newpath
                self.paths.append(newpath)


    def get_field (self, point):
        return self._map[point.y][point.x]


    def _check_field (self, p1, p2) -> bool:
        height = self.get_field(p1).height
        if ord(height) + 1 >= ord(self.get_field(p2).height):
            if not self.get_field(p2).visited:
                    self.get_field(p2).visited = True
                    return True
        return False


    def _check_possible_fields (self, point):
        possible_fields = []
        if point.x > 0:
            left = Point(point.x-1,point.y)
            if self._check_field(point,left):
                possible_fields.append(left)
        if point.x < self.max_x:
            right = Point(point.x+1,point.y)
            if self._check_field(point,right):
                possible_fields.append(right)
        if point.y > 0:
            up = Point(point.x,point.y-1)
            if self._check_field(point,up):
                possible_fields.append(up)
        if point.y < self.max_y:
            down = Point(point.x,point.y+1)
            if self._check_field(point,down):
                possible_fields.append(down)
        return possible_fields


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Field:
    height: str
    visited: bool = False


if __name__ == '__main__':
    main()
