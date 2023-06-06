import cv2 as cv
import math
import numpy as np
import Result

def trig(im):
    

def main():
    im = cv.imread('./images/moss.jpg')
    hcl = cv.cvtColor(im, cv.COLOR_BGR2LAB)
    Result.singleWindow(hcl)

if __name__ == '__main__':
    main()