import urllib.request
import os

os.makedirs("data", exist_ok=True)
url = "https://raw.githubusercontent.com/gilbertsoong/opencv-tutorial/master/videos/ball.mp4"

try:
    urllib.request.urlretrieve(url, "data/video.mp4")
    print("Video descargado en data/video.mp4")
except Exception as e:
    print(f"No se pudo descargar el video: {e}")
    print("Coloca tu propio video como data/video.mp4")
