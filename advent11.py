#!/usr/bin/env python3

# Usage: cat advent11.input | ./advent11.py


"""

https://adventofcode.com/2021/day/11

"""
import sys
from dataclasses import dataclass


def main():

    board1 = Board()
    board2 = Board()
    for line in sys.stdin:
        board1.add_row(line.strip())
        board2.add_row(line.strip())

    # Part 1:

    print("Before any steps:")
    print(board1)

    for step in range(100):
        board1.step()
        print("After step", step+1)
        print(board1)

    print("Tolat flash count", board1.flash_count)
    # Tolat flash count 1591


    # Part 2:

    steps = 0
    flashes = 0
    all_flashes = board2.max_row * board2.max_col
    while flashes < all_flashes:
        steps += 1
        flashes = board2.step()

    print("All flashes ({}) after {} steps".format(all_flashes,steps))
    # All flashes (100) after 314 steps

class Board:

    def __init__ (self):
        self.board=[]
        self.max_row = 0
        self.max_col = 0
        self.flash_count = 0


    def add_row (self,input_row):
        row = []
        self.max_col = max(self.max_col, len(input_row))
        for num in input_row:
            octupus = Octopus(int(num))
            row.append(octupus)
        self.board.append(row)
        self.max_row += 1


    def step (self):
        for row in range(self.max_row):
            for col in range(self.max_col):
                self._inc_pos(row,col)
        return self._count_and_reset_flashes()


    def _count_and_reset_flashes (self):
        count = 0
        for row in range(self.max_row):
            for col in range(self.max_col):
                if self.board[row][col].flash:
                    count += 1
                    self.board[row][col].flash = False
        self.flash_count += count
        return count


    def _inc_pos (self, row, col):
        #print("inc:",row,col,self.max_row,self.max_col)
        if row < 0: return False
        if col < 0: return False
        if row >= self.max_row: return False
        if col >= self.max_col: return False
        if self.board[row][col].inc():
            self._inc_neighbors(row,col)


    def _inc_neighbors (self, row, col):
        self._inc_pos(row-1,col-1)
        self._inc_pos(row-1,col)
        self._inc_pos(row-1,col+1)
        self._inc_pos(row,col-1)
        self._inc_pos(row,col+1)
        self._inc_pos(row+1,col-1)
        self._inc_pos(row+1,col)
        self._inc_pos(row+1,col+1)


    def __str__ (self):
        out = ""
        for row in self.board:
            for octopus in row:
                out += str(octopus)
            out += "\n"
        #out += "Flashcount: {}\n".format(self.flash_count)
        return out



@dataclass
class Octopus:
    energy: int
    flash: bool = False

    def inc (self):
        if self.flash:
            return False
        self.energy += 1
        if self.energy > 9:
            self.energy = 0
            self.flash = True
            return True
        return False

    def __str__ (self):
        return f"{self.energy:2}"



if __name__ == '__main__':
    main()
