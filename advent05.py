#!/usr/bin/env python3

"""
Part 1:

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where
x1,y1 are the coordinates of one end the line segment and x2,y2 are the
coordinates of the other end.
These line segments include the points at both ends. In other words:

    An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines:
lines where either x1 = x2 or y1 = y2.

To avoid the most dangerous areas, you need to determine the number of points
where at least two lines overlap.


Part 2:

Include diagonal lines

"""

import sys
import re
from collections import defaultdict


def main():

    # List with all lines:
    lines = []

    # Read the input and create line objects::
    for input_line in sys.stdin:
        line = Line(input_line.strip())
        lines.append(line)

    field = Field_of_hydrothermal_vents()

    for line in lines:
        if line.is_horzontal_or_vertical():
            for point in line:
                field.inc(point)

    print("Spots for horizontal+vertical lines:", field.count_spots())
    # Spots for horizontal+vertical lines: 6225

    for line in lines:
        if not line.is_horzontal_or_vertical():
            for point in line:
                field.inc(point)

    print("Spots for all lines:", field.count_spots())
    # Spots for all lines: 22116


class Field_of_hydrothermal_vents:

    def __init__ (self):
        self.field = defaultdict(int)

    def inc (self, point):
        self.field[point] += 1

    def count_spots (self):
        spots = 0
        for point in self.field:
            if self.field[point] > 1:
                spots += 1
        return spots


class Line:

    def __init__ (self, text):
        self.parse_text_line(text)
        (self.cursor_x, self.cursor_y) = (self.x1, self.y1)
        # directions (step_x, step_y) for the iterator
        direction = lambda x: [1, 0, -1][(x <= 0) + (x < 0)]
        self.step_x = direction(self.x2 - self.x1)
        self.step_y = direction(self.y2 - self.y1)

    def parse_text_line (self, text):
        # Format: "683,807 -> 370,494"
        matches = re.search('^(\d+),(\d+)\s+->\s+(\d+),(\d+)$', text)
        if matches:
            (self.x1,self.y1,self.x2,self.y2) = list(map(int, matches.group(1,2,3,4)))
        else:
            raise ValueError

    def is_horzontal_or_vertical (self):
        return self.x1 == self.x2 or self.y1 == self.y2

    def __iter__(self):
        return self

    def __next__(self):
        (pos_x, pos_y) = (self.cursor_x, self.cursor_y)
        self.cursor_x += self.step_x
        self.cursor_y += self.step_y
        if pos_x > max(self.x1, self.x2) or pos_x < min(self.x1, self.x2) or pos_y > max(self.y1, self.y2) or pos_y < min(self.y1, self.y2):
            raise StopIteration
        return (pos_x, pos_y)

    def __str__ (self):
        return "{}|{} - {}|{}  (Step: {}|{})".format(self.x1,self.y1,self.x2,self.y2,self.step_x,self.step_y)


if __name__ == '__main__':
    main()
