from PIL import Image, ImageEnhance

image = Image.open("./images/barn_house.jpg")

color_enhancer = ImageEnhance.Color(image)

enhanced_image = color_enhancer.enhance(0)
