from PIL import Image, ImageOps, ImageFile, ImageEnhance

def main():
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    im = Image.open("images/water _view.JPG")
    im2 = ImageOps.autocontrast(im, 30)
    im2 = ImageEnhance.Color(im2)
    im2 = im2.enhance(3)
    im2.show()

if __name__ == '__main__':
    main()