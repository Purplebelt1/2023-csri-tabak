from PIL import Image

def fade(img, location_inverse, stop = True):
    #img is image to fade, location_inverse is the inverse of the fraction of the image's width
    # at which the RGB values will be equal, stop determines if the RGB values will continue to
    # be altered beyond being equal after the location set is reached 
    
    #create list to hold new color data and intialize counter for rows
    color_data = []
    i = 1
    #iterates over colors in img
    for color in img.getdata():
        #determines mean value of RGB values at pixel and the distance of each value from mean
        mean = (color[0] + color[1] + color[2]) // 3
        rdis = mean - color[0]
        gdis = mean - color[1]
        bdis = mean - color[2]
        #creates coeffcient to apply to distance from mean such that the change increases from 
        #the left side of img
        col = i / img.size[0]
        location = location_inverse
        adjust = col * location
        #checks stop and if adjust would bring RGB values beyond mean and alters adjust so that RGB
        #values go to mean instead
        if stop and adjust > 1:
            adjust = 1
        #creates new RGB values
        newr = color[0] + int(adjust * rdis)
        newg = color[1] + int(adjust * gdis)
        newb = color[2] + int(adjust * bdis)
        #collects new RGB values and appends to list
        new_color = (newr, newg, newb)
        color_data.append(new_color)
        #increments i and checks if pixel is in next row. If it is, i is set to 1
        i += 1
        if i >= img.size[0] + 1:
            i = 1
    #makes new image of same data type and size as img with the new colors
    newim = Image.new(img.mode,img.size)
    newim.putdata(color_data)
    return newim

def main():
    faded_image = Image.open("images/faded.JPG")
    newim = fade(faded_image, 3/2)
    newim.show()

if __name__ == '__main__':
    main()