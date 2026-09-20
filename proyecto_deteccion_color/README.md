# Detección de color y seguimiento de objetos por color (HSV)

## Instalación
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Descargar video de prueba (opcional)
```bash
python3 src/download_test_video.py
```

## Ejecutar detección de color
Edita `src/color_detection.py` y descomenta la opción que quieras probar.
Luego ejecuta:
```bash
python3 src/color_detection.py
```

## Rangos de color HSV comunes (OpenCV: H 0-179, S 0-255, V 0-255)
- **Rojo**: `[0, 100, 100]` a `[10, 255, 255]` (y `[170, 100, 100]` a `[180, 255, 255]`)
- **Verde**: `[40, 100, 100]` a `[80, 255, 255]`
- **Azul**: `[100, 100, 100]` a `[130, 255, 255]`
- **Amarillo**: `[20, 100, 100]` a `[30, 255, 255]`
- **Púrpura / Magenta**: `[120, 50, 50]` a `[160, 255, 255]` *(presente en la pluma del sombrero de data/imagen.jpg)*

## Archivos generados en `output/`
- `resultado.jpg`: Imagen con los píxeles del color aislado (el resto en negro) y recuadros de detección.
- `resultado_deteccion.jpg`: Imagen original completa con los recuadros verdes y etiquetas de los objetos detectados.
- `resultado_mask.jpg`: Máscara binaria (blanco = coincide con el color, negro = descartado).

