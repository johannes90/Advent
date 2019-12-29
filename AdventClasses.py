"""

"""
import queue

class IntComputer: 

    INSTRUCTION_LEN      = 2
    NUM_ADDRESSING_MODES = 3

    def __init__(self, debug_mode = False):

        self.memory           = []                       # RAM of Int Computer
        self.program_pointer  = None                     # points on the adress of the current instruction of the programm
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
        # Use setter function to check if adressing mode of target is 0 or 2 (1 does not make sense )
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

        solution = self.input.get()
        self.set_parameter_from_mode(self.addressing_modes[-1], solution, self.program_pointer)

    # Instruction 4: 
    def outqueue(self):

        # Output value (print and store in a list)
        outp = self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer)
        self.increment_program_pointer()

        self.output = outp
        print(outp)
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
            # solution_adress = self.memory[self.program_pointer]

        else:
            raise ValueError 
        self.increment_program_pointer()

    # The opcode (current adress the pointer points on) is filled up to NUM_ADDRESSING_MODES + INSTRUCTION_LEN (=5) digits in total
    # The first left NUM_ADDRESSING_MODES (=3) of the opcode determine the mode of adressing the target of the operation, followed by INSTRUCTION_LEN(2) instructions
    # Let (AM3, AM2, AM1, I2, I1) be the zero padded opcode and, then the entries mean:
    # AM3 = adressing mode of the target 
    # AM2 = adressing mode of the second argument
    # AM1 = adressing mode of the first argument
    # I2, I1 = Instruction 
    def build_adressing_modes(self, opcode):

        # Fill up opcode with zeros to constant length
        opcode_str = str(opcode).zfill(self.NUM_ADDRESSING_MODES + self.INSTRUCTION_LEN)

        self.addressing_modes = list(map( lambda x : int(x), list(opcode_str[:self.NUM_ADDRESSING_MODES])))

    # execution of the programm based on the values of the puzzle inputs
    def execute_programm(self):
        self.program_pointer = 0
        
        iter = 0
        while(self.program_pointer>=0):
            last_pointer = self.program_pointer             
            opcode = self.memory[self.program_pointer]
            self.increment_program_pointer()
            
            self.build_adressing_modes(opcode)

            # The last two digits of the opcode are the instruction
            instruction_code = opcode%100

            # Evaluate the correct function 
            self.instruction_dict[instruction_code]()

            if self.debug_mode:
                self.debug_print_at_end_iter(iter, opcode, last_pointer)
            iter += 1
    # Reads the memory of the int computer at a given address
    def read_memory(self, adress):
        return self.memory[adress]

    # Sets the memory of the int computer at a given address 
    def set_memory(self, adress, value):
        self.memory[adress] = value

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
        print("adressing modes: ", self.addressing_modes)   
        print("Instruction: ", opcode%100, "-> fct:", str(self.instruction_dict[opcode%100])) 