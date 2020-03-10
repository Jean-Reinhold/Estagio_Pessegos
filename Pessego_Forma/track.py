import numpy as np 

contador = 25
pasta = open('Bere.txt', "w+")

while contador != 61: 
    pasta.write(str(contador) + " " + str(contador - 1 + np.random.rand(0)))