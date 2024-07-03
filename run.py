from separate_head import separate_face, crop_and_resize
from sd_cartoon_translation import generate_cartoon_image_from_image
from lib_sync import generate_video_from_image
from overlay_vid_prep import remove_video_background

import os
import subprocess
import time
import requests


def get_filename_without_extension(file_path):
    # Extrahiere den Dateinamen aus dem Pfad
    filename = os.path.basename(file_path)
    # Entferne die Dateiendung
    filename_without_extension = os.path.splitext(filename)[0]
    return filename_without_extension


def check_and_start_server(url, start_command):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Server at {url} is already running.")
            return True
    except requests.ConnectionError:
        print(f"Server at {url} is not running. Starting it now.")
        subprocess.Popen(start_command, shell=True)

    # Warte bis der Server läuft
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Server at {url} is now running.")
                break
        except requests.ConnectionError:
            pass
        time.sleep(1)


def make_video(input_path, cartoon_style=True):
    # make sure servers are active
    check_and_start_server("http://127.0.0.1:7860", "SadTalker/webui.sh")
    if cartoon_style:
        check_and_start_server("http://127.0.0.1:7861", "stable_diffusion/webui/webui.sh")

    filename = get_filename_without_extension(input_path)

    separate_face(input_path, f"data/separat_head/{filename}.png", 'dfc14e4af3894540b71e257bbb6fdf9a')
    crop_and_resize(f"data/separat_head/{filename}.png", f"data/ressized_head/{filename}.png")

    if cartoon_style:
        generate_cartoon_image_from_image(f"data/ressized_head/{filename}.png", f"data/cartoon/{filename}.png")
        generate_video_from_image(f"data/cartoon/{filename}.png", f"data/libsync_video/{filename}.mp4")
    else:
        generate_video_from_image(f"data/ressized_head/{filename}.png", f"data/libsync_video/{filename}.mp4")

    remove_video_background(f"data/libsync_video/{filename}.mp4", f"data/final_video/{filename}.mov")


if __name__ == "__main__":
    make_video("data/inputs/2.jpg")
