import cv2 as cv
import numpy as np
import Result
import math
from sklearn.cluster import MiniBatchKMeans

def basicPosterization(img, channel_num):
    divisor = 255 / channel_num
    return np.rint(np.rint(img / divisor) * divisor).astype("uint8")

def kMeanPosterization(img , clusters):
    (h, w) = img.shape[:2]
    img = cv.cvtColor(img, cv.COLOR_BGR2LAB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))
    clt = MiniBatchKMeans(n_clusters = clusters)
    labels = clt.fit_predict(img)
    quant = clt.cluster_centers_.astype("uint8")[labels]
    quant = quant.reshape((h, w, 3))
    quant = cv.cvtColor(quant, cv.COLOR_LAB2BGR)
    return quant

def main():
    path = "./images/wolf.jpg"
    base_img = cv.imread(path)

    posterized1 = basicPosterization(base_img, 3)
    posterized2 = kMeanPosterization(base_img, 6)

    Result.multiWindow([base_img,posterized1, posterized2])

if __name__ == '__main__':
    main()