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

Calculate the result as in part one.
"""


import sys
import re

def main():
    # First line of input contains the guessed numbers (we convert to array-of-int)
    guessed_numbers=list(map(int, sys.stdin.readline().strip().split(',')))

    # Array with all board:
    boards = []

    # Read input and create all boards:
    for line in sys.stdin:
        if line.strip():
            # Non empty line: convert to array-of-int and add to the last board:
            board.add_row(list(map(int, re.split("\s+",line.strip()))))
        else:
            # Empty line: create a new board
            board = Board()
            boards.append(board)

    print("Find the first board that wins")
    (sum, number) = guess(boards, guessed_numbers, "find first")
    print("Sum of unmarked numbers: {}, last guessed number: {}, Product {}".format(sum, number, sum*number))
    # Sum of unmarked numbers: 1137, last guessed number: 5, Product 5685

    print("Find the last board that wins")
    (sum, number) = guess(boards, guessed_numbers, "find last")
    print("Sum of unmarked numbers: {}, last guessed number: {}, Product {}".format(sum, number, sum*number))
    # Sum of unmarked numbers: 430, last guessed number: 49, Product 21070


def guess (boards, guessed_numbers, strategy):
    last_guessed = last_sum = 0
    for guessed in guessed_numbers:
        # print("Guessing ",guessed)
        for board in boards:
            if board.bingo:
                continue
            board.mark(guessed)
            #print(board)
            if not board.bingo and board.check_bingo():
                sum = board.get_unmarked_sum()
                if strategy == "find first":
                    return (sum, guessed)
                last_guessed = guessed
                last_sum = sum
    return (last_sum, last_guessed)



class Board:

    def __init__ (self):
        self.board = []
        self.marked = []
        for row in range(5):
            self.marked.append([False]*5)
        self.bingo = False

    def add_row (self, row):
        self.board.append(row)

    def mark (self, guessed):
        for row in range(5):
            for col in range(5):
                if self.board[row][col] == guessed:
                    #print("Mark number {} row={} and col={}".format(guessed,row,col))
                    self.marked[row][col] = True

    def check_bingo(self):
        for row in range(5):
            hit = True
            for col in range(5):
                if not self.marked[row][col]:
                    hit = False
            if hit:
                #print("Hit in row {}".format(row+1))
                self.bingo = True
        for col in range(5):
            hit = True
            for row in range(5):
                if not self.marked[row][col]:
                    hit = False
            if hit:
                #print("Hit in col {}".format(col+1))
                self.bingo = True
        return self.bingo

    def get_unmarked_sum(self):
        sum = 0
        for row in range(5):
            for col in range(5):
                if not self.marked[row][col]:
                    sum += self.board[row][col]
        return sum

    # Only for the debug output: string representation of the board and marks
    def __str__(self):
        out = "-------------\n"
        for row in self.board:
            for num in row:
                out += "|" + str(num)
            out += "|\n"
        for row in self.marked:
            for bool in row:
                out += "|" + ("X" if bool else "-")
            out += "|\n"
        return out



if __name__ == '__main__':
    main()
