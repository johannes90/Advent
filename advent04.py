"""
Day 4: Secure Container

Password criteria
1: It is a six-digit number.
2: The value is within the range given in your puzzle input.
3: Two adjacent digits are the same (like 22 in 122345).
4: Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

"""

def is_decreasing_two_adjacent(number):

    # Convert the number into a string
    number_str = str(number)

    last_digit       = 0     # allways neutral element for first digit
    is_decreasing    = True  # Only toggle to False if the non-decreasing condition apply
    has_two_adjacent = False # Only toggle to True if the two-adjacent-digits condition apply

    # Go through digits in number and check if they decrease
    for digit_str in number_str:
    
        digit = int(digit_str)

        # Condition for non-decreasing order
        if last_digit > digit:
            is_decreasing =  False            

        # Condition for two adjacent digits 
        if last_digit == digit:
            has_two_adjacent = True

        # Increment last digit 
        last_digit = digit

    return (is_decreasing, has_two_adjacent) 

def is_decreasing_exactly_two_adjacent(number):
    
    # Convert the number into a string
    number_str = str(number)

    adjacent_counter = 0
    last_last_digit  = -1
    last_digit       = 0     # allways neutral element for first digit
    is_decreasing    = True  # Only toggle to False if the non-decreasing condition apply
    has_two_adjacent = False # Only toggle to True if the two-adjacent-digits condition apply

    # Go through digits in number and check if they decrease
    for digit_str in number_str:
    
        digit = int(digit_str)

        # Condition for non-decreasing order
        if last_digit > digit:
            is_decreasing =  False            

        # Count adjacent digits
        if digit ==  last_digit:
            adjacent_counter += 1
        else: 
            # If adjacent counter was 1 there existed exactly two adjacent and not more digits
            if adjacent_counter == 1:
                has_two_adjacent = True
            adjacent_counter = 0

        # Increment last digit and the digit before
        last_last_digit = last_digit
        last_digit      = digit

    if adjacent_counter == 1: 
        has_two_adjacent = True
    return (is_decreasing, has_two_adjacent) 


input1 = 235741
input2 = 706948

num_possible_pw = 0

# Iterate through the range and check the criteria
for number in range(235741, 706948 + 1):
    (is_decreasing, has_two_adjacent) = is_decreasing_exactly_two_adjacent(number)

    # Increase counter if both conditions apply
    if(is_decreasing and has_two_adjacent):
        num_possible_pw += 1

print(num_possible_pw)