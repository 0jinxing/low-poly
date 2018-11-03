import numpy as np
import cv2 as cv


def get_center(points):
    points = np.array(points)
    return int(np.sum(points[:, 0])/len(points)), int(np.sum(points[:, 1])/len(points))


def get_subdiv(feature):
    rows, cols = feature.shape[:2]
    points = []
    points.extend(zip(*np.where(feature == 255)[::-1]))
    rect = (0, 0, cols, rows)
    subdiv = cv.Subdiv2D(rect)
    for point in points:
        subdiv.insert(point)
    return subdiv


def rect_contains(rect, point):
    if point[0] < rect[0] or point[1] < rect[1] or point[0] > rect[2] or point[1] > rect[3]:
        return False
    return True


def get_delaunay(img, feature):
    canvas = img.copy()
    subdiv = get_subdiv(feature)
    triangle_list = subdiv.getTriangleList()
    rows, cols = img.shape[:2]
    r = (0, 0, cols, rows)

    for t in triangle_list:
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(r, pt3):
            pts = np.array([pt1, pt2, pt3], np.int32)
            center = get_center(pts)
            color = img[int(center[1]), int(center[0])]
            cv.fillPoly(canvas, [pts], tuple(color.tolist()))
    return canvas
