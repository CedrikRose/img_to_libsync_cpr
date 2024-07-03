import moviepy.editor as mpy
from PIL import Image
import numpy as np
import os

def replace_white_with_transparency(image, tolerance=30):
    """ Replace white pixels with transparency, with a given tolerance """
    image = image.convert("RGBA")
    data = np.array(image)
    red, green, blue, alpha = data.T
    white_areas = (np.abs(255 - red) <= tolerance) & (np.abs(255 - green) <= tolerance) & (np.abs(255 - blue) <= tolerance)
    data[..., :-1][white_areas.T] = (0, 0, 0)
    data[..., -1][white_areas.T] = 0
    return Image.fromarray(data)

def process_video_to_apng(input_path, output_path, tolerance=30):
    video = mpy.VideoFileClip(input_path)
    temp_dir = "temp_frames"
    
    # Create temporary directory for frames
    os.makedirs(temp_dir, exist_ok=True)
    
    # Process and save each frame as PNG with transparency
    for i, frame in enumerate(video.iter_frames()):
        img = Image.fromarray(frame)
        img = replace_white_with_transparency(img, tolerance)
        img.save(os.path.join(temp_dir, f"frame_{i:04d}.png"))
    
    # Combine frames into APNG using Pillow
    frames = [Image.open(os.path.join(temp_dir, f"frame_{i:04d}.png")) for i in range(len(os.listdir(temp_dir)))]
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=int(1000/video.fps), loop=0, disposal=2)
    
    # Clean up temporary frames
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)

if __name__ == "__main__":
    # Example usage
    input_video = "gooeyai lipsync (2).mp4"
    output_video = "videoooo.apng"
    process_video_to_apng(input_video, output_video, tolerance=30)
