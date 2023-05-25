import cv2 as cv
import argparse
import numpy as np
from sklearn.cluster import KMeans


path = "./images/tree_swing.jpg"
base_img = cv.imread(path)

def basicPoserization(img):
    return base_img // 128 * 128

def kMeanPosterization(img , clusters):
    (h, w) = img.shape[:2]
    img = cv.cvtColor(img, cv.COLOR_BGR2LAB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))
    clt = KMeans(n_clusters = clusters)
    labels = clt.fit_predict(img)
    quant = clt.cluster_centers_.astype("uint8")[labels]
    quant = quant.reshape((h, w, 3))
    quant = cv.cvtColor(quant, cv.COLOR_LAB2BGR)
    return quant

posterized1 = basicPoserization(base_img)
posterized2 = kMeanPosterization(base_img, 2)

#cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL)
#cv.namedWindow("Resized Window2", cv.WINDOW_NORMAL)
#cv.namedWindow("Resized Window3", cv.WINDOW_NORMAL)
#cv.resizeWindow("Resized_Window3", 800, 800)
#cv.resizeWindow("Resized_Window", 800, 800)
#cv.resizeWindow("Resized Window2", 800, 800)
# Displaying the image
#cv.imshow("Resized_Window", posterized1)
cv.imwrite("./results/posterization.jpg", np.hstack([base_img, posterized1, posterized2]))
#cv.imshow("Resized Window2", base_img)

cv.waitKey(0)
cv.destroyAllWindows()