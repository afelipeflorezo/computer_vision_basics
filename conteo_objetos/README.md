# Conteo de Objetos en Imágenes mediante Contornos (OpenCV)

Módulo para la detección, filtrado morfológico, enumeración y cálculo de propiedades geométricas (área, centroides, cajas delimitadoras) de objetos dispersos en imágenes con OpenCV.

---

## Flujo del Algoritmo

1. **Preprocesamiento:** Conversión a escala de grises y suavizado con filtro Gaussiano ($7 \times 7$) para atenuar ruido y sombras sutiles.
2. **Binarización:** Umbralización automática de Otsu inversa (`THRESH_BINARY_INV + THRESH_OTSU`) para aislar los elementos sobre el fondo.
3. **Morfología matemática:** Operación de apertura (`cv2.MORPH_OPEN`) con elemento estructurante elíptico para suprimir falsos positivos y separar uniones débiles.
4. **Detección de contornos:** Extracción de contornos externos (`cv2.RETR_EXTERNAL`).
5. **Filtrado y análisis geométrico:** Filtro por umbral de área mínima/máxima y cálculo del centroide con momentos espaciales ($m_{10}/m_{00}, m_{01}/m_{00}$).
6. **Visualización:** Numeración secuencial ordenada (#1, #2, #3...), delimitación perimetral y guardado de resultados.

---

## Estructura del Módulo

```text
conteo_objetos/
├── README.md               # Documentación y guía de ejecución
├── requirements.txt        # Dependencias (opencv-python, numpy)
├── data/                   # Imágenes de prueba de entrada
├── notebooks/              # Espacio de trabajo interactivo
├── output/                 # Imágenes anotadas y máscaras binarias generadas
└── src/
    ├── generate_sample_objects.py # Generador de dataset sintético de monedas
    └── object_counter.py          # Pipeline de conteo y etiquetado
```

---

## Instalación y Ejecución

1. Activa el entorno virtual:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

2. Generar imagen de prueba:
```bash
python3 src/generate_sample_objects.py
```

3. Ejecutar conteo de objetos:
```bash
python3 src/object_counter.py
```

Los resultados se guardan en `output/conteo_resultado.jpg` y `output/conteo_resultado_mask.jpg`.
