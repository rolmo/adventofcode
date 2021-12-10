#!/usr/bin/env python3

# Usage: cat advent10.input | ./advent10.py


"""

https://adventofcode.com/2021/day/10

"""

import sys
from dataclasses import dataclass
import statistics

Opener_sign =  {"<":True,"(":True,"{":True,"[":True}
Closer_sign =  {">":True,")":True,"}":True,"]":True}
Close_sign_for = {"<":">","(":")","{":"}","[":"]"}
Points_for_unexpected_closer =  {">":25137,")":3,"}":1197,"]":57}
Points_for_autocomplete =  {">":4,")":1,"}":3,"]":2}


def main():

    error_points = 0
    autocomplete_scores = []
    for line in sys.stdin:
        code = line.strip()
        try:
            check_code(code)
        except UnexpectedCloser as e:
            error_points += Points_for_unexpected_closer[e.char]
        except CloserWithoutOpener as e:
            error_points += Points_for_unexpected_closer[e.char]
        except UnclosedOpener as e:
            score = 0
            for char in e.chars[::-1]:
                score *= 5
                score += Points_for_autocomplete[Close_sign_for[char]]
            autocomplete_scores.append(score)
        #except UnclosedOpener:

    print("Corrupted Code Points:", error_points)       # 311949
    print("Autocomplete Points:", statistics.median(autocomplete_scores))  # 3042730309


def check_code(code):
    stack = []
    for c in code:
        # print(stack)
        if c in Opener_sign:
            stack.append(c)
        elif c in Closer_sign:
            if len(stack) == 0:
                raise CloserWithoutOpener(c)
            opener = stack.pop()
            if c != Close_sign_for[opener]:
                raise UnexpectedCloser(c)
        else:
            raise NoCloserOrOpener
    if len(stack):
        raise UnclosedOpener(stack)




class Error(Exception):
    """Base class for other exceptions"""
    pass

class UnexpectedCloser(Error):
    """Raised when we get an closer sign that matches not the opener"""

    def __init__(self, char, message="Unexpected closer"):
        self.char = char
        self.message = message
        super().__init__(self.message)

class CloserWithoutOpener(Error):
    """Raised when we get an closer but there is no open opener"""

    def __init__(self, char, message="Closer without opener"):
        self.char = char
        self.message = message
        super().__init__(self.message)

class UnclosedOpener(Error):
    """We ar at the end of the strting, but there are unclosed openers"""

    def __init__(self, chars, message="Closer without opener"):
        self.chars = chars
        self.message = message
        super().__init__(self.message)



if __name__ == '__main__':
    main()
