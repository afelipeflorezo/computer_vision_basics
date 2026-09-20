import cv2
import numpy as np
import os

os.makedirs("output", exist_ok=True)


def detectar_bordes_sobel(img_path, out_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"No se pudo leer {img_path}")
    sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.sqrt(sobel_x**2 + sobel_y**2)
    mag = mag / mag.max() * 255 if mag.max() > 0 else mag
    mag = np.uint8(mag)
    cv2.imwrite(out_path, mag)
    print(f"Sobel guardado en {out_path}")


def detectar_bordes_canny(img_path, out_path, t1=50, t2=150):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"No se pudo leer {img_path}")
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    edges = cv2.Canny(blurred, t1, t2)
    cv2.imwrite(out_path, edges)
    print(f"Canny guardado en {out_path}")


def guardar_comparacion(img_path, sobel_path, canny_path, out_path):
    original = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    sobel = cv2.imread(sobel_path, cv2.IMREAD_GRAYSCALE)
    canny = cv2.imread(canny_path, cv2.IMREAD_GRAYSCALE)
    h = 240
    original = cv2.resize(original, (int(original.shape[1] * h / original.shape[0]), h))
    sobel = cv2.resize(sobel, (original.shape[1], h))
    canny = cv2.resize(canny, (original.shape[1], h))

    def etiqueta(img, texto):
        panel = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.putText(panel, texto, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        return panel

    combo = np.hstack([
        etiqueta(original, "Original"),
        etiqueta(sobel, "Sobel"),
        etiqueta(canny, "Canny"),
    ])
    cv2.imwrite(out_path, combo)
    print(f"Comparacion guardada en {out_path}")


if __name__ == "__main__":
    imagenes = ["data/edificio.jpg", "data/perro.jpg", "data/objetos.jpg"]

    for img in imagenes:
        nombre = os.path.splitext(os.path.basename(img))[0]
        sobel_path = f"output/{nombre}_sobel.png"
        canny_path = f"output/{nombre}_canny.png"
        detectar_bordes_sobel(img, sobel_path)
        detectar_bordes_canny(img, canny_path)
        guardar_comparacion(img, sobel_path, canny_path, f"output/{nombre}_comparacion.png")
