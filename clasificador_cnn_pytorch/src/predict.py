import os
import cv2
import numpy as np

os.makedirs("output", exist_ok=True)

CLASSES = ["Circulo", "Cuadrado", "Triangulo"]

def predecir_imagen(img_path, model_path="output/cnn_model.pth", out_path="output/prediccion_resultado.jpg"):
    """Carga el modelo entrenado y clasifica una imagen de prueba."""
    try:
        import torch
        import torch.nn.functional as F
    except ImportError:
        print("\n" + "!" * 65)
        print("ℹ️ PyTorch no está instalado.")
        print("   Instala PyTorch con: pip install torch torchvision")
        print("!" * 65 + "\n")
        return

    from model import SimpleCNN

    if not os.path.exists(model_path):
        print(f"Aviso: El archivo de pesos {model_path} no existe.")
        print("Entrenando un modelo rápido de demostración...")
        from train import entrenar_modelo
        entrenar_modelo(epochs=3)

    img = cv2.imread(img_path)
    if img is None:
        print(f"Error al abrir la imagen: {img_path}")
        return

    # Redimensionar a 32x32 para la CNN
    resized = cv2.resize(img, (32, 32))
    # Convertir a tensor (1, 3, 32, 32)
    tensor = torch.from_numpy(resized).permute(2, 0, 1).float() / 255.0
    tensor = (tensor - 0.5) / 0.5
    tensor = tensor.unsqueeze(0)

    # Cargar modelo
    device = torch.device("cpu")
    model = SimpleCNN(num_classes=len(CLASSES))
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    with torch.no_grad():
        outputs = model(tensor)
        probs = F.softmax(outputs, dim=1).numpy()[0]
        pred_idx = int(np.argmax(probs))
        pred_class = CLASSES[pred_idx]
        confidence = probs[pred_idx] * 100

    print("\n" + "=" * 45)
    print(f" PREDICCIÓN CNN PYTORCH ({os.path.basename(img_path)})")
    print("=" * 45)
    print(f"Clase predicha: {pred_class.upper()} ({confidence:.2f}%)")
    print("-" * 45)
    print("Probabilidades por clase:")
    for c_name, p in zip(CLASSES, probs):
        bar = "█" * int(p * 20)
        print(f"  {c_name:<12}: {p * 100:>5.1f}%  {bar}")
    print("=" * 45)

    # Crear imagen con panel visual de resultados
    canvas_w, canvas_h = 500, 260
    canvas = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 245

    # Insertar imagen de entrada (ampliada a 160x160)
    display_img = cv2.resize(img, (160, 160))
    canvas[50:210, 30:190] = display_img
    cv2.rectangle(canvas, (30, 50), (190, 210), (100, 100, 100), 2)

    # Títulos y texto
    cv2.putText(canvas, "Entrada", (80, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (40, 40, 40), 2)
    cv2.putText(canvas, f"Prediccion: {pred_class}", (210, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 150, 0), 2)
    cv2.putText(canvas, f"Confianza: {confidence:.1f}%", (210, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50), 1)

    # Barras de probabilidad gráficas
    y_bar = 140
    for c_name, p in zip(CLASSES, probs):
        cv2.putText(canvas, f"{c_name}:", (210, y_bar), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (40, 40, 40), 1)
        bar_len = int(p * 180)
        cv2.rectangle(canvas, (300, y_bar - 12), (300 + bar_len, y_bar + 2), (0, 160, 0) if c_name == pred_class else (180, 180, 180), -1)
        cv2.putText(canvas, f"{p*100:.0f}%", (305 + bar_len, y_bar), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (80, 80, 80), 1)
        y_bar += 30

    cv2.imwrite(out_path, canvas)
    print(f"Visualización de predicción guardada en: {out_path}\n")

if __name__ == "__main__":
    from dataset import guardar_muestras_individuales
    guardar_muestras_individuales()
    predecir_imagen("data/circulo_test.png")
