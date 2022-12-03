#!/usr/bin/env python3

# Usage: cat advent01.input | ./advent01_1.py

"""
https://adventofcode.com/2022/day/2

Usage: cat advent02.input | ./advent02.py

"""

import sys
import collections


Char2item = {
    "A": "Rock",
    "B": "Paper",
    "C": "Scissors",
    "X": "Rock",
    "Y": "Paper",
    "Z": "Scissors"        
}
Worser_as = {
    "Rock": "Scissors",
    "Scissors": "Paper",
    "Paper": "Rock"
}
Better_as = {
    "Scissors": "Rock",
    "Paper": "Rock",
    "Rock": "Scissors" 
}
Points4item = {
    "Rock": 1,
    "Paper": 2,
    "Scissors": 3
}


def main ():

    my_points1 = 0  # Part One
    my_points2 = 0  # Part Two
    for line in sys.stdin:
        (left_char,right_char) = line.split()

        # Part One
        round = Round(Char2item[left_char],Char2item[right_char])
        my_points1 += round.points_right()
        
        # Part Two
        if right_char == "X":
            # X=must loose: worser item for me
            round2 = Round(Char2item[left_char], Worser_as[Char2item[left_char]])
        if right_char == "Y":
            # Y=draw: same item for both sides
            round2 = Round(Char2item[left_char], Char2item[left_char])
        if right_char == "Z":
            # Z=must win: better item for me
            round2 = Round(Char2item[left_char], Better_as[Char2item[left_char]])
        print(round2)
        my_points2 += round2.points_right()

    print("My points (Part 1):", my_points1)
    # My points (Part 1): 13221

    print("My points (Part 2):", my_points2)
    # My points (Part 2): 13131


class Round:

    left = None   # left is for opponent
    right = None  # right is for me

    def __init__ (self, left, right) -> None:
        self.left = Item(left)
        self.right = Item(right)
    
    def points_right (self) -> int:
        win_points = 0
        if self.left == self.right:
            win_points = 3
        if self.right.better(self.left):
            win_points = 6
        return win_points + self.right.points()

    def __str__ (self) -> str:
        return "{} - {} (right gets {} points)".format(self.left, self.right, self.points_right())



class Item:

    def __init__ (self, item) -> None:
        self.item = item

    def better (self, opponent) -> bool:
        if Worser_as[self.item] == opponent.item:
            return True
        return False

    def points (self) -> int:
        return Points4item[self.item]

    def __eq__(self, opponent: object) -> bool:
        if self.item == opponent.item:
            return True
        return False

    def __str__ (self) -> str:
        return self.item



if __name__ == '__main__':
    main()
