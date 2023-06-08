from PIL import Image, ImageChops
import math

def shiftSubtract(im, offset):
    #Takes image im and creates a offset version.
    #The new image and im are subtracted and then
    #cropped to remove the parts that looped around
    #to the other side of the image.

    #finds smallest integer ratio of width and height
    div = math.gcd(im.size[0], im.size[1])
    xdim = im.size[0] // div
    ydim = im.size[1] // div
    #multiplies ratio by offset so offset is applied 
    #according to the width and height ratio
    xoff = xdim * offset
    yoff = ydim * offset
    #creates offset image and subtracts with original
    im2 = ImageChops.offset(im, xoff, yoff)
    im3 = ImageChops.difference(im, im2)
    #removes looped parts of image
    im3 = im3.crop((xoff, yoff, im3.size[0], im3.size[1]))
    return im3


def main():
    #tests shiftSubtract
    im = Image.open("images/calm_water.JPG")
    im3 = shiftSubtract(im, 90)
    #im3 = im3.crop((0,0,im3.size[0], (im3.size[1] * 7)//10))
    im3 = im3.crop(((im3.size[0] * 1) // 5,0,(im3.size[0] * 9) // 10, (im3.size[1] * 23) // 40))

    im3.show()
    #im3.save("timber.jpg")


if __name__ == '__main__':
    main()