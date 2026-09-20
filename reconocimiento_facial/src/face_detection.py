import cv2
import os

os.makedirs("output", exist_ok=True)


def detectar_caras_en_imagen(img_path, out_path):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite(out_path, img)
    print(f"Detectadas {len(faces)} cara(s). Resultado guardado en {out_path}")


def detectar_caras_en_video(video_path, out_path):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        out_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4)))
    )

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        out.write(frame)
        frame_count += 1
        if frame_count % 30 == 0:
            print(f"Procesados {frame_count} frames...")

    cap.release()
    out.release()
    print(f"Video guardado en {out_path}")


if __name__ == "__main__":
    detectar_caras_en_imagen(
        "data/foto_grupo.jpg", "output/foto_grupo_detected.jpg"
    )
    # detectar_caras_en_video("data/video.mp4", "output/video_detected.mp4")
