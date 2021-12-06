#!/usr/bin/env python3

# Usage: cat advent06.input | ./advent06.py


"""

Part1:

Although you know nothing about this specific species of lanternfish, you make
some guesses about their attributes. Surely, each lanternfish creates a new
lanternfish once every 7 days.

However, this process isn't necessarily synchronized between every lanternfish -
one lanternfish might have 2 days left until it creates another lanternfish,
while another might have 4. So, you can model each fish as a single number that
represents the number of days until it creates a new lanternfish.

Furthermore, you reason, a new lanternfish would surely need slightly longer
before it's capable of producing more lanternfish: two more days for its first
cycle.

So, suppose you have a lanternfish with an internal timer value of 3:

    After one day, its internal timer would become 2.
    After another day, its internal timer would become 1.
    After another day, its internal timer would become 0.
    After another day, its internal timer would reset to 6, and it would create
        a new lanternfish with an internal timer of 8.
    After another day, the first lanternfish would have an internal timer of 5,
        and the second lanternfish would have an internal timer of 7.

A lanternfish that creates a new fish resets its timer to 6, not 7 (because 0 is
included as a valid timer value). The new lanternfish starts with an internal
timer of 8 and does not start counting down until the next day.

Realizing what you're trying to do, the submarine automatically produces a list
of the ages of several hundred nearby lanternfish (your puzzle input). For
example, suppose you were given the following list:

3,4,3,1,2

This list means that the first fish has an internal timer of 3, the second fish
has an internal timer of 4, and so on until the fifth fish, which has an
internal timer of 2. Simulating these fish over several days would proceed as
follows:

Initial state: 3,4,3,1,2
After  1 day:  2,3,2,0,1
After  2 days: 1,2,1,6,0,8
After  3 days: 0,1,0,5,6,7,8
After  4 days: 6,0,6,4,5,6,7,8,8
After  5 days: 5,6,5,3,4,5,6,7,7,8
After  6 days: 4,5,4,2,3,4,5,6,6,7
After  7 days: 3,4,3,1,2,3,4,5,5,6
After  8 days: 2,3,2,0,1,2,3,4,4,5
After  9 days: 1,2,1,6,0,1,2,3,3,4,8
After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8

Each day, a 0 becomes a 6 and adds a new 8 to the end of the list, while each
other number decreases by 1 if it was present at the start of the day.

In this example, after 18 days, there are a total of 26 fish. After 80 days,
there would be a total of 5934.

Find a way to simulate lanternfish. How many lanternfish would there be after 80
days?


Part2:

How many lanternfish would there be after 256 days?

"""

import sys
import time

def main():
    start_time = time.time()
    random_list=list(map(int, sys.stdin.readline().strip().split(',')))

    time_to_live = 2560   # How many days we spend for the reproduction
    fishes = []
    result_cache = {}
    for next_spawn in random_list:
        ident_output = 0
        fish = Fish(time_to_live, result_cache, ident_output, next_spawn)
        fishes.append(fish)

    total = 0
    for fish in fishes:
        # print(fish)   # this prints recursive all siblings ... only usable for small tests
        total += fish.me_and_siblings

    end_time = time.time()

    print("Total: {} (cosumed time: {} ms)".format(total, 1000 * (end_time - start_time)))
    # For time_to_live = 80:
    # Total: 346063 (cosumed time: 2.863168716430664 ms)
    # For time_to_live = 256:
    # Total: 1572358335990 (cosumed time: 23.419857025146484 ms)
    # And for time_to_live = 2560  :-)
    # Total: 2325385468360990176669515856523251980773072991727171248428903734983932396487363680651827688875358058 (cosumed time: 2207.188844680786 ms)


# To determine the total number, we follow a recursive approach with depth-first
# search. For each node we cache the result with a cache key of "days to live"
# and "next spawning date". If we encounter a cache hit, we can skip the
# creation of the siblings fpr this node and use the cached result.

# An inital count of 300 fishes with ttl=256 needs about 20 milliseconds

class Fish:

    def __init__ (self, time_to_live, result_cache, ident_output, next_spawn=8):
        self.time_to_live = time_to_live
        self.result_cache = result_cache
        self.ident_output = ident_output
        self.next_spawn = next_spawn
        self.childs = []

        cache_key = "{}-{}".format(self.time_to_live, self.next_spawn)
        if cache_key in self.result_cache:
            self.me_and_siblings = self.result_cache[cache_key]
        else:
            while self.time_to_live > 0:
                self.aging()
            self.me_and_siblings = 1
            for child in self.childs:
                self.me_and_siblings += child.me_and_siblings
            self.result_cache[cache_key] = self.me_and_siblings


    def aging (self):
        self.next_spawn -= 1
        self.time_to_live -= 1
        if self.next_spawn < 0:
            self.next_spawn = 6
            self.childs.append(Fish(self.time_to_live, self.result_cache, self.ident_output+1))


    def __str__ (self):
        s = "  "*self.ident_output + "s={} ttl={} me_and_siblings={}".format(self.next_spawn, self.time_to_live, self.me_and_siblings)
        for child in self.childs:
            s += "\n" + str(child)
        return s



if __name__ == '__main__':
    main()
