from PIL import Image, ImageFilter, ImageChops

#gets edges plus some by using gaussian blur and merging images
def edging(img):
    im = img.filter(ImageFilter.GaussianBlur(200))
    im2 = img.filter(ImageFilter.GaussianBlur(1))
    return ImageChops.subtract(image1 = im, image2 = im2)

#makes half the image a negative
def negative_half(img):
    box = (0,0, img.size[0] // 2, img.size[1])
    region = img.crop(box)
    img = img.point(lambda p: 255 - p)
    img.paste(region, box)
    return img

#opens image and applies changes to it
def main():
    calm_image = Image.open("images/calm_water.JPG")
    im = edging(calm_image)
    im2 = negative_half(im)
    im2.show()

if __name__ == '__main__':
    main()