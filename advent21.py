#!/usr/bin/env python3

# Usage: cat advent21.input | ./advent21.py

"""
https://adventofcode.com/2021/day/21

Part 1: 100 sided dice

"""


import sys
import re
from dataclasses import dataclass

def main():

    board = Board()

    for line in sys.stdin:
        board.addPlayer(line.strip())

    dice = Dice()

    for player in board:
        dice_sum = next(dice) + next(dice) + next(dice)
        player.movePlayer(dice_sum)
        print(player)

    print("Dices:", dice.count)
    print("Looser:", board.looser())
    print(board.looser().points * dice.count)
    # 506466



class Board:

    def __init__ (self):
        self.players = list()


    def addPlayer (self, input):
        (name, position) = input.split(' starting position: ')
        self.players.append(Player(name, int(position)))


    def looser (self):
        looser = None
        for player in self.players:
            if looser == None:
                looser = player
            else:
                if player.points < looser.points:
                    looser = player
        return looser


    def __iter__ (self):
        self.curent_player = -1
        return self


    def __next__ (self):
        self.curent_player += 1
        if self.curent_player >= len(self.players):
            self.curent_player = 0
        for player in self.players:
            if player.points >= 1000:
                raise StopIteration
        return self.players[self.curent_player]



@dataclass
class Dice:
    num: int = 0
    count: int = 0

    def __iter__ (self):
        return self


    def __next__ (self):
        self.count += 1
        self.num += 1
        if self.num > 100:
            self.num = 1
        return self.num



@dataclass
class Player:
    name: str
    position: int
    points: int = 0

    def movePlayer (self, positions):
        self.position += positions
        while self.position > 10:
            self.position -= 10
        self.points += self.position



if __name__ == '__main__':
    main()
