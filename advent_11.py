from AdventClasses import IntComputer
from AdventClasses import PaintRobot

# Load puzzle input 
f = open("advent_11_input.txt", "r") # TODO: not passed, out= 203 0
puzzle_input = f.read()

# Create new intcomputer
intcomputer = IntComputer(False)

"""
 Start: direction: Up, panels all black

 Input at current panel:
 -> color of current panel  (black
  = 0, white = 1) 

Output at current
 -> 1: outputs the new color (0=black, 1=white)
 -> 2: Turn (0=left, 1=right)
"""

# Parse puzzle input 
intcomputer.parse_instruction(puzzle_input)

# This is done in the initialization of color_out queue
# Set first input/color the robot is on  
#intcomputer.set_input(0)

# Execute programm
intcomputer.execute_programm()

print("Number of printed panels: ", len(intcomputer.robot.panels_painted))
