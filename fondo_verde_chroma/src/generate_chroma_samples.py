import os
import cv2
import numpy as np

os.makedirs("data", exist_ok=True)

def generar_muestras_chroma(width=640, height=480):
    # 1. Imagen con fondo verde puro (Chroma Key) y una figura humana / presentador
    img_verde = np.zeros((height, width, 3), dtype=np.uint8)
    # Verde puro estándar de croma (BGR: 0, 255, 0)
    img_verde[:] = (0, 255, 0)

    # Dibujar cuerpo/torso (azul oscuro)
    cv2.ellipse(img_verde, (width // 2, height + 40), (140, 200), 0, 0, 360, (120, 50, 20), -1)
    # Cuello
    cv2.rectangle(img_verde, (width // 2 - 25, height // 2 + 30), (width // 2 + 25, height // 2 + 90), (160, 195, 235), -1)
    # Cabeza (tono piel)
    cv2.circle(img_verde, (width // 2, height // 2), 65, (160, 195, 235), -1)
    # Cabello (castaño oscuro)
    cv2.ellipse(img_verde, (width // 2, height // 2 - 25), (68, 50), 0, 180, 360, (20, 40, 60), -1)
    # Gafas / detalles
    cv2.circle(img_verde, (width // 2 - 24, height // 2), 16, (20, 20, 20), 2)
    cv2.circle(img_verde, (width // 2 + 24, height // 2), 16, (20, 20, 20), 2)
    cv2.line(img_verde, (width // 2 - 8, height // 2), (width // 2 + 8, height // 2), (20, 20, 20), 2)
    # Sonrisa
    cv2.ellipse(img_verde, (width // 2, height // 2 + 30), (25, 12), 0, 0, 180, (40, 40, 180), 2)

    cv2.imwrite("data/sujeto_fondo_verde.jpg", img_verde)
    print("Imagen con croma verde generada en: data/sujeto_fondo_verde.jpg")

    # 2. Fondo virtual de reemplazo (Playa tropical / atardecer)
    fondo = np.zeros((height, width, 3), dtype=np.uint8)
    horizon = int(height * 0.55)
    # Cielo degradado atardecer
    for y in range(horizon):
        t = y / horizon
        color = (
            int(40 * (1 - t) + 20 * t),
            int(120 * (1 - t) + 160 * t),
            int(255 * (1 - t) + 220 * t)
        )
        fondo[y, :] = color

    # Sol
    cv2.circle(fondo, (int(width * 0.75), int(horizon * 0.6)), 45, (180, 240, 255), -1)

    # Mar (azul verdoso)
    for y in range(horizon, height):
        t = (y - horizon) / (height - horizon)
        color = (
            int(160 * (1 - t) + 120 * t),
            int(140 * (1 - t) + 80 * t),
            int(20 * (1 - t) + 10 * t)
        )
        fondo[y, :] = color

    # Palmera decorativa al costado
    cv2.ellipse(fondo, (80, height), (50, 260), 15, 180, 270, (40, 60, 90), 8)
    cv2.circle(fondo, (110, height // 2 - 20), 40, (30, 110, 50), -1)

    cv2.imwrite("data/fondo_playa.jpg", fondo)
    print("Fondo virtual generado en: data/fondo_playa.jpg")

if __name__ == "__main__":
    generar_muestras_chroma()
