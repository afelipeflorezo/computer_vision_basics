import cv2
import urllib.request
import os

os.makedirs("data", exist_ok=True)

# Imagen de prueba con caras (grupo de personas)
url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/faces.jpg"
urllib.request.urlretrieve(url, "data/foto_grupo.jpg")

print("Imagen de prueba descargada en data/foto_grupo.jpg")
