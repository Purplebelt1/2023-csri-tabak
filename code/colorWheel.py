import cv2 as cv
import numpy as np
import Result

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
    

def splitComplimentary(img, hue, go_to_nearest_hue = True):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    hue = hue % 180
    sec = (hue + 105) % 180
    ter = (hue + 75) % 180
    h,s,v = cv.split(hsv)
    if go_to_nearest_hue:
        hue_dst = np.where(h > hue, h - hue, hue - h)
        hue_alt = np.subtract(np.add(h, 180), hue)
        hue_true_dst = np.where(hue_dst <= hue_alt, hue_dst, hue_alt)
        sec_dst = np.where(h > sec, h - sec, sec - h)
        sec_alt = np.subtract(np.add(h, 180), sec)
        sec_true_dst = np.where(sec_dst <= sec_alt, sec_dst, sec_alt)
        ter_dst = np.where(h > ter, h - ter, ter - h)
        ter_alt = np.subtract(np.add(h, 180), ter)
        ter_true_dst = np.where(ter_dst <= ter_alt, ter_dst, ter_alt)
        hue_hue = np.where(np.logical_and((hue_true_dst <= sec_true_dst), (hue_true_dst <= ter_true_dst)), hue, -1)
        hue_sec = np.where(np.logical_and(hue_hue == -1, (sec_true_dst <= ter_true_dst)), sec, hue_hue)
        new_hue = np.where(hue_sec == -1, ter, hue_sec).astype('uint8')
        ret_im = cv.merge((new_hue))
    else:
        new_ter = np.where(h < 60, ter, 181)
        new_hue = np.where(np.logical_and((new_ter == 181), (h < 120)), hue, new_ter)
        new_sec = np.where(new_hue == 181, sec, new_hue).astype('uint8')
        ret_im = cv.merge((new_sec,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def analogous(img, hue):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    hue = hue % 180
    sec = (hue + 15) % 180
    ter = (hue - 15) % 180
    new_ter = np.where(h < 60, ter, 181)
    new_hue = np.where(np.logical_and((new_ter == 181), (h < 120)), hue, new_ter)
    new_sec = np.where(new_hue == 181, sec, new_hue).astype('uint8')
    ret_im = cv.merge((new_sec, s, v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def tetradic(img, hue):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    hue = hue % 180
    sec = (hue + 45) % 180
    ter = (hue + 90) % 180
    qua = (hue + 135) % 180
    new_hue = np.where(h < 45, hue, 181)
    new_sec = np.where(np.logical_and(h < 90, new_hue == 181), sec, new_hue)
    new_ter = np.where(np.logical_and(h < 135, new_sec == 181), ter, new_sec)
    new_qua = np.where(new_ter == 181, qua, new_ter).astype('uint8')
    ret_im = cv.merge((new_qua,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im    


def main():
    im = cv.imread('images/warm_sun.jpg')
    chg01 = monochromatic(im, 45)
    chg02 = monochromatic(im, 90)
    chg03 = monochromatic(im, 135)
    chg04 = monochromatic(im, 180)
    chg = opposites(im, 160)
    chg2 = tertiary(im, 0)
    chg3 = splitComplimentary(im, 90)
    chg4 = analogous(im, 160)
    chg5 = tetradic(im, 160)

    Result.singleWindow([chg3], imDim = im.shape[:2])

if __name__ == '__main__':
    main() 