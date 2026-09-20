# Clasificador de Imágenes con una CNN Simple en PyTorch

Módulo educativo para la construcción, entrenamiento y evaluación de una Red Neuronal Convolucional (CNN) en **PyTorch** para clasificación de imágenes geométricas (Círculos, Cuadrados y Triángulos), extensible a datasets estándar como MNIST o CIFAR-10.

---

## Arquitectura de la Red (`SimpleCNN`)

```text
Entrada: Imagen RGB (3, 32, 32)
  │
  ├── [Conv2d(3 -> 32, kernel=3, pad=1) + BatchNorm + ReLU]
  ├── [MaxPool2d(2, 2)]                           ──> (32, 16, 16)
  │
  ├── [Conv2d(32 -> 64, kernel=3, pad=1) + BatchNorm + ReLU]
  ├── [MaxPool2d(2, 2)]                           ──> (64, 8, 8)
  │
  ├── [Flatten]                                    ──> (4096)
  ├── [Linear(4096 -> 128) + ReLU + Dropout(0.3)] ──> (128)
  └── [Linear(128 -> 3)]                           ──> (Logits de 3 clases)
```

- **Función de Pérdida:** `nn.CrossEntropyLoss()`
- **Optimizador:** Adam (`lr=0.001`)
- **Aceleración por Hardware:** Soporta detección automática de Apple Silicon (`mps`), NVIDIA (`cuda`) o CPU.

---

## Estructura del Módulo

```text
clasificador_cnn_pytorch/
├── README.md               # Guía técnica y explicación
├── requirements.txt        # Dependencias (torch, torchvision, opencv-python, numpy)
├── data/                   # Muestras sintéticas generadas
├── notebooks/              # Espacio para notebooks Jupyter
├── output/                 # Pesos entrenados (.pth) y gráfica de predicción
└── src/
    ├── model.py            # Definición de SimpleCNN (nn.Module)
    ├── dataset.py          # Generador de formas geométricas y PyTorch Dataset
    ├── train.py            # Bucle de entrenamiento y evaluación
    └── predict.py          # Inferencia visual con probabilidades Softmax
```

---

## Instalación y Ejecución

1. Activar entorno virtual e instalar PyTorch:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

2. Entrenar la red neuronal:
```bash
python3 src/train.py
```
El modelo se entrenará rápidamente y guardará los pesos en `output/cnn_model.pth`.

3. Clasificar una imagen nueva:
```bash
python3 src/predict.py
```
Se mostrará la clase ganadora en consola y se guardará un panel comparativo con el gráfico de barras de confianza en `output/prediccion_resultado.jpg`.
