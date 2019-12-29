from AdventClasses import IntComputer

# Load puzzle input 
f = open("advent_11_input.txt", "r") # TODO: not passed, out= 203 0
puzzle_input = f.read()

# Create new intcomputer
intcomputer = IntComputer(False)


# How many panels does the robot print at least once ?

# 

"""
 - a robot (intcomputer) moves on a 2D grid, detect color of panel and print panel black or white
 - at start all panels are black
 - robot starts facing up

 Input at current panel:
 -  input=0 -> robot over black 
 -  input=1 -> robot over white 

Output at current
 -> 1: outputs the new color (0=black, 1=white)
 -> 2: Turn (0=left, 1=right)

 - move forward one panel

"""

# Parse puzzle input 
intcomputer.parse_instruction(puzzle_input)

# Provide input 
intcomputer.set_input()

# Run program 
intcomputer.execute_programm()