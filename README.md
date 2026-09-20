# Computer Vision Basics

Repositorio de proyectos y experimentos introductorios en Visión por Computadora utilizando Python y OpenCV.

## Casos de Aplicación

El repositorio está organizado en módulos independientes según el caso de uso:

### 1. [Detección de Bordes (Sobel / Canny)](deteccion_bordes/)
Implementación de filtros clásicos para la detección y análisis de bordes en imágenes (Sobel horizontal/vertical y algoritmo de Canny) con generación de imágenes de prueba y comparativas visuales.
- **Directorio:** `deteccion_bordes/`
- **Técnicas:** Filtros Sobel ($G_x, G_y$), Detector Canny
- **Documentación y uso:** Ver [deteccion_bordes/README.md](deteccion_bordes/README.md)

### 2. [Reconocimiento Facial Básico (Haar Cascades)](reconocimiento_facial/)
Detección de rostros en imágenes estáticas y flujos de video utilizando clasificadores en cascada de Haar provistos por OpenCV (`haarcascade_frontalface_default.xml`).
- **Directorio:** `reconocimiento_facial/`
- **Técnicas:** Haar Feature-based Cascade Classifiers
- **Documentación y uso:** Ver [reconocimiento_facial/README.md](reconocimiento_facial/README.md)

### 3. [Detección de Color y Seguimiento de Objetos (HSV)](proyecto_deteccion_color/)
Segmentación por color en espacio HSV, filtrado por máscaras y seguimiento de objetos delimitados por cajas contenedoras en imágenes estáticas, archivos de video y cámara web en tiempo real.
- **Directorio:** `proyecto_deteccion_color/`
- **Técnicas:** Espacio de color HSV, umbralización (`cv2.inRange`), máscaras binarias (`cv2.bitwise_and`), contornos y rectángulos delimitadores (`cv2.findContours`, `cv2.boundingRect`)
- **Documentación y uso:** Ver [proyecto_deteccion_color/README.md](proyecto_deteccion_color/README.md)

---

## Estructura del Repositorio

```text
computer_vision_basics/
├── README.md                     # Documentación principal
├── .gitignore                    # Reglas globales de exclusión
│
├── deteccion_bordes/             # Módulo 1: Detección de bordes
│   ├── README.md
│   ├── requirements.txt
│   ├── data/                     # Imágenes de prueba de entrada
│   ├── output/                   # Resultados con bordes detectados
│   └── src/
│       ├── edge_detection.py
│       └── generate_sample_images.py
│
├── reconocimiento_facial/        # Módulo 2: Detección de rostros
│   ├── README.md
│   ├── requirements.txt
│   ├── data/                     # Fotos y videos de entrada
│   ├── notebooks/                # Notebooks de exploración y pruebas
│   ├── output/                   # Resultados con rostros delimitados
│   └── src/
│       ├── download_test_image.py
│       └── face_detection.py
│
└── proyecto_deteccion_color/     # Módulo 3: Detección y seguimiento de color (HSV)
    ├── README.md
    ├── requirements.txt
    ├── data/                     # Imágenes y videos de prueba
    ├── notebooks/                # Notebooks de experimentación
    ├── output/                   # Resultados con objetos delimitados y máscaras
    └── src/
        ├── download_test_video.py
        └── color_detection.py
```
