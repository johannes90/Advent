test  = "012, 5,6,7 "
print(test)
import queue


test_queue = queue.LifoQueue()

intstring = list(map(lambda x: int(x), test.split(",")))
print(intstring[1] + intstring[2])
print(type(intstring[0]))


instruction_dict = {1: "add_function", 2: "multiply"}
print(instruction_dict[1])

def add_function(arg1, arg2):

    return arg1 + arg2

print(eval(instruction_dict[1])(1, 2))

