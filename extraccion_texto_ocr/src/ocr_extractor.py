import cv2
import numpy as np
import os

os.makedirs("output", exist_ok=True)

def preprocesar_para_ocr(img):
    """Preprocesa la imagen para optimizar la tasa de acierto del motor OCR."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Suavizado suave para remover artefactos de compresión
    denoised = cv2.medianBlur(gray, 3)
    # Umbralización de Otsu
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return gray, thresh

def detectar_regiones_de_texto(img_thresh, img_original):
    """Detecta regiones y líneas de texto mediante gradiente morfológico."""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 4))
    # Invertir para que el texto sea blanco
    inv = cv2.bitwise_not(img_thresh)
    dilated = cv2.dilate(inv, kernel, iterations=1)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    annotated = img_original.copy()

    cajas = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w > 30 and h > 10:
            cajas.append((x, y, w, h))
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 140, 255), 2)

    return annotated, cajas

def extraer_texto_ocr(img_path, out_txt="output/texto_extraido.txt", out_img="output/ocr_anotado.jpg"):
    """Extrae texto de una imagen utilizando Tesseract OCR o fallback morfológico si el binario no está instalado."""
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: No se pudo cargar la imagen: {img_path}")
        return

    gray, thresh = preprocesar_para_ocr(img)
    annotated_morph, cajas = detectar_regiones_de_texto(thresh, img)

    tesseract_disponible = False
    texto_extraido = ""

    try:
        import pytesseract
        # Probar ejecución de Tesseract
        texto_extraido = pytesseract.image_to_string(thresh, lang="spa+eng", config="--psm 6")
        data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)

        annotated = img.copy()
        n_boxes = len(data['text'])
        palabras_detectadas = 0

        for i in range(n_boxes):
            if int(data['conf'][i]) > 40 and data['text'][i].strip():
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
                palabras_detectadas += 1

        tesseract_disponible = True
        cv2.imwrite(out_img, annotated)
        print(f"✅ Tesseract OCR ejecutado exitosamente. Palabras delimitadas: {palabras_detectadas}")

    except Exception as e:
        print("\n" + "!" * 65)
        print("ℹ️ AVISO: Motor Tesseract no detectado en el sistema operativo.")
        print("   Para habilitar el reconocimiento óptico de caracteres completo:")
        print("     - En macOS: brew install tesseract tesseract-lang")
        print("     - En Ubuntu/Debian: sudo apt install tesseract-ocr tesseract-ocr-spa")
        print("     - En Python: pip install pytesseract pillow")
        print("   Se activó la detección morfológica visual de bloques de texto.")
        print("!" * 65 + "\n")

        # Usar la imagen anotada morfológicamente
        cv2.imwrite(out_img, annotated_morph)
        texto_extraido = (
            "--- DETECCION MORFOLOGICA DE TEXTO ---\n"
            f"Lineas de texto detectadas en la imagen: {len(cajas)}\n"
            "Nota: Instala el motor Tesseract en tu sistema para decodificar caracteres alfabéticos."
        )

    # Guardar texto extraído
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(texto_extraido)

    print(f"\n--- TEXTO EXTRAÍDO ---")
    print(texto_extraido.strip())
    print(f"----------------------")
    print(f"Archivo de texto guardado en: {out_txt}")
    print(f"Imagen con regiones delimitadas guardada en: {out_img}\n")

if __name__ == "__main__":
    test_img = "data/documento_texto.png"
    if not os.path.exists(test_img):
        from generate_sample_text import generar_documento_texto
        generar_documento_texto(test_img)

    extraer_texto_ocr(test_img)
