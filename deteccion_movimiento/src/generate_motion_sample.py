import os
import cv2
import numpy as np

os.makedirs("data", exist_ok=True)

def generar_video_movimiento(out_path="data/video_movimiento.mp4", width=640, height=480, n_frames=90):
    """Genera un video sintético con un fondo estático y un objeto que se mueve a través de la escena."""
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, 25, (width, height))

    # Fondo fijo (habitación / piso estático)
    fondo_base = np.ones((height, width, 3), dtype=np.uint8) * 220
    # Dibujar líneas del piso para dar contexto espacial
    for y in range(int(height * 0.6), height, 40):
        cv2.line(fondo_base, (0, y), (width, y), (180, 180, 180), 1)
    for x in range(0, width, 80):
        cv2.line(fondo_base, (x, int(height * 0.6)), (int(x * 1.3), height), (180, 180, 180), 1)

    # Objeto en movimiento (una esfera roja con sombra)
    for f in range(n_frames):
        frame = fondo_base.copy()

        # Posición horizontal animada (ida y vuelta)
        t = f / n_frames
        obj_x = int(80 + (width - 160) * (0.5 - 0.5 * np.cos(2 * np.pi * t)))
        obj_y = int(height * 0.72 + 30 * np.sin(4 * np.pi * t))
        radius = 35

        # Sombra en el suelo
        cv2.ellipse(frame, (obj_x, int(height * 0.72 + 45)), (radius, 12), 0, 0, 360, (140, 140, 140), -1)

        # Objeto principal (círculo rojo con gradiente)
        cv2.circle(frame, (obj_x, obj_y), radius, (30, 30, 220), -1)
        # Brillo especular
        cv2.circle(frame, (obj_x - 10, obj_y - 10), 10, (120, 120, 255), -1)

        out.write(frame)

    out.release()
    print(f"Video sintético de movimiento generado en: {out_path} ({n_frames} fotogramas)")

if __name__ == "__main__":
    generar_video_movimiento()
