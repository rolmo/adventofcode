#!/usr/bin/env python3

# Usage: cat advent22.input | ./advent22.py

"""
https://adventofcode.com/2021/day/12
"""

import sys


def main():

    cuboids = []
    edges_x1 = set()
    edges_x1 = set()
    edges_y1 = set()
    edges_y1 = set()
    edges_z1 = set()
    edges_z1 = set()
    for line in sys.stdin:
        cuboid = Cuboid()
        cuboid.parse_input(line.strip())

        # For part1: only look at cubes inside -50 ... +50
        if min(cuboid.x1,cuboid.x2,cuboid.y1,cuboid.y2,cuboid.z1,cuboid.z2) < -50:
            continue
        if max(cuboid.x1,cuboid.x2,cuboid.y1,cuboid.y2,cuboid.z1,cuboid.z2) > 50:
            continue

        edges_x1.add(cuboid.x1)
        edges_x2.add(cuboid.x2)
        edges_y1.add(cuboid.y1)
        edges_y2.add(cuboid.y2)
        edges_z1.add(cuboid.z1)
        edges_z2.add(cuboid.z2)
        cuboids.append((cuboid))


    print("Edges:", len(edges_x1), len(edges_x2), len(edges_y1), len(edges_y2), len(edges_z1), len(edges_z2))
    print("Cuboids:", len(cuboids))

    # Split all cubes at all x-edges
    handy_cuboids = []
    for cuboid in cuboids:
        if cuboid.state == "off":
            handy_cuboids.append(cuboid)
        else:
            handy_cuboids += cuboid.split_x(edges_x1,edges_x2)
    cuboids = handy_cuboids

    print("Split x", len(cuboids))

    handy_cuboids = []
    for cuboid in cuboids:
        if cuboid.state == "off":
            handy_cuboids.append(cuboid)
        else:
            handy_cuboids += cuboid.split_y(edges_y)
    cuboids = handy_cuboids

    print("Split y", len(cuboids))

    handy_cuboids = []
    for cuboid in cuboids:
        if cuboid.state == "off":
            for c in handy_cuboids:
                if cuboid.contains(c):
                    c.state = "ignore"
        else:
            res = cuboid.split_z(edges_z)
            for cuboid in res:
                append = True
                for c in handy_cuboids:
                    if c.state == "on" and c == cuboid:
                        print("Double",cuboid)
                        append = False
                if append:
                    handy_cuboids.append(cuboid)
    cuboids = handy_cuboids

    print("Split z (and merge/delete)", len(cuboids))



    # for n in range(len(cuboids)):
    #     this = cuboids[n]
    #     if this.state == "on":
    #         for o in range(n, len(cuboids)):
    #             other = cuboids[o]
    #             if other.state == "off":
    #                 if this == other:
    #                     this.state = "ignore"

    cubes = 0
    for cuboid in cuboids:
        if cuboid.state == "on":
            print(cuboid, cuboid.num_cubes())
            cubes += cuboid.num_cubes()
    print("Cubes in all Steps: {:.3g} {}".format(cubes, cubes))

    # Results (for cuboids in range -50...50)




    # Cuboids: 420
    # Split x 39267
    # Split y 3747009
    # Split z 356743268
    # Cubes in all Steps: 3.26e+15


    #print(len(reactor))
    # 580012

    # Num of cubes in all steps:
    # 3821083646676509


class Cuboid:

    def __init__ (self, state=None, x1=0,x2=0,y1=0,y2=0,z1=0,z2=0):
        self.state = state
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2


    def parse_input (self, input):
        (self.state, coordinates) = input.split(" ")
        xyz = coordinates.split(",")
        for n in xyz:
            (direction,range) = n.split("=")
            (start,end) = range.split("..")
            if direction == "x":
                self.x1 = int(start)
                self.x2 = int(end)
            if direction == "y":
                self.y1 = int(start)
                self.y2 = int(end)
            if direction == "z":
                self.z1 = int(start)
                self.z2 = int(end)

    def num_cubes (self):
        return (1+self.x2-self.x1) * (1+self.y2-self.y1) * (1+self.z2-self.z1)

    # def __iter__ (self):
    #     self.cursor_x = self.x1
    #     self.cursor_y = self.y1
    #     self.cursor_z = self.z1
    #     self.stopIter = False
    #     return self
    #
    # def __next__ (self):
    #     if self.stopIter:
    #         raise StopIteration
    #     cube = (self.cursor_x,self.cursor_y,self.cursor_z)
    #     if self.cursor_z < self.z2:
    #         self.cursor_z += 1
    #     else:
    #         self.cursor_z = self.z1
    #         if self.cursor_y < self.y2:
    #             self.cursor_y += 1
    #         else:
    #             self.cursor_y = self.y1
    #             if self.cursor_x < self.x2:
    #                 self.cursor_x += 1
    #             else:
    #                 self.stopIter = True
    #     return cube


    def __eq__ (self, other):
        if self.x1 == other.x1 and self.x2 == other.x2 \
            and self.y1 == other.y1 and self.y2 == other.y2 \
            and self.z1 == other.z1 and self.z2 == other.z2:
            return True
        return False

    def contains (self, other):
        if self.x1 <= other.x1 and self.x2 >= other.x2 \
            and self.y1 <= other.y1 and self.y2 >= other.y2 \
            and self.z1 <= other.z1 and self.z2 >= other.z2:
            return True
        return False


    # def intersect (self, other):
    #     cuboids = [Cuboid(self.state,self.x1,self.x2,self.y1,self.y2,self.z1,self.z2)]
    #
    #     split_x = []
    #     if self.x1 < other.x1 < self.x2:
    #         split_x.append(other.x1)
    #     if self.x1 < other.x2 < self.x2:
    #         split_x.append(other.x2)
    #     if len(split_x) > 0:
    #         new_cuboids = []
    #         for cuboid in cuboids:
    #             new_cuboids += cuboid._split_x(split_x)
    #         cuboids = new_cuboids
    #
    #     split_y = []
    #     if self.y1 < other.y1 < self.y2:
    #         split_y.append(other.y1)
    #     if self.y1 < other.y2 < self.y2:
    #         split_y.append(other.y2)
    #     if len(split_y) > 0:
    #         new_cuboids = []
    #         for cuboid in cuboids:
    #             new_cuboids += cuboid._split_y(split_y)
    #         cuboids = new_cuboids
    #
    #     split_z = []
    #     if self.z1 < other.z1 < self.z2:
    #         split_z.append(other.z1)
    #     if self.z1 < other.z2 < self.z2:
    #         split_z.append(other.z2)
    #     if len(split_z) > 0:
    #         new_cuboids = []
    #         for cuboid in cuboids:
    #             new_cuboids += cuboid._split_z(split_z)
    #         cuboids = new_cuboids
    #
    #     return cuboids


    def split_x (self, edges1, edges2):
        rest = self.copy()
        cuboids = []
        for edge in sorted(edges):
            if self.x1 < edge < self.x2:
                new_cube = rest.copy()
                new_cube.x2 = edge
                rest.x1 = edge
                cuboids.append(new_cube)
        cuboids.append(rest)
        return cuboids

    def split_y (self, edges):
        rest = self.copy()
        cuboids = []
        for edge in sorted(edges):
            if self.y1 < edge < self.y2:
                new_cube = rest.copy()
                new_cube.y2 = edge
                rest.y1 = edge
                cuboids.append(new_cube)
        cuboids.append(rest)
        return cuboids

    def split_z (self, edges):
        rest = self.copy()
        cuboids = []
        for edge in sorted(edges):
            if self.z1 < edge < self.z2:
                new_cube = rest.copy()
                new_cube.z2 = edge
                rest.z1 = edge
                cuboids.append(new_cube)
        cuboids.append(rest)
        return cuboids


    def copy (self):
        return Cuboid(self.state,self.x1,self.x2,self.y1,self.y2,self.z1,self.z2)

    # def _split_x (self, x):
    #     if len(x) == 1:
    #         cuboid1 = Cuboid(self.state,self.x1,x[0],self.y1,self.y2,self.z1,self.z2)
    #         cuboid2 = Cuboid(self.state,x[0],self.x2,self.y1,self.y2,self.z1,self.z2)
    #         return [cuboid1, cuboid2]
    #     if len(x) == 2:
    #         cuboid1 = Cuboid(self.state,self.x1,x[0],self.y1,self.y2,self.z1,self.z2)
    #         cuboid2 = Cuboid(self.state,x[0],x[1],self.y1,self.y2,self.z1,self.z2)
    #         cuboid3 = Cuboid(self.state,x[1],self.x2,self.y1,self.y2,self.z1,self.z2)
    #         return [cuboid1, cuboid2, cuboid3]
    #
    # def _split_y (self, y):
    #     if len(y) == 1:
    #         cuboid1 = Cuboid(self.state,self.x1,self.x2,self.y1,y[0],self.z1,self.z2)
    #         cuboid2 = Cuboid(self.state,self.x1,self.x2,y[0],self.y2,self.z1,self.z2)
    #         return [cuboid1, cuboid2]
    #     if len(y) == 2:
    #         cuboid1 = Cuboid(self.state,self.x1,self.x2,self.y1,y[0],self.z1,self.z2)
    #         cuboid2 = Cuboid(self.state,self.x1,self.x2,y[0],y[1],self.z1,self.z2)
    #         cuboid3 = Cuboid(self.state,self.x1,self.x2,y[1],self.y2,self.z1,self.z2)
    #         return [cuboid1, cuboid2, cuboid3]
    #
    # def _split_z (self, z):
    #     if len(z) == 1:
    #         cuboid1 = Cuboid(self.state,self.x1,self.x2,self.y1,self.y2,self.z1,z[0])
    #         cuboid2 = Cuboid(self.state,self.x1,self.x2,self.y1,self.y2,z[0],self.z2)
    #         return [cuboid1, cuboid2]
    #     if len(z) == 2:
    #         cuboid1 = Cuboid(self.state,self.x1,self.x2,self.y1,self.y2,self.z1,z[0])
    #         cuboid2 = Cuboid(self.state,self.x1,self.x2,self.y1,self.y2,z[0],z[1])
    #         cuboid3 = Cuboid(self.state,self.x1,self.x2,self.y1,self.y2,z[1],self.z2)
    #         return [cuboid1, cuboid2, cuboid3]


    def __str__ (self):
        return "(s={}, x={}..{} y={}..{} z={}..{})".format(self.state, self.x1, self.x2, self.y1, self.y2, self.z1, self.z2)

    __repr__ = __str__


if __name__ == '__main__':
    main()
