# Lector de Códigos QR y Códigos de Barras con OpenCV

Módulo para la detección, localización poligonal y decodificación de códigos QR y códigos de barras en imágenes estáticas, videos y flujos de cámara web en tiempo real utilizando la API nativa de OpenCV (`cv2.QRCodeDetector`).

---

## Estructura del Módulo

```text
lector_qr_barras/
├── README.md               # Instrucciones de uso y documentación
├── requirements.txt        # Dependencias de Python
├── data/                   # Imágenes de prueba (códigos QR y de barras)
├── notebooks/              # Espacio para pruebas interactivas
├── output/                 # Resultados con polígonos y datos decodificados
└── src/
    ├── generate_sample_qr.py # Generador de códigos QR y de barras
    └── qr_reader.py          # Lector y decodificador con OpenCV
```

---

## Instalación

1. Activa tu entorno virtual:
```bash
source venv/bin/activate
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

---

## Uso Rápido

### 1. Generar imágenes de prueba
```bash
python3 src/generate_sample_qr.py
```
Crea `data/codigo_qr.png` y `data/codigo_barras.png`.

### 2. Detectar y decodificar código QR
```bash
python3 src/qr_reader.py
```
El resultado anotado con el recuadro verde y el texto decodificado se guardará en `output/qr_resultado.jpg`.

### 3. Ejecutar con cámara web en tiempo real
Edita `src/qr_reader.py` y descomenta la llamada `leer_qr_en_camara()`.
Presiona **'q'** para salir de la ventana interactiva.
