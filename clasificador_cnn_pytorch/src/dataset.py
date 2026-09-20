import os
import cv2
import numpy as np

os.makedirs("data", exist_ok=True)

CLASSES = ["Circulo", "Cuadrado", "Triangulo"]

def dibujar_forma(tipo, size=32):
    """Genera una imagen sintética de 32x32 con una forma geométrica centrada con ligeras variaciones."""
    img = np.ones((size, size, 3), dtype=np.uint8) * 255
    center = size // 2

    # Color aleatorio (no blanco)
    color = (
        int(np.random.randint(20, 220)),
        int(np.random.randint(20, 220)),
        int(np.random.randint(20, 220))
    )

    offset_x = np.random.randint(-2, 3)
    offset_y = np.random.randint(-2, 3)
    cx, cy = center + offset_x, center + offset_y

    if tipo == 0:  # Círculo
        r = np.random.randint(9, 13)
        cv2.circle(img, (cx, cy), r, color, -1)
    elif tipo == 1:  # Cuadrado
        half = np.random.randint(8, 12)
        cv2.rectangle(img, (cx - half, cy - half), (cx + half, cy + half), color, -1)
    elif tipo == 2:  # Triángulo
        half = np.random.randint(9, 13)
        pts = np.array([
            [cx, cy - half],
            [cx - half, cy + half],
            [cx + half, cy + half]
        ], dtype=np.int32)
        cv2.fillPoly(img, [pts], color)

    # Ruido gaussiano sutil
    noise = np.random.randint(-8, 8, (size, size, 3), dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return img

def generar_dataset_sintetico(samples_per_class=150):
    """Genera matrices NumPy de entrenamiento y prueba."""
    X_train, y_train = [], []
    X_test, y_test = [], []

    np.random.seed(42)
    for c in range(3):
        # 80% train, 20% test
        for _ in range(int(samples_per_class * 0.8)):
            X_train.append(dibujar_forma(c))
            y_train.append(c)
        for _ in range(int(samples_per_class * 0.2)):
            X_test.append(dibujar_forma(c))
            y_test.append(c)

    return (
        np.array(X_train, dtype=np.uint8),
        np.array(y_train, dtype=np.int64),
        np.array(X_test, dtype=np.uint8),
        np.array(y_test, dtype=np.int64)
    )

def guardar_muestras_individuales():
    """Genera imágenes individuales en data/ para pruebas de inferencia."""
    cv2.imwrite("data/circulo_test.png", dibujar_forma(0, size=64))
    cv2.imwrite("data/cuadrado_test.png", dibujar_forma(1, size=64))
    cv2.imwrite("data/triangulo_test.png", dibujar_forma(2, size=64))
    print("Muestras de prueba guardadas en:")
    print("  - data/circulo_test.png")
    print("  - data/cuadrado_test.png")
    print("  - data/triangulo_test.png")

try:
    import torch
    from torch.utils.data import Dataset

    class ShapesDataset(Dataset):
        def __init__(self, images, labels, transform=None):
            self.images = images
            self.labels = labels
            self.transform = transform

        def __len__(self):
            return len(self.images)

        def __getitem__(self, idx):
            img = self.images[idx]
            label = self.labels[idx]

            # Transponer de HWC a CHW y normalizar a [0, 1]
            img_tensor = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0
            # Normalización estándar (mean=0.5, std=0.5)
            img_tensor = (img_tensor - 0.5) / 0.5

            return img_tensor, torch.tensor(label, dtype=torch.long)
except ImportError:
    ShapesDataset = None

if __name__ == "__main__":
    guardar_muestras_individuales()
