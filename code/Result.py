import cv2 as cv
import numpy as np
import math

def singleWindow(pics, height=800, width=800, imDim=(800,800), name="default", dtype="h"):
    imDim = imDim[::-1]
    cv.namedWindow(name, cv.WINDOW_NORMAL)
    cv.resizeWindow(name, height, width)
    if type(pics) == list:
        if dtype == "h":
            cv.imshow(name, np.hstack(pics))
        elif dtype == "v":
            cv.imshow(name, np.vstack(pics))
        elif dtype == "s":
            for i in range(len(pics)):
                pics[i] = cv.resize(pics[i],imDim,interpolation = cv.INTER_AREA)
            num_pics = len(pics)
            pics_sqrt = math.sqrt(num_pics)
            if int(pics_sqrt) == pics_sqrt:
                pics_sqrt = int(pics_sqrt)
                photo_square_arr = []
                for i in range(pics_sqrt):
                    photo_square_arr.append(np.hstack(pics[i*pics_sqrt:i*pics_sqrt+pics_sqrt]))
                photo_square = np.vstack(photo_square_arr)
                cv.imshow(name, photo_square)

            else:
                ValueError("Must use a perfect square number of pictures!")
    else:
        cv.imshow(name, pics)
    cv.waitKey(0)
    cv.destroyAllWindows()

def multiWindow(pics, height=800, width=800, name="default"):
    count = 0
    for i in pics:
        cv.namedWindow(name + str(count), cv.WINDOW_NORMAL)
        cv.resizeWindow(name + str(count), height, width)
        cv.imshow(name + str(count), i)
        count += 1
    cv.waitKey(0)
    cv.destroyAllWindows()

def main():
    img1 = cv.imread("./images/barn_house.jpg")
    img2 = cv.imread("./images/fire.jpg")
    img3 = cv.imread("./images/wolf.jpg")
    img4 = cv.imread("./images/moss.jpg")
    singleWindow([img1,img1,img1,img1], dtype="s")


if __name__ == "__main__":
    main()