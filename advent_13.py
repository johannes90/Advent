"""
    Day 13: Care Package
    The Intcomputer is used as a brain inside an Arcade
    The intcomputer is provided with the current joystick position (-1:left 0:stay +1:right)
    The intcomputer outputs the players score or game tiles position and id (0:empty 1:wall 2:block 3:game paddle 4:ball)
    Part 1: How many blocks are on the screen (with no input)
    Part 2: What is score when the game is finished
"""

from IntComputer import IntComputer
from Arcade import Arcade
import numpy as np
import matplotlib.pyplot as plt

# Initialize the arcade
arcade = Arcade()

# Set game mode
arcade.set_game_mode("AI")

# Start the game
arcade.start_game()


# Part 1 : Block tiles on the screen when the game exits:
print(arcade.block_tile_counter)

# Part 2: Break all blocks, what is the score after last block is broken
# -> score is displayed in console

# TODO: Print the game display dynamically  

