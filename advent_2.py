from IntComputer import *


# 2. Advent day:
f = open("advent_02_input.txt", "r")
puzzle_data = f.read()

print(puzzle_data)

intcomputer2 = IntComputer()

intcomputer2.parse_instruction(puzzle_data)

# Puzzle instruction: replace memory position 1 with 12 and position 2 with 2
intcomputer2.set_memory(1, 12)
intcomputer2.set_memory(2, 2)

intcomputer2.execute_programm()

# Check the solution 
print("solution of 2. advent - part1: ", intcomputer2.read_memory(0))

# 5. Advent day: