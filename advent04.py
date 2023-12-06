#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/4

Usage:
cat advent04.input | ./advent04.py
"""

import sys
import re
from dataclasses import dataclass


def main ():
    cards = parse_input(sys.stdin.read().strip().split('\n'))

    print("Part 1:", part1(cards))
    # 24542
    print("Part 2:", part2(cards))
    # 8736438


def part1 (cards):
    total_sum = 0
    for card in cards:
        card_sum = 0
        for num in card.my_numbers:
            if num in card.winning_numbers:
                if card_sum > 0:
                    card_sum = card_sum * 2
                else:
                    card_sum = 1
        total_sum = total_sum + card_sum
    return total_sum


def part2 (cards):
    for idx in range(len(cards)):
        card_sum = 0
        for num in cards[idx].my_numbers:
            if num in cards[idx].winning_numbers:
                card_sum = card_sum + 1
        for add_instances_for_card in range(idx+1, idx+1+card_sum):
            cards[add_instances_for_card].instances = cards[add_instances_for_card].instances + cards[idx].instances
    total_sum = 0
    for card in cards:
        total_sum = total_sum + card.instances
    return total_sum


def parse_input (input):
    cards = []
    for line in input:
        winning_numbers = []
        my_numbers = []
        numbers = line.split(':')[1]
        left, right = numbers.split('|')
        winning_numbers = [int(x) for x in re.split('\s+', left.strip())]
        my_numbers = [int(x) for x in re.split('\s+', right.strip())]
        cards.append(Card(winning_numbers, my_numbers))
    return cards


@dataclass
class Card:
    winning_numbers: list[int]
    my_numbers: list[int]
    instances: int = 1


if __name__ == '__main__':
    main()