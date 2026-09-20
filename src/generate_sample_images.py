import cv2
import numpy as np
import os
os.makedirs("data", exist_ok=True)
# Imagen 1: cuadrado sobre fondo
img1 = np.zeros((300, 300), dtype=np.uint8)
cv2.rectangle(img1, (80, 80), (220, 220), 255, -1)
cv2.imwrite("data/cuadrado.png", img1)
# Imagen 2: círculos concéntricos
img2 = np.zeros((300, 300), dtype=np.uint8)
for r in [30, 60, 90, 120]:
    cv2.circle(img2, (150, 150), r, 255, 2)
cv2.imwrite("data/circulos.png", img2)
# Imagen 3: patrón de tablero (ajedrez)
img3 = np.zeros((300, 300), dtype=np.uint8)
for i in range(10):
    for j in range(10):
        if (i + j) % 2 == 0:
            img3[i*30:(i+1)*30, j*30:(j+1)*30] = 255
cv2.imwrite("data/ajedrez.png", img3)
print("Imágenes generadas en data/")
