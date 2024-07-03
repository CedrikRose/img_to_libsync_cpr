import os
import requests
from PIL import Image
import time
import signal

def separate_face(input_image, output_image, api_key):
    response = requests.post(
        'https://www.cutout.pro/api/v1/matting?mattingType=3',
        files={'file': open(input_image, 'rb')},
        headers={'APIKEY': api_key},
    )
    with open(output_image, 'wb') as out:
        out.write(response.content)

def close_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def crop_and_resize(image_path, output_path, size=512, content_size=400):
    # Lade das Bild
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    # Erstelle eine neue Kopie des Bildes, um die Originaldaten nicht zu verändern
    new_img = Image.new("RGBA", (width, height))

    # Ersetze transparente Pixel durch weiße Pixel
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            if pixel[3] == 0:  # Wenn der Alpha-Wert 0 (transparent) ist
                new_img.putpixel((x, y), (255, 255, 255, 255))  # Setze das Pixel auf weiß
            else:
                new_img.putpixel((x, y), pixel)

    # Extrahiere die Alpha-Ebene
    alpha = new_img.split()[-1]

    # Finde die nicht-transparenten Pixel
    non_transparent = alpha.getdata()

    # Initialisiere die Werte
    min_x, min_y = width, height
    max_x = max_y = 0

    # Suche die Grenzen
    for y in range(height):
        for x in range(width):
            if non_transparent[y * width + x] != 0:
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y

    # Crop-Rahmen bestimmen
    if max_x < min_x or max_y < min_y:
        # Wenn keine nicht-transparenten Pixel gefunden wurden, das ganze Bild ist transparent
        return None

    cropped_img = new_img.crop((min_x, min_y, max_x + 1, max_y + 1))

    # Erstelle ein quadratisches Bild mit weißem Hintergrund
    square_img = Image.new("RGBA", (size, size), (255, 255, 255, 255))

    # Berechne die neue Größe und bewahre das Seitenverhältnis
    cropped_width, cropped_height = cropped_img.size
    aspect_ratio = cropped_width / cropped_height
    if aspect_ratio > 1:
        new_height = int(content_size / aspect_ratio)
        new_width = content_size
    else:
        new_width = int(content_size * aspect_ratio)
        new_height = content_size

    # Skaliere das zugeschnittene Bild auf die neue Größe
    resized_img = cropped_img.resize((new_width, new_height), Image.LANCZOS)

    # Berechne die Position, um das skalierte Bild in der Mitte des quadratischen Bildes zu platzieren
    x_offset = (size - new_width) // 2
    y_offset = (size - new_height) // 2

    # Füge das skalierte Bild in das quadratische Bild ein
    square_img.paste(resized_img, (x_offset, y_offset))
    close_file(output_path)
    # Geschnittenes und skaliertes Bild speichern
    square_img.save(output_path)
    return output_path

if __name__ == "__main__":
    separate_face("2.jpg")
    crop_and_resize('solo_head.png', 'output.png')