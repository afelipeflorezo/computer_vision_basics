# Detección de Movimiento con Diferencia de Frames (OpenCV)

Módulo para la detección y delimitación automática de objetos y personas en movimiento mediante sustracción de fotogramas temporales consecutivos (`cv2.absdiff`), umbralización y consolidación morfológica.

---

## Principio de Funcionamiento

1. **Captura temporal:** Se almacenan fotogramas continuos en escala de grises y se suavizan con desenfoque Gaussiano.
2. **Diferencia absoluta:** La función `cv2.absdiff(frame_{t-1}, frame_t)` cancela todos los elementos estáticos del fondo (cuyo valor de diferencia es $\approx 0$) y resalta exclusivamente las regiones donde ocurrió cambio de intensidad.
3. **Binarización y dilatación:** Se aplica umbral fijo y dilatación iterativa para unir fragmentos de un mismo cuerpo u objeto en movimiento.
4. **Filtrado de contornos:** Se descartan perturbaciones térmicas o ruidos menores a un área mínima umbral ($min\_area$).
5. **Alerta visual:** Se trazan recuadros de advertencia en rojo y un indicador de estado dinámico ("MOVIMIENTO DETECTADO" / "SIN MOVIMIENTO").

---

## Estructura del Módulo

```text
deteccion_movimiento/
├── README.md               # Documentación y guía
├── requirements.txt        # Dependencias de Python
├── data/                   # Videos de prueba de movimiento
├── notebooks/              # Pruebas interactivas
├── output/                 # Video procesado con recuadros y captura instantánea
└── src/
    ├── generate_motion_sample.py # Generador sintético de video con movimiento
    └── motion_detection.py       # Algoritmo de detección en video y cámara en vivo
```

---

## Uso

1. Activar entorno virtual e instalar dependencias:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

2. Generar video de prueba:
```bash
python3 src/generate_motion_sample.py
```

3. Procesar detección en video:
```bash
python3 src/motion_detection.py
```

4. Ejecutar con cámara web en tiempo real:
Descomenta `detectar_movimiento_camara()` en `src/motion_detection.py` y ejecútalo. Presiona **'q'** para salir.
