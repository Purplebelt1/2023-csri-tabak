from PIL import Image, ImageOps, ImageFile, ImageEnhance
import Chopchop
import Edging

def contrastEnhacne(im, degree, enhance):
    im2 = ImageOps.autocontrast(im, degree)
    im2 = ImageEnhance.Color(im2)
    im2 = im2.enhance(enhance)
    return im2



def main():
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    im = Image.open("images/water _view.JPG")
    #im2 = contrastEnhance(im, 30, 3)
    im3 = im.convert("L")
    im3 = ImageOps.equalize(im3)
    im4 = ImageOps.colorize(im3, (153,75,0), "Purple", "Orange")#(1, 92, 31), "Purple", (88, 149, 219)) #(153, 75, 0) - dark orange
    im5 = Edging.edging(im4, 2)
    im6 = im5.convert("1")
    im6 = im6.convert("L")
    im7 = ImageOps.colorize(im6, "black", "white", "black")
    #im4.save("base.jpg")
    im7.save("outline.jpg")
    #im6.show()
    im7.show()

if __name__ == '__main__':
    main()