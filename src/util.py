import cv2
import numpy as np
import random

def writeDocumentationImage(image, name):
    cv2.imwrite("images/" + name + ".png", image)

def showImage(image, name="image"):
    print("Showing image: '%s'" % name)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def drawLine(image, a, b, color, thickness=1):
    cv2.line(image, tuple(a), tuple(b), color, thickness)


def drawContour(image, contour, color, thickness=4):
    for i in range(len(contour)):
        p1 = tuple(contour[i])
        p2 = tuple(contour[int((i+1) % len(contour))])
        drawLine(image, p1, p2, color, thickness)



def drawBoundaries (image, boundaries, color=(128, 128, 0)):
    p_min, p_max = boundaries
    cv2.rectangle(image, p_min, p_max, color)


def drawPerspective(image, perspective, thickness=4):
    (a,b,c,d) = perspective

    #    cv2.polylines(image, np.array(perspective, 'int32'), False, (0,0,255) )
    drawLine(image, a,c, (255,0,0), thickness)
    drawLine(image, b,d, (255,0,255), thickness)


def drawLines(image, lines):
    for l in lines:
        l.draw(image)

def drawPoint(image, point, color, thickness=4):
    cv2.circle(image, point, thickness, color)


def extractPerspective(image, perspective, w, h, dest=None):
    if dest is None:
        dest = ((0,0), (w, 0), (w,h), (0, h))

    perspective = np.array(perspective ,np.float32)
    dest = np.array(dest ,np.float32)

    coeffs = cv2.getPerspectiveTransform(perspective, dest)
    return cv2.warpPerspective(image, coeffs, (w, h))


def ratio(a,b):
    if a == 0 or b == 0:
        return -1
    return min(a,b)/float(max(a,b))

def randomColor(ncol=3):
    return [random.randint(0,255) for x in range(ncol)]
