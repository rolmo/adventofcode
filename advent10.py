#!/usr/bin/env python3

# Usage: cat advent10.input | ./advent10.py


"""

https://adventofcode.com/2021/day/10

"""

import sys
from dataclasses import dataclass
import statistics


# Set some constants:
Close_sign_for = {"<":">","(":")","{":"}","[":"]"}
# All Keys:
Opener_sign = [*Close_sign_for]
# All values:
Closer_sign = list(Close_sign_for.values())

Points_for_unexpected_closer =  {">":25137,")":3,"}":1197,"]":57}
Points_for_autocomplete =  {">":4,")":1,"}":3,"]":2}



def main():

    error_points = 0
    autocomplete_scores = []
    for line in sys.stdin:
        code = line.strip()
        try:
            check_code(code)
        except UnmatchedCloser as e:
            print(e, e.char)
            error_points += Points_for_unexpected_closer[e.char]
        except CloserWithoutOpener as e:
            print(e, e.char)
            error_points += Points_for_unexpected_closer[e.char]
        except UnclosedOpener as e:
            #print(e, e.chars)
            score = 0
            for char in e.chars[::-1]:
                score *= 5
                score += Points_for_autocomplete[Close_sign_for[char]]
            autocomplete_scores.append(score)

    print("Corrupted Code Points:", error_points)       # 311949
    print("Autocomplete Points:", statistics.median(autocomplete_scores))  # 3042730309


def check_code(code):
    stack = []
    for c in code:
        if c in Opener_sign:
            stack.append(c)
        elif c in Closer_sign:
            if len(stack) == 0:
                raise CloserWithoutOpener(c)
            opener = stack.pop()
            if c != Close_sign_for[opener]:
                raise UnmatchedCloser(c)
        else:
            raise NoCloserOrOpener
    if len(stack):
        raise UnclosedOpener(stack)




class UnmatchedCloser(Exception):
    """Raised when we find a closer that matches not the corresponding opener"""

    def __init__(self, char, message="Unmatched closer"):
        self.char = char
        self.message = message
        super().__init__(self.message)

class CloserWithoutOpener(Exception):
    """Raised when we find a closer but there is no open opener"""

    def __init__(self, char, message="Closer without opener"):
        self.char = char
        self.message = message
        super().__init__(self.message)

class UnclosedOpener(Exception):
    """We are at the end of the string, but there are unclosed openers"""

    def __init__(self, chars, message="Opener without closer"):
        self.chars = chars
        self.message = message
        super().__init__(self.message)



if __name__ == '__main__':
    main()
