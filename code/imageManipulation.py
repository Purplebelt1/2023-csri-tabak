from PIL import Image, ImageEnhance, ImageFile, ImageOps

#take R, G, and B values and return adjusted values
def pixelProcRed(intensity, dr):

    return intensity / dr

def pixelProcBlue(intensity, db):

    return intensity / db

def pixelProcGreen(intensity, dg):

    return intensity / dg

def color_adjust(img, adjustRed = 1, adjustGreen = 1, adjustBlue = 1):
    #alters RGB values and makes new image with new values
    #enhances color of new image
    multiBands = img.split()

    redBand = multiBands[0].point(lambda p: pixelProcRed(p, adjustRed))

    greenBand = multiBands[1].point(lambda p: pixelProcGreen(p, adjustGreen))

    blueBand = multiBands[2].point(lambda p: pixelProcBlue(p, adjustBlue))

    newImage = Image.merge("RGB", (redBand, greenBand, blueBand))

    water_color_enhancer = ImageEnhance.Color(newImage)

    return water_color_enhancer.enhance(2)

def color_filter(img):
    #create boxes to crop image
    box = (img.size[0] // 4,img.size[1] // 4, (3 * img.size[0]) // 4, (3 * img.size[1]) // 4)
    ulbox = (0, 0, img.size[0] // 2, img.size[1] // 2)
    urbox = (img.size[0] // 2, 0, img.size[0], img.size[1] // 2)
    blbox = (0, img.size[1] // 2, img.size[0] // 2, img.size[1])
    brbox = (img.size[0] // 2, img.size[1] // 2, img.size[0], img.size[1])

    #divide image into four corner regions and middle region

    region = img.crop(box)
    regionr = img.crop(ulbox)
    regiong = img.crop(blbox)
    regionb = img.crop(brbox)
    regionc = img.crop(urbox)

    #add color filter and enhance color to four corner regions

    regionr = color_adjust(regionr, 2)

    regionb = color_adjust(regionb, 1, 1, 2)

    regiong = color_adjust(regiong, 1, 2)

    regionc = color_adjust(regionc)

    #filter middle section to be black and white and resize back to original size
    region_color_enhancer = ImageEnhance.Color(region)

    region_enhanced_image = region_color_enhancer.enhance(0)

    region_enhanced_image = region_enhanced_image.resize((img.size[0] // 2, img.size[1] // 2))

    #connect regions into image

    upper = Image.new('RGB', (img.size[0], img.size[1] // 2))
    upper.paste(regionr, (0,0))
    upper.paste(regionc, (img.size[0] // 2,0))
    bottom = Image.new('RGB', (img.size[0], img.size[1] // 2))
    bottom.paste(regiong, (0,0))
    bottom.paste(regionb, (img.size[0] // 2,0))
    merge = Image.new('RGB', (img.size[0], img.size[1]))
    merge.paste(upper, (0,0))
    merge.paste(bottom, (0,img.size[1] // 2))
    #solarizes image before middle black and white
    #section is added
    merge = ImageOps.solarize(merge)
    merge.paste(region_enhanced_image, box)
    return merge

def main():
    water_image = Image.open("images/water _view.JPG")
    im = color_filter(water_image)
    im = ImageOps.expand(im, 50)
    im.show()

if __name__ == '__main__':
    main()
