import cv2
import numpy as np
import os

os.makedirs("output", exist_ok=True)

def aplicar_chroma_key(fore_img_path, back_img_path, out_path="output/chroma_resultado.jpg",
                       lower_green=None, upper_green=None):
    """Sustituye el fondo verde de una imagen por un fondo virtual especificado."""
    if lower_green is None:
        lower_green = [35, 100, 100]
    if upper_green is None:
        upper_green = [85, 255, 255]

    fore = cv2.imread(fore_img_path)
    back = cv2.imread(back_img_path)

    if fore is None:
        print(f"Error: No se pudo abrir la imagen de primer plano: {fore_img_path}")
        return
    if back is None:
        print(f"Error: No se pudo abrir la imagen de fondo: {back_img_path}")
        return

    # Redimensionar el fondo virtual para coincidir exactamente con el tamaño del primer plano
    h, w, _ = fore.shape
    back = cv2.resize(back, (w, h))

    # 1. Convertir a espacio HSV
    hsv = cv2.cvtColor(fore, cv2.COLOR_BGR2HSV)

    # 2. Crear máscara de verde
    lower = np.array(lower_green, dtype=np.uint8)
    upper = np.array(upper_green, dtype=np.uint8)
    green_mask = cv2.inRange(hsv, lower, upper)

    # 3. Refinar máscara (suavizado y dilatación leve para evitar halos verdes en los bordes)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
    green_mask = cv2.dilate(green_mask, kernel, iterations=1)

    # 4. Máscara invertida (donde NO hay verde = sujeto)
    subject_mask = cv2.bitwise_not(green_mask)

    # 5. Aislar sujeto y aislar fondo
    sujeto = cv2.bitwise_and(fore, fore, mask=subject_mask)
    fondo_reemplazo = cv2.bitwise_and(back, back, mask=green_mask)

    # 6. Composición final
    resultado = cv2.add(sujeto, fondo_reemplazo)

    cv2.imwrite(out_path, resultado)
    cv2.imwrite(out_path.replace(".jpg", "_mask.jpg"), green_mask)

    print(f"\n--- Resultado Chroma Key ---")
    print(f"Píxeles verdes reemplazados: {cv2.countNonZero(green_mask)} de {h * w} ({cv2.countNonZero(green_mask) / (h * w) * 100:.1f}%)")
    print(f"Composición guardada en: {out_path}")
    print(f"Máscara binaria guardada en: {out_path.replace('.jpg', '_mask.jpg')}")

def chroma_key_en_camara(fondo_path="data/fondo_playa.jpg", lower_green=None, upper_green=None):
    """Ejecuta el efecto de croma en vivo usando la cámara web."""
    if lower_green is None:
        lower_green = [35, 100, 100]
    if upper_green is None:
        upper_green = [85, 255, 255]

    back = cv2.imread(fondo_path)
    if back is None:
        print(f"Error: Fondo virtual no encontrado en {fondo_path}")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara web")
        return

    print("Iniciando filtro de Fondo Verde en tiempo real... Presiona 'q' para salir.")
    lower = np.array(lower_green, dtype=np.uint8)
    upper = np.array(upper_green, dtype=np.uint8)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w, _ = frame.shape
        back_resized = cv2.resize(back, (w, h))

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        inv_mask = cv2.bitwise_not(mask)

        fg = cv2.bitwise_and(frame, frame, mask=inv_mask)
        bg = cv2.bitwise_and(back_resized, back_resized, mask=mask)
        comp = cv2.add(fg, bg)

        cv2.imshow("Chroma Key en Tiempo Real", comp)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sujeto_path = "data/sujeto_fondo_verde.jpg"
    fondo_path = "data/fondo_playa.jpg"

    if not os.path.exists(sujeto_path) or not os.path.exists(fondo_path):
        from generate_chroma_samples import generar_muestras_chroma
        generar_muestras_chroma()

    aplicar_chroma_key(sujeto_path, fondo_path, "output/chroma_resultado.jpg")

    # Para probar con tu cámara web frente a una tela o fondo verde, descomenta:
    # chroma_key_en_camara()
