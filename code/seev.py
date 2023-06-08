import cv2 as cv
import math
import numpy as np
import Result

#def lab2lch(img):
#    im = img.copy()
#    for i in range(im.shape[0]):
#        for j in range(im.shape[1]):
#            chroma = math.sqrt((im[i,j,1])**2 + (im[i,j,2])**2)
#            if chroma == 0:
#                hue = 0
#            else:
#                hue = math.degrees(math.asin(im[i,j,2] / chroma))
#            im[i,j,1] = chroma
#            im[i,j,2] = hue
#    return im
#    
#def newlab2lch(img):
#    im = img.copy()
#    l,a,b = cv.split(im.astype(np.float32))
#    l = np.multiply(l, (100/255))
#    a = np.subtract(a, 128)
#    b = np.subtract(b, 128)
#    chroma = np.sqrt(np.add(np.square(a), np.square(b)))
#    hueright = np.multiply((180 / math.pi), np.arctan(b,a))
#    hueleft = np.where(hueright == 0, 180, np.subtract(np.multiply(np.divide(hueright, np.abs(hueright)), 180), hueright))
#    hueneg = np.where(a < 0, hueleft, hueright)
#    hue = np.where(hueneg < 0, np.add(360,hueneg), hueneg)
#    newim = cv.merge((l, chroma, hue))
#    return newim
#
#
#def lch2lab(img):
#    im = img.copy()
#    for i in range(im.shape[0]):
#        for j in range(im.shape[1]):
#            if im[i,j,1] == 0:
#                a = 0
#                b = 0
#            else:
#                b = int(math.sin(math.radians(im[i,j,2])) * im[i,j,1])
#                a = int(math.sqrt(((im[i,j,1]) ** 2) - ((b) ** 2)))
#            im[i,j,1] = a
#            im[i,j,2] = b
#    return im
#
#def newlch2lab(img):
#    im = img.copy()
#    l,c,h = cv.split(im.astype('f'))
#    l = l.astype(np.float32)
#    b = np.multiply(np.sin(np.multiply((math.pi / 180), h)), c).astype(np.float32)
#    a = np.sqrt(np.subtract(np.square(c), np.square(b)))
#    #a = np.multiply(np.cos(np.multiply((math.pi / 180), h)), c).astype(np.float32)
#    #b = (np.sin(np.radians(h)) * c).astype(np.float32)
#    #aRight = (np.sqrt(np.subtract(np.square(c), np.square(b)))).astype(np.float32)
#    #aLeft = np.multiply(-1, aRight)
#    #a = np.where(np.logical_and(90 > h, h > -90), aRight, aLeft)
#    newim = cv.merge((l,a,b))
#    return newim
#
#
#
#def main():
#    im = cv.imread('./images/moss.jpg')
#    lab = cv.cvtColor(im, cv.COLOR_BGR2LAB)
#    test = newlab2lch(lab)
#    print("here")
#    l,c,h = cv.split(test.astype('f'))
#    #h[:] = 270
#    merged = cv.merge((l,c,h))
#    test2 = newlch2lab(merged)
#    bgr = cv.cvtColor(test2, cv.COLOR_LAB2BGR)
#    Result.multiWindow([im, bgr])










#take 2

def hsv(im, hue = None, saturation = None, value = None):
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    if isinstance(hue, int) and hue != -1:
        while hue > 179:
            hue -= 180
        while hue < 0:
            hue += 180
        h[:] = hue
    if isinstance(saturation, int) and saturation != -1:
        while saturation > 255:
            saturation -= 256
        while saturation < 0:
            saturation += 256
        s[:] = saturation
    if isinstance(value, int) and value != -1:
        while value > 255:
            value -= 256
        while value < 0:
            value += 256
        v[:] = value
    new = cv.merge((h,s,v))
    bgr = cv.cvtColor(new, cv.COLOR_HSV2BGR)
    return bgr

def main():
    im = cv.imread('./images/moss.jpg')
    im2 = hsv(im, 33)
    Result.singleWindow([im2])



if __name__ == '__main__':
    main()