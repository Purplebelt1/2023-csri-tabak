from PIL import Image, ImageEnhance
import cv2 as cv
import numpy as np
from scipy.interpolate import UnivariateSpline

def LookupTable(x, y):
  spline = UnivariateSpline(x, y)
  return spline(range(256))

#frost effect
def frosty(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel = cv.split(img)
    red_channel = cv.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
    blue_channel = cv.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
    win= cv.merge((blue_channel, green_channel, red_channel))
    return win

base_img = cv.imread("./images/stairs1.jpg")
frosted = frosty(base_img)


cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL)
cv.namedWindow("Resized Window2", cv.WINDOW_NORMAL)
cv.resizeWindow("Resized_Window", 800, 800)
cv.resizeWindow("Resized Window2", 800, 800)
# Displaying the image
cv.imshow("Resized_Window", frosted)
cv.imshow("Resized Window2", base_img)

cv.waitKey(0)
cv.destroyAllWindows()