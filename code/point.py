from PIL import Image, ImageFile, ImageOps, ImageEnhance, ImageChops, ImageFilter
ImageFile.LOAD_TRUNCATED_IMAGES = True

#def pixelProcRed(intensity):
#
#    return 0
#
#def pixelProcBlue(intensity):
#
#    return (intensity * 2) % 255
#
#def pixelProcGreen(intensity):
#
#    return intensity / 2

im2 = Image.open("images/pointed.JPG")
im3 = Image.open("images/faded.JPG")
im4 = Image.open("/home/justin/Documents/2023-csri-tabak/images/water _view.JPG")


im = im2.point(lambda p: 255 - p)
im = im.point(lambda p: p-100 if(p>100) else (p+120))
im = im.filter(ImageFilter.GaussianBlur(200))
im = ImageChops.subtract(image1 = im, image2 = im2)
#im = im.point(lambda p: 255 - p)
enhanced_im = ImageEnhance.Brightness(im)
im = enhanced_im.enhance(2)
#m = im.convert("L")
im = ImageChops.subtract(image1 = im3, image2 = im)


#multiBands = im.split()
#
#redBand = multiBands[0].point(pixelProcRed)
#
#greenBand = multiBands[1].point(pixelProcGreen)
#
#blueBand = multiBands[2].point(pixelProcBlue)
#
#im = Image.merge("RGB", (redBand, greenBand, blueBand))

#enhanced_im = ImageEnhance.Brightness(im)
#im = enhanced_im.enhance(2)


#im4 = im4.point(lambda p: 255 - p)
#im = ImageChops.subtract(image1 = im4, image2 = im)

#im = im.point(lambda p: 255 - p)

im.show()
#im2.show()