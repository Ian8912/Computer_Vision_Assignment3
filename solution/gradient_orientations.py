import cv2 as cv
import numpy as np


def gradient_orientations(image):
    """
    Calculates the gradient orientations of an input image using the Sobel filter.

    Parameters:
    image (numpy.ndarray): The input image.

    Returns:
    numpy.ndarray: The gradient orientation of every pixel of the input image in the range [-180, 180) degrees

    """
    # If image is in color, convert image to grayscale
    if len(image.shape) == 3:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    else:
        image = image.astype(np.uint8)

    # Step 1: Calculate the gradient using the Sobel filter
    grad_x = cv.Sobel(image, cv.CV_64F, 1, 0, ksize=3)
    grad_y = cv.Sobel(image, cv.CV_64F, 0, 1, ksize=3)

    # Step 2: Calculate the direction of the gradient
    # Flip Y to match our convention that the positive Y axis points downwards
    grad_orient = np.arctan2(grad_y, grad_x)

    # Convert to degrees
    grad_orient_deg = np.rad2deg(grad_orient)

    return grad_orient_deg
