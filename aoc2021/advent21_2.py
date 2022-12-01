#!/usr/bin/env python3

# Usage: cat advent21.input | ./advent21_2.py

"""
https://adventofcode.com/2021/day/21

Part 2: all possible games with dics 1-2 and total of 21 points
"""

import sys
from collections import Counter
from collections import defaultdict
import decimal

Occurrence = Counter()

def main():
    global Occurrence

    (n,pos) = sys.stdin.readline().strip().split(' starting position: ')
    pos1 = int(pos)
    (n,pos) = sys.stdin.readline().strip().split(' starting position: ')
    pos2 = int(pos)


    points1 = 0
    points2 = 0
    player = "player 2" # We must start with "player 2", because we set None as "dice" and the first iteration call do nothing - but twist the players
    path = "start"   # Path is only for debugging - not necesaary for the result
    dice = None
    cache = defaultdict(Counter)

    # Calculate the occurrence for sum of three dices with three sides
    for d1 in range(1,4):
        for d2 in range(1,4):
            for d3 in range(1,4):
                Occurrence += Counter({d1+d2+d3:1})


    result = play(pos1,pos2,points1,points2,player,path,dice,cache)
    print(result)
    # Counter({'player 1': 632979211251440, 'player 2': 401295357757593})


def play (pos1,pos2,points1,points2,player,path,dice,cache):
    global Occurrence

    if dice:
        if player == "player 1":
            pos1 = move(pos1, dice)
            points1 += pos1
        if player == "player 2":
            pos2 = move(pos2, dice)
            points2 += pos2
    #print("Status:",pos1,pos2,points1,points2,player,path)
    if points1 >= 21:
        return Counter({"player 1": 1})
    if points2 >= 21:
        return Counter({"player 2": 1})
    cache_key = "{}-{}-{}-{}-{}".format(pos1,pos2,points1,points2,player)
    if cache_key in cache:
        return cache[cache_key]
    result = Counter()
    for dice in range(3,10):
        if player == "player 1": next_player = "player 2"
        if player == "player 2": next_player = "player 1"
        res = play(pos1,pos2,points1,points2,next_player,path+str(dice),dice,cache)
        for n in range(Occurrence[dice]):
            result += res
    cache[cache_key] = result
    return result


def move(pos,dice):
    new_pos = pos + dice
    if new_pos > 10:
        new_pos -= 10
    return new_pos


if __name__ == '__main__':
    main()
