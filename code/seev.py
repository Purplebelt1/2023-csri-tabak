import cv2 as cv
import math
import numpy as np
import Result

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
    l,a,b = cv.split(im.astype('f'))
    chroma = np.sqrt(np.add(np.square(a), np.square(b)))
    hueRight = np.where(chroma == 0, 0, np.degrees(np.arcsin(np.divide(b, chroma))))
    hueLeft = np.where(chroma == 0, 0, np.add(180,np.degrees(np.arcsin(np.divide(b, chroma)))))
    hue = np.where(a > 0, hueRight, hueLeft)
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
    b = (np.sin(np.radians(h)) * c).astype(np.float32)
    aRight = (np.sqrt(np.subtract(np.square(c), np.square(b)))).astype(np.float32)
    aLeft = np.multiply(-1, aRight)
    a = np.where(np.logical_and(90 > h, h > -90), aRight, aLeft)
    newim = cv.merge((l,a,b))
    return newim



def main():
    im = cv.imread('./images/moss.jpg')
    lab = cv.cvtColor(im, cv.COLOR_BGR2LAB)
    test = newlab2lch(lab)
    print("here")
    l,c,h = cv.split(test.astype('f'))
    #h[:] = 180
    merged = cv.merge((l,c,h))
    test2 = newlch2lab(merged)
    bgr = cv.cvtColor(test2, cv.COLOR_LAB2BGR)
    Result.multiWindow([im, bgr])

if __name__ == '__main__':
    main()