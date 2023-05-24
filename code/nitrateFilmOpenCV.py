import cv2 as cv
import numpy as np

img = cv.imread("./images/barn_house.jpg")

grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

(thresh, bwImg) = cv.threshold(grayImg, 50, 255, cv.THRESH_BINARY)
 
#cv.imshow('Black white image', bwImg)

cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL)
  
# Using resizeWindow()
cv.resizeWindow("Resized_Window", 300, 700)

# Displaying the image
cv.imshow("Resized_Window", bwImg)

cv.waitKey(0)
cv.destroyAllWindows()