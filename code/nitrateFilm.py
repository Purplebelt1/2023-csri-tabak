from PIL import Image, ImageEnhance
import numpy as np

img = Image.open("./images/barn_house.jpg")

color_enhancer = ImageEnhance.Color(img)

enhanced_img = color_enhancer.enhance(0)

enhanced_img.load()

img_array = np.asarray(enhanced_img, dtype='int32')

def gaus(std, mean, x):
    return (1/(std))*np.e**(-(x-mean)**2/(2*std**2))

def norm(vals):
    return [(v-min(vals))/(max(vals)-min(vals)) for v in vals]

def build_gaus(width, height):
    # get a uniform range of floats in the range 0-1 for the x/y axes
    x_vals = np.arange(0, width, 1)
    y_vals = np.arange(0, height, 1)
    
    # calculate standard deviation/mean - meaningless in this case
    # but required to produce Gaussian
    x_std, y_std = np.std(x_vals), np.std(y_vals)
    x_m, y_m = np.mean(x_vals), np.mean(y_vals)

    # create Gaussians for both x/y axes
    x_gaussian = [gaus(x_std, x_m, x) for x in x_vals]
    y_gaussian = [gaus(y_std, y_m, y) for y in y_vals]

    # normalize the Gaussian to 0-1
    x_gaussian = np.array(norm(x_gaussian))
    y_gaussian = np.array(norm(y_gaussian))
    
    return x_gaussian, y_gaussian






enhanced_img.show()
