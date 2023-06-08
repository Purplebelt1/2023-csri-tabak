from PIL import Image
import colorsys
import numpy as np
import math
import cv2 as cv

def lab2lch(img):
    im = img.copy()
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            chroma = math.sqrt((im[i,j,1])**2 + (im[i,j,2])**2)
            if chroma == 0:
                hue = 0
            else:
                hue = math.degrees(math.asin(im[i,j,2] / chroma))
            im[i,j,1] = chroma
            im[i,j,2] = hue
    return im
    
def newlab2lch(img):
    im = img.copy()
    l,a,b = cv.split(im.astype(np.float32))
    chroma = np.sqrt(np.add(np.square(a), np.square(b)))
    #hueRight = np.where(chroma == 0, 0, np.degrees(np.arcsin(np.divide(b, chroma))))
    #hueLeft = np.where(chroma == 0, 0, np.add(180,np.degrees(np.arcsin(np.divide(b, chroma)))))
    #hueRight = np.where(a == 0, np.multiply(90, np.divide(b, np.abs(b))), np.degrees(np.arctan(np.divide(b,a))))
    #check1 = np.multiply((180 / math.pi),np.arctan(np.divide(b,a)))
    #heck2 = np.subtract(360,np.multiply((180 / math.pi),np.arctan(np.divide(np.multiply(b, -1),a))))
    #check3 = np.subtract(180, np.multiply((180 / math.pi),np.arctan(np.divide(b,np.multiply(a, -1)))))
    #check4 = np.add(180, np.multiply((180 / math.pi),np.arctan(np.divide(np.multiply(b, -1),np.multiply(a, -1)))))
    #hueUpperRight = np.where(a == 0, 90, check1)
    #hueBottomRight = np.where(a == 0, 270, check2)
    #hueUpperLeft = np.where(a == 0, 90, check3)
    #hueBottomLeft = np.where(a == 0, 270, check4)
    #hueRight = np.where(b > 0, hueUpperRight, hueBottomRight)
    #hueLeft = np.where(b > 0, hueUpperLeft, hueBottomLeft)
    #hue = np.where(a > 0, hueRight, hueLeft)
    #print(np.any(hueUpperRight < 0))
    #hueAdjustUpperRight = np.where(hueUpperRight < 0, hueUpperRight + 360, hueUpperRight)
    #hueLeft = np.where(hueAdjustUpperRight > 180, np.subtract(540, hueAdjustUpperRight), np.subtract(180, hueAdjustUpperRight))
    #hueLeft = np.subtract(180, hueAdjustUpperRight)
    #hueLowerRight = np.where(a == 0, )
    #hueLeft = np.where(hueRight > 0, 180 - hueRight, -180 - hueRight)
    #hue = np.where(a < 0, hueAdjustUpperRight, hueLeft)
    hueright = np.degrees(np.arctan(b,a))
    hueleft = np.subtract(np.multiply(np.divide(hueright, np.abs(hueright)), 180), hueright)
    hue = np.where(a < 0, hueleft, hueright)
    print(l)
    #print(hue)
    #if chroma == 0:
    #    hue = 0
    #else:
    #    hue = math.degrees(math.asin(im[::2] / chroma))
    #im[::1] = chroma
    #im[::2] = hue
    newim = cv.merge((l, chroma, hue))
    return newim


def lch2lab(img):
    im = img.copy()
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i,j,1] == 0:
                a = 0
                b = 0
            else:
                b = int(math.sin(math.radians(im[i,j,2])) * im[i,j,1])
                a = int(math.sqrt(((im[i,j,1]) ** 2) - ((b) ** 2)))
            im[i,j,1] = a
            im[i,j,2] = b
    return im

def newlch2lab(img):
    im = img.copy()
    l,c,h = cv.split(im.astype('f'))
    l = l.astype(np.float32)
    b = np.multiply(np.sin(np.multiply((math.pi / 180), h)), c).astype(np.float32)
    a = np.multiply(np.cos(np.multiply((math.pi / 180), h)), c).astype(np.float32)
    #b = (np.sin(np.radians(h)) * c).astype(np.float32)
    #aRight = (np.sqrt(np.subtract(np.square(c), np.square(b)))).astype(np.float32)
    #aLeft = np.multiply(-1, aRight)
    #a = np.where(np.logical_and(90 > h, h > -90), aRight, aLeft)
    newim = cv.merge((l,a,b))
    return newim



def main():
    im = Image. open('./images/moss.jpg')
    rgb = im.convert('RGB')
    arr = np.asarray(rgb)
    #test = newlab2lch(lab)
    #print("here")
    #l,c,h = cv.split(test.astype('f'))
    #h[:] = 0
    #merged = cv.merge((l,c,h))
    #test2 = newlch2lab(merged)
    #bgr = cv.cvtColor(test2, cv.COLOR_LAB2BGR)
    #Result.multiWindow([im, bgr])


if __name__ == '__main__':
    main()