#!/usr/bin/env python3

# Usage: cat advent12.input | ./advent12.py


"""

https://adventofcode.com/2021/day/12

"""

import sys
import time

Small_Caves_Only_One = 1
One_Small_Cave_Twice = 2

def main():

    map = Map()
    for line in sys.stdin:
        map.add_path(line.strip())

    # To see all possible paths, set:
    #map.verbose = True

    start_time = time.time()

    # Part 1:
    map.criterium = Small_Caves_Only_One
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
            if self.criterium == Small_Caves_Only_One and self.stop_criteria_one(next_cave,path):
                continue
            if self.criterium == One_Small_Cave_Twice and self.stop_criteria_two(next_cave,path):
                continue
            sub_count += self.find_ways(next_cave, path+","+next_cave)
        return sub_count


    def stop_criteria_one (self, cave, path):
        if cave.islower():
            paths = path.split(",")
            if cave in paths:
                return True
        return False


    def stop_criteria_two (self, next_cave, path):
        if next_cave.isupper():
            return False
        paths = path.split(",")
        paths.append(next_cave)
        count_per_cave = {}
        for cave in paths:
            if cave.islower():
                if cave in count_per_cave:
                    count_per_cave[cave] += 1
                else:
                    count_per_cave[cave] =1
        double_small_caves = 0
        for cave, count in count_per_cave.items():
            if count > 2:
                return True
            if count > 1:
                double_small_caves += 1
        if double_small_caves > 1:
            return True
        return False



if __name__ == '__main__':
    main()
