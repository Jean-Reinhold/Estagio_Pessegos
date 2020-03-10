import cv2 as cv 
import numpy as np 
import os 

i = 0
image_paths = os.listdir("/home/jean/Documentos/peach_estruturado/Peach_by_HSV/verdes/r/")
for path in image_paths: 
    image_paths[i] = "/home/jean/Documentos/peach_estruturado/Peach_by_HSV/verdes/r/" + path 
    i+=1

txt_medias = open("valores_min_max.txt", "w+")

i = 0
src = cv.imread(image_paths[i])

max_h = 255  
max_s = 255
max_v = 255
min_h = 0
min_s = 0 
min_v = 0


def h(x):

    global max_h  
    global max_s 
    global max_v 
    global min_h     
    global min_s
    global min_v
  
    max_h = cv.getTrackbarPos("max_h", "w")
    max_s = cv.getTrackbarPos("max_s", "w")
    max_v = cv.getTrackbarPos("max_v", "w")   
    min_h = cv.getTrackbarPos("min_h", "w")
    min_s = cv.getTrackbarPos("min_s", "w")
    min_v = cv.getTrackbarPos("min_v", "w") 
    img = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    
    minHSV = np.array([[[min_h, min_s, min_v]]])
    maxHSV = np.array([[[max_h, max_s, max_v]]])
    
    maskHSV = cv.inRange(img, minHSV, maxHSV)
    resultHSV = cv.bitwise_or(src, src, mask = maskHSV)

    cv.resize(maskHSV, (1000, 1000))
    cv.imshow("w",maskHSV)
 
cv.namedWindow('w')
cv.createTrackbar("max_h", "w", 0, 255, h)
cv.createTrackbar("min_h", "w", 0, 255, h)
cv.createTrackbar("max_v", "w", 0, 255, h)
cv.createTrackbar("min_v", "w", 0, 255, h)
cv.createTrackbar("max_s", "w", 0, 255, h)
cv.createTrackbar("min_s", "w", 0, 255, h)

h(0)
while (True): 

        k = cv.waitKey(0)
        if k == 32:
            txt_medias.write(str(min_h)+' '+str(max_h)+";" + str(min_s)+' '+str(max_s)+";" + str(min_v)+' '+str(max_v)+";\n")

            i+=1
            if i >= len(image_paths): 
                break

            src = cv.imread(image_paths[i])
            h(0)
            
        else: 
            continue

txt_medias.close()

        
    