"""
    Day 13: Care Package

    - draw square tiles on a grid 
    - every every 3 output instructions specify:
       -> x = dist from left, 
       -> y = dist from top
       -> tile id

       or if 
       arg1 = -1, arg2 = 0 
       -> arg3 = current score 

    - tile ID: 
        -> 0: empty tile 
        -> 1: wall tile  (indestructable barriers)
        -> 2: block tile (can be broken)
        -> 3: horizontal paddle tile (indestructable)
        -> 4: ball tile (moves diagonal, bounces off objects)

    - set memory[0] = 2 to play for free
    
    - joystick 
        -> -1: Left 
        -> 0:  neutral
        -> 1:  right 

    Part2: 
    I just have to print/plot the arcade game 
    and provide the correct joystick inputs

    The rest is handled by the intcode programm
    
    Output Int -> Arcade: 
    -sobald ein output da ist, wird er
    in der arcade instr queue gespeichter,

    - sobald die queue voll ist, werden die instr geparsed
    -> ein neuer Bildschirm entsteht

    Sobald ein Ball und ein paddle exisieren und 
    direkt nachdem ein neuer Bildschirm entsteht, 
    soll das paddle anhand geregelt werden 
    -> input an den Intcomputer 

    

                          

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

# Set memory at adress 0 to 2 in order to play for free 
intcomputer.set_memory(0, 2)

# Execute Arcade
intcomputer.execute_arcade_programm()

# Part 1 : Block tiles on the screen when the game exits:
print(intcomputer.arcade.block_tile_counter)

# Part 2: Break all blocks, what is the score after last block is broken

# Print the game 

