from PIL import Image, ImageChops, ImageFilter
import math

def shiftSubtract(im, offset):
    div = math.gcd(im.size[0], im.size[1])
    xdim = im.size[0] // div
    ydim = im.size[1] // div
    xoff = xdim * offset
    yoff = ydim * offset
    im2 = ImageChops.offset(im, xoff, yoff)
    im3 = ImageChops.difference(im, im2)
    im3 = im3.crop((xoff, yoff, im3.size[0], im3.size[1]))
    return im3


def main():
    im = Image.open("images/calm_water.JPG")
    im2 = Image.open("images/pointed.JPG")
    im3 = shiftSubtract(im, 90)
    im3 = im3.crop((0,0,im3.size[0], (im3.size[1] * 7)//10))
    im3.show()


if __name__ == '__main__':
    main()