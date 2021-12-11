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

    print("Tolat flash count:", board1.flash_count)
    # Tolat flash count: 1591


    # Part 2:

    steps = 0
    flashes = 0
    all_flashes = board2.rows * board2.cols
    while flashes < all_flashes:
        steps += 1
        flashes = board2.step()

    print("All flashes ({}) after {} steps".format(all_flashes,steps))
    # All flashes (100) after 314 steps




class Board:

    def __init__ (self):
        self.board=[]
        self.rows = 0
        self.cols = 0
        self.flash_count = 0


    def add_row (self,input_row):
        row = []
        self.cols = len(input_row)
        for num in input_row:
            octupus = Octopus(int(num))
            row.append(octupus)
        self.board.append(row)
        self.rows += 1


    def step (self):
        for row in range(self.rows):
            for col in range(self.cols):
                self._inc_pos(row,col)
        return self._count_and_reset_flashes()


    def _octopus (self, row, col):
        """ Returns a single octupus for row+col """
        return self.board[row][col]

    def _count_and_reset_flashes (self):
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self._octopus(row,col).reset_flash():
                    count += 1
        self.flash_count += count
        return count


    def _inc_pos (self, row, col):
        # Do nothing for unreachable positions:
        if 0 > row or row >= self.rows: return
        if 0 > col or col >= self.cols: return
        # Increment the energy for the octopus ...
        if self._octopus(row,col).inc():
            # ... and if the octopus flashes, increment all neighbors
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
    _energy: int
    _flash: bool = False

    def inc (self):
        """
        inc increments the energy by one.

        if the energy raises the threshold 9:
            - set energy to 0
            - set a flag "flash"
            - return True (all other cases return False)

        if the flag "flash" is already set, do nothing
        """
        if self._flash:
            return False
        self._energy += 1
        if self._energy > 9:
            self._energy = 0
            self._flash = True
            return True
        return False

    def reset_flash (self):
        if self._flash:
            self._flash = False
            return True
        return False

    def __str__ (self):
        return f"{self._energy:2}"



if __name__ == '__main__':
    main()
