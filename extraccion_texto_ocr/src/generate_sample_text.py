import os
import cv2
import numpy as np

os.makedirs("data", exist_ok=True)

def generar_documento_texto(out_path="data/documento_texto.png", width=700, height=450):
    """Genera una imagen con apariencia de documento / letrero con varias líneas de texto nítidas."""
    img = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Marco o borde sutil del documento
    cv2.rectangle(img, (20, 20), (width - 20, height - 20), (220, 220, 220), 2)
    cv2.rectangle(img, (30, 30), (width - 30, height - 30), (70, 70, 70), 1)

    # Encabezado
    cv2.putText(img, "VISION POR COMPUTADORA - OCR", (50, 75),
                cv2.FONT_HERSHEY_DUPLEX, 0.9, (20, 20, 20), 2)
    cv2.line(img, (50, 95), (width - 50, 95), (100, 100, 100), 1)

    # Líneas de texto principales
    lineas = [
        ("INFORME TECNICO DE PROCESAMIENTO", 140, 0.7, (0, 102, 204), 2),
        ("Extraccion automatica de texto con Tesseract y OpenCV.", 185, 0.6, (40, 40, 40), 1),
        ("Permite digitalizar recibos, placas vehiculares y letreros.", 225, 0.6, (40, 40, 40), 1),
        ("ID DE DOCUMENTO: DOC-2026-CV-994", 280, 0.65, (0, 128, 0), 2),
        ("FECHA DE EMISION: 20/09/2026", 320, 0.6, (50, 50, 50), 1),
        ("ESTADO: APROBADO Y VERIFICADO", 360, 0.6, (50, 50, 50), 1),
        ("WWW.COMPUTERVISION.ORG", 410, 0.55, (120, 120, 120), 1)
    ]

    for (texto, y, scale, color, thick) in lineas:
        cv2.putText(img, texto, (50, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick)

    cv2.imwrite(out_path, img)
    print(f"Documento de prueba generado en: {out_path}")

if __name__ == "__main__":
    generar_documento_texto()
