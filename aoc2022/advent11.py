#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/11

Usage: cat advent11.input | python3 ./advent11.py

"""
import sys

DIFF_BY_3 = True
NO_DIFF_BY_3 = False

def main ():

    input = sys.stdin.read().strip().split("\n")
    part1(input)
    part2(input)


def part1(input):
    monkeys = parse_input(input, DIFF_BY_3)

    for round in range(20):
        for monkey in monkeys:
            for (item, to_monkey) in monkey:
                monkeys[to_monkey].append_item(item)

    (first,second) = sorted([monkey.num_of_inspections for monkey in monkeys])[-2:]
    print(first * second)
    # 99840


def part2(input):
    monkeys = parse_input(input, NO_DIFF_BY_3)

    # To avoid to big numbers, we divide the items by the common multiple 
    # of the divisors of all monkeys:
    common_multiple = 1
    for monkey in monkeys:
        common_multiple *= monkey.test_divisible_by
    for monkey in monkeys:
        monkey.common_multipler = common_multiple

    for round in range(10000):
        for monkey in monkeys:
            for (item, to_monkey) in monkey:
                monkeys[to_monkey].append_item(item)

    (first,second) = sorted([monkey.num_of_inspections for monkey in monkeys])[-2:]
    print(first * second)
    # 20683044837


def parse_input(input, diff_by_3):
    monkeys = []
    for line in input:
        if ":" in line:
            (left, right) = line.split(":")
            if left.startswith("Monkey "):
                monkey =  Monkey(left, diff_by_3)
                monkeys.append(monkey)
            elif left == "  Starting items":
                for item in right.split(","):
                    monkey.append_item(int(item))
            elif left == "  Operation":
                monkey.operator = right.strip()
            elif left == "  Test":
                monkey.test_divisible_by = int(right.split(" ")[3])
            elif left == "    If true":
                monkey.pass_true = int(right.split(" ")[4])
            elif left == "    If false":
                monkey.pass_false = int(right.split(" ")[4])
            else:
                raise NotImplementedError
    return monkeys


class Monkey:

    def __init__ (self, name:str, diff_by_3:bool) -> None:
        self._name = name
        self._items = []
        self._num_of_inspections = 0
        self._diff_by_3 = diff_by_3
        self._common_multipler = None

    def append_item (self, item:int) -> None:
        self._items.append(item)

    @property
    def name (self):
        return self._name

    @property
    def num_of_inspections (self):
        return self._num_of_inspections

    def set_operator (self, operator:str) -> None:
        if operator.startswith("new ="):
            self._operator = operator.split("=")[1]
        else:
            raise AttributeError

    operator = property(None, set_operator)

    @property
    def test_divisible_by (self):
        return self._test_divisible_by

    @test_divisible_by.setter
    def test_divisible_by (self, number: int) -> None:
        self._test_divisible_by = number


    def set_pass_true (self, number: int) -> None:
        self._pass_true = number
    def set_pass_false (self, number: int) -> None:
        self._pass_false = number
    def set_common_multipler (self, common_multipler: int) -> None:
        self._common_multipler = common_multipler

    pass_true = property(None, set_pass_true)
    pass_false  = property(None, set_pass_false)
    common_multipler = property(None, set_common_multipler)


    def __iter__(self):
        return self

    def __next__ (self):
        if len(self._items) == 0:
            raise StopIteration

        self._num_of_inspections += 1

        item = self._items.pop(0)
        old = item  # we need "old" in the eval expression ...
        item = eval(self._operator)
        if self._diff_by_3:
            item //= 3
        if self._common_multipler:
             item %= self._common_multipler
        if item % self._test_divisible_by:
            throw_to = self._pass_false
        else:
            throw_to = self._pass_true
        return (item, throw_to)


    def __str__(self):
        txt = self._name
        txt += "\n  items      :" + str(self._items)
        txt += "\n  operator   :" + self._operator
        txt += "\n  div by     :" + str(self._test_divisible_by)
        txt += "\n  pass true  :" + str(self._pass_true)
        txt += "\n  pass false :" + str(self._pass_false)
        return txt

if __name__ == '__main__':
    main()
