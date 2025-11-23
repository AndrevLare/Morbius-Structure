from MoebiusStrip import (Strip, Universe, Gate)
from MorbiusFlower import MorbiusFlower


# Creación strips (4):

strip1 = Strip()
for i in range(1, 6):
    strip1.append(i, i+5)

strip1.add(3,"Hola", "Mundo") #Se agrega un universo con heaven = "Hola" y hell = "Mundo"
print("Strip 1:")
print (strip1)


strip2 = Strip()
for i in range(10, 16):
    strip2.append(i, i+5)

strip2.delete(3) #Se elimina el universo del índice 3 (4, 9) 
print("Strip 2:")
print (strip2)


strip3 = Strip()
for i in range(20, 26):
    strip3.append(i, i+5)

print("Strip 3:")
print (strip3)
print(f"Universo con índice 4: {strip3.find(4)}")

#strip3.find(7) #Arroja error

strip4 = Strip()
for i in range(30, 36):
    strip4.append(i, i+5)

print("Strip 4:")
print (strip4)
print(f"Índice del universo con valores heaven = 32, hell = 37: {strip4.index(32, 37)}")

#Creación Flor

flower = MorbiusFlower(strip2)
flower.append(strip3)
flower.append(strip4)
flower.add(0, strip1)

print(flower)

print("strip en índice 2:")
print(flower.find(2))

flower.delete(3)
print(flower)