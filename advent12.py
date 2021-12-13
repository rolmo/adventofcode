#!/usr/bin/env python3

# Usage: cat advent12.input | ./advent12.py


"""
https://adventofcode.com/2021/day/12

The input consists of paths between caves.
Small caves consist of lowercase letters, large caves consist of uppercase letters.

Part 1:

Find all paths from "start" to "end". Large caves can be traversed as many times
as you like, small caves may only be visited once.

Part 2:

Find all paths from "start" to "end". Large caves can be traversed as many times
as you like, one of the small caves (only one) can visited twice.

"""

import sys
import collections
import time

Small_Caves_Only_Once = 1
One_Small_Cave_Twice = 2

def main():

    map = Map()
    for line in sys.stdin:
        map.add_path(line.strip())

    # To see all possible paths, set:
    #map.verbose = True

    start_time = time.time()

    # Part 1:
    map.criterium = Small_Caves_Only_Once
    num = map.find_ways()
    print(num)
    # 4885

    # Part 2:
    map.criterium = One_Small_Cave_Twice
    num = map.find_ways()
    print(num)
    # 117095

    end_time = time.time()
    print("(time: {} ms)".format(1000 * (end_time - start_time)))
    # (time: 2451.6968727111816 ms)


class Map:

    def __init__ (self):
        self.connections = {}
        self.criterium = 1
        self.verbose = False


    def add_path (self, path):
        (cave1,cave2) = path.split("-")
        if not cave1 in self.connections:
            self.connections[cave1] = []
        if not cave2 in self.connections:
            self.connections[cave2] = []
        self.connections[cave1].append(cave2)
        self.connections[cave2].append(cave1)


    def find_ways (self, cave="start", path="start"):
        if cave == "end":
            if self.verbose:
                print("Path:", path)
            return 1
        sub_count = 0
        for next_cave in self.connections[cave]:
            if next_cave == "start":
                continue
            if self.criterium == Small_Caves_Only_Once and self.stop_criteria_one(next_cave,path):
                continue
            if self.criterium == One_Small_Cave_Twice and self.stop_criteria_two(next_cave,path):
                continue
            sub_count += self.find_ways(next_cave, path+","+next_cave)
        return sub_count


    def stop_criteria_one (self, cave, path):
        """ Return True (= stop) if the cave is lowercase and already in the path """
        if cave.islower():
            paths = path.split(",")
            if cave in paths:
                return True
        return False


    def stop_criteria_two (self, next_cave, path):
        """
        Return True (= stop) if the cave is lowercase and ...
        - if the cave already visited twice
        - if the cave is already visited and an other cave is already visited twice
        """
        paths = path.split(",")
        paths.append(next_cave)
        counter = collections.Counter(paths)
        double_small_caves = 0
        for cave in counter.keys():
            if cave.islower():
                if counter[cave] > 1:
                    double_small_caves += 1
                    if counter[cave] > 2:
                        return True
        if double_small_caves > 1:
            return True
        return False



if __name__ == '__main__':
    main()
