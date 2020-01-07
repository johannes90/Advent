# Day 11: (Composition = robot hat die andere klasse als variable)
# Interfaces haben namen und definieren Methoden, die vorhanden sein müssen 
# Interfaces brauch ich in python wahrscheinlich nicht weil es einfach so funktioniert
# Incomputer 
import queue
import numpy as np
import matplotlib.pyplot as plt
from IntComputer import IntComputer


class PaintRobot:

    def __init__(self):
        
        self.DIR             = {0: [0,1], 1: [-1,0], 2: [0,-1], 3: [1,0]}  # Directions on 2D plane: up,left,down,right   
        self.NUM_ROBOT_INSTR = 2
        self.orientation     = 0                                                   
        self.position        = (0,0)
        self.color           = 0
        self.panels          = {self.position: self.color}
        self.min_x           = 0
        self.min_y           = 0 
        self.max_x           = 0
        self.max_y           = 0
        self.instruction     = queue.Queue(self.NUM_ROBOT_INSTR)                   
        self.brain           = IntComputer(False, 11) # composition
        
        # Connect the brain with the robot in order to obtain the inputs
        self.brain.connect_with_next_intcomputer(self)
        f = open("advent_11_input.txt", "r")
        self.robot_programm = f.read()


    # Start painting by providing the programm and then using the robots intcomputer to process the programm    
    def start_painting(self):
        
        # Feed the robot programm to its brain (intcomputer)
        self.brain.parse_instruction(self.robot_programm)
        
        # Give initial color of the robot to the intcomputer  
        self.brain.set_input(self.get_color())
        
        # Execute the program using the braint (intcomputer)
        self.brain.execute_programm()


    # Process the input coming from the outputting device (intcomputer)
    def set_input(self, input):
        
        self.instruction.put(input)
        
        # 2 inputs = 1 instruction
        if self.instruction.full():
            self.paint_and_move()


    # Turn is either 0=left 1 = right
    def update_orientation(self, turn):

        self.orientation = (self.orientation + 2*turn-1)%4


    # Paint the current panel with a given color
    def update_color(self, color):

        self.panels[self.position] = color
        #self.color_grid2D[self.position] = color


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

        # Add current (x,y) coordinate to the set of painted coordinates
        #self.panels_painted.add(self.position) 
        if (self.position in self.panels) == False:
            self.panels[self.position] = 0 # every new panel is black
        
        # Pass current color to the robots brain (intcomputer) as an input 
        self.brain.set_input(self.get_color())

        # update min values
        self.update_min_max(new_x, new_y)


    # Getter function for the color of the current position
    def get_color(self):

        return self.panels[self.position]
        #return self.color_grid2D[self.position]

    # Update min and max x,y coordinates 
    def update_min_max(self, x, y):

        if x < self.min_x:
            self.min_x = x
        elif x > self.max_x:
            self.max_x = x

        if y < self.min_y:
            self.min_y = y
        elif y > self.max_y:
            self.max_y = y

    # Convert the dictionary into a map 
    def build_map(self):

        x_dim = (self.max_x - self.min_x) + 1
        y_dim = (self.max_y - self.min_y) + 1
        color_grid2D = np.zeros((x_dim, y_dim))

        # Loop through all seen panels and plot them on a grid
        for item in self.panels.items(): 

            # Shift data to have only positive values
            x = item[0][0] - self.min_x
            y = item[0][1] - self.min_y 
            position = (x,y)
            color    = item[1]
            color_grid2D[position] = color 
        
        return color_grid2D