#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/7

Usage: cat advent07.input | python3 ./advent07.py

"""

DISKSPACE_TOTAL = 70000000
DISKSPACE_NEEDED = 30000000


import sys

def main ():

    input = sys.stdin.read().strip().split("\n")

    tree = build_tree(input)

    # Part 1:
    list = []
    tree.all_sizes(list)
    sum = 0
    for dir in list:
        if dir[1] <= 100000:
            sum += dir[1]
    print(sum)
    # 1648397


    # Part 2:
    used = tree.size()
    free_space = DISKSPACE_TOTAL - used
    to_free = DISKSPACE_NEEDED - free_space
    print("used            :", used)
    print("Total disk space:", DISKSPACE_TOTAL)
    print("Needed space    :", DISKSPACE_NEEDED)
    print("Free Space      :", free_space)
    print("Space to delete :", to_free)

    space_to_delete = DISKSPACE_TOTAL
    delete = None
    for dir in list:
        if dir[1] >= to_free:
            if dir[1] < space_to_delete:
                delete = dir
                space_to_delete =  dir[1]
    print("To delete:", delete)
    # To delete: ('/nzwbc/zcv/nbq', 1815525)



def build_tree (input):

    root = Node("/")
    pointer = root

    for line in input:
        if line == "$ cd /":
            pointer = root
        elif line.startswith("$ cd "):
            dir = line.split(" ")[2]
            pointer = pointer.cd(dir)
        elif line == "$ ls":
            pass
        else:
            (out1,out2) = line.split(" ")
            if out1 == "dir":
                # Dir ("dir <name>")
                pointer.add_dir(out2)
            else:
                # File ("<size> <name>")
                pointer.add_file(out2, int(out1))

    return root



class Node:
    name = None
    parent = None
    subdirs = None
    files = None

    def __init__ (self, name, parent = None):
        self.name = name
        self.parent = parent
        self.files = []
        self.subdirs = {}

    def add_file (self, name, size):
        self.files.append((name, size))

    def add_dir (self, name):
        new_node = Node(name, self)
        self.subdirs[name] = new_node

    def cd (self, name):
        if name == "..":
            return self.parent
        return self.subdirs[name]

    def level (self):
        if self.parent == None:
            return 0
        else:
            return self.parent.level() + 1

    def size (self):
        size = 0
        for file in self.files:
            size += file[1]
        for dir in self.subdirs.keys():
            size += self.subdirs[dir].size()
        return size

    def path (self):
        if self.parent == None:
            return ""
        return self.parent.path() + "/" + self.name 

    def all_sizes(self, list):
        list.append((self.path(), self.size()))
        for dir in self.subdirs.keys():
            self.subdirs[dir].all_sizes(list)

    def __str__ (self):
        spacer = "| " * self.level()
        output = spacer + "Dir: " + self.name + " (" + self.path() + ")"
        for file in self.files:
            output += "\n{}{} {}".format(spacer, *file)
        for dir in self.subdirs.keys():
            output += "\n{}{}".format(spacer, self.subdirs[dir])
        return output


if __name__ == '__main__':
    main()
