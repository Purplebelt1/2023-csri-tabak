from PIL import Image, ImageOps, ImageFile, ImageEnhance, ImageFilter
import Chopchop
import Edging

def contrastEnhance(im, degree, enhance):
    im2 = ImageOps.autocontrast(im, degree)
    im2 = ImageEnhance.Color(im2)
    im2 = im2.enhance(enhance)
    return im2

def poster(im, chanels):
    im = im.copy()
    divisor = 255 / chanels
    im = im.point(lambda p: (p // divisor) * divisor)
    return im

def main():
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    im = Image.open("images/embossed.jpg")
    #im2 = contrastEnhance(im, 30, 3)
    im3 = im.convert("L")
    im3 = ImageOps.equalize(im3)
    im4 = ImageOps.colorize(im3, "White", "DarkGoldenRod")#darkblue", "Darkgoldenrod")#"Blue", "Yellow", "Green")
    # - for purple sky -(153,75,0), "Purple", "Orange")
    #(1, 92, 31), "Purple", (88, 149, 219)) #(153, 75, 0) - dark orange
    im5 = Edging.edging(im4, 2)
    im6 = im5.convert("1")
    im6 = im6.convert("L")
    im7 = ImageOps.colorize(im6, "black", "white", "black")
    im8 = poster(im, 2)
    #im4 = im4.filter(ImageFilter.GaussianBlur(2))
    #im4 = ImageEnhance.Sharpness(im4)
    #im4 = im4.enhance(2)
    #im4.save("base.jpg")
    #im7.save("outline.jpg")
    #im6.show()
    #im8.save("to_emboss.jpg")
    #im4.save("post_butchering.jpg")
    print(im4.size)
    im4.show()

if __name__ == '__main__':
    main()