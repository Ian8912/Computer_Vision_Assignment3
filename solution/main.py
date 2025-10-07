import os
import sys

from pathlib import Path
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from gradient_orientations import gradient_orientations
from oriented_edges import *
from detect_lines import detect_lines

def main():
    # Load the image
    img = cv.imread("data/frame0040.jpg", cv.IMREAD_GRAYSCALE)

    # Calculate the oriented edges
    sigma = 1.4
    threshold = 40
    direction = 0
    tolerance = 15
    edge_img = oriented_edges(img, sigma, threshold, direction, tolerance)
    # edge_img = bug_oriented_edges(img, sigma, threshold, direction, tolerance)
    display_image(edge_img, "Oriented Edges")

    # Write edge direction images to data/
    ROOT = Path(__file__).resolve().parents[1]
    DATA_DIR = ROOT / "data"          
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for d in [0, 15, 45, 90, 135, 180]:
        out = oriented_edges(img, 1.4, 40, d, 15)
        out_path = DATA_DIR / f"edges_dir_{d}.png"
        cv.imwrite(str(out_path), out)


    img = cv.imread("data/perpendicular-lines.jpg", cv.IMREAD_GRAYSCALE)
    lines = detect_lines(img, sigma=1.5, threshold=50, numLines=5)
    
    draw_lines(img, lines)

# Function to display images
def display_image(img, title="Image"):
    img = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX)
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def draw_lines(img, lines):
    lines_image = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    for rho, theta in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
        cv.line(lines_image, pt1, pt2, (0, 255, 255), 2)
    
    display_image(lines_image, "Detected Lines")

if __name__ == "__main__":
    main()