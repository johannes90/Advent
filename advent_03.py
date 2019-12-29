"""
Day 3: Crossed Wires - Part1 
Find intersection point with lowest manhatten distance to the origin

"""
import numpy as np
import time
import matplotlib.pyplot as plt
from operator import add
# Load data
wire1_instructions = "R1003,D430,L108,D570,R459,U7,L68,D232,L130,U93,R238,U951,L821,U723,L370,U873,L680,U749,R110,U17,R185,U484,R550,U356,L212,U350,L239,D208,R666,U70,L369,U448,R54,D402,R165,D375,L468,U886,L303,U779,L752,U664,L120,U643,R405,D288,L220,U727,L764,D615,R630,U688,R961,U499,L782,D852,L743,U443,R355,U856,L795,U235,L876,D511,L108,U637,R427,D338,L699,D911,L506,D607,L539,U977,R654,D634,L196,U944,R922,D774,R358,U828,L970,D386,R795,U602,R249,U793,L171,D217,L476,D123,L179,U820,R895,D239,R363,D629,L226,D811,R962,D848,R218,D581,R369,D872,L653,D281,R304,D302,R780,U636,L413,D712,L642,D886,R613,U736,L968,D82,R953,U408,L130,U654,R312,U74,L610,D798,R242,D586,L808,D664,L764,U455,R264,U384,L154,D484,R883,D276,L423,U11,L145,U156,L268,U46,R202,U641,R920,D483,R859,U94,L173,D796,R11,D328,R48,D161,L615,D396,R350,D48,R946,D233,R385,D294,R640,D301,R810,D824,L969,D469,R34,U995,R750,D827,R52,U606,R143,U868,L973,U863,L17,U995,L236,U994,R403,D312,R49,U143,L399,U821,R974,U119,R410,D233,R228,D326,R112,D512,L950,D103,L590,U80,R7,U441,L744,U643,L80,D631,L576,U680,R369,U741,L87,D748,R773,U145,R464,U546,R80,D251,L972,U414,L390,U148,L84,D481,L425,U293,L564,U880,R535,U703,R981,U944,R224,D366,R29,U517,R342,U686,L384,D650,R983,D287,L108,U713,L523,U695,R881,D126,R151,U153,R161,D791,L599,D936,L816,U387,R411,U637,L434,D22,L720,U579,L661,D644,L220,U325,R753,D392,L503,U617,R1,D956,L607,U602,L800,D749,L193,U215,L91,U733,L606,U510,L124,D550,R303,D835,R19,D326,R577,U265,L156,D924,L122,D186,R803,U3,R879"
wire2_instructions = "L1003,U603,L675,U828,R671,U925,R466,D707,L39,U1,R686,U946,L438,U626,R714,D365,L336,D624,R673,U672,L729,D965,R824,D533,R513,D914,R829,U275,L424,U10,L244,U158,R779,D590,R116,U714,R662,D989,R869,D547,R817,U315,R439,D29,L599,D870,L645,U656,R845,U19,R960,U669,L632,D567,L340,U856,R955,D314,R452,D896,R574,D162,R240,U302,R668,U706,R394,D24,L422,U884,R804,U576,L802,U400,R405,U676,L344,D628,R672,U580,R710,U536,L712,U738,L266,D212,R552,D229,R265,U835,R152,U784,L478,D87,L783,D327,R728,U590,R408,D397,R363,D654,R501,D583,R445,U897,R888,D480,R455,U593,R906,D506,R985,D361,R361,D619,L462,D873,L248,D348,R540,D578,L274,D472,R254,U647,R54,U681,L33,U343,R913,U120,L64,D849,L953,U407,L64,U744,L482,U240,L82,U69,R480,D796,L137,U527,R428,U67,R123,U688,L985,D944,R583,D804,R331,U328,R906,U376,L966,U433,R863,D931,L315,D9,L77,D141,L738,D661,R742,D44,R383,U78,R106,D301,L186,U907,L304,U786,L256,U718,R861,D145,R694,D721,R607,D418,R358,U600,R228,D139,R476,D451,L49,U616,L491,U8,R371,D735,R669,U388,L905,D282,L430,U491,L775,U891,L831,U350,L247,D609,R489,U266,R468,D748,R134,U187,R882,D315,R344,D363,R349,U525,R831,U644,R207,D563,L1,D946,L559,U789,L187,U370,L284,D910,L394,D560,L705,U661,R272,U109,L12,D554,L670,D169,L375,D100,R382,D491,L53,D916,R152,U82,L236,U845,L860,U732,R327,D190,R888,U722,R770,U993,R509,D970,L225,D756,R444,D992,L746,D35,R329,D452,R728,U575,L325,U414,L709,D844,R692,D575,R132,D520,L506,D384,L581,U36,L336,U849,L944,U450,R138,D186,L613,U805,R32,U763,R210,U556,R125,D499,R729"

# Returns a tuple (dx, dy) describing the difference given an instruction
def delta_xy_from_instruction(instr):
    dx, dy = 0,0
    if instr[0] == "L":
        dx =  - int(instr[1:])
        
    elif instr[0] == "R":
        dx =  int(instr[1:])
        
    elif instr[0] == "U":
        dy =  int(instr[1:])
    
    elif instr[0] == "D":
        dy =  - int(instr[1:])  
    
    return (dx, dy)

# Returns a list of tuples decribing all points between a 2D point(x,y) and a distance (dx,dy)
def approx_line(point_xy, prev_step, dx, dy):
    x1 = point_xy[0]
    y1 = point_xy[1]

    # We only move in constant x or constant y direction
    assert((dx == 0) or (dy == 0))

    # Move in x direction:
    x2 = x1 + dx
    y2 = y1 + dy

    # This is the number of steps:
    num_new_points = int(max(abs(x2 - x1), abs(y2 - y1)))
    
    # Compute all intermediate points (including start, end)
    line_x = list(np.linspace(x1, x2, num_new_points+1))         
    line_y = list(np.linspace(y1, y2, num_new_points+1))   
    
    # list of made steps 
    steps = list(np.linspace(prev_step, prev_step + num_new_points, num_new_points+1)) #TODO: check if we have overlapping points or count overlaps twice

    # convert lines into list of (x,y) tuples 
    line_point_tuples = list(zip(line_x, line_y))

    return (line_point_tuples, steps)

# Converts a wire of instruction strings to a wire of (x,y) points
def instr_wire_to_points(wire):

    # Go through wire and compute point lists of (x,y) tuples from instructions
    point_prev = (0,0)
    steps_prev  = 0
    wire_point_tuples = [point_prev]
    steps = [0]
    for instr in wire:  
        (dx, dy) = delta_xy_from_instruction(instr)

        # Compute current chunk of tuples
        (point_tuples_chunk, steps_chunk) = approx_line(point_prev, steps_prev, dx, dy) 
        
        # Add current chunk to the wire list
        wire_point_tuples.extend(point_tuples_chunk[1:])
        steps.extend(steps_chunk[1:])

        # Update next point (set on last point to ommit overlapping pieces)
        point_prev = point_tuples_chunk[-1] 
        steps_prev = steps_chunk[-1]

    return (wire_point_tuples, steps)

# Transform wire string into list of strings containing the instructions
wire1_instructions = wire1_instructions.split(",")
wire2_instructions = wire2_instructions.split(",")

# Transform instruction lists into lists of (x,y) tuples 
(wire1_tuple_list, wire1_steps) = instr_wire_to_points(wire1_instructions)
(wire2_tuple_list, wire2_steps) = instr_wire_to_points(wire2_instructions)

# Transform list of tuples into a set of tuples
wire1_tuple_set = set(wire1_tuple_list)
wire2_tuple_set = set(wire2_tuple_list)

# Compute intersection set between the two wire sets
intersections_set =  wire1_tuple_set.intersection(wire2_tuple_set)
intersections_set.remove((0.0, 0.0))

# Compute smalles manhatten distance of intersections (excluding the origin = 0.0)
d_L1     = list(map(lambda point: abs(point[0]) + abs(point[1]), intersections_set))
d_L1_ind = np.argmin(d_L1)
min_dist = min(d_L1)
print("Smalles manhatten distance of the two wires: ", min_dist)

"""
    Part 2: Lowest number of steps to an intersection
"""
# Transform points into arrays 
wire1_arr          = np.asarray(wire1_tuple_list)
wire2_arr          = np.asarray(wire2_tuple_list)
intersections_list = list(intersections_set)
intersections_arr  = np.asarray(intersections_list)

wire1_intersections_indices = []
wire2_intersections_indices = []
for intersection in intersections_list:

    # get indices of the intersection tuples in the wire 
    wire1_ind = wire1_tuple_list.index(intersection)
    wire1_intersections_indices.append(wire1_ind)

    wire2_ind = wire2_tuple_list.index(intersection)
    wire2_intersections_indices.append(wire2_ind)

    # Those should all lead to the intersection
    print("intersection: ",  intersection, 
    "wire 1 point at index of intersection: ",wire1_tuple_list[wire1_ind], 
    "wire 2 point at index of intersection: ",wire2_tuple_list[wire2_ind])  

# TODO: now we could check if the index lead to the correct intersection point
print(intersections_arr[14,0] + intersections_arr[14,1])


# Add index of both wires to obtain total steps to reach that intersection with both wires
total_steps = list(map(add, wire1_intersections_indices, wire2_intersections_indices))
min_total_steps = min(total_steps)
print("minimum steps to intersection: ", min_total_steps)

# Visualize of part 1 and part2
plt.figure()
# Plot both wires
plt.plot(wire1_arr[:, 0], wire1_arr[:, 1], color = "red", label = "wire 1")
plt.plot(wire2_arr[:, 0], wire2_arr[:, 1], color = "blue", label = "wire 2")
# Plot all intersections and mark the one with the lowest distance
plt.scatter(intersections_arr[:,0], intersections_arr[:,1], color = "green", label = "intersections", marker = "s")
plt.scatter(intersections_arr[14,0], intersections_arr[14,1], color = "red", label = "smalles distance", marker = "s")

plt.legend()
plt.show()

print()
# Wir haben beide Kabel und die Schnittpunkte 
# Wir können einfach die dx, dy werte benutzen 
#  Jeder Punkt bekommt nochmal einen aufsummierten ds Wert (ds = dx + dy) -> wire1_steps, wire2_steps
# TODO: Extract ds, values to the intersections 
# TODO: Chose lowest ds value