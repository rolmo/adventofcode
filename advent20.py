#!/usr/bin/env python3

# Usage:
#  cat advent20.input | ./advent20.py 2
#  cat advent20.input | ./advent20.py 50

"""
https://adventofcode.com/2021/day/20
"""


import sys
from dataclasses import dataclass
from pprint import pformat


def main():

    number_of_enhancements = 2
    try:
        number_of_enhancements = int(sys.argv[1])
    except IndexError:
        print("give number of enhancements as first argument (default is 2)")

    board = Board()

    # First line of input contains the "enhancement_algorithm":
    board.enhancement_algorithm = sys.stdin.readline().strip()

    # Read the rest of the input and create the board:
    for line in sys.stdin:
        if line.strip():
            board.add_row(line.strip())


    board.extend(number_of_enhancements * 2)
    for n in range(number_of_enhancements):
        #print(board)
        board.enhance()
    #print(board)
    c = board.count_light_pixel()
    print(c)
    # 2:
    # 5464
    # 50:
    # 19228

class Board:

    def __init__ (self):
        self.enhancement_algorithm = ""
        self.board = []
        self.num_rows = 0
        self.num_cols = 0


    def add_row (self, input):
        self.board.append(input)
        self.num_rows += 1
        self.num_cols = len(input)

    def count_light_pixel (self):
        c = 0
        for row in self.board:
            c += row.count('#')
        return c

    def extend (self, num):
        for row in range(self.num_rows):
            self.board[row] = "." * num + self.board[row] + "." * num
        for n in range(num):
            self.board.insert(0, "." * (self.num_cols + 2 * num))
        for n in range(num):
            self.board.append("." * (self.num_cols + 2 * num))
        self.num_rows += 2 * num
        self.num_cols += 2 * num


    def enhance (self):
        board = []
        for row in range(1, self.num_rows-1):
            new_row = ""
            for col in range (1,self.num_cols-1):
                new_row += self.enhancement_algorithm[self._range_as_num(row,col)]
            board.append(new_row)
        self.board = board
        self.num_rows -= 2
        self.num_cols -= 2


    def _range_as_num (self, row, col):
        bits =  self.board[row -1][(col-1):(col+2)]
        bits += self.board[row   ][(col-1):(col+2)]
        bits += self.board[row +1][(col-1):(col+2)]
        bits = bits.replace(".","0")
        bits = bits.replace("#","1")
        return int(bits, 2)

    def __str__ (self):
        output = "\n"
        for row in self.board:
            output += row + "\n"
        return output


if __name__ == '__main__':
    main()
