from PIL import Image, ImageDraw, ImageFile, ImageFilter, ImageChops, ImageEnhance
ImageFile.LOAD_TRUNCATED_IMAGES = True

water = Image.open("/home/justin/Documents/2023-csri-tabak/images/calm_water.JPG")

im = water.filter(ImageFilter.GaussianBlur(2))
im2 = water.filter(ImageFilter.GaussianBlur(1))
im3 = ImageChops.subtract(image1 = im, image2 = im2)


im3 = im3.filter(ImageFilter.GaussianBlur(2))
im3 = im3.convert("1")
im3 = im3.point(lambda p: 1 - p)
im3 = im3.convert("RGB")


#im3 = ImageChops.subtract(image1 = water, image2 = im3)


im3.show()