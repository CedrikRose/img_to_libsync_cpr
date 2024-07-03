import cv2

def make_white_transparent(input_path, output_path):
    # Video laden
    video = cv2.VideoCapture(input_path)

    # Codec und Videoschreiber initialisieren
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, video.get(cv2.CAP_PROP_FPS), (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    # Alle Frames durchlaufen
    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Weißen Bereich definieren
        lower_white = (220, 220, 220)
        upper_white = (255, 255, 255)

        # Maske für weiße Pixel erstellen
        mask = cv2.inRange(frame, lower_white, upper_white)

        # Ursprüngliches Bild und Maske kombinieren, um Transparenz zu erzeugen
        transparent_frame = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))

        # Ausgabevideo schreiben
        out.write(transparent_frame)

    # Ressourcen freigeben
    video.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    make_white_transparent('gooey.ai lipsync (2).mp4', 'output_video.mp4')