import cv2 as cv
import numpy as np

img = cv.imread("./images/barn_house.jpg")


blurred_img = cv.GaussianBlur(img, (31, 31), 0)


mean = 0
stddev = 180
noise = np.zeros(img.shape, np.uint8)
cv.randn(noise, mean, stddev)

# Add noise to image



noisy_img = cv.add(blurred_img, noise)

bwImg = cv.cvtColor(noisy_img, cv.COLOR_BGR2GRAY)
bwImg = cv.cvtColor(bwImg, cv.COLOR_GRAY2BGR)


bwImgWdt = bwImg.shape[0]
bwImgHght = bwImg.shape[1]



yellow_layer = np.full(bwImg.shape, (0,255,255), np.uint8)

bwYlwTint = cv.addWeighted(bwImg, 0.85, yellow_layer, 0.15, 0)

BLACK = [0,0,0]
black_border_img = cv.copyMakeBorder(bwYlwTint, 2,2,2,2, cv.BORDER_CONSTANT, value=BLACK)

#mask = np.zeros(img.shape)
#mask = np.pad(mask, pad_width=2, mode='constant', constant_values=[1,1,1])

#print(mask)

#blurred_img = cv.GaussianBlur(black_border_img, (21, 21), 0)

#output = np.where(mask==[1,1,1],blurred_img,black_border_img)

#(thresh, bwImg) = cv.threshold(grayImg, 100, 255, cv.THRESH_BINARY)
 
#cv.imshow('Black white image', bwImg)

cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL)
  
# Using resizeWindow()
cv.resizeWindow("Resized_Window", 300, 700)

# Displaying the image

print("Heyo")
cv.imshow("Resized_Window", black_border_img)

cv.waitKey(0)
cv.destroyAllWindows()