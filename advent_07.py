from AdventClasses import IntComputer
import itertools

import threading

f = open("advent_07_input.txt", "r") 

puzzle_data = f.read()

posible_inputs = list(range(5,10))
posible_input_sequences  = list(itertools.permutations(posible_inputs)) # We can use a simple permutation here because every phase setting is used exactly once

Amp = 5*[None]
for i in range(5):
    Amp[i] = IntComputer()

for i in range(5):
    Amp[i].connect_with_next_intcomputer(Amp[(i+1)%5])

# Loop over all input/phase sequences to find maximum thrust output
highest_output = 0 

for input_sequence in posible_input_sequences:

    # Set initial input 
    for i in range(5):
        Amp[i].parse_instruction(puzzle_data)
        Amp[i].set_input(input_sequence[i])

    # The first one is not connected
    Amp[0].set_input(0)
    
    # Execute Amplifiers
    threads = []
    for i in range(5):
        t = threading.Thread(target = Amp[i].execute_programm, args = ())
        t.start()
        threads.append(t)

    # Join all threads
    for thread in threads:
        thread.join()

    if highest_output < Amp[4].output:
        highest_output = Amp[4].output

print("highest output: ", highest_output)
