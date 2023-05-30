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
def Frosty(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])  # Lookup table for increasing blue channel
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])  # Lookup table for decreasing red channel
    
    blue_channel, green_channel, red_channel = cv.split(img)  # Split the image into separate channels
    red_channel = cv.LUT(red_channel, decreaseLookupTable).astype(np.uint8)  # Apply lookup table to the red channel
    blue_channel = cv.LUT(blue_channel, increaseLookupTable).astype(np.uint8)  # Apply lookup table to the blue channel
    
    frost = cv.merge((blue_channel, green_channel, red_channel))  # Merge the modified channels into an image
    
    return frost  # Return the resulting frost effect image

def Toasty(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])  # Lookup table for increasing blue channel
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])  # Lookup table for decreasing red channel
    
    blue_channel, green_channel, red_channel = cv.split(img)  # Split the image into separate channels
    blue_channel = cv.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)  # Apply lookup table to the red channel
    red_channel = cv.LUT(red_channel, increaseLookupTable).astype(np.uint8)  # Apply lookup table to the blue channel
    
    frost = cv.merge((blue_channel, green_channel, red_channel))  # Merge the modified channels into an image
    
    return frost  # Return the resulting frost effect image

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
    scratched_photo = np.where(bi_scratches == [0, 0, 0], bwYlwTint, bi_scratches)

    return scratched_photo


def main():
  base_img = cv.imread("./images/stairs1.jpg")
  frosted = Frosty(base_img)
  toasted = Toasty(base_img)
  vintage = VintageVibe(base_img)
  Result.singleWindow([base_img,frosted,toasted,vintage], dtype="s")

if __name__ == '__main__':
   main()