import os
import cv2 as cv 

c = 0 
nomes = os.listdir("/home/jean/Documentos/peach_estruturado/Peach_by_HSV/verdes")

for i in nomes: 
    os.rename("/home/jean/Documentos/peach_estruturado/Peach_by_HSV/verdes/" + i, "/home/jean/Documentos/peach_estruturado/Peach_by_HSV/verdes/" + str(c) + ".jpeg")
    c+=1