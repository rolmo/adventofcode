#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/7

Usage:
cat advent07.input | ./advent07.py
"""

import sys
import re
import collections

TYPES = {
    'fife_of_a_kind': 7,
    'four_of_a_kind': 6,
    'full_house': 5,
    'three_of_a_kind': 4,
    'two_pairs': 3,
    'one_pair': 2,
    'high_card': 1,
}

def main ():
    input = sys.stdin.read().strip().split('\n')
    input_cards = parse_input(input)

    print("Part 1:", part1(input_cards))
    # 253910319
    print("Part 2:", part2(input_cards))
    # 254083736


def part1 (input_cards):
    Hand.cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'T', 'J', 'Q', 'K', 'A']
    hands = []
    for (cards, bid) in input_cards:
        hand = Hand(cards, bid)
        hands.append(hand)
    hands_rank = sum = 0
    for hand in sorted(hands):
        hands_rank += 1
        sum += hand.bid * hands_rank
    return sum


def part2 (input_cards):
    Hand.cards = ['J', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'T', 'Q', 'K', 'A']
    hands = []
    for (cards, bid) in input_cards:
        hand = Hand(cards, bid)
        hand.set_rank_with_joker()
        hands.append(hand)
    hands_rank = sum = 0
    for hand in sorted(hands):
        hands_rank += 1
        sum += hand.bid * hands_rank
    return sum


def parse_input (input, ignore_spaces=False):
    groups = []
    for line in input:
        cards, bid = line.split(' ')
        groups.append((cards, int(bid)))
    return groups



class Hand:

    def __init__ (self, cards, bid):
        self.cards = cards
        self.bid = bid
        self.set_type(self.cards)
        self.set_rank()


    def set_type (self, cards):
        col = collections.Counter(list(cards))
        quantity = []
        for card in col:
            quantity.append(col[card])
        if 5 in quantity:
            self.type = "fife_of_a_kind"
        elif 4 in quantity:
            self.type = "four_of_a_kind"
        elif 3 in quantity and 2 in quantity:
            self.type = "full_house"
        elif 3 in quantity:
            self.type = "three_of_a_kind"
        elif quantity.count(2) == 2:
            self.type = "two_pairs"
        elif 2 in quantity:
            self.type = "one_pair"
        else:
            self.type = "high_card"


    def set_rank_with_joker (self):
        highest_rank = 0
        for j in Hand.cards:
            if j != 'J':
                cards = self.cards
                cards = cards.replace('J', j)
                self.set_type(cards)
                self.set_rank()
                if self.rank > highest_rank:
                    highest_rank = self.rank
                else:
                    self.rank = highest_rank


    def set_rank (self):
        rank = TYPES[self.type]
        for card in self.cards:
            rank = rank * 100 + Hand.cards.index(card)
        self.rank = rank


    def __eq__ (self, other):
        return self.rank == other.rank


    def __lt__ (self, other):
        return self.rank < other.rank


if __name__ == '__main__':
    main()