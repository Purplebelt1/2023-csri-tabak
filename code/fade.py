from PIL import Image

faded_image = Image.open("images/faded.JPG")

color_data = []
i = 1
for color in faded_image.getdata():
    mean = (color[0] + color[1] + color[2]) // 3
    rdis = mean - color[0]
    gdis = mean - color[1]
    bdis = mean - color[2]
    col = i / 4032
    location = 3/2
    adjust = col * location
    if adjust > 1:
        adjust = 1
    newr = color[0] + int(adjust * rdis)
    newg = color[1] + int(adjust * gdis)
    newb = color[2] + int(adjust * bdis)
    new_color = (newr, newg, newb)
    color_data.append(new_color)
    i += 1
    if i >= 4033:
        i = 1


newim = Image.new(faded_image.mode,faded_image.size)
newim.putdata(color_data)
newim.show()