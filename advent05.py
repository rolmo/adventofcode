#!/usr/bin/env python3

"""
Part 1:

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

    An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap.


Part 2:

Include diagonal lines

"""

import sys
import re

def main():

    # List with all lines:
    lines = []

    # Read the input and create line objects::
    max_x = max_y = 0
    for input_line in sys.stdin:
        line = Line(input_line.strip())
        lines.append(line)
        max_x = max(max_x, line.max_x())
        max_y = max(max_y, line.max_y())

    board = Board(max_x, max_y)

    for line in lines:
        if line.is_horzontal_or_vertical():
            for point in line:
                board.inc(point)

    print("Spots for horizontal+vertival lines:", board.count_spots())

    for line in lines:
        if not line.is_horzontal_or_vertical():
            for point in line:
                board.inc(point)

    print("Spots for all lines:", board.count_spots())



class Board:

    def __init__ (self, max_x, max_y):
        self.board=[]
        for x in range(max_x):
            self.board.append([])
            for y in range(max_y):
                self.board[x].append(0)

    def inc (self, point):
        (x,y) = point
        self.board[x-1][y-1] += 1

    def count_spots (self):
        spots = 0
        for row in self.board:
            for cell in row:
                if cell > 1:
                    spots += 1
        return spots


class Line:

    def __init__ (self, text):
        self.parse_text_line(text)
        self.cursor_x = self.x1
        self.cursor_y = self.y1
        # directions (set_x, step_y) for the iterator
        self.step_x = self.step_y = 0
        if self.x1 < self.x2: self.step_x = 1
        if self.x1 > self.x2: self.step_x = -1
        if self.y1 < self.y2: self.step_y = 1
        if self.y1 > self.y2: self.step_y = -1

    def parse_text_line (self, text):
        # 683,807 -> 370,494
        matches = re.search('^(\d+),(\d+)\s+->\s+(\d+),(\d+)$', text)
        if matches:
            self.x1 = int(matches.group(1))
            self.y1 = int(matches.group(2))
            self.x2 = int(matches.group(3))
            self.y2 = int(matches.group(4))

    def max_x (self):
        return (max(self.x1, self.x2))

    def max_y (self):
        return (max(self.y1, self.y2))

    def is_horzontal_or_vertical (self):
        return self.x1 == self.x2 or self.y1 == self.y2

    def __iter__(self):
        return self

    def __next__(self):
        pos_x = self.cursor_x
        pos_y = self.cursor_y
        self.cursor_x += self.step_x
        self.cursor_y += self.step_y
        if pos_x > max(self.x1, self.x2) or pos_x < min(self.x1, self.x2) or pos_y > max(self.y1, self.y2) or pos_y < min(self.y1, self.y2):
            raise StopIteration
        return (pos_x, pos_y)

    def __str__ (self):
        return "{}|{} - {}|{}  (Step: {}|{})".format(self.x1,self.y1,self.x2,self.y2,self.step_x,self.step_y)


if __name__ == '__main__':
    main()
