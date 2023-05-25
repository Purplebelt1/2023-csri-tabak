from PIL import Image, ImageEnhance, ImageFile

#take R, G, and B values and return adjusted values
def pixelProcRed(intensity):

    return intensity / adjustRed

def pixelProcBlue(intensity):

    return intensity / adjustBlue

def pixelProcGreen(intensity):

    return intensity / adjustGreen

def color_adjust(img):
    #alters RGB values and makes new image with new values
    #enhances color of new image
    multiBands = img.split()

    redBand = multiBands[0].point(pixelProcRed)

    greenBand = multiBands[1].point(pixelProcGreen)

    blueBand = multiBands[2].point(pixelProcBlue)

    newImage = Image.merge("RGB", (redBand, greenBand, blueBand))

    water_color_enhancer = ImageEnhance.Color(newImage)

    return water_color_enhancer.enhance(2)

#open image

water_image = Image.open("images/water _view.JPG")

#create boxes to crop image

box = (1008,756, 3024, 2268)
ulbox = (0, 0, 2016, 1512)
urbox = (2016, 0, 4031, 1512)
blbox = (0, 1512, 2016, 3023)
brbox = (2016, 1512, 4031, 3023)

#divide image into four corner regions and middle region

region = water_image.crop(box)
regionr = water_image.crop(ulbox)
regiong = water_image.crop(blbox)
regionb = water_image.crop(brbox)
regionc = water_image.crop(urbox)

#add color filter and enhance color to four corner regions
adjustRed = 2

adjustBlue = 1

adjustGreen = 1

regionr = color_adjust(regionr)


adjustRed = 1

adjustBlue = 2

regionb = color_adjust(regionb)


adjustBlue = 1

adjustGreen = 2

regiong = color_adjust(regiong)


adjustGreen = 1

regionc = color_adjust(regionc)

#filter middle section to be black and white and resize back to original size
region_color_enhancer = ImageEnhance.Color(region)

region_enhanced_image = region_color_enhancer.enhance(0)

region_enhanced_image = region_enhanced_image.resize((2016, 1512))

#connect regions into image

upper = Image.new('RGB', (4032, 1512))
upper.paste(regionr, (0,0))
upper.paste(regionc, (2016,0))
bottom = Image.new('RGB', (4032, 1512))
bottom.paste(regiong, (0,0))
bottom.paste(regionb, (2016,0))
merge = Image.new('RGB', (4032, 3024))
merge.paste(upper, (0,0))
merge.paste(bottom, (0,1512))
merge.paste(region_enhanced_image, box)
merge.show()
