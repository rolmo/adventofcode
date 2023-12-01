#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/2

Usage: cat advent02.input | ./advent02.py

"""

import sys

def main ():

    my_points1 = 0  # Part One
    my_points2 = 0  # Part Two
    for line in sys.stdin:
        (left_char,right_char) = line.split()

        round = Round(get_item(left_char), get_item(right_char))
        my_points1 += round.points_right()

        # Part Two
        if right_char == "X":
            # X = must loose: worser item for me
            left = get_item(left_char)
            right = get_item(left.worser)
        if right_char == "Y":
            # Y = draw: same item for both sides
            left = right = get_item(left_char)
        if right_char == "Z":
            # Z = must win: better item for me
            left = get_item(left_char)
            right = get_item(left.better)
        round = Round(left, right)
        my_points2 += round.points_right()

    print("My points (Part 1):", my_points1)
    # My points (Part 1): 13221

    print("My points (Part 2):", my_points2)
    # My points (Part 2): 13131



def get_item (char: str) -> object:
    match char:
        case "A" | "X" | "Rock":
            return Rock()
        case "B" | "Y" | "Paper":
            return Paper()
        case "C" | "Z" | "Scissors":
            return Scissors()



class Round:

    def __init__ (self, left, right) -> None:
        self.left = left
        self.right = right
    
    def points_right (self) -> int:
        win_points = 0
        if self.left == self.right:
            win_points = 3
        if self.right > self.left:
            win_points = 6
        return win_points + self.right

    def __str__ (self) -> str:
        return "{} - {} (right gets {} points)".format(self.left, self.right, self.points_right())



class Item:

    def __str__(self) -> str:
        return type(self).__name__

    def __eq__(self, other: object) -> bool:
        if type(self).__name__ == type(other).__name__:
            return True
        return False

    def __gt__(self, other: object) -> bool:
        if type(other).__name__ == self.worser:
            return True
        return False

    def __radd__(self, other):
        return self.points + other


class Rock(Item):
    better = "Paper"
    worser = "Scissors"
    points = 1

class Paper(Item):
    better = "Scissors"
    worser = "Rock"
    points = 2

class Scissors(Item):
    better = "Rock"
    worser = "Paper"
    points = 3


if __name__ == '__main__':
    main()
