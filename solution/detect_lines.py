import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def detect_lines(img, sigma, threshold, numLines):

    # --- PROVIDED CODE: Pre-processing ---

    # 1. If the image is in color, convert it to grayscale
    if len(img.shape) == 3:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    else:
        gray = img.astype(np.uint8)

    # 2. Blur the image to reduce noise
    gray = cv.GaussianBlur(gray, (0, 0), sigma)

    # 3. Detect edges using the Canny edge detector
    edges = cv.Canny(gray, threshold, 2 * threshold)

    # Display the edges (for debugging)
    # plt.figure()
    # plt.imshow(edges, cmap="gray")
    # plt.show()

    # --- YOUR IMPLEMENTATION GOES HERE (The Hough Space Setup and Voting Process) ---

    # Parameterization: rho = x*cos(theta) + y*sin(theta)
    # Use 1° theta resolution and 1-pixel rho resolution
    h, w = edges.shape
    max_dist = int(np.ceil(np.hypot(h, w)))          # diagonal length
    rhos = np.arange(-max_dist, max_dist + 1, 1)     # [-R, R]
    theta_range = np.deg2rad(np.arange(0, 180, 1))   # [0 degrees, 180 degrees)
    accumulator = np.zeros((len(rhos), len(theta_range)), dtype=np.uint32)

    # Precompute cos/sin for all thetas
    cos_t = np.cos(theta_range)
    sin_t = np.sin(theta_range)

    # Get edge (y, x) coordinates
    ys, xs = np.nonzero(edges)   # edges > 0

    # Vote: for each edge point, compute rho for all thetas and increment bins
    for y, x in zip(ys, xs):
        # Vectorized across all thetas
        r = x * cos_t + y * sin_t                 # shape: [num_thetas]
        r_idx = np.round(r + max_dist).astype(int)
        accumulator[r_idx, np.arange(len(theta_range))] += 1

    # --- END OF YOUR IMPLEMENTATION ---


    # --- PROVIDED CODE: Peak Finding and Line Extraction ---
    #
    # The following code finds the top 'numLines' peaks in the accumulator
    # and converts them back to (rho, theta) pairs. It also performs a simple
    # non-maximum suppression to avoid re-detecting very similar lines.

    # Return the top numLines lines
    lines = []
    for i in range(numLines):
        # Find the maximum value in the accumulator
        max_value = np.max(accumulator)
        if max_value == 0:
            break

        # Find the index of the maximum value
        max_index = np.argmax(accumulator)
        rho_index, theta_index = np.unravel_index(max_index, accumulator.shape)

        # Convert index to rho and theta values
        rho = rho_index - max_dist
        theta = theta_range[theta_index]

        # Add the line to the list of lines
        lines.append((rho, theta))

        # Set an area of the accumulator around the line to zero
        # This is to prevent detecting the same line multiple times
        # We set the area to zero by setting the accumulator values to zero
        # in a rectangle around the line
        # The rectangle is centered at the line and has a width of 10 pixels
        # and a height of 2 degrees.

        # Calculate the coordinates of the rectangle
        x1 = max(0, rho_index - 5)
        x2 = min(accumulator.shape[0], rho_index + 5)
        y1 = max(0, theta_index - 3)
        y2 = min(accumulator.shape[1], theta_index + 5)

        # Set the area to zero
        accumulator[x1:x2, y1:y2] = 0
        
    return lines