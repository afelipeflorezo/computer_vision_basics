import os
import urllib.request

os.makedirs("data", exist_ok=True)

# Fotos reales (Lorem Picsum) para que Canny/Sobel muestren bordes de objetos,
# no solo figuras geométricas sintéticas.
imagenes = {
    "edificio.jpg": "https://picsum.photos/id/1015/640/480",  # paisaje / estructuras
    "perro.jpg": "https://picsum.photos/id/237/640/480",      # animal
    "objetos.jpg": "https://picsum.photos/id/292/640/480",    # naturaleza muerta
}

for nombre, url in imagenes.items():
    destino = os.path.join("data", nombre)
    print(f"Descargando {nombre}...")
    urllib.request.urlretrieve(url, destino)

print("Imágenes generadas en data/")
