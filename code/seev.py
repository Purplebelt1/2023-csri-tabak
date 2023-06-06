import cv2 as cv
import math
import numpy as np
import Result

def trig(im):
    

def main():
    im = cv.imread('./images/moss.jpg')
    lab = cv.cvtColor(im, cv.COLOR_BGR2LAB)
    print(lab.shape)
    bgr = cv.cvtColor(lab, cv.COLOR_LAB2BGR)
    Result.singleWindow(bgr)

if __name__ == '__main__':
    main()