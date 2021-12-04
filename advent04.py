#!/usr/bin/env python3

# Usage: cat advent04.input | ./advent04.py

"""
Part One:

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
Numbers are chosen at random, and the chosen number is marked on all boards on
which it appears. (Numbers may not appear on all boards.) If all numbers in any
row or any column of a board are marked, that board wins. (Diagonals don't count.)

The score of the winning board can now be calculated. Start by finding the sum
of all unmarked numbers on that board.
Then, multiply that sum by the number that was just called when the board won.

Part Two:

Figure out which board will win last

Calculate the result like part one.
"""


import sys
import re
from dataclasses import dataclass
from pprint import pformat


def main():
    # First line of input contains the random numbers (we convert to array-of-int)
    random_list=list(map(int, sys.stdin.readline().strip().split(',')))

    # Array with all boards:
    boards = []

    # Read the rest of the input and create all boards:
    for line in sys.stdin:
        if line.strip():
            # Non empty line: convert to array-of-int and add to the last board:
            board.add_row(list(map(int, re.split("\s+",line.strip()))))
        else:
            # Empty line: create a new board
            board = Board()
            boards.append(board)


    print("Find the first winning board:")
    board = run(boards, random_list, "find first")
    print(board)
    sum = board.get_unmarked_sum()
    last_marked = board.last_marked
    print("Sum of unmarked numbers: {}, last marked number: {}, Product {}".format(sum, last_marked, sum*last_marked))
    # Sum of unmarked numbers: 1137, last marked number: 5, Product 5685

    print("Find the last winning board:")
    board = run(boards, random_list, "find last")
    print(board)
    sum = board.get_unmarked_sum()
    last_marked = board.last_marked
    print("Sum of unmarked numbers: {}, last marked number: {}, Product {}".format(sum, last_marked, sum*last_marked))
    # Sum of unmarked numbers: 430, last marked number: 49, Product 21070




def run (boards, random_list, strategy):
    """
    Check each random number agains all board and returns the first or the last
    board that has a Bingo!
    """
    for number in random_list:
        for board in boards:
            if board.bingo:
                # To find the last board, we skip boards with an Bingo!
                continue
            board.mark(number)
            if board.check_bingo():
                if strategy == "find first":
                    # Stop immediately and return first bingo board:
                    return board
                last_bingo_board = board
    return last_bingo_board



class Board:

    def __init__ (self):
        self.matrix = []
        self.bingo = False
        self.last_marked = None

    def add_row (self, row):
        self.matrix.append(list(map(lambda x: Cell(x), row)))

    def mark (self, number):
        for row in range(5):
            for col in range(5):
                if self.matrix[row][col].mark(number):
                    self.last_marked = number

    def check_bingo(self):
        for row in range(5):
            hit = True
            for col in range(5):
                if not bool(self.matrix[row][col]):
                    hit = False
            if hit:
                self.bingo = True
                return True
        for col in range(5):
            hit = True
            for row in range(5):
                if not bool(self.matrix[row][col]):
                    hit = False
            if hit:
                self.bingo = True
                return True
        return False

    def get_unmarked_sum(self):
        sum = 0
        for row in range(5):
            for col in range(5):
                # the int() returns 0 for marked Cells:
                sum += int(self.matrix[row][col])
        return sum

    def __str__(self):
        return pformat(self.matrix)


@dataclass
class Cell:
    number: int
    marked: bool = False

    def mark(self, number):
        if number == self.number:
            self.marked = True
        return self.marked

    def __eq__(self, other):
        return self.number == other

    def __int__ (self):
        if self.marked:
            return 0
        else:
            return self.number

    def __bool__ (self):
        return self.marked

    def __str__ (self):
        return f"\033[91m{self.number:2}\033[0m" if self.marked else f"{self.number:2}"

    __repr__ = __str__




if __name__ == '__main__':
    main()
