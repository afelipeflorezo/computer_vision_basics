import os
import cv2
import numpy as np

os.makedirs("data", exist_ok=True)

def generar_frame_carretera(width=800, height=500, dash_offset=0):
    """Genera una imagen con perspectiva de carretera, línea izquierda continua amarilla y línea derecha discontinua blanca."""
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # 1. Cielo (azul degradado)
    horizon = int(height * 0.45)
    for y in range(horizon):
        color = (180 - int(y * 0.3), 130 - int(y * 0.2), 60 + int(y * 0.2))
        img[y, :] = color

    # 2. Paisaje / pasto a los costados
    img[horizon:, :] = (30, 80, 40)

    # 3. Asfalto (polígono trapezoidal)
    road_pts = np.array([
        [int(width * 0.42), horizon],
        [int(width * 0.58), horizon],
        [width, height],
        [0, height]
    ], dtype=np.int32)
    cv2.fillPoly(img, [road_pts], (65, 65, 68))

    # 4. Línea izquierda continua (Amarilla)
    cv2.line(img, (int(width * 0.44), horizon + 10), (int(width * 0.12), height), (0, 215, 255), 8)

    # 5. Línea derecha discontinua (Blanca)
    steps = 14
    for i in range(steps):
        t0 = (i + (dash_offset % 1.0)) / steps
        t1 = (i + 0.6 + (dash_offset % 1.0)) / steps
        if t1 > 1.0:
            continue
        # Interpolación con perspectiva
        x0 = int((width * 0.56) + t0 * (width * 0.88 - width * 0.56))
        y0 = int(horizon + 10 + t0 * (height - (horizon + 10)))
        x1 = int((width * 0.56) + t1 * (width * 0.88 - width * 0.56))
        y1 = int(horizon + 10 + t1 * (height - (horizon + 10)))
        thickness = max(2, int(3 + t0 * 5))
        cv2.line(img, (x0, y0), (x1, y1), (255, 255, 255), thickness)

    # 6. Capó del vehículo en la parte inferior
    hood_pts = np.array([
        [int(width * 0.25), height],
        [int(width * 0.75), height],
        [int(width * 0.65), int(height * 0.94)],
        [int(width * 0.35), int(height * 0.94)]
    ], dtype=np.int32)
    cv2.fillPoly(img, [hood_pts], (20, 20, 20))

    return img

def generar_datos_prueba():
    # Imagen estática
    img = generar_frame_carretera()
    cv2.imwrite("data/carretera.jpg", img)
    print("Imagen de carretera de prueba guardada en: data/carretera.jpg")

    # Video de carretera (60 frames con movimiento continuo de líneas)
    video_path = "data/carretera_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, 20, (800, 500))
    for f in range(60):
        frame = generar_frame_carretera(dash_offset=(f * 0.1))
        out.write(frame)
    out.release()
    print(f"Video sintético de carretera guardado en: {video_path}")

if __name__ == "__main__":
    generar_datos_prueba()
