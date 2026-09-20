# Detección de bordes con OpenCV (Canny/Sobel)
## Instalación
```bash
source venv/bin/activate
pip install -r requirements.txt
```
## Generar imágenes de prueba
```bash
python3 src/generate_sample_images.py
```
## Ejecutar detección de bordes
```bash
python3 src/edge_detection.py
```
Los resultados se guardan en `output/` (Sobel, Canny y una comparación Original | Sobel | Canny por foto).
Las imágenes de `data/` son fotografías reales (edificio/paisaje, perro, objetos), no figuras geométricas.
