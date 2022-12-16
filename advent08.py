#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/8

Usage: cat advent08.input | python3 ./advent08.py

"""

import sys

def main ():
    input = sys.stdin.read().strip().split("\n")

    grid = Grid(input)
    grid.mark_visible_trees()
    print(grid)

    print("Count of visible trees:", grid.count_visible())
    # Count of visible Trees: 1690

    print("Best view score:", grid.bestview())
    # Best view score: 535680


class Grid:

    def __init__ (self, input):
        self._grid = []
        for line in input:
            row = list(map(lambda x: [int(x), False], list(line)))
            self._grid.append(row)
        self._max_x = len(self._grid[0])
        self._max_y = len(self._grid)

    def mark_visible_trees (self):
        # Follow each of the 4 edges and mark all visible trees
        for x in range(self._max_x):
            self._inspect_one_direction([x], range(self._max_y))
            self._inspect_one_direction([x], range(self._max_y - 1, -1, -1))
        for y in range(self._max_y):
            self._inspect_one_direction(range(self._max_x), [y])
            self._inspect_one_direction(range(self._max_x - 1, -1, -1), [y])

    def _inspect_one_direction(self, range_x, range_y):
        height = -1
        for x in range_x:
            for y in range_y:
                if self._grid[y][x][0] > height:
                    self._grid[y][x][1] = True
                    height = self._grid[y][x][0]

    def count_visible(self):
        return sum(map(lambda row: len(list(filter(lambda x: x[1], row))), self._grid))

    def bestview(self):
        best_scenic_score = 0
        for x in range(self._max_x):
            for y in range(self._max_y):
                scenic_score = self._look_around(x,y)
                if scenic_score > best_scenic_score:
                    best_scenic_score = scenic_score
        return best_scenic_score

    def _look_around(self,x,y):
        distance1 = self._look_direction(x,y,0,1)
        distance2 = self._look_direction(x,y,1,0)
        distance3 = self._look_direction(x,y,0,-1)
        distance4 = self._look_direction(x,y,-1,0)
        return distance1 * distance2 * distance3 * distance4

    def _look_direction(self,x,y,dx,dy):
        height = self._grid[y][x][0]
        width = 0
        while True:
            x = x + dx
            y = y + dy
            if x not in range(self._max_x): break
            if y not in range(self._max_y): break
            width += 1
            if self._grid[y][x][0] >= height: break
        return width

    def __str__(self):
        output = ""
        for row in self._grid:
            for tree in row:
                if tree[1]:
                    output += f"\033[1;36m{tree[0]:2}\033[0m"
                else:
                    output += f"{tree[0]:2}"
            output += "\n" 
        return output


if __name__ == '__main__':
    main()
