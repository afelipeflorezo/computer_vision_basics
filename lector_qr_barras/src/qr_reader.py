import cv2
import numpy as np
import os

os.makedirs("output", exist_ok=True)

def leer_qr_en_imagen(img_path, out_path="output/qr_resultado.jpg"):
    """Detecta y decodifica códigos QR en una imagen estática usando OpenCV QRCodeDetector."""
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: No se pudo cargar la imagen: {img_path}")
        return None

    detector = cv2.QRCodeDetector()
    val, points, straight_qrcode = detector.detectAndDecode(img)

    annotated = img.copy()
    if points is not None and len(points) > 0:
        points = points[0].astype(np.int32)
        cv2.polylines(annotated, [points], True, (0, 255, 0), 3)

        if val:
            print(f"✅ Código QR detectado exitosamente!")
            print(f"   Contenido decodificado: {val}")
            
            # Posición para el texto
            x, y = points[0]
            cv2.putText(annotated, f"QR: {val}", (max(10, x), max(30, y - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            print("⚠️ QR detectado pero no se pudo decodificar el contenido de texto.")
    else:
        print(f"ℹ️ No se detectó ningún código QR con QRCodeDetector en {img_path}.")

    cv2.imwrite(out_path, annotated)
    print(f"Resultado guardado en {out_path}")
    return val

def leer_qr_en_video(video_path, out_path="output/qr_video_resultado.mp4"):
    """Procesa un archivo de video y decodifica códigos QR en cada fotograma."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el video: {video_path}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    detector = cv2.QRCodeDetector()
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        val, points, _ = detector.detectAndDecode(frame)
        if points is not None and len(points) > 0:
            pts = points[0].astype(np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
            if val:
                x, y = pts[0]
                cv2.putText(frame, val, (x, max(30, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()
    print(f"Video procesado ({frame_count} frames) y guardado en {out_path}")

def leer_qr_en_camara():
    """Lectura de códigos QR en tiempo real utilizando la cámara web."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara web")
        return

    detector = cv2.QRCodeDetector()
    print("Iniciando lector QR con cámara web... Presiona 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        val, points, _ = detector.detectAndDecode(frame)
        if points is not None and len(points) > 0:
            pts = points[0].astype(np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
            if val:
                x, y = pts[0]
                cv2.putText(frame, f"QR: {val}", (max(10, x), max(30, y - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Lector QR en Tiempo Real", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 1. Leer código QR en imagen de prueba
    test_img = "data/codigo_qr.png"
    if not os.path.exists(test_img):
        print(f"Generando imagen de prueba en {test_img}...")
        from generate_sample_qr import generar_codigo_qr
        generar_codigo_qr(output_path=test_img)

    leer_qr_en_imagen(test_img, "output/qr_resultado.jpg")

    # 2. Para probar con cámara en tiempo real, descomenta la siguiente línea:
    # leer_qr_en_camara()
