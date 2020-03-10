import numpy as np
import cv2 as cv
import os 

def ponderar (src, pb, pg, pr):
    b, g, r = cv.split(src)
    b = b // pb
    g = g // pg
    r = r // pr
    return cv.merge((b, g, r))

def binariza(src, metodo, thresh = 0):
    if metodo == 'otsu': 
        return cv.threshold(src,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    if metodo == 'comum':
        return cv.threshold(image, 128, 255, 0)

def segmentacao(path, scr, metodo):
    fonte = np.array(cv.imread(scr))
    image = cv.medianBlur(cv.imread(scr), 5)
    image = ponderar(image, 5, 15, 1)
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, thresh = binariza(image, metodo) 

    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE,
                                        cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(image, contours, -1, (0,255,0), 3)

    circles = cv.HoughCircles(image,cv.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=80,maxRadius=150)
    circles = np.uint16(np.around(circles))

    for i in circles[0,:]:
        img  = fonte [i[1]-i[2]:i[1]+i[2] , i[0]-i[2]:i[0]+i[2]]
        cv.imwrite(path, img)
        
database = os.listdir('database/')
c = 0

for i in database: 
    segmentacao(str(c) + '.jpg', 'database/'+i , 'otsu')