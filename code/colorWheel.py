import cv2 as cv
import numpy as np
import Result
import math

def monochromatic(img, hue):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    hue = hue % 180
    h,s,v = cv.split(hsv)
    newhue = (np.ones(h.shape) * hue).astype('uint8')
    retim = cv.merge((newhue,s,v))
    retim = cv.cvtColor(retim, cv.COLOR_HSV2BGR)
    return retim




def opposites(img, hue):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    hue = hue % 180
    opis = (hue + 90) % 180
    h,s,v = cv.split(hsv)
    huedst = np.where(h > hue, h - hue, hue - h)
    huealt = np.subtract(np.add(h, 180), hue)
    hueTruedst = np.where(huedst <= huealt, huedst, huealt)
    opisdst = np.where(h > opis, h - opis, opis - h)
    opisalt = np.subtract(np.add(h, 180), opis)
    opisTruedst = np.where(opisdst <= opisalt, opisdst, opisalt)
    newhue = np.where(hueTruedst <= opisTruedst, hue, opis).astype('uint8')
    retim = cv.merge((newhue,s,v))
    retim = cv.cvtColor(retim, cv.COLOR_HSV2BGR)
    return retim

def tertiary(img, hue):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    hue = abs(hue % 180)
    sec = (hue + 60) % 180
    ter = (hue + 120) % 180
    h,s,v = cv.split(hsv)
    huedst = np.where(h > hue, h - hue, hue - h)
    huealt = np.subtract(np.add(h, 180), hue)
    hueTruedst = np.where(huedst <= huealt, huedst, huealt)
    secdst = np.where(h > sec, h - sec, sec - h)
    secalt = np.subtract(np.add(h, 180), sec)
    secTruedst = np.where(secdst <= secalt, secdst, secalt)
    terdst = np.where(h > ter, h - ter, ter - h)
    teralt = np.subtract(np.add(h, 180), ter)
    terTruedst = np.where(terdst <= teralt, terdst, teralt)
    huehue = np.where(np.logical_and((hueTruedst <= secTruedst), (hueTruedst <= terTruedst)), hue, -1)
    huesec = np.where(np.logical_and(huehue == -1, (secTruedst <= terTruedst)), sec, huehue)
    newhue = np.where(huesec == -1, ter, huesec).astype('uint8')
    retim = cv.merge((newhue,s,v))
    retim = cv.cvtColor(retim, cv.COLOR_HSV2BGR)
    return retim
    

def splitComplimentary(img, hue):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    hue = hue % 180
    sec = (hue + 105) % 180
    ter = (hue + 75) % 180
    h,s,v = cv.split(hsv)
    huedst = np.where(h > hue, h - hue, hue - h)
    huealt = np.subtract(np.add(h, 180), hue)
    hueTruedst = np.where(huedst <= huealt, huedst, huealt)
    secdst = np.where(h > sec, h - sec, sec - h)
    secalt = np.subtract(np.add(h, 180), sec)
    secTruedst = np.where(secdst <= secalt, secdst, secalt)
    terdst = np.where(h > ter, h - ter, ter - h)
    teralt = np.subtract(np.add(h, 180), ter)
    terTruedst = np.where(terdst <= teralt, terdst, teralt)
    huehue = np.where(np.logical_and((hueTruedst <= secTruedst), (hueTruedst <= terTruedst)), hue, -1)
    huesec = np.where(np.logical_and(huehue == -1, (secTruedst <= terTruedst)), sec, huehue)
    newhue = np.where(huesec == -1, ter, huesec).astype('uint8')
    retim = cv.merge((newhue,s,v))
    retim = cv.cvtColor(retim, cv.COLOR_HSV2BGR)
    return retim



def main():
    im = cv.imread('images/calm_water.JPG')
    chg01 = monochromatic(im, 45)
    chg02 = monochromatic(im, 90)
    chg03 = monochromatic(im, 135)
    chg04 = monochromatic(im, 180)
    chg = opposites(im, 160)
    chg2 = tertiary(im, 0)
    chg3 = splitComplimentary(im, 0)

    Result.singleWindow([chg], imDim = im.shape[:2])

if __name__ == '__main__':
    main() 