"""
    Day 13: Care Package

    - draw square tiles on a grid 
    - every every 3 output instructions specify:
       -> x = dist from left, 
       -> y = dist from top
       -> tile id

    - tile ID: 
        -> 0: empty tile 
        -> 1: wall tile  (indestructable barriers)
        -> 2: block tile (can be broken)
        -> 3: horizontal paddle tile (indestructable)
        -> 4: ball tile (moves diagonal, bounces off objects)
"""

from AdventClasses import IntComputer
from AdventClasses import PaintRobot
import numpy as np
import matplotlib.pyplot as plt

# Load puzzle input 
f = open("advent_13_input.txt", "r") # TODO: not passed, out= 203 0
puzzle_input = f.read()

# Create new intcomputer
intcomputer = IntComputer(False, 13)

# Parse puzzle input 
intcomputer.parse_instruction(puzzle_input)

# Execute Arcade
intcomputer.execute_arcade_programm()


print(intcomputer.arcade.counter)