import cv2 as cv
import numpy as np
import Result

def monochromatic(img, hue):
    #changes all hues in img to to hue and returns new image
    #copies img and converts it to hsv
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    #prevents hue from being outside applicable range
    hue = hue % 180
    #splits image into hue, saturation, and value channels
    h,s,v = cv.split(hsv)
    #makes new hue channel
    new_hue = (np.ones(h.shape) * hue).astype('uint8')
    #merges new hue channel with other channels and converts back to bgr
    ret_im = cv.merge((new_hue,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im




def opposites(img, hue):
    #changes all hues in img to to hue or its complementary color and returns new image
    #copies img and converts it to hsv
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    #prevents hue from being outside applicable range and calculates opisite hue
    hue = hue % 180
    opis = (hue + 90) % 180
    #splits image into hue, saturation, and value channels
    h,s,v = cv.split(hsv)
    #makes new hue channel where hues are changed to hue or opis depending
    #on which is closer in value
    hue_dst = np.where(h > hue, h - hue, hue - h)
    hue_alt = np.subtract(np.add(h, 180), hue)
    hue_true_dst = np.where(hue_dst <= hue_alt, hue_dst, hue_alt)
    opis_dst = np.where(h > opis, h - opis, opis - h)
    opis_alt = np.subtract(np.add(h, 180), opis)
    opis_true_dst = np.where(opis_dst <= opis_alt, opis_dst, opis_alt)
    new_hue = np.where(hue_true_dst <= opis_true_dst, hue, opis).astype('uint8')
    #merges new hue channel with other channels and converts back to bgr
    ret_im = cv.merge((new_hue,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def tertiary(img, hue):
    #changes all hues in img to to hue or its tertiary colors and returns new image
    #copies img and converts it to hsv
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    #prevents hue from being outside applicable range and calculates tertiary hues
    hue = hue % 180
    sec = (hue + 60) % 180
    ter = (hue + 120) % 180
    #splits image into hue, saturation, and value channels
    h,s,v = cv.split(hsv)
    #makes new hue channel where hues are changed to hue, sec, or ter depending
    #on which is closer in value
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
    #merges new hue channel with other channels and converts back to bgr
    ret_im = cv.merge((new_hue,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im
    

def split_complimentary(img, hue, go_to_nearest_hue = True):
    #changes all hues in img to to hue or its split complimentary colors and returns new image
    #go_to_nearest_hue determines whether hue go to the nearest applicable hue
    #or whether a set range of hue are changed regardless of distance 
    #copies img and converts it to hsv
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    #prevents hue from being outside applicable range and calculates split complimentary hues
    hue = hue % 180
    sec = (hue + 105) % 180
    ter = (hue + 75) % 180
    #splits image into hue, saturation, and value channels
    h,s,v = cv.split(hsv)
    #makes new hue channel where hues are changed to hue, sec, or ter depending
    #on which is closer in value if go_to_nearest is True
    #otherwise hues in seat ranges are changed to hue, sec, or der regardless of distance
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
    else:
        new_ter = np.where(h < 60, ter, 181)
        new_sec = np.where(np.logical_and((new_ter == 181), (h < 120)), hue, new_ter)
        new_hue = np.where(new_sec == 181, sec, new_sec).astype('uint8')
    #merges new hue channel with other channels and converts back to bgr
    ret_im = cv.merge((new_hue,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im


def split_complimentary_shadows(img, hue, lbound = 20, hbound = 80):
    #changes all hues in img to to hue or its split complimentary colors and returns new image
    #lbound and hbound determine the value percentiles that act as boundaries between hues
    #copies img and converts it to hsv
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    #splits image into hue, saturation, and value channels
    h,s,v = cv.split(hsv)
    #prevents hue from being outside applicable range and calculates split complimentary hues
    hue = hue % 180
    bri = (hue + 105) % 180
    dar = (hue + 75) % 180
    #finds value matching the percentiles of lbound and hbound
    low = np.percentile(v, lbound)
    high = np.percentile(v, hbound)
    #makes new hue channel where hues are changed to hue, bri, or dar depending
    #on the values at the location of the hue
    new_dar = np.where(v < low, dar, 181)
    new_bri = np.where(v > high, bri, new_dar)
    new_hue = np.where(new_bri == 181, hue, new_bri).astype('uint8')
    #merges new hue channel with other channels and converts back to bgr
    ret_im = cv.merge((new_hue, s, v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im


def analogous(img, hue):
    #changes all hues in img to to hue or its analagous colors and returns new image
    #copies img and converts it to hsv
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    #splits image into hue, saturation, and value channels
    h,s,v = cv.split(hsv)
    #prevents hue from being outside applicable range and calculates analagous hues
    hue = hue % 180
    sec = (hue + 15) % 180
    ter = (hue - 15) % 180
    #makes new hue channel where hues are changed to hue, sec, or ter depending
    #on which is closer in value
    new_ter = np.where(h < 60, ter, 181)
    new_hue = np.where(np.logical_and((new_ter == 181), (h < 120)), hue, new_ter)
    new_sec = np.where(new_hue == 181, sec, new_hue).astype('uint8')
    #merges new hue channel with other channels and converts back to bgr
    ret_im = cv.merge((new_sec, s, v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def analogous_shadows(img, hue, lbound = 20, hbound = 80):
    #changes all hues in img to to hue or its analagous colors and returns new image
    #lbound and hbound determine the value percentiles that act as boundaries between hues
    #copies img and converts it to hsv
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    #splits image into hue, saturation, and value channels
    h,s,v = cv.split(hsv)
    #prevents hue from being outside applicable range and calculates analagous hues
    hue = hue % 180
    bri = (hue + 15) % 180
    dar = (hue - 15) % 180
    #finds value matching the percentiles of lbound and hbound
    low = np.percentile(v, lbound)
    high = np.percentile(v, hbound)
    #makes new hue channel where hues are changed to hue, bri, or dar depending
    #on the values at the location of the hue
    new_dar = np.where(v < low, dar, 181)
    new_bri = np.where(v > high, bri, new_dar)
    new_hue = np.where(new_bri == 181, hue, new_bri).astype('uint8')
    #merges new hue channel with other channels and converts back to bgr
    ret_im = cv.merge((new_hue, s, v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im


def tetradic(img, hue):
    #changes all hues in img to to hue or its tetradic colors and returns new image
    #copies img, converts it to hsv, and splits the channels
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    #prevents hue from being outside applicable range and calculates tetradic hue
    hue = hue % 180
    sec = (hue + 45) % 180
    ter = (hue + 90) % 180
    qua = (hue + 135) % 180
    #makes new hue channel where hues are changed to hue, sec, ter, or qua depending
    #on which is closer in value
    new_hue = np.where(h < 45, hue, 181)
    new_sec = np.where(np.logical_and(h < 90, new_hue == 181), sec, new_hue)
    new_ter = np.where(np.logical_and(h < 135, new_sec == 181), ter, new_sec)
    new_qua = np.where(new_ter == 181, qua, new_ter).astype('uint8')
    #merges new hue channel with other channels and converts back to bgr
    ret_im = cv.merge((new_qua,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im    

def tetradic_shadows(img, hue, lbound = 25, mbound = 50, hbound = 75):
    #changes all hues in img to to hue or its tetradic colors and returns new image
    #lbound, mbound, and hbound determine the value percentiles that act
    #as boundaries between hues
    #copies img, converts it to hsv, and splits the channels
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    #prevents hue from being outside applicable range and calculates tetradic hue
    hue = hue % 180
    sec = (hue + 45) % 180
    ter = (hue + 90) % 180
    qua = (hue + 135) % 180
    #finds value matching the percentiles of lbound, mbound, and hbound
    low = np.percentile(v, lbound)
    mid = np.percentile(v, mbound)
    high = np.percentile(v, hbound)
    #makes new hue channel where hues are changed to hue, sec, ter, or qua depending
    #on the values at the location of the hue
    new_hue = np.where(v < high, hue, qua)
    new_ter = np.where(v < mid, ter, new_hue)
    new_sec = np.where(v < low, sec, new_ter).astype('uint8')
    #merges new hue channel with other channels and converts back to bgr
    ret_im = cv.merge((new_sec,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im    

def value_split(img, split, round_down = True):
    #limits the number of possible values in img based on split and returns new image
    #round_down determines whether the values will be rounded down to the nearest
    #applicable value or rounded up
    #copies img, converts it to hsv, and splits the channels
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    #determines a divisor to use for spliting values
    point = 255 // (split - 1)
    #creates new value channel by floor dividing by divsor and multipling by divisor
    if round_down:
        new_val = np.multiply(np.floor(np.divide(v, point)), point).astype('uint8')
    else:
        new_val = np.multiply(np.minimum((split - 1),np.ceil(np.divide(v, point))), point).astype('uint8')
    #merges new value channel with other channels and converts back to bgr
    ret_im = cv.merge((h,s,new_val))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im    

def complementary_shadows(img, hue, mbound = 50):
    #changes all hues in img to to hue or its complementary color and returns new image
    #mbound determine the value percentile that act as a boundary between hues
    #copies img, converts it to hsv, and splits the channels
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    #prevents hue from being outside applicable range and calculates complementary hue
    hue = hue % 180
    opis = (hue + 90) % 180
    #finds value matching the percentile of mbound
    mid = np.percentile(v, mbound)
    #makes new hue channel where hues are changed to hue or opis depending
    #on the values at the location of the hue 
    new_hue = np.where(v < mid, opis, hue).astype('uint8')
    #merges new hue channel with other channels and converts back to bgr
    ret_im = cv.merge((new_hue, s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def hue_shift(img, hue = 90):
    #shifts all hues in img by hue and returns new image
    #creates copy of img, converts it hsv, and splits the channels
    im = img.copy()
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    #adjusts hue to be applicable range and
    hue = hue % 180
    #calculates new hue channel
    #when adding hue would result in a nonappliacble value
    #the hue values are subtracted from alt_hue instead for an applicable value
    alt_hue = 180 - hue
    new_hue = np.where(alt_hue <= h, h - alt_hue, h + hue).astype('uint8')
    #merges new hue channel with other channels and converts back to bgr
    ret_im = cv.merge((new_hue,s,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def saturation_drain(img, percent_sat):
    #lowers the saturation in img to the percentage percent_sat
    #of the original saturation and returns a new image
    #creates copy of img
    im = img.copy()
    #adjusts percent_sat to applicable range
    if percent_sat > 100:
        percent_sat = 100
    elif percent_sat < 0:
        percent_sat = 0
    percent_sat = percent_sat / 100
    #converts img copy to hsv and splits its channels
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    #makes new saturation channel
    new_sat = (s * percent_sat).astype('uint8')
    #merges new saturation channel with other channels and converts back to bgr
    ret_im = cv.merge((h,new_sat,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def set_saturation(img, sat):
    #changes all values in img to val and returns new image
    #copies img, converts it to hsv, and makes sure sat is within aplicable range
    im = img.copy()
    sat = sat % 256
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    #splits image into hue, saturation, and value channels
    h,s,v = cv.split(hsv)
    #makes new saturation channel
    new_sat = (np.ones(s.shape) * sat).astype('uint8')
    #merges new saturation channel with other channels and converts back to bgr
    ret_im = cv.merge((h,new_sat,v))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im

def set_value(img, val):
    #changes all values in img to val and returns new image
    #copies img, converts it to hsv, and makes sure val is within aplicable range
    im = img.copy()
    val = val % 256
    hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
    #splits image into hue, saturation, and value channels
    h,s,v = cv.split(hsv)
    #makes new value channel
    new_val = (np.ones(v.shape) * val).astype('uint8')
    #merges new value channel with other channels and converts back to bgr
    ret_im = cv.merge((h,s,new_val))
    ret_im = cv.cvtColor(ret_im, cv.COLOR_HSV2BGR)
    return ret_im


def main():
    im = cv.imread('images/justin/IMG_3731.jpeg')

    im2 = split_complimentary_shadows(im, 134, 20, 80)
    im3 = tetradic_shadows(im, 179, 25, 50, 75)
    
    #cv.imwrite('undecided.jpg', im2)
    #cv.imwrite('undecided2.jpg', im3)

    Result.singleWindow([im2, im3], imDim = im.shape[:2])#, dtype= 's')
    
if __name__ == '__main__':
    main()