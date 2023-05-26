import cv2 as cv
import numpy as np

def singleWindow(pics, height=800, width=800, name="default"):
    cv.namedWindow(name, cv.WINDOW_NORMAL)
    cv.resizeWindow(name, height, width)
    if type(pics) == list:
        cv.imshow(name, np.hstack(pics))
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
