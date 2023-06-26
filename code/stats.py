import math
import cv2 as cv
import numpy as np
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
    # Define constants C1 and C2 for stability in SSIM calculation
    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2

    # Convert the input images to float64 data type
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)

    # Create a Gaussian kernel with a size of 11 and standard deviation of 1.5
    kernel = cv.getGaussianKernel(11, 1.5)

    # Create a 2D window by taking the outer product of the Gaussian kernel
    window = np.outer(kernel, kernel.transpose())

    # Apply the 2D filter to compute the mean of img1 and img2 using the window
    mu1 = cv.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
    mu2 = cv.filter2D(img2, -1, window)[5:-5, 5:-5]

    # Compute squared means and cross mean between mu1 and mu2
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2

    # Compute the variances of img1 and img2 using the window
    sigma1_sq = cv.filter2D(img1 ** 2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv.filter2D(img2 ** 2, -1, window)[5:-5, 5:-5] - mu2_sq

    # Compute the covariance between img1 and img2 using the window
    sigma12 = cv.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

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
  
def main():
     original = cv.imread("./images/wolf.jpg")
     compressed = cv.imread("./results/comic_wolf.jpg")
     psnr_value = calculate_psnr(original, compressed)
     ssim_value = calculate_ssim(original,compressed)
     print(f"PSNR value is {psnr_value} dB")
     print(f"SSIM value is {ssim_value}")
       
if __name__ == "__main__":
    main()
