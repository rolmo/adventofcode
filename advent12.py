#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/12

Usage:
cat advent12.input | ./advent12.py
"""

import sys
import time

def main ():
    input = sys.stdin.read().strip().split('\n')

    print("Part 1:", part1(input))
    # 7633
    print("Part 2:", part2(input))
    # 23903579139437


def part1 (input):
    sum = 0
    for line in input:
        #print(line)
        springs = Springs(line)
        sum += springs.arrangements()
    return sum

def part2 (input):
    sum = 0
    for line in input:
        unfolded = unfold(line)
        #print(unfolded)
        springs = Springs(unfolded)
        start_time = time.time()
        arrangements = springs.arrangements()
        end_time = time.time()
        #print(arrangements, "arrangements - Seconds:", end_time - start_time)
        sum += arrangements
    return sum

def unfold (line):
    row, checksum = line.split(' ')
    new_row = "?".join([row for i in range(5)])
    new_checksum = ",".join([checksum for i in range(5)])
    return new_row + " " + new_checksum



class Springs:

    def __init__ (self, row):
        self.row, checksum = row.split(' ')
        self.checksum = [int(i) for i in checksum.split(',')]
        self.num_of_known_ok = self.row.count('.')
        self.num_of_known_broken = self.row.count('#')
        self.num_of_unknown = self.row.count('?')
        self.num_of_broken = sum(self.checksum)
        self.num_of_unknown_broken = self.num_of_broken - self.num_of_known_broken
        self.num_of_unknown_ok = self.num_of_unknown - self.num_of_unknown_broken


    def arrangements (self):
        cached_solutions = {}
        return self.test_placing_first_number(self.row, self.checksum, cached_solutions)


    def test_placing_first_number (self, row, checksum, cached_solutions, depth=0):
        verbose = False
        cache_key = row + (",".join([str(i) for i in checksum]))
        if cache_key in cached_solutions:
            return cached_solutions[cache_key]
        if len(checksum) == 0:
            if not "#" in row:
                if verbose: print("    "*depth, "Found a solution!")
                return 1
            else:
                return 0
        number = checksum[0]
        padded_row = "." + row + "." # Add a dot at the beginning and end to make the algorithm easier
        if verbose: print("    "*depth, "Search possible positions for:", number, "in", padded_row)
        combinations = 0
        for i in range(1, len(padded_row) - number + 1):
            if "." in padded_row[i:i+number]:
                continue
            if padded_row[i-1] == "#":
                continue
            if padded_row[i+number] == "#":
                continue
            if "#" in padded_row[0:i]:
                continue
            # We have found a place for the number - but is the rest also solvable?
            # We reduce the problem to a smaller one and call us recursively:
            if verbose: print("    "*depth, "Possible", number, "at", i)
            result = self.test_placing_first_number(row[i+number:], checksum[1:], cached_solutions, depth+1)
            combinations += result
        cache_key = row + (",".join([str(i) for i in checksum]))
        cached_solutions[cache_key] = combinations
        return combinations



if __name__ == '__main__':
    main()