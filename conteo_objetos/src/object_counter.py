import cv2
import numpy as np
import os

os.makedirs("output", exist_ok=True)

def contar_objetos(img_path, out_path="output/conteo_resultado.jpg", min_area=400, max_area=50000):
    """Detecta, cuenta y numera objetos en una imagen utilizando procesamiento morfológico y contornos de OpenCV."""
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: No se pudo cargar la imagen: {img_path}")
        return 0

    # 1. Escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Desenfoque Gaussiano para reducir ruido de alta frecuencia
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # 3. Umbralización (Otsu inversa para resaltar objetos oscuros sobre fondo claro)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 4. Operación morfológica de apertura para eliminar motas diminutas y separar bordes
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # 5. Encontrar contornos externos
    contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    annotated = img.copy()
    objetos_validos = []
    
    for c in contours:
        area = cv2.contourArea(c)
        if min_area <= area <= max_area:
            objetos_validos.append((area, c))

    # Ordenar objetos por posición horizontal o vertical para numeración ordenada
    # Ordenar de izquierda a derecha (coordenada X del centroide)
    def obtener_cx(item):
        M = cv2.moments(item[1])
        return int(M["m10"] / M["m00"]) if M["m00"] != 0 else 0

    objetos_validos.sort(key=obtener_cx)

    print("\n" + "=" * 50)
    print(f" RESULTADOS DEL CONTEO DE OBJETOS ({os.path.basename(img_path)})")
    print("=" * 50)
    print(f"Total de objetos contabilizados: {len(objetos_validos)}")
    print("-" * 50)
    print(f"{'ID':<6}{'Área (px)':<14}{'Centroide (X, Y)':<18}")
    print("-" * 50)

    for i, (area, c) in enumerate(objetos_validos, start=1):
        # Calcular centroide mediante momentos
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0

        # Dibujar contorno verde
        cv2.drawContours(annotated, [c], -1, (0, 255, 0), 2)

        # Dibujar círculo en el centroide
        cv2.circle(annotated, (cx, cy), 4, (0, 0, 255), -1)

        # Dibujar caja delimitadora
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (255, 100, 0), 1)

        # Etiqueta con el número de objeto
        label = f"#{i}"
        cv2.putText(annotated, label, (cx - 12, cy - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        print(f"#{i:<5}{int(area):<14}({cx}, {cy})")

    print("=" * 50)

    # Guardar resultados
    mask_out = out_path.replace(".jpg", "_mask.jpg")
    cv2.imwrite(out_path, annotated)
    cv2.imwrite(mask_out, opened)

    print(f"Imagen anotada guardada en: {out_path}")
    print(f"Máscara binaria guardada en: {mask_out}\n")
    return len(objetos_validos)

if __name__ == "__main__":
    test_img = "data/monedas_objetos.jpg"
    if not os.path.exists(test_img):
        print("Generando imagen sintética de monedas...")
        from generate_sample_objects import generar_imagen_objetos
        generar_imagen_objetos(test_img)

    contar_objetos(test_img)
