#!/usr/bin/env python3

# Usage: cat advent08.input | ./advent08.py


"""
https://adventofcode.com/2021/day/8

"""

import sys
import time
from dataclasses import dataclass
from pprint import pformat
import itertools

def main():

    all_data = []
    for line in sys.stdin:
        (input, output) = line.strip().split(' | ')
        all_data.append(Data(input.split(" "),output.split(" ")))


    # Part 1:

    count = 0
    for data in all_data:
        for output in data.outputs:
            if segment_count_to_number(output):
                count += 1
    print("Count of 1/4/7/8:", count)
    # Count of 1/4/7/8: 456

    # Part 2.1: determine the numbers by puzzling

    start_time = time.time()

    total = 0
    for data in all_data:
        ssl = Seven_Segment_Learning()
        ssl.learn(data.inputs)
        for n in range(4):
            num = data.outputs[n]
            total += ssl.get_number(num) * (10**(3-n))

    end_time = time.time()

    print("Sum over all outputs: {} (time: {} ms)".format(total, 1000 * (end_time - start_time)))
    # Sum over all outputs: 1091609 (time: 6.201267242431641 ms)

    # Part 2.2: determine the numbers by brute force (test all permutations)

    start_time = time.time()

    total = 0
    for data in all_data:
        for permutation in list(itertools.permutations(list("abcdefg"))):
            ss = Seven_Segment_Brute_Force(permutation)
            all_matches = True
            for num in data.inputs:
                if ss.get_number(num) == None:
                    all_matches = False
                    break
            if all_matches:
                for n in range(4):
                    num = data.outputs[n]
                    total += ss.get_number(num) * (10**(3-n))
                break

    end_time = time.time()

    print("Sum over all outputs: {} (time: {} ms)".format(total, 1000 * (end_time - start_time)))
    # Sum over all outputs: 1091609 (time: 2214.4858837127686 ms)

# For Part 1:
def segment_count_to_number(segments):
    if len(segments) == 2 : return 1
    if len(segments) == 4 : return 4
    if len(segments) == 3 : return 7
    if len(segments) == 7 : return 8
    return None


# For Part 2.1:
class Seven_Segment_Learning:

    def __init__ (self):
        self.patterns = {}

    def learn (self, numbers):
        for c in sorted(numbers, key=len):
            c = ''.join(sorted(c))
            if len(c) == 2:   # -> 1
                self.patterns[c] = 1
                one = c
                filter_one = lambda x : not x in one
            if len(c) == 3:   # -> 7
                self.patterns[c] = 7
                #top = list(filter(filter_one, c))
            if len(c) == 4:   # -> 4
                self.patterns[c] = 4
                #mid_toleft = list(filter(filter_one, c))
                four = c
                filter_four = lambda x : not x in four
            if len(c) == 5:   # -> 2,3,5
                diff_four_one = list(filter(filter_one, four))
                filter_diff_four_one = lambda x : not x in diff_four_one
                if len(list(filter(filter_four, c))) == 3:
                    self.patterns[c] = 2
                elif len(list(filter(filter_diff_four_one, c))) == 4:
                    self.patterns[c] = 3
                else:
                    self.patterns[c] = 5
            if len(c) == 6:    # -> 0,6,9
                if len(list(filter(filter_four, c))) == 2:
                    self.patterns[c] = 9
                elif len(list(filter(filter_one, c))) == 4:
                    self.patterns[c] = 0
                else:
                    self.patterns[c] = 6
            if len(c) == 7:    # --> 8
                self.patterns[c] = 8

    def get_number(self,num):
        num = ''.join(sorted(num))
        return(self.patterns[num])


# For Part 2.2:
class Seven_Segment_Brute_Force:

    def __init__ (self, wiring):
        # Example for wiring: ('f', 'b', 'd', 'e', 'c', 'g', 'a')
        ordered = ('a','b','c','d','e','f','g')
        self.patterns = {}
        self.wiring = {}
        for n in range(7):
            self.wiring[wiring[n]] = ordered[n]

    #   + a +
    #   b   c
    #   + d +
    #   e   f
    #   + g +
    def get_number (self, input):
        x = self.wire(input)
        if x == ["a","b","c","e","f","g"]: return 0
        if x == ["c","f"]: return 1
        if x == ["a","c","d","e","g"]: return 2
        if x == ["a","c","d","f","g"]: return 3
        if x == ["b","c","d","f"]: return 4
        if x == ["a","b","d","f","g"]: return 5
        if x == ["a","b","d","e","f","g"]: return 6
        if x == ["a","c","f"]: return 7
        if x == ["a","b","c","d","e","f","g"]: return 8
        if x == ["a","b","c","d","f","g"]: return 9
        return None

    def wire (self,input):
        result = []
        for n in list(input):
            result.append(self.wiring[n])
        return sorted(result)


@dataclass
class Data:
    inputs: list
    outputs: list


if __name__ == '__main__':
    main()
