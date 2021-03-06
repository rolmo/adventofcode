#!/usr/bin/env python3

# Usage: cat advent10.input | ./advent10.py


"""

https://adventofcode.com/2021/day/10

Part 1:

Some of the lines aren't corrupted, just incomplete; you can ignore these lines for now.
Stop at the first incorrect closing character on each corrupted line.
Compute the total sum of error points:
    ): 3 points.
    ]: 57 points.
    }: 1197 points.
    >: 25137 points.

Part 2:

Now, discard the corrupted lines. The remaining lines are incomplete.
Complete this line and calculete the result with:
    ): 1 point.
    ]: 2 points.
    }: 3 points.
    >: 4 points.
For each missing bracket calculate a score with:
 - Start with a total score of 0.
 - Multiply the total score by 5, then add the value of next missing bracket
 - The final result is the median over all single scores (There will always be an odd number of scores).

"""

import sys
from dataclasses import dataclass
import statistics


# Set some constants:
Close_sign_for = {"<":">","(":")","{":"}","[":"]"}
# All keys:
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
        except UnmatchedCloserError as e:
            #print(e, e.char)
            error_points += Points_for_unexpected_closer[e.char]
        except UnclosedOpenerError as e:
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
                raise UnmatchedCloserError(c,"Closer without opener")
            opener = stack.pop()
            if c != Close_sign_for[opener]:
                raise UnmatchedCloserError(c)
        else:
            raise NoCloserOrOpenerError
    if len(stack):
        raise UnclosedOpenerError(stack)




class UnmatchedCloserError(Exception):
    """Raised when we find a unmatched closer"""

    def __init__(self, char, message="Unmatched closer"):
        self.char = char
        self.message = message
        super().__init__(self.message)

class UnclosedOpenerError(Exception):
    """We are at the end of the string, but there are unclosed openers"""

    def __init__(self, chars, message="Opener without closer"):
        self.chars = chars
        self.message = message
        super().__init__(self.message)



if __name__ == '__main__':
    main()
