from PIL import Image, ImageFile, ImageOps, ImageEnhance, ImageChops, ImageFilter

def main():
    #allows image to show
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    im2 = Image.open("images/pointed.JPG")
    im3 = Image.open("images/faded.JPG")

    #This all is just semi-random changes made until the image looked nice
    im = im2.point(lambda p: 255 - p)
    im = im.point(lambda p: p-100 if(p>100) else (p+120))
    im = im.filter(ImageFilter.GaussianBlur(200))
    im = ImageChops.subtract(image1 = im, image2 = im2)
    enhanced_im = ImageEnhance.Brightness(im)
    im = enhanced_im.enhance(2)
    im = ImageChops.subtract(image1 = im3, image2 = im)

    im.show()

if __name__ == '__main__':
    main()