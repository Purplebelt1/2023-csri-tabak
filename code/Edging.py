from PIL import Image, ImageFilter, ImageChops

calm_image = Image.open("images/calm_water.JPG")

im = calm_image.filter(ImageFilter.GaussianBlur(200))
im2 = calm_image.filter(ImageFilter.GaussianBlur(1))
im3 = ImageChops.subtract(image1 = im, image2 = im2)

box = (0,0, 2016, 3024)
region = im3.crop(box)

im3 = im3.point(lambda p: 255 - p)
im3.paste(region, box)
im3.show()