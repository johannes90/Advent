"""
    Module description
"""

import queue
import numpy as np
import matplotlib.pyplot as plt
from IntComputer import IntComputer
# Day 13: 
class Arcade:

    def __init__(self):
        
        self.tiles     = {}

        #NOTE: I assume there exist only one ball and one paddle  
        self.ball      = {"x": -1, "y": -1}  
        self.paddle    = {"x": -1, "y": -1}  

        self.instruction = queue.Queue(3)
        self.block_tile_counter  = 0 

        # Part 2:
        self.joystick = 0  # 0=neutral, -1=left, +1=right
        self.score    = 0  # represents current score
        self.game_ready = False
        self.game_changed = False # ball or paddle moved 
        self.ball_moved   = True # the ball moved 

    # Get Instructions (once the intcomputer generates an output)
    def get_instructions(self, new_instr):
        self.instruction.put(new_instr)

    # The instructions(intcomputer -> Arcade) update the tiles on the map or display the players score 
    def parse_instructions(self, instr):
        
        # Every 3 instructions an action is performed
        arg1 = instr.get()
        arg2 = instr.get()
        arg3 = instr.get()
        assert(instr.empty() == True)

        # Update the players score 
        if arg1 == -1  and arg2  == 0:
            self.score = arg3
            print("The players score is: ", self.score)

        # Or Update the tiles 
        else:
            tile_pos = (arg1, arg2) 
            tile_ID  = arg3
            self.tiles[tile_pos] = tile_ID

            # Update the ball and paddle copy
            if tile_ID == 4: # ball
                self.ball["x"] = arg1
                self.ball["y"] = arg2

                self.game_changed = True
                
            elif tile_ID == 3: # paddle   
                self.paddle["x"] = arg1
                self.paddle["y"] = arg2

                self.game_changed = True
            # Solution to part 1: count all block tiles
            elif tile_ID == 2: 
                self.block_tile_counter += 1
            
    # Function that controls the paddle tile
    def control_joystick(self):

        # We only apply a new input if the old one was processed 
        # -> That is taken care of because we only control after a new state 
        # of the game is observed 
        
        # We want to control the paddle directly below the ball
        pos_error = self.paddle["x"] - self.ball["x"]

        # Apply a simple proportional feedback controller
        self.joystick = np.sign(-pos_error)
        #print("ball: ", self.ball["x"], "paddle: ", self.paddle["x"], "-> joystick = ", self.joystick)

    def plot_arcade_status(self, multiple):

        if multiple == 0:     
            # Print the current status of the tiles
            tileID_marker = {1: "p", 2: "s", 3: "_", 4: "o"} #1=wall, 2=block, 3=paddle, 4=ball
            tileID_color  = {1: "black", 2: "black", 3: "red", 4: "red"}
            for key, value in self.tiles.items():   # {(x,y) pos: tile ID}
                if value != 0:
                    plt.scatter(*zip(*[key]), marker = tileID_marker[value], color = "black")
            
            plt.show(block=True)
            #plt.pause(1)
            #plt.close()

            self.game_changed = False 
        else:
            pass 