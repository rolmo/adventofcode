#!/usr/bin/env python3

# Usage: cat advent15.input | ./advent15.py

"""
https://adventofcode.com/2021/day/15
"""

import sys


#https://de.wikipedia.org/wiki/Dijkstra-Algorithmus
#https://algorithms.discrete.ma.tum.de/graph-algorithms/spp-dijkstra/index_de.html


from dataclasses import dataclass
from collections import defaultdict
import time


def main():

    map = Map()
    for line in sys.stdin:
        map.add_row(line.strip())

    total_risc = map.find_best_way()
    print(total_risc)
    # 373

    start_time = time.time()

    map.extend_map_5()
    #map.print_board()
    total_risc = map.find_best_way()
    print(total_risc)
    # 2868

    end_time = time.time()
    print("(time: {} ms)".format(1000 * (end_time - start_time)))
    # (time: 1894.0558433532715 ms)

class Map:

    def __init__ (self):
        self.map=[]
        self.max_x = -1
        self.max_y = -1
        self.queue = defaultdict(set)
        self._loops = 0


    def add_row (self,input_row):
        row = []
        self.max_x = len(input_row) -1
        for num in input_row:
            node = Node(int(num))
            row.append(node)
        self.map.append(row)
        self.max_y += 1


    # Only for part 2: resize the map with x5 for x and y (x25 for the positions)
    def extend_map_5 (self):
        new_map = []
        for y5 in range(5):
            for y in range (self.max_y + 1):
                row = list()
                for x5 in range(5):
                    for x in range(self.max_x +1):
                        risc = self.map[x][y].risc
                        new_risc = risc + x5 + y5
                        if new_risc > 9:
                            new_risc -= 9
                        row.append(Node(new_risc))
                new_map.append(row)
        self.map = new_map
        self.max_x = 5 * self.max_x + 4
        self.max_y = 5 * self.max_y + 4


    def find_best_way (self):
        startpoint = Point(0,0)
        self._mark_node(startpoint, 0)
        while True:
            self._loops += 1
            point = self._get_next_from_queue()
            if point == None:
                break
            total_risc = self.map[point.x][point.y].total_risc
            neighbors = self._get_neighbors(point)
            for neighbor in neighbors:
                risc = self.map[neighbor.x][neighbor.y].risc
                self._mark_node(neighbor, total_risc + risc)
        print("Loops", self._loops)
        return self.map[self.max_x][self.max_y].total_risc


    def _mark_node(self, point, total_risc):
        if self.map[point.x][point.y].visited:
            if self.map[point.x][point.y].total_risc < total_risc:
                return
        self.map[point.x][point.y].total_risc = total_risc
        self.map[point.x][point.y].visited = True
        self.queue[total_risc].add(point)


    def _get_next_from_queue (self):
        for risc in sorted(self.queue.keys()):
            if len(self.queue[risc]):
                point = self.queue[risc].pop()
                return point
            else:
                del(self.queue[risc])
        return None


    def _get_neighbors (self, point):
        neighbors = set()
        if point.x > 1: neighbors.add(Point(point.x - 1, point.y))
        if point.y > 1: neighbors.add(Point(point.x, point.y - 1))
        if point.y < self.max_y: neighbors.add(Point(point.x, point.y + 1))
        if point.x < self.max_x: neighbors.add(Point(point.x + 1, point.y))
        return neighbors


    def print_board (self):
        for row in self.map:
            for col in row:
                print("{}.{:2} ".format(col.risc, col.get_total_risc()), end="")
                #print("{:2} ".format(col.risc), end="")
            print()


@dataclass
class Node:
    risc: int
    total_risc: int = None
    visited: bool = False
    #predecessor = None

    def __str__ (self):
        return f"risc={self.risc}, total_risc={self.total_risc}"

    def get_total_risc (self):
        if self.total_risc == None:
            return "-"
        return self.total_risc


@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int


if __name__ == '__main__':
    main()
