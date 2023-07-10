from PIL import Image, ImageEnhance
import math
import cv2 as cv
import numpy as np
from scipy.interpolate import UnivariateSpline
import Result




# Creates a lookup table using spline interpolation
#
# INPUT
#
#    x: A list of base numbers. The numbers you wish to be turned into the y array
#
#    y: A list of adjusted numbers. The numbers you wish those in x array to be turned into.
#
# OUTPUT
#
#    LUT: A full lookup table from 0 to 255 built from spline inerpolation from x to y.
#
def LookupTable(x, y):
    spline = UnivariateSpline(x, y)  # Create a spline using x and y values
    LUT = spline(range(256))  # Evaluate the spline for each value in the range 0-255
    return LUT




def drawRegularPolygon(img, coords, size, sides, thickness, color, rotation, fill_type = "none"):

    coords[0] = round(coords[0])
    coords[1] = round(coords[1])


    img = img.copy()


    pts1 = np.empty([sides, 1], dtype = int)
    pts2 = np.empty([sides, 1], dtype = int)

    #angles = np.linspace(1, 2 * math.pi, sides, endpoint=False) + rotation
    #cos_vals = np.cos(angles) * size + coords[0]
    #sin_vals = np.sin(angles) * size + coords[1]
    #pts1 = np.round(cos_vals).astype(int)
    #pts2 = np.round(sin_vals).astype(int)

    for i in range(len(pts1)):

        pts1[i] = round(math.cos((i+1)/sides*2*math.pi + rotation) * size) + coords[0]
        pts2[i] = round(math.sin((i+1)/sides*2*math.pi + rotation) * size) + coords[1]
    

    


    if fill_type == "center":
        pts1 = np.clip(pts1, 0, img.shape[1] * 2)
        pts2 = np.clip(pts2, 0, img.shape[0] * 2)

        pts = np.concatenate((pts1,pts2), axis=1)
        if coords[0] < 0 or coords[0] >= img.shape[1] or coords[1] < 0 or coords[1] >= img.shape[0]:
            color_tuple = (255,255,255)
        else:
            color_tuple = tuple([int(i) for i in img[coords[1]][coords[0]]])
        img = cv.fillPoly(img, pts=[pts], color=color_tuple)

    elif fill_type == "average":
        pts1 = np.clip(pts1, 0, img.shape[1])
        pts2 = np.clip(pts2, 0, img.shape[0])
        #pts = np.column_stack((pts1,pts2))
        pts = np.concatenate((pts1,pts2), axis=1)
        #print(pts)

        mask = np.zeros(img.shape[:2], np.uint8)
        mask = cv.drawContours(mask, [pts], -1, 255, -1)
        mean_color = cv.mean(img, mask=mask)
        img = cv.fillPoly(img, pts=[pts], color=mean_color)



    else:
        img = cv.polylines(img, [pts], True, color, thickness)

    return img
    
    
def drawRegularTessellation(img, size, thickness, color, shape):
    img = img.copy()
    shape = shape.lower()
    if shape == "triangle":
        sides = 3
        row_move_horz = size*math.sqrt(3)/2
        row_move_vert = size/2
        col_move_horz = -1 * size * math.sqrt(3)/2
        col_move_vert = size * 1.5
        row_rot = math.pi
        start_rot = 1/6*math.pi
    elif shape == "square":
        sides = 4
        row_move_horz = size/math.sqrt(2)*2
        row_move_vert = 0
        col_move_horz = 0
        col_move_vert = size/math.sqrt(2)*2
        row_rot = 0
        start_rot = .25*math.pi
    elif shape == "hexagon":
        sides = 6
        row_move_horz = size * 3
        row_move_vert = 0
        col_move_horz = 3*size/2
        col_move_vert = size/2*math.sqrt(3)
        row_rot = 0
        start_rot = 0
    else:
        ValueError("shape must be either triangle, square, or hexagon!")
    
    per_row = round(img.shape[1]/(row_move_horz) + 2)
    per_col = round(img.shape[0]/(col_move_vert) + 2)
    #per_col = 1

    print(per_row)
    print(per_col)

    coords = [0, 0]

    i = 0
    while coords[1] < img.shape[0]:
        j = 0
        while coords[0] < img.shape[1]:

            coords[1] = round((col_move_vert * i) + (row_move_vert * ((j+1)%2)))
            
            img = drawRegularPolygon(img, coords, size, sides, thickness, color, j%2 * row_rot + start_rot, "average")

            coords[0] += row_move_horz
            coords[0] = round(coords[0])

            j += 1


        coords[0] = round((i+1)%2 * col_move_horz)
        i += 1
        #coords[1] = col_move_vert * (i+1)

    return img

def readCoordsFromFile(path):
    file = open(path, 'r')
    lines = file.readlines()
    result = ''.join([item for item in lines])[1:-2].split(")\n(")
    result = [list(map(int, item.split(','))) for item in result]
    file.close()
    return result


#
#
# INPUT
#
#
#
# OUTPUT
#
#
#
def colorInRangeThreshold(img, lower_bound, upper_bound ,invert = False):

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_bound, upper_bound)
    if invert:
        mask = cv.bitwise_not(mask)
    target = cv.bitwise_and(img,img, mask=mask)
    #target = cv.cvtColor(target, cv.COLOR_HSV2BGR)

    return target, mask


# Changed the input image into a cool effect by increasing preset B valuse in BGR and decreasing R values
#
# INPUT
#
#    img: The input image to be manipulated.
#
# OUTPUT
#
#    frost: The output image after manipulation
#
def Frosty(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])  # Lookup table for increasing blue channel
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])  # Lookup table for decreasing red channel
    
    blue_channel, green_channel, red_channel = cv.split(img)  # Split the image into separate channels
    red_channel = cv.LUT(red_channel, decreaseLookupTable).astype(np.uint8)  # Apply lookup table to the red channel
    blue_channel = cv.LUT(blue_channel, increaseLookupTable).astype(np.uint8)  # Apply lookup table to the blue channel
    
    frost = cv.merge((blue_channel, green_channel, red_channel))  # Merge the modified channels into an image
    
    return frost  # Return the resulting frost effect image


# Changed the input image into a warm effect by increasing preset R valuse in BGR and decreasing B values
#
# INPUT
#
#    img: The input image to be manipulated.
#
# OUTPUT
#
#    toast: The output image after manipulation
#
def Toasty(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])  # Lookup table for increasing blue channel
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])  # Lookup table for decreasing red channel
    
    blue_channel, green_channel, red_channel = cv.split(img)  # Split the image into separate channels
    blue_channel = cv.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)  # Apply lookup table to the red channel
    red_channel = cv.LUT(red_channel, increaseLookupTable).astype(np.uint8)  # Apply lookup table to the blue channel
    
    toast = cv.merge((blue_channel, green_channel, red_channel))  # Merge the modified channels into an image
    
    return toast  # Return the resulting toasty effect image


# Emulates a piece of nitrate film aged and scratched. Adding sepia, film scratches, and slight blur.
#
# INPUT
#
#    img: The input image to be manipulated into looking like nitrate film
#
# OUTPUT
#
#    output: The images after being turned to look like old nitrate film.
#
def VintageVibe(img):
    # Apply Gaussian blur to the input image
    blurred_img = cv.GaussianBlur(img, (31, 31), 0)

    # Convert the blurred image to grayscale
    bwImg = cv.cvtColor(blurred_img, cv.COLOR_BGR2GRAY)
    # Convert the grayscale image back to BGR (color image)
    bwImg = cv.cvtColor(bwImg, cv.COLOR_GRAY2BGR)

    # Create a yellow layer of the same shape as bwImg
    yellow_layer = np.full(bwImg.shape, (0, 255, 255), np.uint8)

    # Create a tinted image by blending bwImg and yellow_layer
    bwYlwTint = cv.addWeighted(bwImg, 0.85, yellow_layer, 0.15, 0)

    # Load scratches image
    scratches = cv.imread("./images/dusty3.jpg")

    # Get dimensions of bwYlwTint
    bwWdt = bwYlwTint.shape[0]
    bwHght = bwYlwTint.shape[1]

    # Resize the scratches image to match the dimensions of bwYlwTint
    resized_scratches = cv.resize(scratches, (bwHght, bwWdt))

    # Threshold the resized scratches image to create a binary mask
    th, bi_scratches = cv.threshold(resized_scratches, 150, 255, cv.THRESH_TOZERO)

    # Replace areas in bi_scratches where the pixels are black with corresponding pixels from bwYlwTint
    output = np.where(bi_scratches == [0, 0, 0], bwYlwTint, bi_scratches)

    return output

def Halloween(img, dark=3):
    return Gamma(Toasty(img), dark)

# Changes the gamma of the image. Gamma is control of the intensity of the middle range relative to a binary color space
#
# INPUT
#
#    img: The input image to be manipulated.
#
#    gamma: The gamma that you want to change the image to with the image having a relative gamma of one.
#
# OUTPUT
#
#    res: The image after it's manipulation
#
def Gamma(img, gamma):
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    res = cv.LUT(img, lookUpTable)
    return res

# Contrast Limited Adaptive Histogram Equalization Algirithim with interpolation.
#
# INPUT
#
#    clipLim: The multiplicatitve limit for amplifacation
#
#    grideSize: The tile grid size for the interpoltation.
#
# OUTPUT
#
#    enhanced_img: The altered image output
#
def CLAHE(img, clipLim = 2.0, gridSize=(16,16)):

    lab= cv.cvtColor(img, cv.COLOR_BGR2LAB)
    l_channel, a, b = cv.split(lab)

    # Applying CLAHE to L-channel
    clahe = cv.createCLAHE(clipLimit=clipLim, tileGridSize=gridSize)
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv.merge((cl,a,b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv.cvtColor(limg, cv.COLOR_LAB2BGR)
    return enhanced_img




# Code taken from StackOverflow. Changes brightness and contrast 
# https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
#
# INPUT
#
#    input_img: The image to be altered
#
#    brightness:
#
#    contrast:
#
# OUTPUT
#
#    buf: The altered image with changed contrast and brightness in BGR color space.
#
def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):
    
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        
        buf = cv.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        
        buf = cv.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf


# An algirthim for changing the saturation by creating a lookup table using a univariate spline based on exponentiating the coeff given
#
# INPUT
#
#    img: The base image to be altered. Must be in BGR color space.
#
#    saturationCoeff: The coeffcient that in exponentiated to create the lookup table
#
# OUTPUT
#
#    output: The image after applying the saturation change in BGR color space.
#
def SaturateByCurve(img, saturationCoeff):

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # If you want to adjust curve adjust the expoenents
    saturationLUT = LookupTable([0,85,170,256],[round(saturationCoeff * 255), round((saturationCoeff ** .5) * 170 + 85),round((saturationCoeff ** .75) * 80 + 170), 256])

    hue, saturation, value = cv.split(hsv)  # Split the image into separate channels

    saturation = cv.LUT(saturation, saturationLUT).astype(np.uint8)

    output = cv.merge((hue, saturation, value))

    output = cv.cvtColor(output, cv.COLOR_HSV2BGR)

    return output



# Returns both inner and outer crop given coordinates of corners in polygon
#
# INPUT
#
#    img: The img you want to crop from
#
#    coords: The coordinates of the corners of the polygon you wish to crop
#
# OUTPUT
#
#    inner_crop: The area inside of your polygon with the rest of the image removed
#
#    outer_crop: The area outside of your polygon with the inside of the polygon turned white
#
def cropPolygon(img, coords):

    ## (1) set bounded rectangle
    coords = np.array(coords)
    rect = cv.boundingRect(coords)
    x,y,w,h = rect
    croped = img[y:y+h, x:x+w].copy()

    ## (2) make mask
    pts = coords - coords.min(axis=0)

    mask = np.zeros(croped.shape[:2], np.uint8)
    cv.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv.LINE_AA)

    ## (3) do bit-op
    inner_crop = cv.bitwise_and(croped, croped, mask=mask)

    ## (4) Create outer crop
    img_copy = img.copy()
    outer_crop = cv.drawContours(img_copy, [coords], -1, (255, 255, 255), -1, cv.LINE_AA)
    return inner_crop, outer_crop

def main():
  base_img = cv.imread("./images/skyline.jpg")
  #new_img = cv.imread("./images/justin/old_bridge.jpeg")
  #hexaGONE = drawRegularPolygon(base_img, [1000,1000], 100, 3, 10, (0,0,255), 0)
  #new_img = CLAHE(new_img, 1.0, (16,16))
  #new_img = SaturateByCurve(new_img, .1)
  #new_img = Toasty(new_img)
  new_img = drawRegularTessellation(base_img, 100, 5, (0,0,0), "hexagon")
  #triangleTess = drawRegularTessellation(base_img, 25, 5, (0,0,0), "triangle")
  #squareTess = drawRegularTessellation(base_img, 25, 5, (0,0,0), "square")
  #print(base_img.shape)
  #croped_outer, croped_inner = cropPolygon(base_img, [[2000,45], [92,200], [63, 75]])
  #thresh, mask = colorInRangeThreshold(base_img, (100,20,10), (115,255,255), True)
  #thresh, mask = colorInRangeThreshold(base_img, (0,0,0), (179,255,255))


  dim = new_img.shape[:2]
  Result.singleWindow([new_img], imDim = dim, dtype = "h")
  #Result.singleWindow([croped_inner])

if __name__ == '__main__':
   main()