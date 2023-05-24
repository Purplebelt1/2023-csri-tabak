from PIL import Image, ImageEnhance

def pixelProcRed(intensity):

    return intensity

def pixelProcBlue(intensity):

    return intensity / 2

def pixelProcGreen(intensity):

    return intensity 

water_image = Image.open("images/water _view.JPG")
print(water_image.size)

box = (1008,756, 3024, 2268)

region = water_image.crop(box)

multiBands = water_image.split()

redBand = multiBands[0].point(pixelProcRed)

greenBand = multiBands[1].point(pixelProcGreen)

blueBand = multiBands[2].point(pixelProcBlue)

newImage = Image.merge("RGB", (redBand, greenBand, blueBand))

water_color_enhancer = ImageEnhance.Color(newImage)

water_enhanced_image = water_color_enhancer.enhance(2)


region_color_enhancer = ImageEnhance.Color(region)

region_enhanced_image = water_color_enhancer.enhance(0)




region_enhanced_image = region_enhanced_image.resize((2016, 1512))

water_enhanced_image.paste(region_enhanced_image, box)

water_enhanced_image.show()