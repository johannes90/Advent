import numpy as np 
import matplotlib.pyplot as plt
from collections import namedtuple

f = open("advent_08_input.txt", "r") 
data = f.read()
f.close()

data_list = list(data)
number_total_pixels =len(data_list)

image_height = 6
image_width  = 25
ImageShape = namedtuple("image_shape", ["height", "width"])
image_shape = ImageShape(image_height, image_width)

pixel_per_layer = image_shape.height * image_shape.width
number_layers = int(number_total_pixels/pixel_per_layer)


def image_pixel_list_to_layer(pixel_list, image_shape):

    layer = np.asarray(pixel_list)
    layer = layer.reshape(image_shape, order = "C")
    
    return layer

def image_list_to_layers(pixel_str, number_layers, pixel_per_layer):

    image = number_layers*[None]
    lowest_number_zeros = 150
    layer_idx_lowest_zeros = 0

    lowest= []
    for i_layer in range(number_layers):
        start = i_layer * pixel_per_layer   
        stop  = (i_layer + 1) * pixel_per_layer
        layer_list   =  pixel_str[start:stop]
        layer_list   = list(map(lambda x: float(x), layer_list))

        layer_2D_arr = image_pixel_list_to_layer(layer_list, image_shape)

        image[i_layer] = layer_2D_arr

        zero_numbers = pixel_per_layer - np.count_nonzero(layer_2D_arr)


        if zero_numbers < lowest_number_zeros:
            lowest_number_zeros    = zero_numbers
            layer_idx_lowest_zeros = i_layer
            lowest.append(zero_numbers)

    return (image, lowest_number_zeros, layer_idx_lowest_zeros)


# Part 1: find layer with fewest 0 pixels
# On that layer: solution = number of 1 digits * number of 1 digits
image2D, lowest_number_zeros, layer_idx_lowest_zeros = image_list_to_layers(data_list, number_layers, pixel_per_layer)
     

digits_1 = np.count_nonzero(image2D[layer_idx_lowest_zeros] == 1)
digits_2 = np.count_nonzero(image2D[layer_idx_lowest_zeros] == 2)

# Solution part 1
print(digits_1 * digits_2)

# part 2
# 
reshaped_image = np.asarray(image2D).reshape(number_layers, -1)


# debug test :
number = 99
test1 = reshaped_image[:number, 1]
test2 = [image2D[i][0,1] for i in range(number)]
assert((test1 - test2).all() == 0)


# Build a merged image: keep first layers pixel if pixel value is not 2(transparent)
merged_image = 2*np.ones(image_shape)

for row in range(image_shape.height):
    for col in range(image_shape.width):

        idx = row * image_shape.width + col

        # find first pixel with value 0 or 1 in all layers
        layer = 0
        pixel = -1
        while layer < 100:

            pixel = reshaped_image[layer, idx] 

            if pixel != 2:
                break
            
            layer +=1

            # print("row={}, col={}, layer={}".format(row,col,layer))

        merged_image[row, col] = pixel



plt.figure()
plt.imshow(merged_image)
plt.show()

