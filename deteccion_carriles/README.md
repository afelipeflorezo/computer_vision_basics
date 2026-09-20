# Detección de Líneas de Carril para Vehículos (OpenCV)

Módulo para la detección de líneas viales y delimitación del carril de circulación en tiempo real, técnica fundamental en los sistemas avanzados de asistencia a la conducción (ADAS) y vehículos autónomos.

---

## Metodología

1. **Detección de bordes (Canny):** Conversión a escala de grises, reducción de ruido con desenfoque Gaussiano y cálculo de gradientes.
2. **Región de Interés (ROI):** Aplicación de una máscara trapezoidal que aisla la perspectiva de la calzada frente al vehículo, ignorando cielo, horizonte y elementos periféricos.
3. **Transformada de Hough Probabilística (`cv2.HoughLinesP`):** Identificación de segmentos lineales continuos y discontinuos.
4. **Agrupación y extrapolación:** Clasificación de pendientes ($m < 0$ para línea izquierda, $m > 0$ para línea derecha), cálculo de rectas promedio y extensión hasta la base de la imagen.
5. **Composición visual:** Trazado de líneas guía e iluminación semitransparente (`cv2.addWeighted`) de la superficie del carril vehicular.

---

## Estructura del Módulo

```text
deteccion_carriles/
├── README.md               # Guía técnica
├── requirements.txt        # Dependencias (opencv-python, numpy)
├── data/                   # Imágenes y videos viales de prueba
├── notebooks/              # Pruebas interactivas
├── output/                 # Resultados de carril detectado (imagen y video)
└── src/
    ├── generate_lane_sample.py # Genera carretera sintética y video de prueba
    └── lane_detection.py      # Algoritmo de detección y seguimiento
```

---

## Ejecución

1. Activar entorno virtual e instalar dependencias:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

2. Generar carretera e imagen/video de prueba:
```bash
python3 src/generate_lane_sample.py
```

3. Ejecutar detección de carriles:
```bash
python3 src/lane_detection.py
```

Resultados generados:
- `output/carril_resultado.jpg`: Fotografía con carril y líneas delimitadas.
- `output/carril_video_resultado.mp4`: Video procesado con carril animado en verde.
