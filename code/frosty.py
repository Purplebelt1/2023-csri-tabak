from PIL import Image, ImageEnhance
import cv2 as cv
import numpy as np
from scipy.interpolate import UnivariateSpline
import Result

# Function to create a lookup table using spline interpolation
def LookupTable(x, y):
    spline = UnivariateSpline(x, y)  # Create a spline using x and y values
    return spline(range(256))  # Evaluate the spline for each value in the range 0-255

# Frost effect function
def frosty(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])  # Lookup table for increasing blue channel
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])  # Lookup table for decreasing red channel
    
    blue_channel, green_channel, red_channel = cv.split(img)  # Split the image into separate channels
    red_channel = cv.LUT(red_channel, decreaseLookupTable).astype(np.uint8)  # Apply lookup table to the red channel
    blue_channel = cv.LUT(blue_channel, increaseLookupTable).astype(np.uint8)  # Apply lookup table to the blue channel
    
    frost = cv.merge((blue_channel, green_channel, red_channel))  # Merge the modified channels into an image
    
    return frost  # Return the resulting frost effect image


def main():
  base_img = cv.imread("./images/stairs1.jpg")
  frosted = frosty(base_img)
  Result.multiWindow([base_img,frosted])

if __name__ == '__main__':
   main()