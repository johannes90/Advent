"""

"""
import queue

class IntComputer: 

    INSTRUCTION_LEN      = 2
    NUM_ADDRESSING_MODES = 3

    def __init__(self):

        self.memory           = []                           # RAM of Inn Computer
        self.program_pointer  = None                         # points on the adress of the current instruction of the programm
        self.instruction_dict = {1:  self.add, 
                                 2:  self.multiply, 
                                 3:  self.inqueue,
                                 4:  self.outqueue,
                                 5:  self.jump_if_True,
                                 6:  self.jump_if_False,
                                 7:  self.less_than,
                                 8:  self.equals,
                                 99: self.halt}

        self.input            = queue.LifoQueue()
        self.addressing_modes  = [0,0,0]                 

    def parse_instruction(self, instruction_string):

        self.memory = list(map(lambda x: int(x), instruction_string.split(",")))

    def increment_program_pointer(self):

        self.program_pointer += 1

    

    # Instruction 1: Addition
    def add(self):

        # We asume the program pointer is on the first argument
        arg1 = self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer) 
        self.increment_program_pointer()

        arg2 = self.get_parameter_from_mode(self.addressing_modes[-2], self.program_pointer) 
        self.increment_program_pointer()

        # Adressing mode of target is never 1(illogical) but might be other than 0 
        solution_adress = self.memory[self.program_pointer]
        self.increment_program_pointer()

        self.memory[solution_adress] = arg1 + arg2

    # Instruction 2: Multiplication
    def multiply(self):
    
        # We asume the program pointer is on the first argument
        arg1 = self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer) 
        self.increment_program_pointer()

        arg2 = self.get_parameter_from_mode(self.addressing_modes[-2], self.program_pointer) 
        self.increment_program_pointer()
    
        solution_adress = self.memory[self.program_pointer]
        self.increment_program_pointer()

        self.memory[solution_adress] = arg1*arg2
    
    # Instruction 3: 
    def inqueue(self):

        solution_adress = self.memory[self.program_pointer]
        self.increment_program_pointer()

        self.memory[solution_adress] = self.input.get() # first-out value of the queue
        
    # Instruction 4: 
    def outqueue(self):

        # Output value 
        print(self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer))
        self.increment_program_pointer()

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

        solution_adress = self.memory[self.program_pointer]
        self.increment_program_pointer()

        self.memory[solution_adress] = 1 if arg1 < arg2 else 0
    
    # Instruction 8:
    def equals(self):
        arg1 = self.get_parameter_from_mode(self.addressing_modes[-1], self.program_pointer) 
        self.increment_program_pointer()

        arg2 = self.get_parameter_from_mode(self.addressing_modes[-2], self.program_pointer) 
        self.increment_program_pointer()

        solution_adress = self.memory[self.program_pointer]
        self.increment_program_pointer()

        self.memory[solution_adress] = 1 if arg1 == arg2 else 0

    # Instruction 99: Halt of program
    def halt(self):
        self.program_pointer = -1

    # 
    def get_parameter_from_mode(self, mode, address):

        if mode == 0:
            return self.memory[self.memory[address]]
        elif mode == 1:
            return self.memory[address]
        else:
            # later adcents day
            print("bla")
    
    # 
    def build_adressing_modes(self, opcode):

        # Fill up opcode with zeros to constant length
        opcode_str = str(opcode).zfill(self.NUM_ADDRESSING_MODES + self.INSTRUCTION_LEN)

        self.addressing_modes = list(map( lambda x : int(x), list(opcode_str[:self.NUM_ADDRESSING_MODES])))

    def execute_programm(self):
        self.program_pointer =0

        while(self.program_pointer>=0):

            opcode = self.memory[self.program_pointer]
            self.increment_program_pointer()
            
            self.build_adressing_modes(opcode)

            # the last two digits of the opcode is the instruction
            instruction_code = opcode%100

            # Evaluate the correct function 
            self.instruction_dict[instruction_code]()

    
    def read_memory(self, adress):
        return self.memory[adress]

    def set_memory(self, adress, value):
        self.memory[adress] = value
