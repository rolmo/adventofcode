#!/usr/bin/env python3

# Usage: cat advent11.input | ./advent11.py


"""

https://adventofcode.com/2021/day/11

"""
import sys
from dataclasses import dataclass


def main():

    board = Board()
    for line in sys.stdin:
        board.add_row(line.strip())


    for step in board:
        if step <= 100:
            print(board)
        if step == 100:
            print("Total flashes after 100 steps:", board.flash_count)
        if step > 100 and board.all_flashes:
            break

    print("All flashes after step:", board.all_flashes)



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


    def _step (self):
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
        if (count == self.rows * self.cols):
            self.all_flashes = self._steps
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

    def __iter__ (self):
        self._steps = 0
        self.all_flashes = False
        return self

    def __next__ (self):
        self._steps += 1
        self._step()
        return self._steps

    def __str__ (self):
        out = f"Board after step {self._steps}\n"
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
