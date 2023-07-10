import math
import cv2 as cv
import numpy as np
from Filters import Toasty, Frosty
from Posterization import kMeanPosterization
import scipy.stats as stats
import skimage



def calculate_psnr(img1, img2):
    # Convert the input images to float64 data type
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    
    # Calculate the mean squared error (MSE) between the images
    mse = np.mean((img1 - img2) ** 2)
    
    # Check if the MSE is zero (to avoid division by zero)
    if mse == 0:
        return float('inf')  # Return positive infinity (since PSNR is undefined in this case)
    
    # Calculate the Peak Signal-to-Noise Ratio (PSNR) using the MSE
    psnr = 20 * math.log10(255.0 / math.sqrt(mse))
    return psnr


def ssim(img1, img2):
    # Define constants C1 and C2 for SSIM calculation
    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2

    # Convert the input images to float64 data type
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)

    # Create a Gaussian kernel with a size of 11 and standard deviation of 1.5
    # Math: G_{i} = a*e-(2i-10)/3
    kernel = cv.getGaussianKernel(11, 1.5)

    # Create a 2D window by taking the outer product of the Gaussian kernel
    # Math: window = G \otimes G^{t}
    window = np.outer(kernel, kernel.transpose())

    # Apply the 2D filter to compute the mean of img1 and img2 using the window
    # Math: \mu_{x}=\frac{1}{N}\sum_{i=1}^{N}x_{i}
    mu1 = cv.filter2D(img1, -1, window)[5:-5, 5:-5]
    
    # Math: \mu_{y}=\frac{1}{N}\sum_{i=1}^{N}y_{i}
    mu2 = cv.filter2D(img2, -1, window)[5:-5, 5:-5]

    # Compute squared means and cross mean between mu1 and mu2
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2

    # Compute the variances of img1 and img2 using the window
    # Math: \sigma_{x}=\sqrt{\frac{1}{N-1}\sum_{i=1}^{N}\left( x_{i} - \mu_{x} \right)^{2}}
    sigma1_sq = cv.filter2D(img1 ** 2, -1, window)[5:-5, 5:-5] - mu1_sq
    # Math: \sigma_{y}=\sqrt{\frac{1}{N-1}\sum_{i=1}^{N}\left( y_{i} - \mu_{y} \right)^{2}}
    sigma2_sq = cv.filter2D(img2 ** 2, -1, window)[5:-5, 5:-5] - mu2_sq

    # Compute the covariance between img1 and img2 using the window
    sigma12 = cv.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

    # Math: SSIM = \left( \frac{\left( 2 * \mu_{x} * \mu_{y} + C1 \right) * \left( 2 * \sigma_{xy} + C2 \right) }{\left( \mu_{x}^{2} * \mu_{y}^{2} + C1 \right) * \left( \sigma_{x}^{2} * \sigma_{y}^{2} + C2 \right)} \right)
    # Compute the SSIM map using the formula for each corresponding pixel
    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / (
            (mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))

    # Return the mean SSIM value of the map as the overall SSIM score
    return ssim_map.mean()



def calculate_ssim(img1, img2):
    # Check if input images have the same dimensions
    if not img1.shape == img2.shape:
        raise ValueError('Input images must have the same dimensions.')

    # Check the number of dimensions of the input images
    if img1.ndim == 2:
        # If the images are grayscale, compute SSIM directly
        return ssim(img1, img2)
    elif img1.ndim == 3:
        # If the images are color (3 channels), compute SSIM for each channel separately
        if img1.shape[2] == 3:
            ssims = []
            for i in range(3):
                ssims.append(ssim(img1[:, :, i], img2[:, :, i]))
            # Return the average SSIM across the channels
            return np.array(ssims).mean()
        # If the images are single-channel, compute SSIM after squeezing the dimensions
        elif img1.shape[2] == 1:
            return ssim(np.squeeze(img1), np.squeeze(img2))
    else:
        # Raise an error for unsupported image dimensions
        raise ValueError('Wrong input image dimensions.')
  
def calculate_entropy(img):
    _bins = 128
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    hist, _ = np.histogram(gray.ravel(), bins=_bins, range=(0, _bins))
    prob_dist = hist / hist.sum()
    entropy = stats.entropy(prob_dist, base=2)
    mean_entropy = np.mean(entropy)
    return mean_entropy



def main():
    pic_list = ["baboon.png", "fruits.png", "HappyFish.jpg", "peppers.png", "tulips.png"]
    dir = "./images/standard_test_images/"
    values_lst = [[[] for _ in range(3)] for _ in range(7)]

    for i in pic_list:
        org = cv.imread(dir + i)
        output_img_lst = [
            Toasty(org),
            Frosty(org),
            kMeanPosterization(org, 4),
            kMeanPosterization(org, 5),
            kMeanPosterization(org, 6),
            kMeanPosterization(org, 7),
            kMeanPosterization(org, 8)
        ]

        for j, output_img in enumerate(output_img_lst):
            values_lst[j][0].append(calculate_entropy(output_img))
            values_lst[j][1].append(calculate_ssim(output_img, org))
            values_lst[j][2].append(calculate_psnr(output_img, org))

    values_lst = [[np.mean(values) for values in sublst] for sublst in values_lst]

    print(values_lst)
       
if __name__ == "__main__":
    main()
