import numpy as np
import cv2 as cv


def get_harris(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    harris = cv.cornerHarris(gray, 2, 3, 0.04)
    corners = np.zeros(gray.shape, dtype=np.uint8)
    corners[harris >= 0.01] = 255
    return corners
