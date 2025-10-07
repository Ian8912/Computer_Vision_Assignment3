# solution/oriented_edges.py (BUGGY VERSION)

import cv2 as cv
import numpy as np
from gradient_orientations import gradient_orientations

def oriented_edges(img, sigma, threshold, direction, tolerance):
    if len(img.shape) == 3:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    else:
        gray = img.astype(np.uint8)

    gray = cv.GaussianBlur(gray, (0, 0), sigma)
    canny_edges = cv.Canny(gray, threshold, 2 * threshold)
    grad_orient = gradient_orientations(gray)

    # Convert gradient orientation to edge orientation [0, 180)
    # The edge is perpendicular to the gradient
    edge_direction = (grad_orient + 90) % 180

    # Normalize the input direction to be in the range [0, 180)
    normalized_direction = direction % 180

    # Check if the edge is within the tolerance
    # Minimal circular difference on a 180° circle → result in [0, 90]
    # Trick: shift into [-90, 90] by wrapping, then take abs
    angle_diff = np.abs(((edge_direction - normalized_direction + 90.0) % 180.0) - 90.0)
    within_tolerance_mask = angle_diff <= tolerance

    # Combine the Canny edges with our orientation mask
    edge_img = np.zeros_like(canny_edges)
    edge_img[(canny_edges == 255) & (within_tolerance_mask)] = 255
    
    return edge_img