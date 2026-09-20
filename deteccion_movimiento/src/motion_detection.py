import cv2
import numpy as np
import os
from datetime import datetime

os.makedirs("output", exist_ok=True)

def procesar_fotograma_movimiento(prev_gray, curr_frame, min_area=600):
    """Calcula la diferencia de frames, umbraliza, extrae contornos y dibuja cajas delimitadoras."""
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.GaussianBlur(curr_gray, (21, 21), 0)

    if prev_gray is None:
        return curr_gray, curr_frame, False, 0

    # 1. Diferencia absoluta entre el fotograma actual y el anterior
    frame_diff = cv2.absdiff(prev_gray, curr_gray)

    # 2. Umbralización para descartar fluctuaciones menores de luz
    _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

    # 3. Dilatación para consolidar áreas de movimiento fragmentadas
    dilated = cv2.dilate(thresh, None, iterations=3)

    # 4. Encontrar contornos de las regiones activas
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    annotated = curr_frame.copy()
    movimiento_detectado = False
    objetos_en_movimiento = 0

    for c in contours:
        if cv2.contourArea(c) > min_area:
            movimiento_detectado = True
            objetos_en_movimiento += 1
            (x, y, w, h) = cv2.boundingRect(c)
            # Recuadro rojo y etiqueta
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(annotated, "MOVIMIENTO", (x, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Banner de estado superior
    if movimiento_detectado:
        cv2.putText(annotated, "ESTADO: MOVIMIENTO DETECTADO", (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        cv2.putText(annotated, "ESTADO: SIN MOVIMIENTO", (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 0), 2)

    return curr_gray, annotated, movimiento_detectado, objetos_en_movimiento

def detectar_movimiento_en_video(video_path, out_path="output/movimiento_resultado.mp4", min_area=600):
    """Procesa un video pregrabado detectando cualquier objeto o persona en movimiento."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error al abrir el video: {video_path}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    prev_gray = None
    frame_count = 0
    movimiento_frames = 0
    captura_guardada = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        prev_gray, annotated, detectado, n_objs = procesar_fotograma_movimiento(prev_gray, frame, min_area)
        out.write(annotated)
        frame_count += 1

        if detectado:
            movimiento_frames += 1
            if not captura_guardada and frame_count > 10:
                cv2.imwrite("output/movimiento_captura.jpg", annotated)
                captura_guardada = True

    cap.release()
    out.release()

    print(f"\n--- Resumen de Detección de Movimiento ---")
    print(f"Total de fotogramas analizados: {frame_count}")
    print(f"Fotogramas con movimiento activo: {movimiento_frames} ({movimiento_frames / max(1, frame_count) * 100:.1f}%)")
    print(f"Video resultante guardado en: {out_path}")
    if captura_guardada:
        print(f"Captura instantánea guardada en: output/movimiento_captura.jpg")

def detectar_movimiento_camara(min_area=800):
    """Detección de movimiento en tiempo real utilizando la cámara web."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo conectar a la cámara web")
        return

    print("Iniciando detección de movimiento con cámara... Presiona 'q' para salir.")
    prev_gray = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        prev_gray, annotated, detectado, n_objs = procesar_fotograma_movimiento(prev_gray, frame, min_area)

        # Marca de tiempo en vivo
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(annotated, timestamp, (20, annotated.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow("Deteccion de Movimiento (Frame Difference)", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = "data/video_movimiento.mp4"
    if not os.path.exists(video_path):
        from generate_motion_sample import generar_video_movimiento
        generar_video_movimiento(video_path)

    detectar_movimiento_en_video(video_path)

    # Para monitorear con tu cámara web en tiempo real, descomenta la siguiente línea:
    # detectar_movimiento_camara()
