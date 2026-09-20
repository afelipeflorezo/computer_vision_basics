# Filtro de Fondo Verde (Chroma Key) en Tiempo Real con OpenCV

Módulo para la eliminación y sustitución de fondos de pantalla verde (Chroma Key) por fondos virtuales estáticos o dinámicos utilizando segmentación en espacio de color HSV y operaciones de máscara alfa.

---

## Proceso de Composición

1. **Transformación de color:** Se convierte la imagen/fotograma de BGR a HSV para desacoplar la luminosidad del tono de color (Hue).
2. **Generación de máscara:** Se define el intervalo de verde típico de pantallas de croma (`H: 35-85, S: 100-255, V: 100-255`).
3. **Refinamiento perimetral (Despill):** Operaciones morfológicas de dilatación y cierre para evitar halos verdes residuales en bordes y cabello.
4. **Composición:** Se aplica la máscara invertida al sujeto y la máscara directa al fondo virtual redimensionado, combinándolos con `cv2.add`.

---

## Estructura del Módulo

```text
fondo_verde_chroma/
├── README.md               # Guía de uso
├── requirements.txt        # Dependencias (opencv-python, numpy)
├── data/                   # Imagen con fondo verde y fondo virtual
├── notebooks/              # Pruebas interactivas
├── output/                 # Composición final y máscara binaria
└── src/
    ├── generate_chroma_samples.py # Generador de imágenes de prueba
    └── chroma_key.py              # Algoritmo de sustitución estática y en vivo
```

---

## Ejecución

1. Activar entorno virtual e instalar dependencias:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

2. Generar imágenes de prueba:
```bash
python3 src/generate_chroma_samples.py
```

3. Aplicar Chroma Key:
```bash
python3 src/chroma_key.py
```

4. Uso con cámara web en vivo:
Descomenta la llamada `chroma_key_en_camara()` dentro de `src/chroma_key.py` y ejecútalo colocándote frente a una pantalla o tela verde. Presiona **'q'** para salir.
