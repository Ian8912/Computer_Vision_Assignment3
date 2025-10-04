import os
import sys

# Get the absolute path of the script's directory
current_directory = os.path.abspath(os.path.dirname(__file__))

# Get the parent directory
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)

# Import required libraries
import pytest
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from solution.detect_lines import detect_lines

# Function to display images
def display_image(img, title="Image"):
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def draw_and_save_lines(img, lines, filename):
    lines_image = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    for rho, theta in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
        cv.line(lines_image, pt1, pt2, (0, 255, 255), 2)
    if not os.path.exists('output'):
        os.makedirs('output')
    cv.imwrite(f"output/{filename}", lines_image)
    # display_image(lines_image, "Detected Lines")

def test_lanes_image():
    img = cv.imread("data/lanes.png", cv.IMREAD_GRAYSCALE)
    lines = detect_lines(img, sigma=1.5, threshold=50, numLines=4)
    draw_and_save_lines(img, lines, "lanes_output.jpg")

def test_lanes1_image():
    img = cv.imread("data/lanes1.jpg", cv.IMREAD_GRAYSCALE)
    lines = detect_lines(img, sigma=1.5, threshold=50, numLines=4)
    draw_and_save_lines(img, lines, "lanes1_output.jpg")

def test_railroad_image():
    img = cv.imread("data/railroad.jpg", cv.IMREAD_GRAYSCALE)
    lines = detect_lines(img, sigma=3, threshold=40, numLines=2)
    draw_and_save_lines(img, lines, "railroad_output.jpg")

def test_perpendicular_lines_image():
    img = cv.imread("data/perpendicular-lines.jpg", cv.IMREAD_GRAYSCALE)
    lines = detect_lines(img, sigma=2, threshold=30, numLines=10)
    draw_and_save_lines(img, lines, "perpendicular_lines_output.jpg")
