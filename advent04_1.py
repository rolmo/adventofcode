#!/usr/bin/env python3

# Usage: cat advent04.input | ./advent04_1.py

import sys
import re

def main():
    guessed_numbers=list(map(int, sys.stdin.readline().strip().split(',')))

    boards = []
    board = None
    board_number = 0
    for line in sys.stdin:
        if line.strip():
            board.add_row(list(map(int, re.split("\s+",line.strip()))))
        else:
            # Empty line: create a new board
            board_number += 1
            board = Board(board_number)
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
    board_number = None

    def __init__ (self, board_number):
        self.rows = []
        self.marked = []
        for row in range(5):
            self.marked.append([False]*5)
        self.board_number = board_number
        self.bingo = False

    def add_row (self, row):
        self.rows.append(row)

    def mark (self, guessed):
        for row in range(5):
            for col in range(5):
                if self.rows[row][col] == guessed:
                    #print("Mark number {} in board={}, row={} and col={}".format(guessed,self.board_number,row,col))
                    self.marked[row][col] = True

    def check_bingo(self):
        for row in range(5):
            hit = True
            for col in range(5):
                if not self.marked[row][col]:
                    hit = False
            if hit:
                #print("Hit in board {} in row {}".format(self.board_number,row+1))
                self.bingo = True
        for col in range(5):
            hit = True
            for row in range(5):
                if not self.marked[row][col]:
                    hit = False
            if hit:
                #print("Hit in board {} in col {}".format(self.board_number,col+1))
                self.bingo = True
        return self.bingo

    def get_unmarked_sum(self):
        sum = 0
        for row in range(5):
            for col in range(5):
                if not self.marked[row][col]:
                    sum += self.rows[row][col]
        return sum


    def __str__(self):
        out = "-------{}------\n".format(self.board_number)
        for row in self.rows:
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
