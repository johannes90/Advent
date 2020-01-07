"""
    Module with classes and functionality for the advent of code asignments
"""
import queue
import numpy as np
import matplotlib.pyplot as plt


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

# Day 11: (Composition = robot hat die andere klasse als variable)
# Interfaces haben namen und definieren Methoden, die vorhanden sein müssen 
# Interfaces brauch ich in python wahrscheinlich nicht weil es einfach so funktioniert
# Incomputer 
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

        self.instruction  = queue.Queue(self.NUM_ROBOT_INSTR)                   # queue for color and turn instruction
        self.color_out    = queue.Queue(1)                                      # queue for the color on the current panel
        self.color_out.put(1)                                                   # startcolor of robot
        
        # Use the oo concept of composition here
        self.brain        = IntComputer() 
        self.brain.connect_with_next_intcomputer(self)


    def execute_programm(self):
        print("")
    # order: (color, turn)
    def get_instructions(self, new_instr):
        self.instruction.put(new_instr)

    # Turn is either 0=left 1 = right
    def update_orientation(self, turn):
        if turn == 0:
            delta_orientation = -1
        elif turn == 1:
            delta_orientation = 1 
        self.orientation = (self.orientation + delta_orientation)%4

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

        # Increment the panel counter and update current color
        self.color_out.put(self.color_grid2D[self.position]) 

        # Add current (x,y) coordinate to the set of painted coordinates
        self.panels_painted.add(self.position)


# Day 2,5,7,9,11:
class IntComputer: 

    INSTRUCTION_LEN      = 2
    NUM_ADDRESSING_MODES = 3

    def __init__(self, debug_mode = False, day = 13):
        self.day              = day
        self.memory           = []                       # RAM of Int Computer
        self.program_pointer  = None                     # points on the address of the current instruction of the programm
        self.instruction_dict = {1:  self.add,           # dictionary for instruction functions
                                 2:  self.multiply, 
                                 3:  self.inqueue,
                                 4:  self.outqueue,
                                 5:  self.jump_if_True,
                                 6:  self.jump_if_False,
                                 7:  self.less_than,
                                 8:  self.equals,
                                 9:  self.adj_rel_base,
                                 99: self.halt}
        self.input             = queue.Queue()  
        self.output            = 0             
        self.next_intcomputer  = None                   # Output for the next intcomputer
        self.relative_base     = 0
        self.memory_size       = 0
        self.addressing_modes  = [0, 0, 0]       
        self.debug_mode        = debug_mode          

        # day 11:
        self.robot             = PaintRobot(100, 100)
        self.out_instr         = queue.Queue(1)  

        # day 13:
        self.arcade            = Arcade()


    # The string of instructions is parsed as a list of ints into the RAM of the Int Computer
    def parse_instruction(self, instruction_string):
        self.memory = list(map(lambda x: int(x), instruction_string.split(",")))
        
        # Reset the input if a new programm is started
        self.input  = queue.Queue()

        some_large_number = 1000000
        self.memory = self.memory + [0]*some_large_number # join the memory list with additional memory
        

    def increment_program_pointer(self):
        self.program_pointer += 1

    """ Instruction functions of the int computer """
    # Instruction 1: Addition
    def add(self):

        # We asume the program pointer is on the first argument
        arg1 = self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer) 
        self.increment_program_pointer()

        arg2 = self.get_parameter_from_mode(self.addressing_modes[-2], self.program_pointer) 
        self.increment_program_pointer()

        solution = arg1 + arg2
        # Use setter function to check if addressing mode of target is 0 or 2 (1 does not make sense )
        self.set_parameter_from_mode(self.addressing_modes[-3], solution, self.program_pointer)

    # Instruction 2: Multiplication
    def multiply(self):
    
        # We asume the program pointer is on the first argument
        arg1 = self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer) 
        self.increment_program_pointer()

        arg2 = self.get_parameter_from_mode(self.addressing_modes[-2], self.program_pointer) 
        self.increment_program_pointer()

        solution = arg1*arg2
        self.set_parameter_from_mode(self.addressing_modes[-3], solution, self.program_pointer)
    
    # Instruction 3: 
    def inqueue(self):
        assert(not self.input.empty()) # TODO: rausnehmen nach debuggen
        solution = self.input.get()
        self.set_parameter_from_mode(self.addressing_modes[-1], solution, self.program_pointer)

    # Instruction 4: 
    def outqueue(self):

        # Output value (print and store in a list)
        outp = self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer)
        self.increment_program_pointer()

        self.output = outp
        #print(outp)
        
        # day 11:
        if self.day == 11 or self.day == 13:
            self.out_instr.put(outp)
        
        if self.next_intcomputer != None:
            self.next_intcomputer.set_input(outp)
                
    # Instruction 5: 
    def jump_if_True(self):

        arg1 = self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer) 
        self.increment_program_pointer()

        arg2 = self.get_parameter_from_mode(self.addressing_modes[-2], self.program_pointer) 
        self.increment_program_pointer()

        if arg1 != 0:
            self.program_pointer = arg2
    
    # Instruction 6:
    def jump_if_False(self):

        arg1 = self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer) 
        self.increment_program_pointer()

        arg2 = self.get_parameter_from_mode(self.addressing_modes[-2], self.program_pointer) 
        self.increment_program_pointer()

        if arg1 == 0:
            self.program_pointer = arg2

    # Instruction 7:
    def less_than(self):

        arg1 = self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer) 
        self.increment_program_pointer()

        arg2 = self.get_parameter_from_mode(self.addressing_modes[-2], self.program_pointer) 
        self.increment_program_pointer()

        solution = 1 if arg1 < arg2 else 0
        self.set_parameter_from_mode(self.addressing_modes[-3], solution, self.program_pointer)

    # Instruction 8:
    def equals(self):
        arg1 = self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer) 
        self.increment_program_pointer()

        arg2 = self.get_parameter_from_mode(self.addressing_modes[-2], self.program_pointer) 
        self.increment_program_pointer()

        solution = 1 if arg1 == arg2 else 0
        self.set_parameter_from_mode(self.addressing_modes[-3], solution, self.program_pointer)

    
    # Instruction 9: adjust the rel base by the value of its only parameter
    def adj_rel_base(self):
        
        #arg1 = self.memory[self.program_pointer]
        arg1 = self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer) 
        self.increment_program_pointer()

        self.relative_base += arg1

    # Instruction 99: Halt of program
    def halt(self):
        self.program_pointer = -1

    # 
    def get_parameter_from_mode(self, mode, address): #TODO: refactoring: do i need mode and address ?(self owns these)
        
        # position mode
        if mode == 0:
            return self.memory[self.memory[address]]
        
        # imidiate mode
        elif mode == 1:
            return self.memory[address]
        
        # relative (position) mode 
        elif mode == 2:
        
            # The address starts at its relative base (that is changed with opcode 9)
            return self.memory[self.memory[address] + self.relative_base] 

        else:
            return ValueError
    
    # Set memory to solution value w.r.t current addressing mode
    def set_parameter_from_mode(self, mode, solution, address): # 


        if mode == 0: #or self.addressing_modes[-3] == 1:
            self.memory[self.memory[address]] = solution # simply like before write solution to address

        # in day 9 a new mode is introduced that holds also for writing
        elif mode == 2:
            self.memory[self.memory[address] + self.relative_base] = solution
            # solution_address = self.memory[self.program_pointer]

        else:
            raise ValueError 
        self.increment_program_pointer()

    # The opcode (current address the pointer points on) is filled up to NUM_ADDRESSING_MODES + INSTRUCTION_LEN (=5) digits in total
    # The first left NUM_ADDRESSING_MODES (=3) of the opcode determine the mode of addressing the target of the operation, followed by INSTRUCTION_LEN(2) instructions
    # Let (AM3, AM2, AM1, I2, I1) be the zero padded opcode and, then the entries mean:
    # AM3 = addressing mode of the target 
    # AM2 = addressing mode of the second argument
    # AM1 = addressing mode of the first argument
    # I2, I1 = Instruction 
    def build_addressing_modes(self, opcode):

        # Fill up opcode with zeros to constant length
        opcode_str = str(opcode).zfill(self.NUM_ADDRESSING_MODES + self.INSTRUCTION_LEN)

        self.addressing_modes = list(map( lambda x : int(x), list(opcode_str[:self.NUM_ADDRESSING_MODES])))

    # execution of the programm based on the values of the puzzle inputs
    def execute_robot_programm(self):
        self.program_pointer = 0
        
        iter = 0
        while(self.program_pointer>=0):
            last_pointer = self.program_pointer             
            opcode = self.memory[self.program_pointer]
            self.increment_program_pointer()
            
            self.build_addressing_modes(opcode)

            # The last two digits of the opcode are the instruction
            instruction_code = opcode%100

            # Input current color (once per 2 ouputs = full instructionsqueue) before execution
            if not self.robot.color_out.empty():
                self.set_input(self.robot.color_out.get())
            
            #  Evaluate the correct function 
            self.instruction_dict[instruction_code]()

            # Feed output instructions to robot 
            if not self.out_instr.empty():# empty or filled with 1 = full 
                self.robot.get_instructions(self.out_instr.get())

            # Once we have aquired enough instructions (=2): paint panel and move forward
            if self.robot.instruction.full():
                self.robot.paint_and_move()


    # execution of the programm based on the values of the puzzle inputs
    def execute_arcade_programm(self):
        self.program_pointer = 0
        
        iter = 0
        while(self.program_pointer>=0):
            last_pointer = self.program_pointer             
            opcode = self.memory[self.program_pointer]
            self.increment_program_pointer()
            
            self.build_addressing_modes(opcode)

            # The last two digits of the opcode are the instruction
            instruction_code = opcode%100
            
            #TODO: nur den Joystick bewegen und diese position weitergeben, wenn ein input verlangt wird
            if instruction_code == 3: 
                self.arcade.control_joystick() 
                self.set_input(self.arcade.joystick) 
                multple = 1000
                self.arcade.plot_arcade_status(iter%multple)

                iter += 1 
            #  Evaluate the correct function 
            self.instruction_dict[instruction_code]()

            # Feed output instructions to arcade
            if not self.out_instr.empty():
                self.arcade.get_instructions(self.out_instr.get())
            
            # Once we gathered 3 instructions -> arcades does an action
            if self.arcade.instruction.full():
                self.arcade.parse_instructions(self.arcade.instruction)
                

               

    # execution of the programm based on the values of the puzzle inputs
    def execute_programm(self):
        self.program_pointer = 0
        
        iter = 0
        while(self.program_pointer>=0):
            last_pointer = self.program_pointer             
            opcode = self.memory[self.program_pointer]
            self.increment_program_pointer()
            
            self.build_addressing_modes(opcode)

            # The last two digits of the opcode are the instruction
            instruction_code = opcode%100
            
            #  Evaluate the correct function 
            self.instruction_dict[instruction_code]()

            if self.debug_mode:
                self.debug_print_at_end_iter(iter, opcode, last_pointer)
            iter += 1
    # Reads the memory of the int computer at a given address
    def read_memory(self, address):
        return self.memory[address]

    # Sets the memory of the int computer at a given address 
    def set_memory(self, address, value):
        self.memory[address] = value

    # Put one element of the input queue 
    def set_input(self, input):
        self.input.put(input)

    # Connects two int computer
    def connect_with_next_intcomputer(self, intcomputer):
        self.next_intcomputer = intcomputer

    # Functionality for debugging prints
    def debug_print_at_end_iter(self, iter, opcode, last_pointer):

        print("Iteration: ", iter)
        print("Pointer(start of iter): ", last_pointer)
        print("Pointer(end of iter): ", self.program_pointer)
        print("Opcode: ", opcode)
        print("addressing modes: ", self.addressing_modes)   
        print("Instruction: ", opcode%100, "-> fct:", str(self.instruction_dict[opcode%100])) 