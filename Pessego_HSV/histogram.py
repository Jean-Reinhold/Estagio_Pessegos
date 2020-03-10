import numpy as np 
import cv2 as cv 
import matplotlib.pyplot as plt 

img = cv.imread("1.jpg")
b, g, r = cv.split(img)

histb, _ = np.histogram(b.flatten(), 256, [0,256])
histg, _ = np.histogram(g.flatten(), 256, [0,256])
histr, _ = np.histogram(r.flatten(), 256, [0,256])

plt.title("histograma Azul")
plt.plot(histb)
plt.show()

plt.title("histograma verde")
plt.plot(histg)
plt.show()

plt.title("histograma vermelho")
plt.plot(histr)
plt.show() 