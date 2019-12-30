from AdventClasses import IntComputer
from AdventClasses import PaintRobot
import numpy as np
import matplotlib.pyplot as plt

# Load puzzle input 
f = open("advent_11_input.txt", "r") # TODO: not passed, out= 203 0
puzzle_input = f.read()

# Create new intcomputer
intcomputer = IntComputer(False)

# Parse puzzle input 
intcomputer.parse_instruction(puzzle_input)

# Execute programm
intcomputer.execute_programm()

print("Number of printed panels: ", len(intcomputer.robot.panels_painted))

# Visualize result:
plt.imshow(np.rot90(np.rot90(np.rot90(np.fliplr(intcomputer.robot.color_grid2D)))))
plt.show()