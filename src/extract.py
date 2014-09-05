from perspective import getPerspective
from util import ratio, extractPerspective
from util import showImage, drawPerspective, drawBoundaries, drawContour, writeDocumentationImage
from util import randomColor


import cv2
import numpy as np


def ignoreContours(img,
                   contours,
                   hierarchy,
                   min_ratio_bounding=0.6,
                   min_area_percentage=0.01,
                   max_area_percentage=0.40,
                   min_ratio_rect=0.5):
    ret = []
    i = -1

    img_area = img.shape[0] * img.shape[1]

    for c in contours:
        i += 1

        if not hierarchy[i][2] == -1:
            continue

        _,_,w,h = tmp = cv2.boundingRect(c)
        if ratio(h,w) < min_ratio_bounding:
            continue

        contour_area = cv2.contourArea(c)
        img_contour_ratio = ratio(img_area, contour_area)
        if img_contour_ratio < min_area_percentage:
            continue
        if img_contour_ratio > max_area_percentage:
            continue

        ret.append(i)

    return ret



def extractBoards(img, w, h):
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ## Doc ##
    #writeDocumentationImage(im_gray, "gray")
    ## Doc ##

    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    ## Doc ##
    #writeDocumentationImage(im_bw, "bw")
    ## Doc ##


    contours,hierarchy = cv2.findContours(im_bw,  cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
    hierarchy = np.squeeze(hierarchy)


    ## Doc ##
    #doc_im_contour = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)
    #for c in contours:
    #    c = np.squeeze(c,1)
    #    drawContour(doc_im_contour, c, randomColor())
    #writeDocumentationImage(doc_im_contour, "contours")
    #doc_im_perspective = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)
    #doc_im_contour = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)
    ## Doc ##


    contour_ids = ignoreContours(im_bw, contours, hierarchy)
    boards = []
    for i in contour_ids:
        c = contours[i]
        c = np.squeeze(c,1)

        ## Doc ##
        #color = randomColor()
        #drawContour(doc_im_contour, c, color)
        ## Doc ##

        perspective=getPerspective(img, c)

        if perspective is not None:
            b = extractPerspective(img, perspective, w, h)
            boards.append(b)
            ## Doc ##
            #drawPerspective(doc_im_perspective, perspective)
            ## Doc ##

    ## Doc ##
    #writeDocumentationImage(boards[-1], "extracted")
    #writeDocumentationImage(doc_im_contour, "contours_filtered")
    #writeDocumentationImage(doc_im_perspective, "perspective")
    ## Doc ##


    return boards
