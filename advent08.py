#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/8

Usage: cat advent08.input | python3 ./advent08.py

Input is a 99x99 Grid

"""

import sys

def main ():
    input = sys.stdin.read().strip().split("\n")

    board = Board(input)
    board.inspect()

    print(board)

    print("Count of visible Trees:", board.count_visible())
    # Count of visible Trees: 1690

    print("Best view score:", board.bestview())
    # Best view score: 535680



class Board:

    def __init__ (self, input):
        self.board = []
        for line in input:
            row = []
            for num in line:
                elem = [int(num), False]
                row.append(elem)
            self.board.append(row)
        self.max_x = len(self.board[0])
        self.max_y = len(self.board)

    def inspect (self):
        for x in range(self.max_x):
            self._inspect_one_direction([x], range(self.max_y))
            self._inspect_one_direction([x], range(self.max_y - 1, -1, -1))
        for y in range(self.max_y):
            self._inspect_one_direction(range(self.max_x), [y])
            self._inspect_one_direction(range(self.max_x - 1, -1, -1), [y])

    def _inspect_one_direction(self, range_x, range_y):
        height = -1
        for x in range_x:
            for y in range_y:
                if self.board[y][x][0] > height:
                    self.board[y][x][1] = True
                    height = self.board[y][x][0]

    def count_visible(self):
        count = 0
        for row in self.board:
            for elem in row:
                if elem[1]:
                    count += 1
        return count

    def bestview(self):
        best_scenic_score = 0
        for x in range(self.max_x):
            for y in range(self.max_y):
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
        height =  self.board[y][x][0]
        width = 0
        while True:
            x = x + dx
            y = y + dy
            if x < 0: break
            if y < 0: break
            if x >= self.max_x: break
            if y >= self.max_y: break
            width += 1
            if self.board[y][x][0] >= height: break
        return width

    def __str__(self):
        output = ""
        for row in self.board:
            for elem in row:
                if elem[1]:
                    output += f"\033[1;36m{elem[0]:2}\033[0m"
                else:
                    output += f"{elem[0]:2}"
            output += "\n" 
        return output


if __name__ == '__main__':
    main()
