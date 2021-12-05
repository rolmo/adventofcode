#!/usr/bin/env python3

# Usage: cat advent05.input | ./advent05.py


"""
Part 1:

Each line of vents is given as a line segment in the format "x1,y1 -> x2,y2"
where x1,y1 are the coordinates of one end of the line segment and x2,y2 are the
coordinates of the other end.
These line segments include the points at both ends. In other words:

    An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

To avoid the most dangerous areas, you need to determine the number of points
where at least two lines overlap.


Part 2:

Include diagonal lines

"""

import sys
import re
from collections import defaultdict
from dataclasses import dataclass


def main():

    # Read the input and create line objects::
    lines = []
    for input_line in sys.stdin:
        line = Line(input_line.strip())
        lines.append(line)

    field = Field_of_hydrothermal_vents()

    for line in lines:
        if line.is_horzontal_or_vertical():
            for point in line:
                field.inc(point)

    print("Overlaps for horizontal+vertical lines:", field.count_overlaps())
    # Overlaps for horizontal+vertical lines: 6225

    for line in lines:
        if not line.is_horzontal_or_vertical():
            for point in line:
                field.inc(point)

    print("Overlaps for all lines:", field.count_overlaps())
    # Overlaps for all lines: 22116



class Field_of_hydrothermal_vents:

    def __init__ (self):
        self.field = defaultdict(int)

    def inc (self, point):
        self.field[str(point)] += 1

    def count_overlaps (self):
        overlaps = 0
        for point in self.field:
            if self.field[point] > 1:
                overlaps += 1
        return overlaps


class Line:

    def __init__ (self, text):
        self.parse_text_line(text)

    def parse_text_line (self, text):
        # Format: "683,807 -> 370,494"
        matches = re.search('^(\d+),(\d+)\s+->\s+(\d+),(\d+)$', text)
        if matches:
            self.point1 = Point(int(matches.group(1)),int(matches.group(2)))
            self.point2 = Point(int(matches.group(3)),int(matches.group(4)))
        else:
            raise ValueError

    def is_horzontal_or_vertical (self):
        return self.point1.x == self.point2.x or self.point1.y == self.point2.y

    def __iter__(self):
        self.cursor = None
        return self

    def __next__(self):
        # To include the first and the last point on the line, we
        # skip the "cursor.move" for the first iteration:
        if not self.cursor:
            self.cursor = self.point1.clone()
            return self.cursor
        if not self.cursor.move(self.point2):
            raise StopIteration
        else:
            return self.cursor

    def __str__ (self):
        return "{} - {}".format(self.point1,self.point2)


@dataclass
class Point:
    x: int
    y: int

    def clone (self):
        return Point(self.x, self.y)

    def move (self, target):
        """
        Moves the point one step towards the target
        Returns False, if target is already reached
        """
        if target.x == self.x and target.y == self.y:
            return False
        if target.x > self.x: self.x += 1
        if target.x < self.x: self.x -= 1
        if target.y > self.y: self.y += 1
        if target.y < self.y: self.y -= 1
        return True


if __name__ == '__main__':
    main()
