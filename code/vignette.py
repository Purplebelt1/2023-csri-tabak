
import numpy as np;
import matplotlib.pyplot as plt;
from PIL import Image, ImageFilter

def distanceFromPoint( x, y , px, py ):
    # x, y are coordinates of a pixel
    # px, py are coordinates of a fixed point
    # 0.0 <= x, y, px, py <= 1.0
    diffX = px - x
    diffY = py - y
    return np.sqrt( diffX * diffX + diffY * diffY )
# distanceFromPoint()

def distanceFromCircle( x, y, cx, cy, radius ):
    # x, y are coordinates of a pixel
    # cx, cy are coordinates of a center of a circle
    # radius is the size of the circle
    # 0.0 <= x, y, cx, cy, radius <= 1.0
    distance = distanceFromPoint( x, y, cx, cy )
    if distance < radius:
        return 0.0
    else:
        return distance - radius
# distanceFromCircle()

def distanceFromLine( xOrY, lineCoordinate ):
    # xOrY is either the x or y coordinate of a pixel
    # lineCoordinate is either the x coordinate
    #   of a vertical line or the y coordinate
    #   of a horizontal line
    # 0.0 <= xOrY, lineCoordinate <= 1.0
    return abs( lineCoordinate - xOrY )
# distanceFromLine()

def distanceFromBand( xOrY, loBound, hiBound ):
    # xOrY is either the x or y coordinate of a pixel
    # loBound, hiBound are either x coordinates
    #   of two vertical lines or y coordinates
    #   of two horizontal lines
    # 0.0 <= xOrY, loBound, hiBound <= 1.0
    if loBound < xOrY < hiBound:
        return 0.0
    elif xOrY < loBound:
        return loBound - xOrY
    else:
        return xOrY - hiBound
# distanceFromBand()

def clip( weight ):
    # assure that weight lies between
    # 0.0 and 1.0 by reducing higher
    # values to 1.0 and increasing lower
    # values to 0.0
    
    weight = max( weight, 0.0)
    weight = min( weight, 1.0)
    
    return weight
# clip()

def translateAndScale( weight, loBound, hiBound ):
    # assure that weight lies between
    # 0.0 and 1.0 by translating and scaling
    #
    # this function is useful when the lowest
    # and highest possible values of weight
    # are known
    result = (weight - loBound) / (hiBound - loBound)

    return result
# translateAndScale()

def weightedAveragePrimaryValues( a, b, weight ):
    # compute the weighted average of either the
    # red, green, or blue components of 2 colors
    # 0 <= a, b <= 255
    # 0.0 <= weight <= 1.0
    return np.uint8((1 - weight) * a + weight * b)
# weightedAveragePrimaryValues()

def weightedAverageColors( a, b, weight ):
    #  compute the weighed average of two colors
    # 0.0 <= weight <= 1.0
    aRed, aGreen, aBlue = a
    bRed, bGreen, bBlue = b

    resultRed = weightedAveragePrimaryValues( aRed, bRed, weight )
    resultGreen = weightedAveragePrimaryValues( aGreen, bGreen, weight )
    resultBlue = weightedAveragePrimaryValues( aBlue, bBlue, weight )

    return (resultRed, resultGreen, resultBlue)
# weightedAverageColors()

def vignette(im, px, py, radius, finalDistance):
    # TO-DO: experiment with other images
    #original2 = Image.open('images/water _view.JPG')
    #original = original2.copy().resize((504, 378))

    # TO-DO:
    #  Experiment with other values of radius
    #  Experiment with other filters
    #  Experiment with ImageEnhance to vary contrast,
    #    brightness, or saturation
    blurred = im.point(lambda p: 0)

    # create a copy that will become
    # a blended version of original and blurred
    result = im.copy()

    # get dimensions of image
    height, width = im.size

    print( 'width = ', width )
    print( 'height = ', height )

    # let proportions with which we blend
    # the two images depend upon a pixel's
    # distance from the point we define here
    
    px = px    
    py = py

    #radius is the radius of the circle, for if
    #a circle is being used
    #the circle will contain only the original image
    #finalDistance is the distance from the edge
    #at which the effect reaches its final change
    #before staying at a constant weight
    radius = radius
    finalDistance = finalDistance

    minimumDistance = 0.0

    d0 = distanceFromPoint( 0.0, 0.0, px, py )
    d1 = distanceFromPoint( 1.0, 0.0, px, py )
    d2 = distanceFromPoint( 0.0, 1.0, px, py )
    d3 = distanceFromPoint( 1.0, 1.0, px, py )
    maximumDistance = max( max(d0, d1), max(d2, d3) ) - radius - finalDistance
    if maximumDistance < 0:
        ValueError("(Radius + Final distance) is greater than center point to furthest corner of screen")
                           
    # pair of nested loops will let us examine the
    # pixels row by row and column by column
    
    for i in range(height):
        # compute a value between 0.0 and 1.0
        # that describes vertical distance of a pixel
        # from the bottom of the image, as a
        # fraction of the image's height
        y = i / height
        
        for j in range(width):
            # compute a value between 0.0 and 1.0
            # that describes horizontal distance of a pixel
            # from the left edge of the image, as a
            # fraction of the image's width
            x = j / width

            # TO-DO: Experiment with different functions
            #   for computing weights used in producing
            #   weighted averages of colors
            #
            #   Try...
            #     distanceFromPoint()
            #     distanceFromCircle()
            #     distanceFromLine()
            #     distanceFromBand()
            #
            #   Try call these functions with
            #   different numerical arguments
            #   (for example, 0.1 instead of 0.3) 
                
            # compute the distance of a pixel
            # from the center of the image
            #weight = distanceFromPoint( x, y, px, py )

            weight = distanceFromCircle( x, y, px, py, radius )

            #weight = distanceFromLine( x, 0.4 )

            #weight = distanceFromBand( x, 0.3, 0.7 )
            
            weight = translateAndScale( weight,
                                        minimumDistance,
                                        maximumDistance )
            weight = clip( weight )

            # raising the weight to a power
            # will make the effect fade faster or slower
            # TO-DO: Experiment with other exponents
            #   or experiment with functions other than
            #   power
            weight = np.power( weight, 1 )

            
            # fetch colors of pixels in both images
            originalColor = im.getpixel( (i, j) )
            blurredColor = blurred.getpixel( (i, j) )

            blendedColor = weightedAverageColors(
                originalColor,
                blurredColor,
                weight )
            
            # put the new color in the right place in
            # the new image
            result.putpixel( (i, j), blendedColor )
    
    return result

def main():
    #test image
    original = Image.open('images/water _view.JPG')
    im = vignette(original, 0.5, 0.5, 0.2, 0.3)
    im.show()
    
if __name__ == '__main__':
    main()