import time
import cv2 as cv
from utils.harris import get_harris
from utils.delaunay import get_delaunay
from utils.poisson import get_poisson


def get_lowpoly(path, output_path=None):
    img = cv.imread(path)
    poisson = get_poisson(*img.shape[:2])
    edges = cv.Canny(img, 100, 200)
    corners = get_harris(img)
    feature = cv.add(poisson, edges, corners)
    output = get_delaunay(img, feature)
    if output_path:
        cv.imwrite(output_path, output)
    return output
