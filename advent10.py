#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/10

Usage:
cat advent10.input | ./advent10.py
"""

import sys
from dataclasses import dataclass

def main ():
    input = sys.stdin.read().strip().split('\n')

    pipes = Pipes(input)

    # Part1:
    steps = pipes.find_path()
    print("Part 1:", steps)
    # 6882
    
    # Part2:
    pipes.replace_start_with_pipe()    
    inner_positions = pipes.find_inner_positions()
    print("Part 2:", inner_positions)
    # 491
 


class Pipes:

    def __init__ (self, input):
        self.pipes = {}    # Hash with all pipes
        row = 0
        for line in input:
            row += 1
            col = 0
            for symbol in line:
                col += 1
                self.pipes[Pos(row, col)] = Pipe(symbol)
                if symbol == "S":
                    self.start = Pos(row, col)
            self.cols = col
        self.rows = row


    def find_path (self):
        """
        From the start position, we follow the pipes on both directions.
        If both paths reach the same field, we stop.
        """
        connected = self._connected(self.start)
        self.path1 = [self.start, connected[0]]
        self.path2 = [self.start, connected[1]]

        while True:
            # path 1
            connected = self._connected(self.path1[-1])
            come_from = self.path1[-2]
            for pos in connected:
                if pos != come_from:
                    self.path1.append(pos)
                    self.pipes[pos].is_in_path = True
            # path 2
            connected = self._connected(self.path2[-1])
            come_from = self.path2[-2]
            for pos in connected:
                if pos != come_from:
                    self.path2.append(pos)
                    self.pipes[pos].is_in_path = True
            # stop if both paths reach the same position:
            if self.path1[-1] == self.path2[-1]:
                break
        return len(self.path1) - 1


    def _connected (self, pos):
        """
        Returns a list with the two positions that are connected to the given position/pipe.
        """
        pipe = self.pipes[pos]
        pipe.is_in_path = True
        connected = list()
        if pipe.north() and self.pipes[pos.north()].south():
            connected.append(pos.north())
        if pipe.east() and self.pipes[pos.east()].west():
            connected.append(pos.east())
        if pipe.south() and self.pipes[pos.south()].north():
            connected.append(pos.south())
        if pipe.west() and self.pipes[pos.west()].east():
            connected.append(pos.west())
        if len(connected) != 2:
            # To find a matching pipe for the start position, we raise an exception if there are not exactly two connections:
            raise Exception("Pipe at", pos, "has", len(connected), "connections")
        return(connected)


    def replace_start_with_pipe (self):
        """
        Test each possible pipe symbol at the start position and replace the start position with
        the pipe that connects to the rest of the pipes.
        """
        for symbol in "|-LJ7F":
            self.pipes[self.start] = Pipe(symbol, True)
            try:
                self._connected(self.start)
                break
            except:
                pass


    def find_inner_positions (self):
        """
        Every time we cross the line, the status (boolean "inner_area") changes, whether we are
        inside or outside the figure.
        But you have to be careful whether you really cross the line or just touch it!
        """
        for row in range(1, self.rows+1):
            inner_area = False
            path_comes_from = None
            for col in range(1, self.cols+1):
                pipe = self.pipes[Pos(row, col)]
                if pipe.is_in_path:
                    if not pipe.west() and not pipe.east():
                        inner_area = not inner_area
                    elif not pipe.west():
                        if pipe.south():
                            path_comes_from = "south"
                        if pipe.north():
                            path_comes_from = "north"
                    elif not pipe.east():
                        if pipe.south() and path_comes_from == "north":
                            inner_area = not inner_area
                        if pipe.north() and path_comes_from == "south":
                            inner_area = not inner_area
                else:
                    pipe.inner_area = inner_area
        inner_positions = 0
        for pos in self.pipes:
            if self.pipes[pos].inner_area:
                inner_positions += 1
        return inner_positions


    def __str__ (self):
        s = ""
        for row in range(1, self.rows+1):
            for col in range(1, self.cols+1):
                pipe = self.pipes[Pos(row, col)]
                if pipe.is_in_path:
                    s += pipe.symbol
                else:
                    if pipe.inner_area:
                        s += "+"
                    else:
                        s += pipe.symbol
            s += "\n"
        return s



@dataclass
class Pos:
    row: int
    col: int

    def north (self):
        return Pos(self.row-1, self.col)

    def south (self):
        return Pos(self.row+1, self.col)
    
    def east (self):
        return Pos(self.row, self.col+1)

    def west (self):
        return Pos(self.row, self.col-1)
    
    def __hash__(self):
        return hash((self.row, self.col))


@dataclass
class Pipe:
    symbol: str
    is_in_path: bool = False
    inner_area: bool = False

    def north (self):
        return self.symbol in ["|", "L", "J", "S"]

    def south (self):
        return self.symbol in ["|", "7", "F", "S"]

    def east (self):
        return self.symbol in ["-", "F", "L", "S"]

    def west (self):
        return self.symbol in ["-", "7", "J", "S"]
    

if __name__ == '__main__':
    main()