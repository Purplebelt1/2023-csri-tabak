import cv2 as cv
import numpy as np
import Result
from sklearn.cluster import MiniBatchKMeans




def basicPoserization(img):
    return img // 128 * 128

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
    path = "./images/tree_swing.jpg"
    base_img = cv.imread(path)

    posterized1 = basicPoserization(base_img)
    posterized2 = kMeanPosterization(base_img, 3)

    Result.multiWindow([base_img,posterized1,posterized2])

if __name__ == '__main__':
    main()