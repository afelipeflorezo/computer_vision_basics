import cv2
import numpy as np
import os

os.makedirs("output", exist_ok=True)

def aplicar_canny(img):
    """Convierte a escala de grises, aplica suavizado y detector Canny."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_de_interes(canny_img):
    """Aplica una máscara trapezoidal para conservar exclusivamente la calzada vehicular."""
    height, width = canny_img.shape
    mask = np.zeros_like(canny_img)

    # Polígono trapezoidal que abarca el carril inferior hasta cerca del horizonte
    poligono = np.array([[
        (int(width * 0.05), height),
        (int(width * 0.40), int(height * 0.50)),
        (int(width * 0.60), int(height * 0.50)),
        (int(width * 0.95), height)
    ]], dtype=np.int32)

    cv2.fillPoly(mask, poligono, 255)
    enmascarado = cv2.bitwise_and(canny_img, mask)
    return enmascarado

def ajustar_lineas(img, lines):
    """Agrupa y promedia los segmentos de línea detectados en dos líneas principales (carril izquierdo y derecho)."""
    left_fit = []
    right_fit = []
    height, width, _ = img.shape

    if lines is None:
        return None, None

    for x1, y1, x2, y2 in lines.reshape(-1, 4):
        if x2 == x1:
            continue
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        # Pendiente negativa = carril izquierdo (en coordenadas de imagen Y hacia abajo)
        # Pendiente positiva = carril derecho
        if -2.0 < slope < -0.3:
            left_fit.append((slope, intercept))
        elif 0.3 < slope < 2.0:
            right_fit.append((slope, intercept))

    def make_coordinates(fit, y1, y2):
        if len(fit) == 0:
            return None
        slope_avg, intercept_avg = np.mean(fit, axis=0)
        x1 = int((y1 - intercept_avg) / slope_avg)
        x2 = int((y2 - intercept_avg) / slope_avg)
        return np.array([x1, y1, x2, y2])

    y_bottom = height
    y_top = int(height * 0.52)

    left_line = make_coordinates(left_fit, y_bottom, y_top)
    right_line = make_coordinates(right_fit, y_bottom, y_top)

    return left_line, right_line

def procesar_frame_carril(frame):
    """Procesa un fotograma individual y devuelve la imagen con el carril resaltado."""
    canny = aplicar_canny(frame)
    roi = region_de_interes(canny)

    # Transformada de Hough probabilística
    lines = cv2.HoughLinesP(roi, 2, np.pi / 180, threshold=40, minLineLength=30, maxLineGap=100)

    left_line, right_line = ajustar_lineas(frame, lines)

    overlay = np.zeros_like(frame)

    # Si se detectan ambas líneas, sombrear la superficie del carril en verde translúcido
    if left_line is not None and right_line is not None:
        lane_pts = np.array([
            [left_line[0], left_line[1]],
            [left_line[2], left_line[3]],
            [right_line[2], right_line[3]],
            [right_line[0], right_line[1]]
        ], dtype=np.int32)
        cv2.fillPoly(overlay, [lane_pts], (0, 180, 0))

        # Dibujar líneas guía roja/azul
        cv2.line(overlay, (left_line[0], left_line[1]), (left_line[2], left_line[3]), (0, 0, 255), 8)
        cv2.line(overlay, (right_line[0], right_line[1]), (right_line[2], right_line[3]), (255, 0, 0), 8)
    elif left_line is not None:
        cv2.line(overlay, (left_line[0], left_line[1]), (left_line[2], left_line[3]), (0, 0, 255), 8)
    elif right_line is not None:
        cv2.line(overlay, (right_line[0], right_line[1]), (right_line[2], right_line[3]), (255, 0, 0), 8)

    # Fusionar con transparencia
    result = cv2.addWeighted(frame, 0.85, overlay, 0.35, 0)
    
    cv2.putText(result, "CARRIL DETECTADO", (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    return result

def detectar_carril_en_imagen(img_path, out_path="output/carril_resultado.jpg"):
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: No se pudo abrir la imagen {img_path}")
        return

    result = procesar_frame_carril(img)
    cv2.imwrite(out_path, result)
    print(f"Resultado de detección de carril guardado en: {out_path}")

def detectar_carril_en_video(video_path, out_path="output/carril_video_resultado.mp4"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error al abrir video {video_path}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 20

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    frames = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        processed = procesar_frame_carril(frame)
        out.write(processed)
        frames += 1

    cap.release()
    out.release()
    print(f"Video procesado ({frames} fotogramas) guardado en: {out_path}")

if __name__ == "__main__":
    test_img = "data/carretera.jpg"
    if not os.path.exists(test_img):
        from generate_lane_sample import generar_datos_prueba
        generar_datos_prueba()

    detectar_carril_en_imagen("data/carretera.jpg", "output/carril_resultado.jpg")
    
    if os.path.exists("data/carretera_video.mp4"):
        detectar_carril_en_video("data/carretera_video.mp4", "output/carril_video_resultado.mp4")
