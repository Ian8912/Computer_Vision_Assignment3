import os
import sys

# Get the absolute path of the script's directory
current_directory = os.path.abspath(os.path.dirname(__file__))

# Get the parent directory
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
sys.path.append(parent_directory)


import pytest
import cv2 as cv
import numpy as np

from solution.oriented_edges import oriented_edges

def test_output_shape():
    img = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
    edge_img = oriented_edges(img, sigma=1.4, threshold=40, direction=0, tolerance=15)
    assert img.shape == edge_img.shape

def test_color_to_gray():
    img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    edge_img = oriented_edges(img, sigma=1.4, threshold=40, direction=0, tolerance=15)
    assert len(edge_img.shape) == 2

def test_direction_0():
    # Read the test image
    image_path = os.path.join('data', 'frame0040.jpg')
    image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

    if image is None:
        pytest.fail(f"Failed to load {input_filename}")

    edge_img = oriented_edges(image, sigma=1.4, threshold=40, direction=0, tolerance=15)

    # Save the output image
    if not os.path.exists('output'):
        os.makedirs('output')
    cv.imwrite(os.path.join('output', 'edge_direction_0.jpg'), cv.normalize(edge_img, None, 0, 255, cv.NORM_MINMAX))

def test_direction_45():
    # Read the test image
    image_path = os.path.join('data', 'frame0040.jpg')
    image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

    if image is None:
        pytest.fail(f"Failed to load {input_filename}")

    edge_img = oriented_edges(image, sigma=1.4, threshold=40, direction=45, tolerance=15)

    # Save the output image
    if not os.path.exists('output'):
        os.makedirs('output')
    cv.imwrite(os.path.join('output', 'edge_direction_45.jpg'), cv.normalize(edge_img, None, 0, 255, cv.NORM_MINMAX))

def test_direction_90():
    # Read the test image
    image_path = os.path.join('data', 'frame0040.jpg')
    image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

    if image is None:
        pytest.fail(f"Failed to load {input_filename}")

    edge_img = oriented_edges(image, sigma=1.4, threshold=40, direction=90, tolerance=15)

    # Save the output image
    if not os.path.exists('output'):
        os.makedirs('output')
    cv.imwrite(os.path.join('output', 'edge_direction_90.jpg'), cv.normalize(edge_img, None, 0, 255, cv.NORM_MINMAX))

def test_direction_135():
    # Read the test image
    image_path = os.path.join('data', 'frame0040.jpg')
    image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

    if image is None:
        pytest.fail(f"Failed to load {input_filename}")

    edge_img = oriented_edges(image, sigma=1.4, threshold=40, direction=135, tolerance=15)

    # Save the output image
    if not os.path.exists('output'):
        os.makedirs('output')
    cv.imwrite(os.path.join('output', 'edge_direction_135.jpg'), cv.normalize(edge_img, None, 0, 255, cv.NORM_MINMAX))