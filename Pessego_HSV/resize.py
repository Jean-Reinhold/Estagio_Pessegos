import cv2 as cv 
import os 

image_paths = os.listdir("verdes/")

for path in image_paths: 
    img = cv.imread('verdes/' + path)
    img = cv.resize(img, (800, 800))
    cv.imwrite("verdes/r" + path, img)