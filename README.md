# Computer Vision Basics

Repositorio de proyectos y experimentos prácticos en Visión por Computadora utilizando Python, OpenCV y PyTorch. Cada módulo está aislado de manera independiente con su propio código fuente, datos de prueba, salidas generadas, dependencias y documentación detallada.

---

## Casos de Aplicación (Módulos)

El repositorio está organizado en 10 módulos según el caso de uso y técnica de procesamiento:

### 1. [Detección de Bordes (Sobel / Canny)](deteccion_bordes/)
Implementación de filtros clásicos para la detección y análisis de bordes en imágenes (Sobel horizontal/vertical y algoritmo de Canny) con generación de imágenes de prueba y comparativas visuales.
- **Directorio:** `deteccion_bordes/`
- **Técnicas:** Filtros Sobel ($G_x, G_y$), Detector Canny
- **Documentación:** Ver [deteccion_bordes/README.md](deteccion_bordes/README.md)

### 2. [Reconocimiento Facial Básico (Haar Cascades)](reconocimiento_facial/)
Detección de rostros en imágenes estáticas y flujos de video utilizando clasificadores en cascada de Haar provistos por OpenCV (`haarcascade_frontalface_default.xml`).
- **Directorio:** `reconocimiento_facial/`
- **Técnicas:** Haar Feature-based Cascade Classifiers
- **Documentación:** Ver [reconocimiento_facial/README.md](reconocimiento_facial/README.md)

### 3. [Detección de Color y Seguimiento de Objetos (HSV)](proyecto_deteccion_color/)
Segmentación por color en espacio HSV, filtrado por máscaras y seguimiento de objetos delimitados por cajas contenedoras en imágenes estáticas, archivos de video y cámara web en tiempo real.
- **Directorio:** `proyecto_deteccion_color/`
- **Técnicas:** Espacio de color HSV, umbralización (`cv2.inRange`), máscaras binarias (`cv2.bitwise_and`), contornos y rectángulos delimitadores (`cv2.findContours`, `cv2.boundingRect`)
- **Documentación:** Ver [proyecto_deteccion_color/README.md](proyecto_deteccion_color/README.md)

### 4. [Lector de Códigos QR y Barras](lector_qr_barras/)
Detección, localización poligonal perimetral y decodificación de códigos QR y códigos de barras en imágenes estáticas, archivos de video y cámara en vivo.
- **Directorio:** `lector_qr_barras/`
- **Técnicas:** `cv2.QRCodeDetector`, detección de polígonos, decodificación en tiempo real
- **Documentación:** Ver [lector_qr_barras/README.md](lector_qr_barras/README.md)

### 5. [Conteo de Objetos por Contornos](conteo_objetos/)
Identificación, filtrado morfológico, enumeración (#1, #2, #3...) y cálculo de propiedades geométricas (área, centroides mediante momentos espaciales) de objetos dispersos.
- **Directorio:** `conteo_objetos/`
- **Técnicas:** Filtro Gaussiano, umbralización de Otsu, apertura morfológica (`cv2.MORPH_OPEN`), contornos externos y momentos (`cv2.moments`)
- **Documentación:** Ver [conteo_objetos/README.md](conteo_objetos/README.md)

### 6. [Detección de Líneas de Carril para Vehículos](deteccion_carriles/)
Sistema de visión artificial para vehículos autónomos y ADAS: detección de líneas viales continuas y discontinuas, extrapolación de pendiente y visualización de carril semitransparente.
- **Directorio:** `deteccion_carriles/`
- **Técnicas:** Canny Edge Detection, Máscara trapezoidal de Región de Interés (ROI), Transformada de Hough Probabilística (`cv2.HoughLinesP`), extrapolación y mezcla alfa (`cv2.addWeighted`)
- **Documentación:** Ver [deteccion_carriles/README.md](deteccion_carriles/README.md)

### 7. [Extracción de Texto OCR (Tesseract y OpenCV)](extraccion_texto_ocr/)
Digitalización y reconocimiento óptico de caracteres a partir de imágenes de documentos y carteles, combinando preprocesamiento morfológico con el motor Tesseract.
- **Directorio:** `extraccion_texto_ocr/`
- **Técnicas:** Filtros de reducción de ruido, binarización de Otsu, localización de cajas delimitadoras por palabra y nivel de confianza con `pytesseract`
- **Documentación:** Ver [extraccion_texto_ocr/README.md](extraccion_texto_ocr/README.md)

### 8. [Filtro de Fondo Verde (Chroma Key)](fondo_verde_chroma/)
Sustitución en tiempo real de fondos verdes de estudio por imágenes o videos virtuales (playa, estudio, oficina) con suavizado de bordes y reducción de halo verde (despill).
- **Directorio:** `fondo_verde_chroma/`
- **Técnicas:** Segmentación en espacio de color HSV, operaciones booleanas bitwise, refinamiento morfológico y composición alfa
- **Documentación:** Ver [fondo_verde_chroma/README.md](fondo_verde_chroma/README.md)

### 9. [Detección de Movimiento por Diferencia de Frames](deteccion_movimiento/)
Sistema de monitoreo y videovigilancia que detecta variaciones temporales en fotogramas consecutivos, señalizando áreas en movimiento con recuadros rojos y estado de alerta.
- **Directorio:** `deteccion_movimiento/`
- **Técnicas:** Sustracción temporal (`cv2.absdiff`), umbralización binaria, dilatación morfológica, filtrado por área de contorno y marcas de tiempo
- **Documentación:** Ver [deteccion_movimiento/README.md](deteccion_movimiento/README.md)

### 10. [Clasificador de Imágenes con CNN Simple (PyTorch)](clasificador_cnn_pytorch/)
Construcción, entrenamiento ligero e inferencia de una Red Neuronal Convolucional (CNN) en PyTorch para clasificar formas geométricas o imágenes estándar, con desglose gráfico de probabilidades Softmax.
- **Directorio:** `clasificador_cnn_pytorch/`
- **Técnicas:** PyTorch `nn.Module`, capas `Conv2d`, `BatchNorm2d`, `MaxPool2d`, `Dropout`, `Linear`, `CrossEntropyLoss`, optimizador Adam y visualización de predicciones
- **Documentación:** Ver [clasificador_cnn_pytorch/README.md](clasificador_cnn_pytorch/README.md)

---

## Estructura del Repositorio

```text
computer_vision_basics/
├── README.md                     # Documentación principal del repositorio
├── .gitignore                    # Reglas globales de exclusión (venv, caches, etc.)
│
├── deteccion_bordes/             # Módulo 1: Detección de bordes (Sobel y Canny)
│   ├── README.md
│   ├── requirements.txt
│   ├── data/                     # Imágenes de prueba de entrada
│   ├── output/                   # Resultados con bordes detectados
│   └── src/
│       ├── edge_detection.py
│       └── generate_sample_images.py
│
├── reconocimiento_facial/        # Módulo 2: Detección de rostros (Haar Cascades)
│   ├── README.md
│   ├── requirements.txt
│   ├── data/
│   ├── notebooks/
│   ├── output/
│   └── src/
│       ├── download_test_image.py
│       └── face_detection.py
│
├── proyecto_deteccion_color/     # Módulo 3: Detección y seguimiento de color (HSV)
│   ├── README.md
│   ├── requirements.txt
│   ├── data/
│   ├── notebooks/
│   ├── output/
│   └── src/
│       ├── download_test_video.py
│       └── color_detection.py
│
├── lector_qr_barras/             # Módulo 4: Lector de códigos QR y de barras
│   ├── README.md
│   ├── requirements.txt
│   ├── data/
│   ├── notebooks/
│   ├── output/
│   └── src/
│       ├── generate_sample_qr.py
│       └── qr_reader.py
│
├── conteo_objetos/               # Módulo 5: Conteo de objetos por contornos
│   ├── README.md
│   ├── requirements.txt
│   ├── data/
│   ├── notebooks/
│   ├── output/
│   └── src/
│       ├── generate_sample_objects.py
│       └── object_counter.py
│
├── deteccion_carriles/           # Módulo 6: Detección de líneas de carril
│   ├── README.md
│   ├── requirements.txt
│   ├── data/
│   ├── notebooks/
│   ├── output/
│   └── src/
│       ├── generate_lane_sample.py
│       └── lane_detection.py
│
├── extraccion_texto_ocr/         # Módulo 7: Extracción de texto OCR
│   ├── README.md
│   ├── requirements.txt
│   ├── data/
│   ├── notebooks/
│   ├── output/
│   └── src/
│       ├── generate_sample_text.py
│       └── ocr_extractor.py
│
├── fondo_verde_chroma/           # Módulo 8: Filtro de fondo verde (Chroma Key)
│   ├── README.md
│   ├── requirements.txt
│   ├── data/
│   ├── notebooks/
│   ├── output/
│   └── src/
│       ├── generate_chroma_samples.py
│       └── chroma_key.py
│
├── deteccion_movimiento/         # Módulo 9: Detección de movimiento por diferencia de frames
│   ├── README.md
│   ├── requirements.txt
│   ├── data/
│   ├── notebooks/
│   ├── output/
│   └── src/
│       ├── generate_motion_sample.py
│       └── motion_detection.py
│
└── clasificador_cnn_pytorch/     # Módulo 10: Clasificador de imágenes con CNN en PyTorch
    ├── README.md
    ├── requirements.txt
    ├── data/
    ├── notebooks/
    ├── output/
    └── src/
        ├── model.py
        ├── dataset.py
        ├── train.py
        └── predict.py
```
