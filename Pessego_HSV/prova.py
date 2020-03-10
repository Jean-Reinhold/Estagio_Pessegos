import cv2 as cv 
import numpy as np

img = cv.imread("verdes/3.jpeg")
minHSV = np.array([[[11, 37, 123]]])
maxHSV = np.array([[[59, 161, 254]]])
mask = cv.inRange(img, minHSV, maxHSV)

cv.imshow('w', mask)
cv.waitKey(0)