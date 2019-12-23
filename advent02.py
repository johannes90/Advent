"""
Day 2: 1202 Program Alarm

List of integers
first integer opcode 1,2 or 99, then 3 positions
1 - add two positions, stores result in third position
2 - multiply
99 - finish
unknown: s.th. went wrong

"""

import numpy as np 

data = np.array([1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,5,19,23,1,6,23,27,1,27,10,31,1,31,5,35,2,10,35,39,1,9,39,43,1,43,5,47,1,47,6,51,2,51,6,55,1,13,55,59,2,6,59,63,1,63,5,67,2,10,67,71,1,9,71,75,1,75,13,79,1,10,79,83,2,83,13,87,1,87,6,91,1,5,91,95,2,95,9,99,1,5,99,103,1,103,6,107,2,107,13,111,1,111,10,115,2,10,115,119,1,9,119,123,1,123,9,127,1,13,127,131,2,10,131,135,1,135,5,139,1,2,139,143,1,143,5,0,99,2,0,14,0])
print(data.shape)
i = 0
while data[i] != 99:
   # print(i)
    if data[i] == 1:
        result = data[data[i+1]] + data[data[i+2]]
        
    elif data[i] == 2:
        result = data[data[i+1]] * data[data[i+2]]

    else:
        print("somethin went wrong")
        break
        
    # Put result at the index of second position after opcode    
    data[data[i+3]] = result
    
    i += 4
    
print(data)


"""
Day 2: 1202 Program Alarm - Part 2:
opcode as before, then instruction

"""
for noun in range(100):
    for verb in range(100):
        data = np.array([1,noun,verb,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,5,19,23,1,6,23,27,1,27,10,31,1,31,5,35,2,10,35,39,1,9,39,43,1,43,5,47,1,47,6,51,2,51,6,55,1,13,55,59,2,6,59,63,1,63,5,67,2,10,67,71,1,9,71,75,1,75,13,79,1,10,79,83,2,83,13,87,1,87,6,91,1,5,91,95,2,95,9,99,1,5,99,103,1,103,6,107,2,107,13,111,1,111,10,115,2,10,115,119,1,9,119,123,1,123,9,127,1,13,127,131,2,10,131,135,1,135,5,139,1,2,139,143,1,143,5,0,99,2,0,14,0])


        i = 0

        while data[i] != 99:
           # print(i)
            if data[i] == 1:
                result = data[data[i+1]] + data[data[i+2]]

            elif data[i] == 2:
                result = data[data[i+1]] * data[data[i+2]]

            else:
                print("somethin went wrong")
                break

            # Put result at the index of second position after opcode    
            data[data[i+3]] = result
            
            i += 4

        if data[0] == 19690720:
            print(str(noun) + " " + str(verb))
            print("solution =", 100*noun + verb)
