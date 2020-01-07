from IntComputer import IntComputer
from PaintRobot import PaintRobot
import numpy as np
import matplotlib.pyplot as plt

# Create the hull painting robot
robot = PaintRobot()

# Part 1: The robot seems to be on a BLACK panel
black = 0
robot.update_color(black)
robot.start_painting()

# Print the solution for part 1
#print("Painted panels ", len(robot.panels_painted))
print("Painted panels: ", len(robot.panels))

# Part 2: The robot seems to be on a WHITE panel
# Create new hull painting robot
robot = PaintRobot()
white = 1
robot.update_color(white)
robot.start_painting()

# Plot the solution for part 2
plt.imshow(np.fliplr(robot.build_map()))
plt.show()
