import cv2 as cv
import numpy as np

img = cv.imread("./images/barn_house.jpg")

blurred_img = cv.GaussianBlur(img, (31, 31), 0)

bwImg = cv.cvtColor(blurred_img, cv.COLOR_BGR2GRAY)
bwImg = cv.cvtColor(bwImg, cv.COLOR_GRAY2BGR)

yellow_layer = np.full(bwImg.shape, (0,255,255), np.uint8)

bwYlwTint = cv.addWeighted(bwImg, 0.85, yellow_layer, 0.15, 0)

black_border_img = cv.copyMakeBorder(bwYlwTint, 2,2,2,2, cv.BORDER_CONSTANT, value=[0,0,0])

scratches = cv.imread("./images/dusty3.jpg")

borImgWdt = black_border_img.shape[0]
borImgHght = black_border_img.shape[1]

# Add speckles to film
resized_scratches = cv.resize(scratches, (borImgHght,borImgWdt))
th, bi_scratches = cv.threshold(resized_scratches, 150, 255, cv.THRESH_TOZERO);
scratched_photo = np.where(bi_scratches == [0,0,0],black_border_img, bi_scratches)

cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL)
cv.namedWindow("Lemme show you this!", cv.WINDOW_NORMAL)
cv.resizeWindow("Resized_Window", 300, 700)
cv.resizeWindow("Lemme show you this!", 800,800)
# Displaying the image
cv.imshow("Resized_Window", scratched_photo)
scritch = cv.imread("./images/scratch.png")
cv.imshow("Lemme show you this!",scritch)

cv.waitKey(0)
cv.destroyAllWindows()