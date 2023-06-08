from PIL import Image, ImageFilter, ImageEnhance, ImageChops

def blur(img, blur):
    im = img.copy()
    blur = im.filter(ImageFilter.GaussianBlur(blur))
    return blur

def colored(img, addr, addg, addb):
    im = img.copy()
    r, g, b = im.split()
    r = r.point(lambda p: min(255, (p + addr)))
    g = g.point(lambda p: min(255, (p + addg)))
    b = b.point(lambda p: min(255, (p + addb)))
    filtered = Image.merge('RGB', (r, g, b))
    return filtered

def stick(img):
    im = img.copy()
    stuck = Image.new('RGB', (im.size[0], 2 * im.size[1]))
    stuck.paste(im, (0,0))
    stuck.paste(im, (0, im.size[1]))
    return stuck

def blind(img, brightness):
    im = img.copy()
    im = ImageEnhance.Brightness(im)
    im = im.enhance(brightness)
    return im

def mixed(img, dist):
    im = img.copy()
    move = ImageChops.offset(im, dist)
    mix = ImageChops.difference(im, move)
    return mix

def main():
    sample = Image.open('images/forest.jpg')
    sample.show()
    blur(sample, 10).show()
    colored(sample, 0,0,100).show()
    stick(sample).show()
    blind(sample, 5).show()
    mixed(sample, 500).show()

if __name__ == '__main__':
    main()