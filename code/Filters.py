from PIL import Image, ImageEnhance
import math
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

def Halloween(img, dark=3):
    return Gamma(Toasty(img), dark)

def Gamma(img, gamma):
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    res = cv.LUT(img, lookUpTable)
    return res

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

def SaturateByCurve(img, saturationCoeff):

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # If you want to adjust curve adjust the expoenents
    saturationLUT = LookupTable([0,85,170,256],[round(saturationCoeff * 255), round((saturationCoeff ** .5) * 170 + 85),round((saturationCoeff ** .75) * 80 + 170), 256])

    hue, saturation, value = cv.split(hsv)  # Split the image into separate channels

    saturation = cv.LUT(saturation, saturationLUT).astype(np.uint8)

    output = cv.merge((hue, saturation, value))

    output = cv.cvtColor(output, cv.COLOR_HSV2BGR)

    return output

def main():
  base_img = cv.imread("./images/barn_house.jpg")
  gamma = Gamma(base_img, 2)
  frosted = Frosty(base_img)
  toasted = Toasty(base_img)
  vintage = VintageVibe(base_img)
  saturate1 = SaturateByCurve(base_img, 0.1)
  saturate2 = SaturateByCurve(base_img, 0.2)
  saturate3 = SaturateByCurve(base_img, 0.3)
  #print(base_img.shape)
  dim = base_img.shape[:2]
  Result.singleWindow([saturate1, saturate2, saturate3, base_img], dtype = "s", imDim = dim)

if __name__ == '__main__':
   main()