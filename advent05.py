#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/5

Usage:
cat advent05.input | ./advent05.py

"""

import sys
from dataclasses import dataclass

RELATION = ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water", "water-to-light", "light-to-temperature", "temperature-to-humidity", "humidity-to-location"]

def main ():
    seeds, almanac = parse_input(sys.stdin.read().strip().split('\n'))

    print("Part 1:", part1(seeds, almanac))
    # 403695602

    print("Part 2:", part2(seeds, almanac))
    # ?????????


def part1 (seeds, almanac):
    maps = {}
    for map in RELATION:
        maps[map] = Mapper(almanac[map])

    minimal_location = None
    for seed in seeds:
        item = seed
        for map in RELATION:
            item = maps[map].map(item)
        if minimal_location is None or item < minimal_location:
            minimal_location = item
    return minimal_location


def part2 (seeds, almanac):
    mapper = Mapper2(seeds)
    for map in RELATION:
        mapper.merge(almanac[map])
    return mapper.get_smalles_possible_number()


def parse_input (input):
    almanac = {}
    for line in input:
        if line.find('seeds:') > -1:
            seeds = [int(x) for x in line.split(':')[1].strip().split(' ')]
        elif line.find('map:') > -1:
            map = line.split(' ')[0]
            almanac[map] = []
        elif len(line) == 0:
            pass
        else:
            almanac[map].append([int(x) for x in line.split(' ')])
    return seeds, almanac



@dataclass
class Map:
    dest: int
    source: int
    range: int

    def is_in_range (self, value):
        if value in range(self.source, self.source + self.range):
            return True


@dataclass
class Map2:
    start: int
    end: int
    offset: int

    def __init__ (self, start, end, offset):
        self.start = start
        self.end = end
        self.offset = offset
        if start > end:
            raise ValueError("Start must be smaller than end")
        

class Mapper:
    
    def __init__ (self, mappings):
        self.relations = []
        for mapping in mappings:
            self.relations.append(Map(mapping[0], mapping[1], mapping[2]))

    def map (self, source):
        for relation in self.relations:
            if relation.is_in_range(source):
                return relation.dest + source - relation.source
        return source



class Mapper2:
        
    def __init__ (self, seeds):
        self.blocks = []
        for i in range(int(len(seeds)/2)):
            self.blocks.append(Map2(seeds[i*2], seeds[i*2] + seeds[i*2+1] - 1, 0))

    def merge (self, mappings):
        print("========== Start new mapping ==========")
        print("Maps at start: {}".format(self.blocks))
        for mapping in mappings:
            start = mapping[1]
            end = mapping[1] + mapping[2]
            offset = mapping[0] - mapping[1]
            add_block = Map2(start, end, offset)
            print("---------- Add Block: {} ----------".format(add_block))
            for block in self.blocks[:]:  # we remove items - so we must work on a copy of the list ("[:]")!
                print("Block: {}".format(block))
                if block.start <= add_block.start and block.end >= add_block.end:
                    # add_block is completely in block
                    print("Add-Block is completely in Block")
                    if block.start < add_block.start:
                        self.blocks.append(Map2(block.start, add_block.start - 1, block.offset))
                    self.blocks.append(Map2(add_block.start, add_block.end, add_block.offset + block.offset))
                    if block.end > add_block.end:
                        self.blocks.append(Map2(add_block.end + 1, block.end, block.offset))
                    self.blocks.remove(block)
                elif block.start >= add_block.start and block.end <= add_block.end:
                    # add_block contains block
                    print("Add-Block contains Block")
                    block.offset = block.offset + add_block.offset
                elif block.start <= add_block.start and block.end >= add_block.start:
                    # add_block starts in block
                    print("Add-Block starts in Block")
                    self.blocks.append(Map2(block.start, add_block.start - 1, block.offset))
                    self.blocks.append(Map2(add_block.start, block.end, block.offset + add_block.offset))
                    self.blocks.remove(block)
                elif block.start <= add_block.end and block.end >= add_block.end:
                    # add_block ends in block
                    print("Add-Block ends in Block")
                    self.blocks.append(Map2(block.start, add_block.end, block.offset + add_block.offset))
                    self.blocks.append(Map2(add_block.end + 1, block.end, block.offset))
                    self.blocks.remove(block)
                else:
                    # add_block is not in block
                    print("Add-Block is not in block (ignoring)")
            print("Maps after mapping: {}".format(self.blocks))
        print("Maps at end: {} (len={})".format(self.blocks,len(self.blocks)))

    def get_smalles_possible_number (self):
        smallest = None
        for block in self.blocks:
            if smallest is None or (block.start + block.offset) < smallest:
                smallest = (block.start + block.offset)
        return smallest




if __name__ == '__main__':
    main()