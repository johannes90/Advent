from AdventClasses import IntComputer

# Load puzzle input 
f = open("advent_09_input.txt", "r") # TODO: not passed, out= 203 0
puzzle_input = f.read()

# Create new intcomputer
intcomputer = IntComputer(False)

# Parse puzzle input 
intcomputer.parse_instruction(puzzle_input)

# Provide input 
intcomputer.set_input(1)

# Run program 
intcomputer.execute_programm()
