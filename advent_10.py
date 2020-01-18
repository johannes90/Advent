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
#data = data4

data_list = data.strip().split("\n")

# parse data string to map 

# We need positions and lines to connect two asteroids
Position = namedtuple("Position", ["x", "y"])
Line = namedtuple("Line", ["m", "b"])
Vector = namedtuple("Vector", ["x", "y"])

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


# every point has a set containing n destinct Lines; those sets are stored in the LINES list
def compute_line_features(points_2D):
    
    LINES = []
    # 3: go through all points
    for point1 in points_2D:
        
        other_points = points_2D.copy()
        other_points.remove(point1)

        lines = set()
        # 4: for every point: go through all remaining points and compute the line y = mx+b 
        for point2 in other_points:

            # NOTE: vertival lines have a infinite slope and b is also infinite
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
    return LINES

def compute_vector_feature(points_2D):

    VECTORS = []
    for point in points_2D:
        
        # Create a subset of points where the current point is excluded
        other_points = points_2D.copy()
        other_points.remove(point)

        vectors = set()
        for other_point in other_points:
            
            # Compute normalized direction
            dx      = other_point.x - point.x
            dy      = other_point.y - point.y            
            length  = np.sqrt(dx**2 + dy**2)
            unit_dx = round(dx/length, 5)
            unit_dy = round(dy/length, 5) 
            unit_vecor = Vector(unit_dx, unit_dy)

            # Store vectors in a set to exclude points that lie on the same line(i.e. not observable)
            vectors.add(unit_vecor)

        VECTORS.append(vectors)
    return VECTORS

def find_best_observer(feature_sets):
    # look for the points with most "lines"
    max_features_number = 0
    max_features_number_idx = 0
    idx = 0
    for feature in feature_sets:

        feature_number = len(feature)
        #print(number_lines)
        if feature_number > max_features_number:
            max_features_number = feature_number
            max_features_number_idx = idx

        idx += 1
    
    return max_features_number, max_features_number_idx
    

map2D, asteroids = parse_data(data_list)
print(data)

#LINES = compute_line_features(asteroids)
VECTORS = compute_vector_feature(asteroids)

features_number, features_number_idx  = find_best_observer(VECTORS)


print("best is {} with {} other asteroids detected".format(asteroids[features_number_idx], features_number))

