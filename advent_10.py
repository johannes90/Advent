"""
    1: convert input into numpy 2d array -> we do not need that 

    2: extract (x,y) positions of all asteroids 
    3: go through all points
    4: for every point: go through all remaining points and compute the line y = mx+b 
    5: store m,b as a tuple in a set 
    6: length of set = visible asteroids for given asteroid 
"""
import numpy as np 
import matplotlib.pyplot as plt
from collections import namedtuple

f = open("advent_10_input.txt", "r") 
data = f.read()
f.close()

# test cases 
data0 = """
.#..#
.....
#####
....#
...##
"""


data1 = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""

data2 = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""

data3 = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""

data4 = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

# Use one of the test cases
data = data4

data_list = data.strip().split("\n")

# parse data string to map 


Position = namedtuple("Position", ["x", "y"])


def parse_data(data_list):

    ast_map = {".":0, "#":1}
    asteroids =  []
    num_rows, num_cols = (len(data_list), len(data_list[0])) 
    map_shape = num_rows, num_cols
    map2D = np.zeros((map_shape))
    
    for row in range(len(data_list)):

        line = data_list[row]
        for col in range(len(line)):

            # Save data to a 2D map for visualizations(not needed so far)
            field = line[col]
            map2D[row, col] = ast_map[field]    

            # store asteroids positions
            if field == "#":
                position = Position(col, (num_rows-1) - row)
                asteroids.append(position)

        row += 1
    return map2D, asteroids

map2D, asteroids = parse_data(data_list)
print(data)


# every point has a set containing n destinct Lines; those sets are stored in the LINES list
LINES = []
Line = namedtuple("Line", ["m", "b"])

# 3: go through all points
for point1 in asteroids:
    
    other_asteroids = asteroids.copy()
    other_asteroids.remove(point1)

    lines = set()
    # 4: for every point: go through all remaining points and compute the line y = mx+b 
    for point2 in other_asteroids:

        # TODO: there are lines with m = +-inf: 
        # NOTE: just save two distinct "features" whether the point is above or below
        if (point2.x - point1.x == 0):
            m = np.sign(point1.y - point2.y)   
            b = point1.x 

        # NOTE: b is the same for two horizontal lines:
        elif(point2.y - point1.y ==0):
            m = np.sign(point2.x - point1.x)
            b = point1.y
        else:
            m = (point2.y - point1.y) / (point2.x - point1.x)
            b = -m * point1.x + point1.y

        # 5: store m,b as a tuple in a set 
        line = Line(m, b)
        lines.add(line)

    # Store all lines for the current point in the list
    LINES.append(lines)
    
# look for the points with most "lines"
max_number_lines = 0
max_number_lines_idx = 0
idx = 0
for lines in LINES:

    number_lines = len(lines)
    #print(number_lines)
    if number_lines > max_number_lines:
        max_number_lines = number_lines
        max_number_lines_idx = idx

    idx += 1
    


print("best is {} with {} other asteroids detected".format(asteroids[max_number_lines_idx], max_number_lines))


# TODO: visualize number of seen asteroids for every asteroid
for lines in LINES:

    number_visible_asteroids = len(lines)

    #print(number_visible_asteroids)