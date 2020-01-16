from typing import List, Dict
from collections import defaultdict, namedtuple
#f = open("advent_06_testinput.txt", "r") 
f = open("advent_06_input.txt", "r") 

data = f.read()
f.close()
# Use a named tuple to store the parent, child pairs (orbits)
# As we do not need mutability we use named tuples instead of dicts
# TODO: do the same with classes instead of named tuples
Orbit = namedtuple("Orbit", ["parent", "child"])

def parse_orbits(data):
    Orbits = []
    for s in data.strip().split("\n"):
        parent, child = s.strip().split(")")

        #create new named tuple Orbit and put into list
        Orbits.append(Orbit(parent, child))
    return Orbits

# One directional tree maps from a child to its parent only 
def build_tree(Orbits):

    parents = {}

    # every child can only have one parent but one parent can have multiple children -> parent is value, child is key
    for orbit in Orbits:
        parents[orbit.child] = orbit.parent

    return parents 

def count_root_path(node, tree):

    num_parents = 0
    # go up the tree until we are at the root node 
    while node != "COM":
        num_parents += 1

        # return the parent of the current node
        node = tree[node]

    return num_parents

def count_all_root_path(tree):
    sum_all_root_path = 0 
    for node in tree.keys():
        sum_all_root_path += count_root_path(node, tree)
    
    return sum_all_root_path

def path_to_root(node, tree):
    
    # the path is a set of nodes
    path = set()

    while node != "COM":
        path.add(node)
        node = tree[node]
    
    return path

# Build parent,child tuples    
Orbits = parse_orbits(data)

# Build a onedirectional child->parent tree
tree = build_tree(Orbits)

# Part 1: count all parents for all children
solution_part1 = count_all_root_path(tree)
print("solution part 1: {}".format(solution_part1))

# Part 2: Shortest path between the parents of the nodes "YOU" and "SAN"
you_path = path_to_root(tree["YOU"], tree)
san_path = path_to_root(tree["SAN"], tree)
union        = you_path | san_path
intersection = you_path & san_path
solution_part2 = len(union) - len(intersection) 
print("solution part 2: {}".format(solution_part2))

