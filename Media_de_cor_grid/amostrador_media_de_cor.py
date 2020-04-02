import cv2 as cv 
import numpy as np 
import os 

#lê as imagens dentro da pasta
def leitor (im_paths, complemento): 
    imgs = list() 
    for path in im_paths: 
        imgs.append(cv.imread(complemento+path))
    return imgs

#divide a imagem um grid com elementos quadrados de aresta k, com intervalo de espaçamento de -stride
def grid_maker (img, k, stride): 
    largura = img.shape[1]
    altura = img.shape[0]

    coluna_i = int (largura / k) 
    linha_i = int (altura / k)
    sub_imgs = list()

    if linha_i < 1 or coluna_i < 1: 
        return None 
    
    for i in range(0, altura, k-stride): 
        for j in range(0, largura, k-stride): 
            sub_imgs.append(np.array(img[i:i+k, j:j+k, :]))
    
    return sub_imgs

im_paths_s = os.listdir("/home/jean/Documentos/quarentine/inputs/saudaveis")
im_paths_d = os.listdir("/home/jean/Documentos/quarentine/inputs/doentes")

imgs_d = leitor(im_paths_d, "inputs/doentes/")
imgs_s = leitor(im_paths_s, "inputs/saudaveis/")


#salvando medias das doentes de cada elemento do grid
f_bgr = open("medias_doentes_bgr.txt", "w")
f_hsv = open("medias_doentes_hsv.txt", "w")

for (img_bgr, path) in zip(imgs_d, im_paths_d): 
    img_hsv = cv.cvtColor(img_bgr, cv.COLOR_BGR2HSV)

    grid_hsv = grid_maker(img_hsv, 20, 5) 
    grid_bgr = grid_maker(img_bgr, 20, 5)

    f_bgr.write(path+";\n")
    for m in grid_bgr: 
        f_bgr.write(str(cv.mean(m)) + ";\n")

    f_hsv.write(path+";\n")
    for m in grid_hsv: 
        f_hsv.write(str(cv.mean(m)) + ";\n")

f_bgr.close()
f_hsv.close()

#salvando medias das saudáveis de cada elemento do grid
f_bgr = open("medias_saudaveis_bgr.txt", "w")
f_hsv = open("medias_saudaveis_hsv.txt", "w")

for (img_bgr, path) in zip(imgs_s, im_paths_s): 
    img_hsv = cv.cvtColor(img_bgr, cv.COLOR_BGR2HSV)

    grid_hsv = grid_maker(img_hsv, 20, 5) 
    grid_bgr = grid_maker(img_bgr, 20, 5)


    f_bgr.write(path+";\n")
    for m in grid_bgr: 
        f_bgr.write(str(cv.mean(m)) + ";\n")

    f_hsv.write(path+";\n")
    for m in grid_hsv: 
        f_hsv.write(str(cv.mean(m)) + ";\n")
        
f_bgr.close()
f_hsv.close()





