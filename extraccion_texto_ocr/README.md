# Extracción de Texto de Imágenes con OCR (Tesseract y OpenCV)

Módulo para el preprocesamiento de imágenes documentales, detección de regiones de texto y extracción de contenido alfanumérico utilizando **Tesseract OCR** y **OpenCV**.

---

## Preprocesamiento para OCR

Para maximizar la precisión de lectura de caracteres, el pipeline ejecuta:
1. **Reducción a escala de grises.**
2. **Filtro de mediana:** Elimina ruido tipo sal y pimienta sin degradar la nitidez de los bordes tipográficos.
3. **Binarización de Otsu:** Calcula el umbral óptimo global para separar el texto del fondo.
4. **Segmentación y delimitación:** Localización de bloques y palabras mediante gradientes morfológicos y cajas delimitadoras con puntaje de confianza.

---

## Requisitos de Instalación

### 1. Motor Tesseract en el Sistema Operativo
- **macOS:**
  ```bash
  brew install tesseract tesseract-lang
  ```
- **Ubuntu / Debian:**
  ```bash
  sudo apt update && sudo apt install -y tesseract-ocr tesseract-ocr-spa
  ```
- **Windows:** Descargar el instalador desde el repositorio oficial de GitHub de UB-Mannheim.

### 2. Dependencias de Python
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## Estructura del Módulo

```text
extraccion_texto_ocr/
├── README.md               # Documentación y guía de instalación
├── requirements.txt        # Dependencias de Python
├── data/                   # Imágenes con texto para digitalizar
├── notebooks/              # Pruebas interactivas
├── output/                 # Texto extraído (.txt) e imágenes anotadas
└── src/
    ├── generate_sample_text.py # Generador de documentos sintéticos de prueba
    └── ocr_extractor.py        # Pipeline de preprocesamiento y extracción OCR
```

---

## Uso

1. Generar imagen de prueba con texto:
```bash
python3 src/generate_sample_text.py
```

2. Ejecutar extracción de texto:
```bash
python3 src/ocr_extractor.py
```

Los resultados se guardan en:
- `output/texto_extraido.txt`: Contenido textual reconocido.
- `output/ocr_anotado.jpg`: Imagen original con las cajas delimitadoras de texto.
