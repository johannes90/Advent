from AdventClasses import IntComputer

f = open("advent5_input.txt", "r")
puzzle_data = f.read()

# Initiate an Int computer 
intcomputer = IntComputer()

# Set input manually to a specific number (given in assigment)
intcomputer.input.put(5)  

# Parse the puzzle input in the RAM of the int computer
intcomputer.parse_instruction(puzzle_data)


intcomputer.execute_programm()