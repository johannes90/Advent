from AdventClasses import IntComputer

# Load puzzle input 
f = open("advent_09_input.txt", "r") 
puzzle_input = f.read()

#puzzle_input = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99" # Test 1: copy of itself as output
#puzzle_input = "1102,34915192,34915192,7,4,7,99,0" # Test 2: ouputs a 16 digit number 
#puzzle_input = "104,1125899906842624,99" # Test 3: outputs the large middle number 

# Create new intcomputer
intcomputer = IntComputer()

# Parse puzzle input 
intcomputer.parse_instruction(puzzle_input)

# Provide input 
intcomputer.set_input(1)

# Run program 
intcomputer.execute_programm()

# TODO: opcode 203 (input opcode and relativ mode seem not to work)
