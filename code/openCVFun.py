import cv2 as cv
import Result
import numpy as np
image = np.zeros((1000,1000,3), np.uint8)
font = cv.FONT_HERSHEY_SIMPLEX
org = (100, 500)
fontScale = 3
color = (255, 0, 255)
thickness = 10
image = cv.putText(image, 'J Dawg!', org, font, 
                   fontScale, color, thickness, cv.LINE_AA)
Result.singleWindow(image)