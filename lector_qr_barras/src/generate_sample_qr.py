import os
import cv2
import numpy as np

os.makedirs("data", exist_ok=True)

def generar_codigo_qr(texto="https://github.com/afelipeflorezo/computer_vision_basics", output_path="data/codigo_qr.png"):
    """Genera un código QR de prueba. Si 'qrcode' está disponible lo usa, sino genera uno con OpenCV."""
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(texto)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)
        print(f"Código QR generado con biblioteca qrcode en {output_path}")
    except ImportError:
        # Fallback sin dependencias externas: Generar patrón de prueba con OpenCV
        size = 350
        qr_img = np.ones((size, size, 3), dtype=np.uint8) * 255
        
        # Dibujar marcadores de posición característicos de QR (tres esquinas)
        def draw_marker(img, x, y, size=70):
            cv2.rectangle(img, (x, y), (x + size, y + size), (0, 0, 0), -1)
            cv2.rectangle(img, (x + 10, y + 10), (x + size - 10, y + size - 10), (255, 255, 255), -1)
            cv2.rectangle(img, (x + 20, y + 20), (x + size - 20, y + size - 20), (0, 0, 0), -1)

        draw_marker(qr_img, 30, 30)
        draw_marker(qr_img, size - 100, 30)
        draw_marker(qr_img, 30, size - 100)
        
        # Patrón aleatorio pseudo-QR en el centro
        np.random.seed(42)
        for i in range(120, size - 120, 14):
            for j in range(30, size - 30, 14):
                if np.random.rand() > 0.5:
                    cv2.rectangle(qr_img, (j, i), (j + 12, i + 12), (0, 0, 0), -1)
                    
        cv2.putText(qr_img, "QR Test Sample", (90, size - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50), 2)
        cv2.imwrite(output_path, qr_img)
        print(f"Código QR sintético de prueba guardado en {output_path}")

def generar_codigo_barras(texto="123456789012", output_path="data/codigo_barras.png"):
    """Genera una imagen con un código de barras simulado (Code 128 / EAN style) con OpenCV."""
    height, width = 180, 420
    img = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Dibujar barras verticales
    np.random.seed(101)
    x = 40
    while x < width - 40:
        bar_width = np.random.choice([2, 4, 6])
        if np.random.rand() > 0.4:
            cv2.rectangle(img, (x, 30), (x + bar_width, height - 50), (0, 0, 0), -1)
        x += bar_width + 2

    # Texto debajo del código
    cv2.putText(img, f"CODE: {texto}", (110, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.imwrite(output_path, img)
    print(f"Código de barras generado en {output_path}")

if __name__ == "__main__":
    generar_codigo_qr()
    generar_codigo_barras()
