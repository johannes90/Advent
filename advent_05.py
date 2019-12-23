from IntComputer import *

f = open("advent5_input.txt", "r")
puzzle_data = f.read()

intcomputer = IntComputer()

# Set manually to a specific number (given in assigment)
intcomputer.input.put(5)  

intcomputer.parse_instruction(puzzle_data)

intcomputer.execute_programm()