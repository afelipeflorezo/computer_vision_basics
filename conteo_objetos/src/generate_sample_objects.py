import os
import cv2
import numpy as np

os.makedirs("data", exist_ok=True)

def generar_imagen_objetos(out_path="data/monedas_objetos.jpg", width=640, height=480):
    """Genera una imagen sintética realista con monedas y piezas circulares dispersas sobre un fondo blanco/claro."""
    np.random.seed(42)
    # Fondo con textura sutil
    img = np.ones((height, width, 3), dtype=np.uint8) * 245
    noise = np.random.randint(-5, 5, (height, width, 3), dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Coordenadas y radios predefinidos para evitar solapamientos excesivos
    objetos = [
        # (x, y, radius, color_bgr, label)
        (100, 100, 42, (45, 140, 220), "Moneda dorada 1"),
        (230, 90, 32, (180, 180, 190), "Moneda plateada 1"),
        (380, 120, 50, (30, 100, 190), "Moneda dorada grande"),
        (520, 110, 28, (170, 170, 180), "Moneda plateada chica"),
        (120, 260, 36, (175, 175, 185), "Moneda plateada 2"),
        (280, 240, 45, (40, 130, 210), "Moneda dorada 2"),
        (440, 270, 34, (50, 150, 230), "Moneda dorada 3"),
        (180, 390, 40, (180, 180, 190), "Moneda plateada 3"),
        (350, 380, 30, (40, 120, 200), "Moneda dorada 4"),
        (500, 390, 48, (35, 110, 195), "Moneda dorada grande 2"),
    ]

    for (x, y, r, color, name) in objetos:
        # Sombra sutil del objeto
        cv2.circle(img, (x + 4, y + 4), r, (210, 210, 210), -1)
        # Objeto principal
        cv2.circle(img, (x, y), r, color, -1)
        # Borde exterior más oscuro
        dark_border = tuple(max(0, c - 40) for c in color)
        cv2.circle(img, (x, y), r, dark_border, 2)
        # Anillo interior para aspecto de moneda
        cv2.circle(img, (x, y), int(r * 0.75), dark_border, 1)

    cv2.imwrite(out_path, img)
    print(f"Imagen de objetos de prueba generada en: {out_path} ({len(objetos)} objetos dibujados)")

if __name__ == "__main__":
    generar_imagen_objetos()
