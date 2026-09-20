import cv2
import numpy as np
import os
os.makedirs("output", exist_ok=True)
def detectar_bordes_sobel(img_path, out_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.sqrt(sobel_x**2 + sobel_y**2)
    mag = np.uint8(np.clip(mag, 0, 255))
    cv2.imwrite(out_path, mag)
    print(f"Sobel guardado en {out_path}")
def detectar_bordes_canny(img_path, out_path, t1=50, t2=150):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    edges = cv2.Canny(blurred, t1, t2)
    cv2.imwrite(out_path, edges)
    print(f"Canny guardado en {out_path}")
if __name__ == "__main__":
    imagenes = ["data/cuadrado.png", "data/circulos.png", "data/ajedrez.png"]
    
    for img in imagenes:
        nombre = img.split("/")[-1].replace(".png", "")
        detectar_bordes_sobel(img, f"output/{nombre}_sobel.png")
        detectar_bordes_canny(img, f"output/{nombre}_canny.png")
