from PIL import Image, ImageFilter, ImageChops

calm_image = Image.open("images/calm_water.JPG")

im = calm_image.filter(ImageFilter.GaussianBlur(200))
im2 = calm_image.filter(ImageFilter.GaussianBlur(1))
im3 = ImageChops.subtract(image1 = im, image2 = im2)

im3.show()