# Day 11: (Composition = robot hat die andere klasse als variable)
# Interfaces haben namen und definieren Methoden, die vorhanden sein müssen 
# Interfaces brauch ich in python wahrscheinlich nicht weil es einfach so funktioniert
# Incomputer 
import queue
import numpy as np
import matplotlib.pyplot as plt
from IntComputer import IntComputer


class PaintRobot:

    def __init__(self, width, height):
        
        self.DIR             = {0: [0,1], 1: [-1,0], 2: [0,-1], 3: [1,0]}       # (x,y) directions (up, left, down, right)
        self.NUM_ROBOT_INSTR = 2

        self.grid_height  = height
        self.grid_width   = width
        self.color_grid2D = np.zeros((self.grid_height, self.grid_width))
        self.orientation  = 0                                                   # start with orientation 0 = upwards
        self.position     = int(self.grid_height/2.0), int(self.grid_width/2.0) # set robot into the middle of the map
        self.panels_painted = {self.position}                                   # set containing the starting point 
        
        # Part 2: set initial panel to white color
        self.color_grid2D[self.position] = 1
        self.instruction  = queue.Queue(self.NUM_ROBOT_INSTR)                   # queue for color and turn instruction
       
        # Use the oo concept of composition here
        self.brain        = IntComputer(False, 11) 
        self.brain.connect_with_next_intcomputer(self)
        f = open("advent_11_input.txt", "r") # TODO: not passed, out= 203 0
        self.robot_programm = f.read()


    # Start painting by providing the programm and then using the robots intcomputer to process the programm    
    def start_painting(self):
        
        # Feed the robot programm to its brain (intcomputer)
        self.brain.parse_instruction(self.robot_programm)
        
        # Give initial color of the robot to the intcomputer  
        self.brain.set_input(self.get_color())
        
        # Execute the intcomputer programm
        # Whenever the intcode computer has an output that is passed 
        # to the robot, the robot processes the output and gives back an input
        self.brain.execute_programm()


    # Process the input coming from the outputting device (intcomputer)
    def set_input(self, input):
        
        self.instruction.put(input)
        # 2 inputs = 1 instruction

        if self.instruction.full():
            self.paint_and_move()


    # Turn is either 0=left 1 = right
    def update_orientation(self, turn):
        if turn == 0:
            delta_orientation = -1
        elif turn == 1:
            delta_orientation = 1 
        self.orientation = (self.orientation + delta_orientation)%4


    # Paint the current panel with a given color
    def update_color(self, color):
        self.color_grid2D[self.position] = color


    # Paint current panel and go forward in current direction (we asume a full queue with 2 instructions)
    def paint_and_move(self):
        
        # get instructions for (new color, turn)
        color = self.instruction.get()
        turn  = self.instruction.get() 

        # Update color of panel and orientation of robot
        self.update_color(color)
        self.update_orientation(turn)

        # Go to next panel
        new_x         = self.position[0] + self.DIR[self.orientation][0]
        new_y         = self.position[1] + self.DIR[self.orientation][1]
        self.position = (new_x, new_y)

        # Pass current color to the robots brain (intcomputer) as an input 
        self.brain.set_input(self.get_color())

        # Add current (x,y) coordinate to the set of painted coordinates
        self.panels_painted.add(self.position) 


    # Getter function for the color of the current position
    def get_color(self):

        return self.color_grid2D[self.position]