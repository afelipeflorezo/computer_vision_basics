import cv2
import numpy as np
import os

os.makedirs("output", exist_ok=True)

def detectar_color_en_imagen(img_path, out_path, color_lower, color_upper):
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: No se pudo abrir la imagen: {img_path}")
        return

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower = np.array(color_lower)
    upper = np.array(color_upper)
    
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    
    # Encontrar contornos y dibujar cajas delimitadoras para ver exactamente qué se detectó
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    annotated = img.copy()
    objetos_detectados = 0
    
    for contour in contours:
        if cv2.contourArea(contour) > 300:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(annotated, "Objeto detectado", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
            objetos_detectados += 1

    cv2.imwrite(out_path, result)
    cv2.imwrite(out_path.replace(".jpg", "_mask.jpg"), mask)
    annotated_path = out_path.replace(".jpg", "_deteccion.jpg")
    cv2.imwrite(annotated_path, annotated)

    pixeles_detectados = cv2.countNonZero(mask)
    print(f"\n--- Resultado Detección de Color ---")
    print(f"Píxeles detectados: {pixeles_detectados}")
    if pixeles_detectados == 0:
        print("⚠️ AVISO: Se detectaron 0 píxeles con ese rango HSV. La imagen resultado se verá completamente negra.")
        print(f"   Rango buscado: Lower {color_lower} a Upper {color_upper}")
        print("   Verifica si el color buscado realmente existe en la imagen o ajusta los umbrales HSV.")
    else:
        print(f"Objetos delimitados: {objetos_detectados}")
        print(f"Imagen con recuadros: {annotated_path}")
        print(f"Imagen aislada por color: {out_path}")
        print(f"Máscara binaria: {out_path.replace('.jpg', '_mask.jpg')}")


def detectar_color_en_video(video_path, out_path, color_lower, color_upper):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"No se pudo abrir el video: {video_path}")
        return
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
    
    lower = np.array(color_lower)
    upper = np.array(color_upper)
    
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(result, "Objeto detectado", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        out.write(result)
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Procesados {frame_count} frames...")
    
    cap.release()
    out.release()
    print(f"Video guardado en {out_path}")

def seguir_objeto_con_camara(color_lower, color_upper):
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return
    
    lower = np.array(color_lower)
    upper = np.array(color_upper)
    
    print("Presiona 'q' para salir")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(result, "Objeto detectado", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow("Deteccion de color", result)
        cv2.imshow("Mascara", mask)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Rangos HSV para colores comunes en OpenCV (H: 0-179, S: 0-255, V: 0-255)
    rojo_lower1 = [0, 100, 100]
    rojo_upper1 = [10, 255, 255]
    
    verde_lower = [40, 100, 100]
    verde_upper = [80, 255, 255]
    
    azul_lower = [100, 100, 100]
    azul_upper = [130, 255, 255]

    # Púrpura / Magenta (ej: pluma del sombrero en data/imagen.jpg)
    purpura_lower = [120, 50, 50]
    purpura_upper = [160, 255, 255]
    
    # Descomenta la opción que quieras probar:
    
    # 1. Detectar color en imagen (cambia el rango según los colores que tenga tu imagen)
    # Por ejemplo, para la pluma púrpura en data/imagen.jpg:
    detectar_color_en_imagen("data/imagen.jpg", "output/resultado.jpg", purpura_lower, purpura_upper)
    # Para buscar verde (en data/imagen.jpg no hay verde, por lo que saldrá negro):
    # detectar_color_en_imagen("data/imagen.jpg", "output/resultado.jpg", verde_lower, verde_upper)
    
    # 2. Detectar color en video
    # detectar_color_en_video("data/video.mp4", "output/video_resultado.mp4", verde_lower, verde_upper)
    
    # 3. Seguir objeto con cámara en tiempo real
    # seguir_objeto_con_camara(verde_lower, verde_upper)

