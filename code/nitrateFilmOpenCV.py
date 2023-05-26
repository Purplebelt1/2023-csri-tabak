import cv2 as cv
import numpy as np
import Result

def filmFilter(img):
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
    base_img = cv.imread("./images/barn_house.jpg")

    scratched = filmFilter(base_img)

    Result.singleWindow(scratched)

if __name__ == '__main__':
    main()