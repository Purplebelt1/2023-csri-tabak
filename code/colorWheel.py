import cv2 as cv
import numpy as np
import Result
import Filters
import Posterization



def monochromatic(img, hue):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    hue = hue % 180
    h,s,v = cv.split(hsv)
    new_hue = (np.ones(h.shape) * hue).astype('uint8')
    ret_im = cv.merge((new_hue,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im




def opposites(img, hue):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    hue = hue % 180
    opis = (hue + 90) % 180
    h,s,v = cv.split(hsv)
    hue_dst = np.where(h > hue, h - hue, hue - h)
    hue_alt = np.subtract(np.add(h, 180), hue)
    hue_true_dst = np.where(hue_dst <= hue_alt, hue_dst, hue_alt)
    opis_dst = np.where(h > opis, h - opis, opis - h)
    opis_alt = np.subtract(np.add(h, 180), opis)
    opis_true_dst = np.where(opis_dst <= opis_alt, opis_dst, opis_alt)
    new_hue = np.where(hue_true_dst <= opis_true_dst, hue, opis).astype('uint8')
    ret_im = cv.merge((new_hue,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def tertiary(img, hue):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    hue = abs(hue % 180)
    sec = (hue + 60) % 180
    ter = (hue + 120) % 180
    h,s,v = cv.split(hsv)
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
    ret_im = cv.merge((new_hue,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im
    

def split_complimentary(img, hue, go_to_nearest_hue = True):
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
        ret_im = cv.merge((new_hue,s,v))
    else:
        new_ter = np.where(h < 60, ter, 181)
        new_hue = np.where(np.logical_and((new_ter == 181), (h < 120)), hue, new_ter)
        new_sec = np.where(new_hue == 181, sec, new_hue).astype('uint8')
        ret_im = cv.merge((new_sec,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im


def split_complimentary_shadows(img, hue, lbound = 20, hbound = 80):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    hue = hue % 180
    bri = (hue + 105) % 180
    dar = (hue + 75) % 180
    low = np.percentile(v, lbound)
    high = np.percentile(v, hbound)
    new_dar = np.where(v < low, dar, 181)
    new_bri = np.where(v > high, bri, new_dar)
    new_hue = np.where(new_bri == 181, hue, new_bri).astype('uint8')
    ret_im = cv.merge((new_hue, s, v))
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

def analogous_shadows(img, hue, lbound = 20, hbound = 80):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    hue = hue % 180
    bri = (hue + 15) % 180
    dar = (hue - 15) % 180
    low = np.percentile(v, lbound)
    high = np.percentile(v, hbound)
    new_dar = np.where(v < low, dar, 181)
    new_bri = np.where(v > high, bri, new_dar)
    new_hue = np.where(new_bri == 181, hue, new_bri).astype('uint8')
    ret_im = cv.merge((new_hue, s, v))
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

def tetradic_shadows(img, hue, lbound = 25, mbound = 50, hbound = 75):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    hue = hue % 180
    sec = (hue + 45) % 180
    ter = (hue + 90) % 180
    qua = (hue + 135) % 180
    low = np.percentile(v, lbound)
    mid = np.percentile(v, mbound)
    high = np.percentile(v, hbound)
    new_hue = np.where(v < high, hue, qua)
    new_ter = np.where(v < mid, ter, new_hue)
    new_sec = np.where(v < low, sec, new_ter).astype('uint8')
    ret_im = cv.merge((new_sec,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im    

def value_split(img, split, round_down = True):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    point = 255 // (split - 1)
    print(v)
    if round_down:
        new_val = np.multiply(np.floor(np.divide(v, point)), point).astype('uint8')
    else:
        new_val = np.multiply(np.minimum((split - 1),np.ceil(np.divide(v, point))), point).astype('uint8')
    print(new_val)
    ret_im = cv.merge((h,s,new_val))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im    

def complementary_shadows(img, hue, value_cutoff = -1):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    hue = hue % 180
    opis = (hue + 90) % 180
    if value_cutoff != -1:
        median = value_cutoff
    else:
        median = np.median(v)
    new_hue = np.where(v < median, opis, hue).astype('uint8')
    ret_im = cv.merge((new_hue, s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def swap(img, val = 250, sat = 5):
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    darken = np.where(np.logical_and(v > val, s < sat), 0, v).astype('uint8')
    ret_im = cv.merge((h,s,darken))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def hue_shift(img, hue = 90):
    im = img.copy()
    hue = hue % 180
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    #print(h[2200][3000])
    #new_hue = np.mod(np.add(h, hue), 180).astype('uint8')
    #test = np.add(h, hue).astype('uint8')
    alt_hue = 180 - hue
    new_hue = np.where(alt_hue <= h, h - alt_hue, h + hue).astype('uint8')
    #print(new_hue[2200][3000])
    ret_im = cv.merge((new_hue,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def saturation_drain(img, percent_sat):
    im = img.copy()
    if percent_sat > 100:
        percent_sat = 100
    elif percent_sat < 0:
        percent_sat = 0
    percent_sat = percent_sat / 100
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    new_sat = (s * percent_sat).astype('uint8')
    ret_im = cv.merge((h,new_sat,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def set_saturation(img, sat):
    im = img.copy()
    sat = sat % 256
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    new_sat = (np.ones(s.shape) * sat).astype('uint8')
    ret_im = cv.merge((h,new_sat,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def set_value(img, val):
    im = img.copy()
    val = val % 256
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    new_val = (np.ones(v.shape) * val).astype('uint8')
    ret_im = cv.merge((h,s,new_val))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im


def main():
    #3306 is cute
    #im = cv.imread('images/puppies/IMG_3304.jpeg')#('images/puppies/IMG_2876.jpeg')
    #im = cv.imread('images/italy/IMG_5845.jpeg')
    #im = cv.imread('images/skyline.jpg')
    #im = cv.imread('images/italy/IMG_5794.jpeg')
    #im = cv.imread('images/other_stuff/IMG_2224.jpeg')#4056.jpeg')#2541.jpeg')
    #im = cv.imread('images/puppies/IMG_3306.jpeg')#329.jpeg')
    #org = monochromatic(im, 70)
    #new_im = analogous(im, 75)
    #im2 = shadows(im, 70)
    #cv.imwrite('analogous.jpg', new_im)
    #cv.imwrite('shadows.jpg', im2)
    #im2 = value_split(im, 3)
    #im = cv.imread('images/other_stuff/IMG_2107.jpeg')#3611.jpeg')
    #im = cv.imread('images/new/IMG_3691.jpeg')
    #im = cv.imread('images/new/IMG_3693.jpeg')
    #im = cv.imread('images/new/IMG_3728.jpeg')
    im = cv.imread('images/new/IMG_3731.jpeg')

    #im2 = split_complimentary_shadows(im, 90, 20, 80)
    #im3 = analogous_shadows(im, 70)
    im2 = split_complimentary_shadows(im, 134, 20, 80)
    #im2 = tetradic(im, 134)
    im3 = tetradic_shadows(im, 179, 25, 50, 75)
    #im2 = monochromatic(im, 0)

    #im2 = set_saturation(im, 55)
    #im2 = set_value(im2, 255)
    
    #im = cv.imread('images/italy/308d245f-3b40-46aa-adf7-33c0250f4470.jpeg')

    #im2 = hue_shift(im, 80)
    
    #im2 = split_complimentary_shadows(im, 100, 20, 60)
    
    cv.imwrite('undecided.jpg', im2)
    cv.imwrite('undecided2.jpg', im3)


   
    Result.singleWindow([im2, im3], imDim = im.shape[:2])#, dtype= 's')
    #Result.singleWindow(im)

if __name__ == '__main__':
    main()