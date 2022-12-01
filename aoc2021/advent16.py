#!/usr/bin/env python3

# Usage: cat advent16.input | ./advent16.py

"""
https://adventofcode.com/2021/day/16
"""

import sys


def main():
    # First line of input contains the complete data stream:
    hexa_input = sys.stdin.readline().strip()

    bit_string = ""
    for char in list(hexa_input):
        bit_string += bin(int(char, 16))[2:].zfill(4)
    print(bit_string)

    data = Data(bit_string)
    result = data.parse()
    #print(len(data.data), data.cursor)
    print(data.version_sum)
    # 821

    print("Result:", result)

class Data:

    Oparator_Types = {
        0 : "sum",
        1 : "product",
        2 : "min",
        3 : "max",
        4 : "literal",
        5 : "gt",
        6 : "lt",
        7 : "eq"
    }
    #Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
    #Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
    #Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
    #Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
    #Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    #Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    #Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.


    def __init__ (self, data):
        self.data = data
        self.cursor = 0
        self.version_sum = 0
        print("Total length:", len(self.data))

    def parse (self):
        type = self.header()
        if type == 'literal':
            num = self.literal()
            print("Literal:",num)
            return num
        else:
            # operator:
            arguments = self._parse_operator()
            num = self._operate(type, arguments)
            return num


    def header (self):
        version = int(self._read_bits(3), 2)
        self.version_sum += version
        type_id = int(self._read_bits(3), 2)
        type = self.Oparator_Types[type_id]
        return type


    def literal (self):
        number = ""
        while True:
            loop_flag = self._read_bits(1)
            number += self._read_bits(4)
            if loop_flag != "1": break
        return (int(number,2))


    def _parse_operator (self):
        length_type_id = self._read_bits(1)

        if length_type_id == "0":
            # One subpackage, lenght of subpackage is coded in the next 15 bits
            length_of_sub_packages = int(self._read_bits(15), 2)
            read_until = self.cursor + length_of_sub_packages
            results = []
            while self.cursor < read_until:
                results.append(self.parse())
        else:
            # More subpackages, number of subpackages is coded in the next 11 bits
            number_of_sub_packages = int(self._read_bits(11), 2)
            print("Read {} subpackages".format(number_of_sub_packages))
            results = []
            for n in range(number_of_sub_packages):
                results.append(self.parse())
        return results


    def _operate (self, operator, arguments):
        print("Operate:", operator, arguments)
        if operator == "sum":
            return sum(arguments)
        if operator == "product":
            result = 1
            for n in arguments:
                result *= n
            return result
        if operator == "min":
            return min(arguments)
        if operator == "max":
            return max(arguments)
        if operator == "gt":
            if arguments[0] > arguments[1]:
                return 1
            return 0
        if operator == "lt":
            if arguments[0] < arguments[1]:
                return 1
            return 0
        if operator == "eq":
            if arguments[0] == arguments[1]:
                return 1
            return 0

    def _read_bits (self, length, debug = None):
        data = self.data[self.cursor:self.cursor+length]
        if debug != None:
            print(debug, data)
        self.cursor += length
        return data


if __name__ == '__main__':
    main()
