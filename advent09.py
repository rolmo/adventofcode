#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/9

Usage: cat advent09.input | python3 ./advent09.py

"""
import sys

ROPE_LEN = 2  # 2

def main ():
    input = sys.stdin.read().strip().split("\n")

    rope = [(0,0) for n in range(ROPE_LEN)]
    positions_t = set()
    for line in input:
        #print(">>>>",line)
        (direction, count) = line.split(" ")
        for n in range(int(count)):
            if direction == "U":
                rope[0] = u(rope[0])
            if direction == "D":
                rope[0] = d(rope[0])
            if direction == "L":
                rope[0] = l(rope[0])
            if direction == "R":
                rope[0] = r(rope[0])
            follow(rope)
            positions_t.add(rope[len(rope)-1])

    print(len(positions_t))
    # ROPE_LEN = 2: 6503
    # ROPE_LEN = 10: 2724

def u (pos):
    return (pos[0],pos[1]+1)
def d (pos):
    return (pos[0],pos[1]-1)
def r (pos):
    return (pos[0]+1,pos[1])
def l (pos):
    return (pos[0]-1,pos[1])

def follow(rope):
    for pos in range(len(rope) - 1):
        (hx,hy) = rope[pos]
        (tx,ty) = rope[pos+1]
        if hx - tx > 1:
            tx += 1
            if ty < hy: ty += 1
            if ty > hy: ty -= 1
        elif hx - tx < -1:
            tx -= 1
            if ty < hy: ty += 1
            if ty > hy: ty -= 1
        elif hy - ty > 1:
            ty += 1
            if tx < hx: tx += 1
            if tx > hx: tx -= 1
        elif hy - ty < -1:
            ty -= 1
            if tx < hx: tx += 1
            if tx > hx: tx -= 1
        rope[pos+1] = (tx,ty)

def printBoard (x,y,rope):
    print("-"*16)
    board = []
    for row in range(y,-1,-1):
        for col in range(x+1):
            char = "."
            for pos in reversed(range(len(rope))):
                if rope[pos] == (col, row):
                    if pos == 0:
                        char = "H"
                    else:
                        char = pos
            print("  {}".format(char), end="")
        print("")



if __name__ == '__main__':
    main()
