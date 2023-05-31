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

#makes two quaters of the image a negative
def negative_checker(img):
    box = (0,0, img.size[0] // 2, img.size[1] // 2)
    region = img.crop(box)
    box2 = (img.size[0] // 2, img.size[1] // 2, img.size[0], img.size[1])
    region2 = img.crop(box2)
    img = img.point(lambda p: 255 - p)
    img.paste(region, box)
    img.paste(region2, box2)
    return img

#opens image and applies changes to it
def checker_plus(img):
    im = img.copy()
    boxul = (0,0, im.size[0] // 2, im.size[1] // 2)
    boxbl = (0, im.size[1] // 2, im.size[0] // 2, im.size[1])
    boxur = (im.size[0] // 2, 0, im.size[0], im.size[1] // 2)
    boxbr = (im.size[0] // 2, im.size[1] // 2, im.size[0], im.size[1])
    regionul = im.crop(boxul)
    regionbl = im.crop(boxbl)
    regionur = im.crop(boxur)
    regionbr = im.crop(boxbr)
    nul = negative_checker(regionul)
    nbl = negative_checker(regionbl)
    nur = negative_checker(regionur)
    nbr = negative_checker(regionbr)
    im.paste(nul, boxul)
    im.paste(nbl, boxbl)
    im.paste(nur, boxbr)
    im.paste(nbr, boxur)
    return im


def main():
    calm_image = Image.open("images/calm_water.JPG")
    im = edging(calm_image)
    im2 = checker_plus(calm_image)
    im2.show()
    #im2 = negative_half(im)
    #im3 = negative_checker(im)

if __name__ == '__main__':
    main()